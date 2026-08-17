from dataclasses import dataclass, field
from typing import List, Dict, Any
from uuid import uuid4


@dataclass
class InvestigationWorkspace:
    """
    Central investigation object.

    Every engine writes its output here.
    The frontend reads only this object.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    # --------------------------------------------------
    # Repository Understanding
    # --------------------------------------------------

    repository: Dict[str, Any] = field(default_factory=dict)

    routes: List[Dict] = field(default_factory=list)

    endpoints: List[Dict] = field(default_factory=list)

    # --------------------------------------------------
    # Workflow Engine
    # --------------------------------------------------

    workflows: List[Dict] = field(default_factory=list)

    knowledge_graph: Dict[str, Any] = field(default_factory=dict)

    investigation_plan: List[Dict] = field(default_factory=list)

    # --------------------------------------------------
    # Reasoning Engine
    # --------------------------------------------------

    hypotheses: List[Dict] = field(default_factory=list)

    evidence: List[Dict] = field(default_factory=list)

    risk: Dict[str, Any] = field(default_factory=dict)

    attack_plans: List[Dict] = field(default_factory=list)

    findings: List[Dict] = field(default_factory=list)

    # --------------------------------------------------
    # Brain
    # --------------------------------------------------

    brain: Dict[str, Any] = field(default_factory=dict)

    # --------------------------------------------------
    # Executive Summary
    # --------------------------------------------------

    executive_summary: Dict[str, Any] = field(default_factory=dict)

    # --------------------------------------------------
    # Timeline
    # --------------------------------------------------

    timeline: List[Dict] = field(default_factory=list)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: Dict[str, Any] = field(default_factory=dict)