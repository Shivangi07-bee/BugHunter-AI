from engines.workflow_engine.workflow_graph import WorkflowGraph
from engines.workflow_engine.workflow_detector import WorkflowDetector
from engines.workflow_engine.models import WorkflowEdge

edges = [

    WorkflowEdge(
        source="/login",
        target="/profile",
        reason="shared_model:User"
    ),

    WorkflowEdge(
        source="/profile",
        target="/orders",
        reason="shared_model:User"
    ),

    WorkflowEdge(
        source="/orders",
        target="/payment",
        reason="shared_model:Order"
    ),

    # Second workflow

    WorkflowEdge(
        source="/admin/login",
        target="/admin/users",
        reason="shared_model:Admin"
    )

]

graph = WorkflowGraph(edges)

adjacency = graph.build()

detector = WorkflowDetector(adjacency)

workflows = detector.detect()

for workflow in workflows:

    print("=" * 50)

    print(workflow.name)

    print()

    for endpoint in workflow.endpoints:

        print("  ", endpoint)