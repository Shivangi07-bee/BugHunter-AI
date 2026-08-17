from dataclasses import dataclass, field
from typing import Dict, List
from uuid import uuid4


@dataclass
class GraphNode:
    """
    Universal graph node.

    Every entity inside BugHunter AI becomes a node.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    type: str = ""

    name: str = ""

    properties: Dict = field(default_factory=dict)


@dataclass
class GraphEdge:
    """
    Relationship between two graph nodes.
    """

    source: str = ""

    target: str = ""

    relationship: str = ""

    confidence: float = 1.0

    metadata: Dict = field(default_factory=dict)