from engines.reasoning_engine.brain.orchestrator import BugHunterBrain
from engines.reasoning_engine.llm.prompt_builder import PromptBuilder

brain = BugHunterBrain()

brain.load_hypotheses(

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

output = brain.run()

builder = PromptBuilder(output)

prompt = builder.build()

print(prompt)