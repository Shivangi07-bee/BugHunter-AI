from pprint import pprint

from engines.reasoning_engine.brain.memory import BrainMemory

brain = BrainMemory()

brain.remember(

    category="Hypothesis",

    title="Authentication Bypass",

    data={

        "endpoint":"/login"

    },

    confidence=0.81,

    tags=["auth","critical"]

)

brain.remember(

    category="Evidence",

    title="JWT Generated",

    data={

        "function":"generate_token"

    },

    confidence=0.91,

    tags=["jwt"]

)

print()

print("SUMMARY")

print(brain.summary())

print()

print("HYPOTHESES")

pprint(

    brain.recall_by_category(

        "Hypothesis"

    )

)

print()

print("SEARCH")

pprint(

    brain.search(

        "token"

    )

)