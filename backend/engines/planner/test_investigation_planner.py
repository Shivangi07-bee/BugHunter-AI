from investigation_planner import InvestigationPlanner


workflows = []

hypotheses = [
    "Payment bypass",
    "Privilege escalation"
]

graph = {
    "nodes": [],
    "edges": [
        {
            "source": "/payment",
            "relationship": "USES",
            "target": "Order"
        }
    ]
}

planner = InvestigationPlanner(
    workflows,
    hypotheses,
    graph
)

tasks = planner.build()

for task in tasks:
    print(task)