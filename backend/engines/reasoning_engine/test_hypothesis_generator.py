from pprint import pprint

from engines.reasoning_engine.hypothesis_generator import (
    HypothesisGenerator
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

generator = HypothesisGenerator(workflow_context)

pprint(generator.generate())