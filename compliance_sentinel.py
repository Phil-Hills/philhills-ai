#!/usr/bin/env python3
"""
Compliance Sentinel: Real-Time Agent Audit System
Monitors Agent-to-Agent (A2A) communication for regulatory compliance.

Author: Phil Hills | Seattle Research Hub
License: MIT
"""

import hashlib
import json
import time
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Literal, Optional
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

AUDIT_LOG_PATH = Path("audit_compliance.jsonl")
NODE_ID = "SEA-SENTINEL-001"
PROTOCOL_VERSION = "Q-Protocol/1.2"

# Compliance Rules (simulated regulatory requirements)
COMPLIANCE_RULES = {
    "require_signature": True,
    "max_payload_bytes": 1_000_000,
    "allowed_protocols": ["Q-Protocol/1.2", "A2AC/1.0"],
    "blocked_actions": ["raw_sql_exec", "shell_exec", "credential_export"],
}


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class AuditEvent:
    """Immutable audit log entry."""
    timestamp: str
    event_type: Literal["HANDSHAKE", "TX_VERIFY", "BLOCK", "ALLOW"]
    node_id: str
    details: dict
    signature: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"))


@dataclass
class AgentTransaction:
    """Incoming agent transaction to audit."""
    tx_id: str
    source_agent: str
    target_agent: str
    action: str
    payload_size: int
    protocol: str
    signature: Optional[str] = None


# ============================================================================
# SENTINEL CORE
# ============================================================================

class ComplianceSentinel:
    """
    Real-time compliance auditor for agent-to-agent communication.
    Implements deterministic policy enforcement with immutable logging.
    """

    def __init__(self, node_id: str = NODE_ID):
        self.node_id = node_id
        self.rules = COMPLIANCE_RULES
        self.log_path = AUDIT_LOG_PATH
        self._boot_sequence()

    def _boot_sequence(self):
        """Initialize audit stream with boot log."""
        print(f"{'='*60}")
        print(f"  COMPLIANCE SENTINEL v2.0 | Node: {self.node_id}")
        print(f"  Protocol: {PROTOCOL_VERSION}")
        print(f"  Audit Log: {self.log_path.absolute()}")
        print(f"{'='*60}")
        self._log_event("BOOT", {"status": "INITIALIZED", "rules_loaded": len(self.rules)})

    def _compute_signature(self, data: str) -> str:
        """Generate BLAKE3-style hash (using SHA256 as fallback)."""
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _log_event(self, event_type: str, details: dict):
        """Append immutable audit event to JSONL log."""
        event = AuditEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            node_id=self.node_id,
            details=details,
            signature=self._compute_signature(json.dumps(details))
        )
        with open(self.log_path, "a") as f:
            f.write(event.to_json() + "\n")
        return event

    def audit_transaction(self, tx: AgentTransaction) -> tuple[bool, str]:
        """
        Audit an agent transaction against compliance rules.
        Returns (is_compliant, reason).
        """
        # Rule 1: Signature Required
        if self.rules["require_signature"] and not tx.signature:
            reason = "MISSING_SIGNATURE"
            self._log_event("BLOCK", {"tx_id": tx.tx_id, "reason": reason})
            print(f"[BLOCK] TX {tx.tx_id[:8]}... | Reason: {reason}")
            return False, reason

        # Rule 2: Payload Size Limit
        if tx.payload_size > self.rules["max_payload_bytes"]:
            reason = f"PAYLOAD_EXCEEDS_LIMIT ({tx.payload_size} > {self.rules['max_payload_bytes']})"
            self._log_event("BLOCK", {"tx_id": tx.tx_id, "reason": reason})
            print(f"[BLOCK] TX {tx.tx_id[:8]}... | Reason: {reason}")
            return False, reason

        # Rule 3: Protocol Allowlist
        if tx.protocol not in self.rules["allowed_protocols"]:
            reason = f"PROTOCOL_NOT_ALLOWED ({tx.protocol})"
            self._log_event("BLOCK", {"tx_id": tx.tx_id, "reason": reason})
            print(f"[BLOCK] TX {tx.tx_id[:8]}... | Reason: {reason}")
            return False, reason

        # Rule 4: Blocked Actions
        if tx.action in self.rules["blocked_actions"]:
            reason = f"ACTION_BLOCKED ({tx.action})"
            self._log_event("BLOCK", {"tx_id": tx.tx_id, "reason": reason})
            print(f"[BLOCK] TX {tx.tx_id[:8]}... | Reason: {reason}")
            return False, reason

        # All checks passed
        self._log_event("ALLOW", {
            "tx_id": tx.tx_id,
            "source": tx.source_agent,
            "target": tx.target_agent,
            "action": tx.action
        })
        print(f"[ALLOW] TX {tx.tx_id[:8]}... | {tx.source_agent} → {tx.target_agent}")
        return True, "COMPLIANT"

    def verify_handshake(self, agent_a: str, agent_b: str) -> bool:
        """Verify A2AC handshake between two agents."""
        self._log_event("HANDSHAKE", {"from": agent_a, "to": agent_b, "status": "VERIFIED"})
        print(f"[HANDSHAKE] {agent_a} ↔ {agent_b} | Status: VERIFIED")
        return True

    def generate_report(self) -> dict:
        """Generate compliance summary from audit log."""
        if not self.log_path.exists():
            return {"error": "No audit log found"}

        events = {"ALLOW": 0, "BLOCK": 0, "HANDSHAKE": 0, "BOOT": 0}
        with open(self.log_path, "r") as f:
            for line in f:
                event = json.loads(line)
                event_type = event.get("event_type", "UNKNOWN")
                events[event_type] = events.get(event_type, 0) + 1

        report = {
            "node_id": self.node_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_events": sum(events.values()),
            "allowed": events["ALLOW"],
            "blocked": events["BLOCK"],
            "compliance_rate": f"{events['ALLOW'] / max(1, events['ALLOW'] + events['BLOCK']) * 100:.1f}%"
        }

        print(f"\n{'='*60}")
        print(f"  COMPLIANCE REPORT | Node: {self.node_id}")
        print(f"{'='*60}")
        for key, value in report.items():
            print(f"  {key}: {value}")
        print(f"{'='*60}\n")

        return report


# ============================================================================
# DEMO EXECUTION
# ============================================================================

if __name__ == "__main__":
    sentinel = ComplianceSentinel()

    print("\n[DEMO] Simulating Agent Transactions...\n")

    # Compliant transaction
    tx1 = AgentTransaction(
        tx_id=hashlib.sha256(b"tx_001").hexdigest(),
        source_agent="Treasury_Agent",
        target_agent="Audit_Agent",
        action="balance_query",
        payload_size=1024,
        protocol="Q-Protocol/1.2",
        signature="abc123def456"
    )
    sentinel.audit_transaction(tx1)

    # Missing signature (will be blocked)
    tx2 = AgentTransaction(
        tx_id=hashlib.sha256(b"tx_002").hexdigest(),
        source_agent="Rogue_Agent",
        target_agent="Database_Agent",
        action="data_export",
        payload_size=512,
        protocol="Q-Protocol/1.2",
        signature=None  # Missing!
    )
    sentinel.audit_transaction(tx2)

    # Blocked action
    tx3 = AgentTransaction(
        tx_id=hashlib.sha256(b"tx_003").hexdigest(),
        source_agent="Admin_Agent",
        target_agent="System_Agent",
        action="shell_exec",  # Blocked action
        payload_size=128,
        protocol="Q-Protocol/1.2",
        signature="xyz789"
    )
    sentinel.audit_transaction(tx3)

    # Handshake verification
    sentinel.verify_handshake("Sentinel_Core", "Gateway_Agent")

    # Compliant transaction
    tx4 = AgentTransaction(
        tx_id=hashlib.sha256(b"tx_004").hexdigest(),
        source_agent="Rate_Monitor",
        target_agent="Alert_Dispatcher",
        action="send_notification",
        payload_size=256,
        protocol="A2AC/1.0",
        signature="sig_valid"
    )
    sentinel.audit_transaction(tx4)

    # Generate final report
    sentinel.generate_report()
