from collections import defaultdict

from .graph_models import GraphNode, GraphEdge


class SecurityKnowledgeGraph:

    def __init__(self):

        self.nodes = {}

        self.edges = []

        self.adjacency = defaultdict(list)

    # -----------------------------

    def add_node(self, node: GraphNode):

        self.nodes[node.id] = node

    # -----------------------------

    def add_edge(self, edge: GraphEdge):

        self.edges.append(edge)

        self.adjacency[edge.source].append(edge.target)

    # -----------------------------

    def get_neighbors(self, node_id):

        return self.adjacency[node_id]

    # -----------------------------

    def summary(self):

        print("=" * 60)

        print("Security Knowledge Graph")

        print()

        print(f"Nodes : {len(self.nodes)}")

        print(f"Edges : {len(self.edges)}")

        print("=" * 60)