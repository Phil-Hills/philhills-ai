import sys
import os
from pathlib import Path

# Add parent directory to path to allow imports when run as script
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import logging
import json
from typing import List, Dict, Any

from agents.agent_platform import BaseAgent, TaskRequest, TaskResponse

logger = logging.getLogger("trend-pipeline")

class TrendPipelineAgent(BaseAgent):
    """
    Orchestrator agent that automates the trend-to-cube pipeline.
    Coordinates: Google Trends → Content Generator → Cube Publisher
    """
    
    def __init__(self):
        super().__init__(
            name="Trend Pipeline",
            description="Automates the trend-to-cube content generation pipeline. Fetches trends, generates summaries, publishes cubes."
        )
    
    async def handle_task(self, request: TaskRequest):
        """
        Run the automated pipeline.
        Input: "run" or specific configuration
        Output: Summary of published cubes
        """
        logger.info(f"[{self.card.name}] Starting pipeline...")
        
        try:
            # Step 1: Get trending topics from Google Trends agent
            trends_agent_id = self._find_agent("Google Trends Agent")
            if not trends_agent_id:
                raise Exception("Google Trends Agent not found")
            
            logger.info("Fetching today's trends...")
            trends_request = TaskRequest(
                requester_id=self.card.uuid,
                content="today's trends"
            )
            
            # Send request and wait for response
            await self.send_message(trends_request, target_id=trends_agent_id)
            trends_response = await self._wait_for_response(trends_request.task_id, timeout=30)
            
            # Parse trends from response (this is simplified - in production, parse the HTML table)
            # For now, we'll use a sample trend
            topics = self._extract_topics_from_response(trends_response.output)
            
            if not topics:
                topics = ["barcelona - frankfurt"]  # Fallback to known trend
            
            # Limit to top 3 for demo
            topics = topics[:3]
            
            # Step 2 & 3: For each topic, generate content and publish cube
            published_cubes = []
            
            for topic in topics:
                try:
                    logger.info(f"Processing topic: {topic}")
                    
                    # Generate content
                    content_gen_id = self._find_agent("Content Generator")
                    if not content_gen_id:
                        raise Exception("Content Generator not found")
                    
                    content_request = TaskRequest(
                        requester_id=self.card.uuid,
                        content=topic
                    )
                    
                    await self.send_message(content_request, target_id=content_gen_id)
                    content_response = await self._wait_for_response(content_request.task_id, timeout=60)
                    
                    # Extract Identity Cube JSON from artifacts
                    if content_response.artifacts:
                        cube_json = content_response.artifacts[0]
                        
                        # Publish cube
                        publisher_id = self._find_agent("Cube Publisher")
                        if not publisher_id:
                            raise Exception("Cube Publisher not found")
                        
                        publish_request = TaskRequest(
                            requester_id=self.card.uuid,
                            content=cube_json
                        )
                        
                        await self.send_message(publish_request, target_id=publisher_id)
                        publish_response = await self._wait_for_response(publish_request.task_id, timeout=30)
                        
                        published_cubes.append({
                            "topic": topic,
                            "status": publish_response.status
                        })
                    
                except Exception as e:
                    logger.error(f"Failed to process topic '{topic}': {e}")
                    published_cubes.append({
                        "topic": topic,
                        "status": "failed",
                        "error": str(e)
                    })
            
            # Format output
            output = f"""
<div style="margin-bottom: 20px;">
    <h3 style="margin: 0 0 15px 0; color: #00d4ff;">🚀 Pipeline Execution Complete</h3>
    <p style="color: #a0aec0;">Processed {len(topics)} trending topics</p>
</div>

<table style="width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.05); border-radius: 8px; overflow: hidden;">
    <thead>
        <tr style="background: rgba(0, 212, 255, 0.1); border-bottom: 2px solid #00d4ff;">
            <th style="padding: 12px; text-align: left; font-weight: 600;">Topic</th>
            <th style="padding: 12px; text-align: center; font-weight: 600;">Status</th>
        </tr>
    </thead>
    <tbody>
"""
            
            for cube in published_cubes:
                status_color = "#10b981" if cube["status"] == "completed" else "#ef4444"
                status_text = "✅ Published" if cube["status"] == "completed" else "❌ Failed"
                
                output += f"""
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
            <td style="padding: 12px; font-weight: 500;">{cube['topic']}</td>
            <td style="padding: 12px; text-align: center; color: {status_color}; font-weight: 600;">
                {status_text}
            </td>
        </tr>
"""
            
            output += """
    </tbody>
</table>

<div style="margin-top: 20px; padding: 15px; background: rgba(0, 212, 255, 0.1); border-radius: 8px;">
    <p style="margin: 0; color: #a0aec0;">
        📊 View all published cubes at <a href="https://philhills.ai/cubes/index.json" style="color: #00d4ff;">philhills.ai/cubes/index.json</a>
    </p>
</div>
"""
            
            response = TaskResponse(
                task_id=request.task_id,
                responder_id=self.card.uuid,
                status="completed",
                output=output
            )
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            response = TaskResponse(
                task_id=request.task_id,
                responder_id=self.card.uuid,
                status="failed",
                output=f"""
<div style="padding: 20px; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 8px;">
    <h3 style="margin: 0 0 10px 0; color: #ef4444;">❌ Pipeline Failed</h3>
    <p style="margin: 0;">{str(e)}</p>
</div>
"""
            )
        
        await self.send_message(response, target_id=request.requester_id)
    
    def _find_agent(self, name: str) -> str:
        """Find agent UUID by name."""
        for uuid, agent in self.bus._agents.items():
            if name.lower() in agent.card.name.lower():
                return uuid
        return None
    
    async def _wait_for_response(self, task_id: str, timeout: int = 30) -> TaskResponse:
        """Wait for a response to a specific task."""
        # This is a simplified implementation
        # In production, use a proper response tracking mechanism
        start_time = asyncio.get_event_loop().time()
        
        while (asyncio.get_event_loop().time() - start_time) < timeout:
            # Check inbox for response
            if not self.inbox.empty():
                cube = await self.inbox.get()
                from agents.protocol import CubeTransport
                payload = CubeTransport.unpack(cube)
                
                if payload.get("task_id") == task_id:
                    return TaskResponse(**payload)
                else:
                    # Put it back for later
                    await self.inbox.put(cube)
            
            await asyncio.sleep(0.1)
        
        raise TimeoutError(f"No response received for task {task_id}")
    
    def _extract_topics_from_response(self, html_output: str) -> List[str]:
        """Extract topic names from HTML table response."""
        # Simple extraction - look for topic names in the HTML
        # In production, use proper HTML parsing
        import re
        topics = []
        
        # Look for patterns like: <td ...>topic name</td>
        matches = re.findall(r'<td[^>]*>([^<#]+)</td>', html_output)
        
        # Filter out numbers, scores, and other non-topic content
        for match in matches:
            match = match.strip()
            if match and not match.isdigit() and len(match) > 3:
                if match not in topics:
                    topics.append(match)
        
        return topics[:10]  # Return top 10

if __name__ == "__main__":
    import argparse
    
    # Parse args
    parser = argparse.ArgumentParser(description='Automated Trend Content Pipeline')
    parser.add_argument('--auto-publish', action='store_true', help='Automatically publish generated content')
    args = parser.parse_args()
    
    # Define main async routine
    async def main():
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Initialize bus and agents
        from agents.agent_platform import MessageBus
        from agents.google_trends_agent import GoogleTrendsAgent
        from agents.content_generator import ContentGeneratorAgent
        from agents.cube_publisher import CubePublisherAgent
        
        bus = MessageBus()
        
        # Register agents
        pipeline = TrendPipelineAgent()
        trends = GoogleTrendsAgent()
        generator = ContentGeneratorAgent()
        publisher = CubePublisherAgent()
        
        bus.register(pipeline)
        bus.register(trends)
        bus.register(generator)
        bus.register(publisher)
        
        # Start agents in background
        agents = [pipeline, trends, generator, publisher]
        tasks = []
        for agent in agents:
            tasks.append(asyncio.create_task(agent.start()))
        
        # Trigger pipeline
        logger.info("Triggering trend pipeline...")
        request = TaskRequest(
            requester_id="system-trigger",
            content="run"
        )
        
        # Send request to pipeline agent
        # We need to inject it into the pipeline agent's inbox or use a specialized trigger
        await pipeline.receive(request)
        
        # Keep running to allow processing
        # In a real deployment, this would be a long-running service
        # For this script, we'll wait a bit then exit if it's a one-off job
        if args.auto_publish:
            # wait for completion
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(5)

    # Run
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
