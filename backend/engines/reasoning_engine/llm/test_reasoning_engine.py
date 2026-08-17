from engines.reasoning_engine.brain.orchestrator import BugHunterBrain

from engines.reasoning_engine.llm.prompt_builder import PromptBuilder

from engines.reasoning_engine.llm.reasoning_engine import (
    AIReasoningEngine,
    MockProvider
)

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

prompt = PromptBuilder(

    brain_output

).build()

engine = AIReasoningEngine(

    MockProvider()

)

result = engine.analyze(

    prompt

)

print("="*70)

print(result.summary)

print()

print(result.attack_analysis)

print()

print(result.verdict)

print(result.confidence)

print()

print(result.recommendations)