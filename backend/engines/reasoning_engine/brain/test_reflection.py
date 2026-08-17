from engines.reasoning_engine.brain.memory import BrainMemory
from engines.reasoning_engine.brain.strategist import Strategist
from engines.reasoning_engine.brain.decision_engine import DecisionEngine
from engines.reasoning_engine.brain.attack_executor import AttackExecutor
from engines.reasoning_engine.brain.reflection import ReflectionEngine

brain = BrainMemory()

brain.remember(

    category="Hypothesis",

    title="Authentication Bypass",

    data={},

    confidence=0.90,

    tags=["auth"]

)

brain.remember(

    category="Hypothesis",

    title="IDOR",

    data={},

    confidence=0.82,

    tags=["idor"]

)

strategies = Strategist(brain).generate()

tasks = DecisionEngine(strategies).decide()

plans = AttackExecutor(tasks).build()

engine = ReflectionEngine(plans, brain)

results = engine.evaluate()

for r in results:

    print("=" * 70)

    print("Strategy :", r.strategy)

    print("Confidence Before :", r.confidence_before)

    print("Confidence After  :", r.confidence_after)

    print("Decision :", r.decision)

    print("Outcome :", r.outcome)

    print()

    print("Observations")

    for obs in r.observations:

        print("-", obs)

    print()

    print("Next Steps")

    for step in r.next_steps:

        print("-", step)

print("\nBrain Memory Summary")
print(brain.summary())