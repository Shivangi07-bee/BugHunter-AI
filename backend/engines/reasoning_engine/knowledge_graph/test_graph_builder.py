from engines.reasoning_engine.knowledge_graph.graph_builder import GraphBuilder

workflow_context = [

    {

        "workflow_name":"Workflow 1",

        "endpoint_count":2,

        "endpoints":[

            {

                "path":"/login",

                "method":"POST",

                "authentication":False,

                "models":["User"],

                "calls":[]

            },

            {

                "path":"/profile",

                "method":"GET",

                "authentication":True,

                "models":["User"],

                "calls":[]

            }

        ]

    }

]

builder = GraphBuilder(workflow_context)

graph = builder.build()

graph.summary()

print()

print("Nodes")

print("--------------------------------")

for node in graph.nodes.values():

    print(node)

print()

print("Edges")

print("--------------------------------")

for edge in graph.edges:

    print(edge)