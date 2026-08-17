from engines.reasoning_engine.agent.agent_controller import AgentController

agent = AgentController(

    [

        {

            "workflow_name":"Authentication",

            "hypotheses":[

                "Authentication Bypass",

                "JWT Forgery",

                "IDOR"

            ]

        }

    ]

)

agent.start()