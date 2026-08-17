from pprint import pprint

from engines.reasoning_engine.risk_ranker import RiskRanker

evidence = [

    {

        "workflow_name": "Workflow 1",

        "hypotheses": [

            {

                "hypothesis": "Can authentication be bypassed?",

                "evidence": {

                    "endpoint_count": 2,

                    "endpoints": [

                        {
                            "path": "/login",
                            "method": "POST",
                            "authentication": False,
                            "models": ["User"]
                        },

                        {
                            "path": "/profile",
                            "method": "GET",
                            "authentication": True,
                            "models": ["User"]
                        }

                    ]

                }

            }

        ]

    }

]

ranker = RiskRanker(evidence)

pprint(ranker.rank())