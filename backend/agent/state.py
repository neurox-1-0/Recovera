from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class AgentState:

    goal: str

    # Contract information
    contract: Dict[str, Any] = field(
        default_factory=dict
    )

    # Monitoring contains multiple records
    monitoring: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Incident records
    incidents: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Provider communication records
    emails: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Financial information
    finance: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # Generated evidence
    evidence: List[str] = field(
        default_factory=list
    )

    # Track executed tools
    completed_tools: List[str] = field(
        default_factory=list
    )

    # Agent confidence score
    confidence: float = 0.0

    # Final recommendation
    recommendation: str = ""