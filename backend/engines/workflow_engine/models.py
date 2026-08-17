from dataclasses import dataclass, field
from typing import Set, List


@dataclass
class EndpointNode:
    """
    Represents a single API endpoint inside the workflow graph.
    """

    path: str
    method: str
    handler: str
    models: Set[str] = field(default_factory=set)
    functions: Set[str] = field(default_factory=set)


@dataclass
class WorkflowEdge:
    """
    Represents a relationship between two endpoints.
    """

    source: str
    target: str
    reason: str


@dataclass
class Workflow:
    """
    Represents a reconstructed business workflow.
    """

    name: str
    endpoints: List[str] = field(default_factory=list)
    shared_models: Set[str] = field(default_factory=set)
    shared_functions: Set[str] = field(default_factory=set)