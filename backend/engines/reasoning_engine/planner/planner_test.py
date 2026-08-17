from engines.reasoning_engine.knowledge_graph.graph_builder import GraphBuilder
from engines.reasoning_engine.planner.attack_planner import AttackPlanner

workflow_context = [

    {

        "workflow_name": "Workflow 1",

        "endpoint_count": 2,

        "endpoints": [

            {

                "path": "/login",

                "method": "POST",

                "authentication": False,

                "models": ["User"],

                "calls": []

            },

            {

                "path": "/profile",

                "method": "GET",

                "authentication": True,

                "models": ["User"],

                "calls": []

            }

        ]

    }

]

graph = GraphBuilder(workflow_context).build()

planner = AttackPlanner(graph)

paths = planner.generate()

for path in paths:

    print("=" * 60)

    print(path.name)

    print(path.attack_type)

    print(path.confidence)

    print(path.steps)

    print(path.evidence)

    print(path.assumptions)