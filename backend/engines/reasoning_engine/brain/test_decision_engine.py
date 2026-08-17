from engines.reasoning_engine.brain.memory import BrainMemory
from engines.reasoning_engine.brain.strategist import Strategist
from engines.reasoning_engine.brain.decision_engine import DecisionEngine


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

    confidence=0.82,

    tags=["idor"]

)

strategist = Strategist(brain)

strategies = strategist.generate()

decision_engine = DecisionEngine(strategies)

tasks = decision_engine.decide()

for task in tasks:

    print("=" * 60)

    print("Strategy :", task.strategy_name)

    print("Priority :", task.priority)

    print("Objective:", task.objective)

    print()

    print("Next Action")

    print(task.next_action)

    print()

    print("Reasoning")

    for reason in task.reasoning:

        print("-", reason)