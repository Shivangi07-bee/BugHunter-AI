from pprint import pprint

from engines.reasoning_engine.evidence_collector import (
    EvidenceCollector
)

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
                "calls": [
                    "authenticate",
                    "generate_token"
                ]
            },

            {
                "path": "/profile",
                "method": "GET",
                "authentication": True,
                "models": ["User"],
                "calls": [
                    "verify_token",
                    "get_user"
                ]
            }

        ]

    }

]

hypotheses = [

    {

        "workflow_name": "Workflow 1",

        "hypotheses": [

            "Can authenticated endpoints be accessed without authentication?",

            "Is there an IDOR involving User resources?"

        ]

    }

]

collector = EvidenceCollector(
    workflow_context,
    hypotheses
)

pprint(collector.collect())