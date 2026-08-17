from dataclasses import dataclass, field
from typing import List, Dict
from uuid import uuid4


@dataclass
class AttackPath:

    id: str = field(default_factory=lambda: str(uuid4()))

    name: str = ""

    entry_point: str = ""

    target: str = ""

    attack_type: str = ""

    confidence: float = 0.0

    steps: List[str] = field(default_factory=list)

    evidence: List[Dict] = field(default_factory=list)

    assumptions: List[str] = field(default_factory=list)


class AttackPlanner:

    """
    Generates attack paths from Security Knowledge Graph.
    """

    def __init__(self, graph):

        self.graph = graph

    # ------------------------------------------------------

    def generate(self):

        attack_paths = []

        endpoint_nodes = [

            node for node in self.graph.nodes.values()

            if node.type == "Endpoint"

        ]

        for source in endpoint_nodes:

            neighbors = self.graph.get_neighbors(source.id)

            for target_id in neighbors:

                target = self.graph.nodes[target_id]

                if target.type != "Model":
                    continue

                attack = AttackPath(

                    name=f"{source.name} -> {target.name}",

                    entry_point=source.name,

                    target=target.name,

                    attack_type="Model Interaction",

                    confidence=0.70,

                    steps=[
                        source.name,
                        target.name
                    ],

                    evidence=[

                        {

                            "relationship": "USES_MODEL",

                            "model": target.name

                        }

                    ],

                    assumptions=[

                        "Shared model may indicate shared state",

                        "Model may expose business logic"

                    ]

                )

                attack_paths.append(attack)

        return attack_paths