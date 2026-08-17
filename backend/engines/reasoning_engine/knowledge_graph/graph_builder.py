from .graph import SecurityKnowledgeGraph
from .graph_models import GraphNode, GraphEdge


class GraphBuilder:

    """
    Converts Workflow Context into a Security Knowledge Graph.
    """

    def __init__(self, workflow_context):

        self.workflow_context = workflow_context

    # ------------------------------------------

    def build(self):

        graph = SecurityKnowledgeGraph()

        endpoint_ids = {}

        model_ids = {}

        for workflow in self.workflow_context:

            for endpoint in workflow["endpoints"]:

                endpoint_node = GraphNode(

                    type="Endpoint",

                    name=endpoint["path"],

                    properties={

                        "method": endpoint["method"],

                        "authentication":
                        endpoint["authentication"]

                    }

                )

                graph.add_node(endpoint_node)

                endpoint_ids[
                    endpoint["path"]
                ] = endpoint_node.id

                for model in endpoint["models"]:

                    if model not in model_ids:

                        model_node = GraphNode(

                            type="Model",

                            name=model

                        )

                        graph.add_node(model_node)

                        model_ids[model] = model_node.id

                    graph.add_edge(

                        GraphEdge(

                            source=endpoint_node.id,

                            target=model_ids[model],

                            relationship="USES_MODEL",

                            confidence=0.95

                        )

                    )

        return graph