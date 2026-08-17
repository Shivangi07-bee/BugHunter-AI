from pprint import pprint

from engines.reasoning_engine.agent.investigation_loop import InvestigationLoop

loop = InvestigationLoop(

    [

        {

            "workflow_name":"Authentication",

            "hypotheses":[

                "Authentication Bypass",

                "IDOR"

            ]

        }

    ]

)

result = loop.run_once()

pprint(result["runtime"])