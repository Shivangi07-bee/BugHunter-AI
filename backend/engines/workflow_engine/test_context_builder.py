from engines.workflow_engine.context_builder import WorkflowContextBuilder
from engines.workflow_engine.models import Workflow

workflows = [

    Workflow(

        name="Workflow 1",

        endpoints=[
            "/login",
            "/profile"
        ],

        shared_models=set(),

        shared_functions=set()

    )

]

endpoint_metadata = [

    {
        "path": "/login",
        "method": "POST",
        "handler": "login",
        "models": ["User"],
        "calls": [
            "authenticate",
            "generate_token"
        ],
        "authentication": False
    },

    {
        "path": "/profile",
        "method": "GET",
        "handler": "profile",
        "models": ["User"],
        "calls": [
            "verify_token",
            "get_user"
        ],
        "authentication": True
    }

]

builder = WorkflowContextBuilder(
    workflows,
    endpoint_metadata
)

contexts = builder.build()

from pprint import pprint

pprint(contexts)