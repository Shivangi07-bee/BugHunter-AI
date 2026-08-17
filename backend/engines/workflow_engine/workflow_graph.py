from collections import defaultdict
from typing import Dict, List, Set

from .models import WorkflowEdge


class WorkflowGraph:
    """
    Builds the application workflow graph from WorkflowEdge objects.

    Example:

        /login
            |
            v
        /profile
            |
            v
        /orders
            |
            v
        /payment
    """

    def __init__(self, edges: List[WorkflowEdge]):
        self.edges = edges
        self.graph: Dict[str, List[str]] = defaultdict(list)

    # -------------------------------------------------------
    # Add edge safely
    # -------------------------------------------------------

    def _add_edge(self, source: str, target: str) -> None:
        if not source or not target:
            return

        if target not in self.graph[source]:
            self.graph[source].append(target)

        # Keep nodes visible even if they have no outgoing edge.
        if target not in self.graph:
            self.graph[target] = []

    # -------------------------------------------------------
    # Build adjacency graph
    # -------------------------------------------------------

    def build(self) -> Dict[str, List[str]]:
        """
        Build the workflow graph.

        The graph remains undirected for workflow discovery because
        two related application nodes belong to the same workflow
        even when the relationship itself is not directional.
        """

        self.graph.clear()

        for edge in self.edges:
            source = getattr(edge, "source", None)
            target = getattr(edge, "target", None)

            if not source or not target:
                continue

            self._add_edge(source, target)
            self._add_edge(target, source)

        return {
            node: sorted(neighbors)
            for node, neighbors in sorted(self.graph.items())
        }

    # -------------------------------------------------------
    # Get neighbors
    # -------------------------------------------------------

    def neighbors(self, node: str) -> List[str]:
        return list(self.graph.get(node, []))

    # -------------------------------------------------------
    # Get all nodes
    # -------------------------------------------------------

    def nodes(self) -> Set[str]:
        return set(self.graph.keys())

    # -------------------------------------------------------
    # Pretty Print
    # -------------------------------------------------------

    def display(self) -> None:
        print("\n===== Workflow Graph =====\n")

        for node in sorted(self.graph.keys()):
            print(node)

            for neighbor in sorted(self.graph[node]):
                print(f"   └── {neighbor}")

        print("-" * 40)