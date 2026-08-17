from typing import Dict, List, Set

from .models import Workflow


class WorkflowDetector:
    """
    Reconstruct application workflows from the endpoint relationship graph.

    Responsibilities:
        1. Normalize graph nodes.
        2. Find connected endpoint groups.
        3. Preserve all discovered endpoints.
        4. Produce deterministic workflow ordering.
        5. Never invent endpoints or application behaviour.

    Important:
        The RelationshipBuilder currently provides an undirected adjacency
        graph. Therefore this detector reconstructs connected workflows,
        but does not pretend that an undirected edge gives a true
        request sequence.
    """

    def __init__(self, graph: Dict[str, List[str]]):
        self.graph = graph or {}
        self.visited: Set[str] = set()

    # =========================================================
    # NODE NORMALIZATION
    # =========================================================

    @staticmethod
    def _normalize_node(node: str) -> str:
        """
        Normalize endpoint names without changing their meaning.

        Examples:

            "/login"              -> "/login"
            "GET /login"          -> "/login"
            "POST /payment"       -> "/payment"
            " /checkout "         -> "/checkout"
        """

        if node is None:
            return ""

        value = str(node).strip()

        if not value:
            return ""

        parts = value.split()

        # Handle:
        # GET /login
        # POST /payment
        # PUT /profile
        if len(parts) >= 2:
            first = parts[0].upper()

            if first in {
                "GET",
                "POST",
                "PUT",
                "PATCH",
                "DELETE",
                "HEAD",
                "OPTIONS",
            }:
                value = parts[1]

        # Remove surrounding whitespace.
        value = value.strip()

        # Endpoint paths should begin with "/".
        if value and not value.startswith("/"):
            value = "/" + value

        # Avoid accidental trailing slash except root.
        if len(value) > 1:
            value = value.rstrip("/")

        return value

    # =========================================================
    # ENDPOINT CLASSIFICATION
    # =========================================================

    @classmethod
    def _is_endpoint(cls, node: str) -> bool:
        """
        Determine whether a graph node represents an HTTP endpoint.
        """

        normalized = cls._normalize_node(node)

        if not normalized:
            return False

        return normalized.startswith("/")

    # =========================================================
    # NORMALIZE GRAPH
    # =========================================================

    def _normalized_graph(self) -> Dict[str, List[str]]:
        """
        Create a clean adjacency graph.

        This prevents small formatting differences such as:

            "/login"
            "GET /login"

        from becoming different nodes.
        """

        normalized: Dict[str, List[str]] = {}

        for raw_node, raw_neighbors in self.graph.items():

            node = self._normalize_node(raw_node)

            if not node:
                continue

            normalized.setdefault(node, [])

            if not isinstance(raw_neighbors, list):
                raw_neighbors = []

            for raw_neighbor in raw_neighbors:

                neighbor = self._normalize_node(raw_neighbor)

                if not neighbor:
                    continue

                if neighbor not in normalized[node]:
                    normalized[node].append(neighbor)

                # Keep the graph safe even if the incoming graph
                # accidentally contains only one direction.
                normalized.setdefault(neighbor, [])

                if node not in normalized[neighbor]:
                    normalized[neighbor].append(node)

        # Stable ordering.
        for node in normalized:
            normalized[node] = sorted(
                set(normalized[node])
            )

        return normalized

    # =========================================================
    # DEPTH FIRST SEARCH
    # =========================================================

    def _dfs(
        self,
        node: str,
        graph: Dict[str, List[str]],
        component: List[str],
    ) -> None:

        if node in self.visited:
            return

        self.visited.add(node)
        component.append(node)

        for neighbor in graph.get(node, []):

            if neighbor not in self.visited:

                self._dfs(
                    neighbor,
                    graph,
                    component,
                )

    # =========================================================
    # CONNECTED COMPONENTS
    # =========================================================

    def _components(
        self,
        graph: Dict[str, List[str]],
    ) -> List[List[str]]:

        components: List[List[str]] = []

        self.visited.clear()

        for node in sorted(graph):

            if node in self.visited:
                continue

            component: List[str] = []

            self._dfs(
                node,
                graph,
                component,
            )

            if component:
                components.append(
                    sorted(component)
                )

        return components

    # =========================================================
    # ENDPOINT ORDERING
    # =========================================================

    def _order_endpoints(
        self,
        endpoints: Set[str],
        graph: Dict[str, List[str]],
    ) -> List[str]:
        """
        Produce deterministic ordering for endpoints.

        Because the current RelationshipBuilder produces an undirected
        graph, this method deliberately does NOT claim to know the real
        HTTP request sequence.

        Ordering preference:

            1. Connectivity structure
            2. Stable lexical order

        This gives predictable UI output while preserving all endpoints.
        """

        if not endpoints:
            return []

        remaining = set(endpoints)

        scores = []

        for endpoint in remaining:

            neighbors = set(
                graph.get(endpoint, [])
            )

            endpoint_neighbors = (
                neighbors & remaining
            )

            scores.append(
                (
                    len(endpoint_neighbors),
                    endpoint,
                )
            )

        # Lower connectivity first, then lexical order.
        scores.sort(
            key=lambda item: (
                item[0],
                item[1],
            )
        )

        return [
            endpoint
            for _, endpoint in scores
        ]

    # =========================================================
    # WORKFLOW NAME
    # =========================================================

    @staticmethod
    def _workflow_name(
        index: int,
        endpoints: List[str],
    ) -> str:
        """
        Generate a meaningful workflow name.
        """

        if not endpoints:
            return f"Workflow {index}"

        first = endpoints[0]

        cleaned = (
            first
            .strip("/")
            .replace("/", " ")
            .replace("-", " ")
            .replace("_", " ")
            .strip()
        )

        if not cleaned:
            return f"Workflow {index}"

        words = cleaned.split()

        label = " ".join(
            word.capitalize()
            for word in words
        )

        return f"{label} Workflow"

    # =========================================================
    # COLLECT SHARED MODELS
    # =========================================================

    def _collect_shared_models(
        self,
        endpoints: List[str],
    ) -> Set[str]:
        """
        The current detector receives only adjacency data, so models
        cannot be recovered here.

        This method intentionally returns an empty set rather than
        inventing model relationships.
        """

        return set()

    # =========================================================
    # COLLECT SHARED FUNCTIONS
    # =========================================================

    def _collect_shared_functions(
        self,
        endpoints: List[str],
    ) -> Set[str]:
        """
        The current detector receives only adjacency data, so function
        metadata cannot be recovered here.

        Return an empty set instead of fabricating information.
        """

        return set()

    # =========================================================
    # DETECT WORKFLOWS
    # =========================================================

    def detect(self) -> List[Workflow]:
        """
        Detect workflows from connected endpoint components.
        """

        graph = self._normalized_graph()

        if not graph:
            return []

        components = self._components(
            graph
        )

        workflows: List[Workflow] = []

        workflow_number = 1

        for component in components:

            # -------------------------------------------------
            # Keep only real HTTP endpoints.
            # -------------------------------------------------

            endpoints = {
                node
                for node in component
                if self._is_endpoint(node)
            }

            if not endpoints:
                continue

            ordered_endpoints = (
                self._order_endpoints(
                    endpoints,
                    graph,
                )
            )

            if not ordered_endpoints:
                continue

            workflow = Workflow(
                name=self._workflow_name(
                    workflow_number,
                    ordered_endpoints,
                ),
                endpoints=ordered_endpoints,
                shared_models=self._collect_shared_models(
                    ordered_endpoints
                ),
                shared_functions=self._collect_shared_functions(
                    ordered_endpoints
                ),
            )

            workflows.append(
                workflow
            )

            workflow_number += 1

        return workflows

    # =========================================================
    # DEBUG INFORMATION
    # =========================================================

    def debug_summary(self) -> Dict:
        """
        Return diagnostic information useful while developing the
        workflow engine.

        This does not affect workflow detection.
        """

        graph = self._normalized_graph()

        components = self._components(
            graph
        )

        endpoint_count = 0

        for node in graph:

            if self._is_endpoint(node):
                endpoint_count += 1

        return {
            "graph_nodes": len(graph),
            "endpoint_nodes": endpoint_count,
            "connected_components": len(
                components
            ),
            "components": components,
        }