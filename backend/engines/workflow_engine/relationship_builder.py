from typing import List, Dict, Set

from .models import EndpointNode, WorkflowEdge


class RelationshipBuilder:
    """
    Builds relationships between API endpoints.

    Relationship sources:
    1. Explicit endpoint dependencies
    2. Shared models
    3. Shared function calls
    4. Route references discovered in endpoint metadata

    The builder intentionally does NOT invent arbitrary relationships.
    """

    def __init__(self, endpoint_metadata: List[Dict]):
        self.endpoint_metadata = endpoint_metadata or []
        self.nodes = self._build_nodes()

    # --------------------------------------------------
    # Convert endpoint metadata into EndpointNode objects
    # --------------------------------------------------

    def _build_nodes(self) -> List[EndpointNode]:

        nodes = []

        for endpoint in self.endpoint_metadata:

            node = EndpointNode(
                path=str(endpoint.get("path", "")),
                method=str(endpoint.get("method", "")),
                handler=str(endpoint.get("handler", "")),
                models=set(endpoint.get("models", []) or []),
                functions=set(
                    endpoint.get("calls", [])
                    or endpoint.get("functions", [])
                    or []
                ),
            )

            if node.path:
                nodes.append(node)

        return nodes

    # --------------------------------------------------
    # Helper: add unique edge
    # --------------------------------------------------

    def _add_edge(
        self,
        edges: List[WorkflowEdge],
        seen: Set[tuple],
        source: str,
        target: str,
        reason: str,
    ):

        if not source or not target:
            return

        if source == target:
            return

        key = (source, target, reason)

        reverse_key = (target, source, reason)

        if key in seen or reverse_key in seen:
            return

        seen.add(key)

        edges.append(
            WorkflowEdge(
                source=source,
                target=target,
                reason=reason,
            )
        )

    # --------------------------------------------------
    # Find relationships
    # --------------------------------------------------

    def build_relationships(self) -> List[WorkflowEdge]:

        edges = []
        seen = set()

        total = len(self.nodes)

        # Map paths for explicit dependency lookup
        endpoint_paths = {
            node.path
            for node in self.nodes
            if node.path
        }

        # --------------------------------------------------
        # 1. Explicit relationships from metadata
        # --------------------------------------------------

        for endpoint in self.endpoint_metadata:

            source = str(endpoint.get("path", ""))

            dependencies = (
                endpoint.get("depends_on", [])
                or endpoint.get("dependencies", [])
                or endpoint.get("next", [])
                or endpoint.get("related_endpoints", [])
                or []
            )

            if isinstance(dependencies, str):
                dependencies = [dependencies]

            for target in dependencies:

                target = str(target)

                if target in endpoint_paths:

                    self._add_edge(
                        edges,
                        seen,
                        source,
                        target,
                        "explicit_dependency",
                    )

        # --------------------------------------------------
        # 2. Shared models / shared functions
        # --------------------------------------------------

        for i in range(total):

            for j in range(i + 1, total):

                node1 = self.nodes[i]
                node2 = self.nodes[j]

                # ------------------------
                # Shared Models
                # ------------------------

                shared_models = node1.models & node2.models

                for model in shared_models:

                    self._add_edge(
                        edges,
                        seen,
                        node1.path,
                        node2.path,
                        f"shared_model:{model}",
                    )

                # ------------------------
                # Shared Function Calls
                # ------------------------

                shared_functions = node1.functions & node2.functions

                for function in shared_functions:

                    self._add_edge(
                        edges,
                        seen,
                        node1.path,
                        node2.path,
                        f"shared_function:{function}",
                    )

        # --------------------------------------------------
        # 3. Detect endpoint references inside calls
        #
        # Example:
        # /checkout calls "/payment"
        #
        # This creates:
        # /checkout -> /payment
        # --------------------------------------------------

        path_lookup = {
            path: path
            for path in endpoint_paths
        }

        for node in self.nodes:

            for function in node.functions:

                function = str(function)

                for path in path_lookup:

                    if path == node.path:
                        continue

                    if path in function:

                        self._add_edge(
                            edges,
                            seen,
                            node.path,
                            path,
                            "endpoint_reference",
                        )

        return edges

    # --------------------------------------------------
    # Build adjacency graph
    # --------------------------------------------------

    def build_graph(self) -> Dict[str, List[str]]:

        graph = {}

        # Every endpoint MUST exist as a graph node,
        # even if it has no relationship yet.

        for node in self.nodes:

            graph.setdefault(node.path, [])

        edges = self.build_relationships()

        for edge in edges:

            graph.setdefault(edge.source, [])
            graph.setdefault(edge.target, [])

            if edge.target not in graph[edge.source]:
                graph[edge.source].append(edge.target)

            if edge.source not in graph[edge.target]:
                graph[edge.target].append(edge.source)

        return graph