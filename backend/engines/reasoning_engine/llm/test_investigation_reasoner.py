from engines.reasoning_engine.brain.orchestrator import BugHunterBrain

from engines.reasoning_engine.runtime.runtime_context import RuntimeContextManager

from engines.reasoning_engine.llm.prompt_builder import PromptBuilder

from engines.reasoning_engine.llm.investigation_reasoner import InvestigationReasoner

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

brain_output = brain.run()

runtime = RuntimeContextManager()

runtime.set_goal("Authentication")

runtime.set_workflow("Authentication Workflow")

builder = PromptBuilder(brain_output)

reasoner = InvestigationReasoner(

    runtime.snapshot(),

    brain_output,

    builder

)

result = reasoner.build()

print(result)