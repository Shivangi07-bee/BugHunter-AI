from engines.reasoning_engine.brain.memory import BrainMemory
from engines.reasoning_engine.brain.strategist import Strategist
from engines.reasoning_engine.brain.decision_engine import DecisionEngine
from engines.reasoning_engine.brain.attack_executor import AttackExecutor

brain = BrainMemory()

brain.remember(

    category="Hypothesis",

    title="Authentication Bypass",

    data={},

    confidence=0.94,

    tags=["auth"]

)

brain.remember(

    category="Hypothesis",

    title="IDOR",

    data={},

    confidence=0.88,

    tags=["idor"]

)

strategies = Strategist(brain).generate()

tasks = DecisionEngine(strategies).decide()

plans = AttackExecutor(tasks).build()

for plan in plans:

    print("=" * 70)

    print(plan.strategy_name)

    print(plan.objective)

    print(plan.priority)

    print()

    for step in plan.attack_steps:

        print(f"Step {step.step_number}")

        print(step.action)

        print(step.request_template)

        print("Expected:", step.expected_result)

        print()