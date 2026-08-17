from pprint import pprint

from engines.reasoning_engine.agent.runtime_state import RuntimeStateManager

runtime = RuntimeStateManager()

runtime.set_goal("Authentication")

runtime.set_strategy("Authentication Assessment")

runtime.set_action("Inspect Login")

runtime.add_pending_action("Replay JWT")

runtime.add_pending_action("Modify JWT")

runtime.complete_action("Replay JWT")

runtime.add_observation("JWT detected")

runtime.add_evidence({

    "endpoint": "/login",

    "type": "JWT"

})

runtime.increase_confidence(0.25)

runtime.next_iteration()

pprint(runtime.snapshot())