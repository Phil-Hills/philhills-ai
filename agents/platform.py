import asyncio
import logging
import uuid
import datetime
import json
from typing import Dict, Any, Optional, List, Callable
from pydantic import BaseModel
from dataclasses import dataclass, field
from agents.identity import get_identity_context
from .protocol import CubeTransport, A2AMessage
from .mesh import AgentMeshCommunicator
from services.cube_protocol import CubeObject

# Import Cube Protocol
try:
    from cube_protocol import CubeProtocol
    CUBE_AVAILABLE = True
except ImportError:
    CUBE_AVAILABLE = False
    logging.warning("cube-protocol not installed. Install: pip install cube-protocol")

logger = logging.getLogger("platform")

@dataclass
class AgentCard:
    uuid: str
    name: str
    description: str
    version: str = "1.0.0"
    capabilities: list = field(default_factory=list)

@dataclass
class TaskRequest:
    requester_id: str
    content: str
    task_id: str = field(default_factory=lambda: str(datetime.datetime.now().timestamp()))
    context: dict = field(default_factory=dict)
    headers: dict = field(default_factory=lambda: {
        "x-a2a-context-id": str(uuid.uuid4()),
        "x-a2a-hop-count": "0",
        "x-a2a-timestamp": datetime.datetime.utcnow().isoformat()
    })

@dataclass
class TaskResponse:
    task_id: str
    responder_id: str
    status: str
    output: str
    artifacts: list = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    headers: dict = field(default_factory=dict)

class MessageBus:
    """
    Simulates a network bus for routing Cube messages between agents.
    """
    def __init__(self):
        self._agents: Dict[str, 'BaseAgent'] = {}
        self._history: List[CubeObject] = []

    def register(self, agent: 'BaseAgent'):
        self._agents[agent.card.uuid] = agent
        agent.connect(self)
        logger.info(f"Registered agent: {agent.card.name} ({agent.card.uuid})")

    async def send(self, message: Any, target_id: str = None):
        """
        Route a message. If target_id is None, broadcast to all (except sender).
        Supports generic Any for A2AC Mesh Packets (Dicts) or legacy CubeObjects.
        """
        self._history.append(message)
        
        # In a real system, we'd route by reading the Cube header or outer envelope.
        # Here we rely on the caller specifying the target ID or broadcasting.
        
        if target_id:
            if target_id in self._agents:
                await self._agents[target_id].receive(message)
            else:
                logger.warning(f"Target agent {target_id} not found.")
        else:
            # Broadcast
            for aid, agent in self._agents.items():
                # Don't echo back (logic to identify sender needs to be better in real impl)
                # For now just send to all
                await agent.receive(message)

class BaseAgent:
    """
    Abstract base agent that communicates via the A2A+Cube protocol.
    """
    def __init__(self, name: str, description: str, instruction: str = None, capabilities: Optional[List[str]] = None, can_delegate: bool = True):
        self.card = AgentCard(
            uuid=str(uuid.uuid4()),
            name=name,
            description=description,
            capabilities=capabilities or []
        )
        # Inject Global Identity
        identity = get_identity_context()
        self.instruction = f"{identity}\n\nSPECIFIC ROLE:\n{instruction}" if instruction else identity
        self.can_delegate = can_delegate
        self.bus: MessageBus = None
        self.inbox: asyncio.Queue = asyncio.Queue()

        # Cube Protocol integration
        self.cube = CubeProtocol() if CUBE_AVAILABLE else None
        
        # Agent Mesh Communicator (Nervous System)
        self.mesh = AgentMeshCommunicator(agent_name=name)
        
        self.stats = {
            "messages_sent": 0,
            "messages_received": 0,
            "tokens_saved": 0,
            "compression_ratio": 0.98  # Average 98% reduction
        }
        
        logger.info(f"Agent {name} initialized with Cube Protocol: {CUBE_AVAILABLE}")

    def connect(self, bus: MessageBus):
        self.bus = bus

    async def receive(self, message: Any):
        """Called by bus when a message arrives."""
        await self.inbox.put(message)

    async def start(self):
        """Start the agent's message processing loop and background tasks."""
        logger.info(f"Agent {self.card.name} starting...")
        
        # Start background task if defined
        if hasattr(self, 'autonomous_background_task'):
            asyncio.create_task(self.autonomous_background_task())
            logger.info(f"Agent {self.card.name} background task started")
        
        while True:
            try:
                # Wait for incoming messages
                message = await self.inbox.get()
                
                # [A2AC] Detect Mesh Packet (Dict) vs Legacy Object (TaskRequest)
                if isinstance(message, dict) and "headers" in message:
                    await self.process_mesh_packet(message)
                
                elif isinstance(message, TaskRequest):
                    # Legacy direct object support
                    response = await self.handle_task(message)
                    
                    # Send response back to requester
                    if self.bus and response:
                        await self.bus.send(response, message.requester_id)
                    
                    # Also notify via handle_response if implemented
                    if hasattr(self, 'handle_response'):
                        await self.handle_response(response)
                
                elif isinstance(message, CubeObject):
                     await self._safe_process_cube(message)
                        
            except Exception as e:
                logger.error(f"Agent {self.card.name} error: {e}")
                await asyncio.sleep(1)
    
    async def process_mesh_packet(self, packet: Dict[str, Any]):
        """
        [A2AC] Unwrap a Mesh Packet and route to handle_task or handle_response.
        """
        try:
            headers = packet.get("headers", {})
            body = packet.get("body", {})
            
            # 1. Validate
            if not self.mesh.validate_incoming(packet):
                return
            
            # 2. Extract Intent
            intent = body.get("intent", "")
            payload_data = body.get("payload", {})
            content = payload_data.get("content", "")
            
            sender = headers.get("x-a2a-sender", "Unknown")
            ctx_id = headers.get("x-a2a-context-id")
            
            logger.info(f"[{self.card.name}] Recv Mesh Packet: {intent} from {sender}")
            
            # 3. Dispatch based on Intent
            if "REPORT" in intent:
                # It is a Response (TaskResponse-equivalent)
                # Construct a virtual TaskResponse
                status = "completed" if "REPORT_FAIL" not in intent else "failed"
                
                # Check if payload content is JSON (some agents output JSON strings)
                output_str = content
                if isinstance(content, (dict, list)):
                    output_str = json.dumps(content)
                    
                response = TaskResponse(
                    task_id=ctx_id or "unknown", # A2AC uses Context ID as primary trace
                    responder_id=sender,
                    status=status,
                    output=output_str,
                    headers=headers
                )
                await self.handle_response(response)
                
            else:
                # It is a Request (TaskRequest-equivalent)
                # Construct a virtual TaskRequest
                request = TaskRequest(
                    requester_id=sender,
                    content=str(payload_data.get("content", "")), # Or re-construct command from Intent if needed
                    task_id=ctx_id or str(uuid.uuid4()),
                    headers=headers
                )
                
                # Special Case: If intent has command structure (e.g. GH|CMD), use that
                # Many agents parse intent/content. Let's use the explicit content field if present, else Intent.
                if "|" in intent and "REPORT" not in intent:
                     # Intent might be "GH|LIST_REPOS|1"
                     request.content = intent

                response = await self.handle_task(request)
                
                # Helper: If response is already a Mesh Packet (Dict), send it directly
                if self.bus and response:
                    await self.bus.send(response, sender)

        except Exception as e:
            logger.error(f"Failed to process Mesh Packet: {e}")

    def _find_agent(self, name: str) -> str:
        """Find agent ID by name."""
        if not self.bus:
            return None
        for agent_id, agent in self.bus._agents.items():
            if name.lower() in agent.card.name.lower():
                return agent_id
        return None
    
    async def send_to_agent(self, target_name: str, message: str) -> TaskResponse:
        """
        Send message directly to another agent (not via Manager).
        Enables true agent-to-agent collaboration.
        """
        target_id = self._find_agent(target_name)
        if not target_id:
            logger.warning(f"Agent {target_name} not found")
            return None
        
        request = TaskRequest(
            requester_id=self.card.uuid,
            content=message
        )
        
        await self.send_message(request, target_id)
        logger.info(f"{self.card.name} → {target_name}: {message[:50]}...")
        
        # TODO: Wait for response if needed
        return None
    
    def compress_message(self, data: Dict[str, Any], domain: str, sequence: str, outcome: str) -> Dict[str, Any]:
        """
        Compress message using Cube Protocol.
        """
        if not self.cube:
            return {
                "cube": json.dumps(data),
                "semantic": f"{domain}|{sequence}|{outcome}",
                "hash": "",
                "compressed": False
            }
        
        payload_json = json.dumps(data, separators=(",", ":"))
        compressed = self.cube.compress(data=payload_json, domain=domain, sequence=sequence, outcome=outcome)
        
        self.stats['tokens_saved'] += (len(payload_json)//4) - (len(compressed['cube'])//4)
        self.stats['messages_sent'] += 1
        return {**compressed, "compressed": True}
    
    def decompress_message(self, cube_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decompress Cube Protocol message.
        """
        if not cube_data.get("compressed", True) or not self.cube:
            return json.loads(cube_data.get("cube", "{}"))
        
        cube_dict = {'cube': cube_data['cube'], 'hash': cube_data['hash']}
        decompressed_bytes = self.cube.decompress(cube_dict)
        return json.loads(decompressed_bytes.decode('utf-8'))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent communication statistics."""
        return {
            "agent": self.card.name,
            "messages_sent": self.stats['messages_sent'],
            "messages_received": self.stats['messages_received'],
            "tokens_saved": self.stats['tokens_saved'],
            "cube_protocol_enabled": CUBE_AVAILABLE
        }

    async def _safe_process_cube(self, cube: CubeObject):
        try:
            await self.process_cube(cube)
        except Exception as e:
            logger.error(f"Agent {self.card.name} failed to process cube: {e}")

    async def process_cube(self, cube: CubeObject):
        """
        Decode and handle a message. Override this.
        """
        payload = CubeTransport.unpack(cube)
        logger.info(f"[{self.card.name}] Received payload: {payload}")
        
        # Basic dispatch based on payload shape
        if "requester_id" in payload and "content" in payload:
            # It's a Request
            req = TaskRequest(**payload)
            response = await self.handle_task(req)
            if response:
                 # [A2AC] If response is already a Mesh Packet (Dict), send directly
                 if isinstance(response, dict):
                     await self.bus.send(response, req.requester_id)
                 else:
                     # Auto-pack response via CubeTransport if legacy (TaskResponse)
                     cube_resp = CubeTransport.pack(response, from_agent=self.card.name)
                     await self.bus.send(cube_resp, req.requester_id)

        elif "status" in payload and "output" in payload:
            # It's a Response
            res = TaskResponse(**payload)
            await self.handle_response(res)

    async def handle_task(self, request: TaskRequest):
        pass

    async def handle_response(self, response: TaskResponse):
        pass

    async def send_message(self, message: A2AMessage, target_id: str):
        if not self.bus:
            raise RuntimeError("Agent not connected to bus")
        
        # Legacy support: use CubeTransport for TaskRequest/Response objects
        if isinstance(message, (TaskRequest, TaskResponse)):
             cube = CubeTransport.pack(message, from_agent=self.card.name)
             await self.bus.send(cube, target_id)
        else:
             # Generic send (e.g. Mesh Packet)
             await self.bus.send(message, target_id)
