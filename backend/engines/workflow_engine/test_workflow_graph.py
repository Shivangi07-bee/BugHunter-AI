from engines.workflow_engine.models import WorkflowEdge
from engines.workflow_engine.workflow_graph import WorkflowGraph

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
    )

]

graph = WorkflowGraph(edges)

graph.build()

graph.display()