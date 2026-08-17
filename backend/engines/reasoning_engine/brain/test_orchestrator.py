from pprint import pprint

from engines.reasoning_engine.brain.orchestrator import BugHunterBrain

hypotheses = [

    {

        "workflow_name":"Authentication",

        "hypotheses":[

            "Authentication Bypass",

            "JWT Forgery",

            "IDOR"

        ]

    }

]

brain = BugHunterBrain()

brain.load_hypotheses(hypotheses)

results = brain.run()

print("\n")

print("="*70)

print("MEMORY SUMMARY")

print("="*70)

pprint(

    results["memory"].summary()

)

print("\n")

print("="*70)

print("FINAL REFLECTION")

print("="*70)

for reflection in results["reflections"]:

    print()

    print(reflection.strategy)

    print(reflection.decision)

    print(reflection.confidence_after)