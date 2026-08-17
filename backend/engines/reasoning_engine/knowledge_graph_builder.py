from typing import Dict, List


class KnowledgeGraphBuilder:

    def __init__(self, endpoint_metadata, workflow_edges):

        self.endpoint_metadata = endpoint_metadata
        self.workflow_edges = workflow_edges

    def build(self):

        nodes = []
        edges = []

        seen = set()

        # ------------------------
        # Endpoint Nodes
        # ------------------------

        for endpoint in self.endpoint_metadata:

            endpoint_name = endpoint["path"]

            if endpoint_name not in seen:

                nodes.append({

                    "id": endpoint_name,

                    "label": endpoint_name,

                    "type": "endpoint"

                })

                seen.add(endpoint_name)

        # ------------------------
        # Model Nodes
        # ------------------------

        for endpoint in self.endpoint_metadata:

            for model in endpoint.get("models", []):

                if model not in seen:

                    nodes.append({

                        "id": model,

                        "label": model,

                        "type": "model"

                    })

                    seen.add(model)

                edges.append({

                    "source": endpoint["path"],

                    "relationship": "USES",

                    "target": model

                })

        # ------------------------
        # Workflow Relationships
        # ------------------------

        for edge in self.workflow_edges:

            edges.append({

                "source": edge.source,

                "relationship": edge.reason,

                "target": edge.target

            })

        return {

            "nodes": nodes,

            "edges": edges

        }