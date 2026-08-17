from engines.reasoning_engine.brain.memory import BrainMemory
from engines.reasoning_engine.brain.strategist import Strategist

brain = BrainMemory()

brain.remember(

    category="Hypothesis",

    title="Authentication Bypass",

    data={},

    confidence=0.95,

    tags=["auth"]

)

brain.remember(

    category="Hypothesis",

    title="IDOR",

    data={},

    confidence=0.88,

    tags=["idor"]

)

strategist = Strategist(brain)

plans = strategist.generate()

for plan in plans:

    print("="*60)

    print(plan.name)

    print(plan.priority)

    print(plan.objective)

    print()

    print("Reasoning")

    for r in plan.reasoning:

        print("-", r)

    print()

    print("Actions")

    for a in plan.actions:

        print("-", a)