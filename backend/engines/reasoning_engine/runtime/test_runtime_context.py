from pprint import pprint

from engines.reasoning_engine.runtime.runtime_context import RuntimeContextManager

runtime = RuntimeContextManager()

runtime.load_repository("Demo App")

runtime.set_workflow("Authentication")

runtime.set_goal("Authentication")

runtime.set_strategy("Authentication Assessment")

runtime.set_endpoint("/login")

runtime.set_authentication_state("Unauthenticated")

runtime.discover_endpoint("/profile")

runtime.discover_endpoint("/orders")

runtime.add_observation("JWT token generated")

runtime.add_attack("Replay JWT")

runtime.add_evidence({

    "endpoint":"/login",

    "type":"JWT"

})

runtime.update_metadata(

    "language",

    "Python"

)

pprint(

    runtime.snapshot()

)