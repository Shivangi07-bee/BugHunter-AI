from engines.reasoning_engine.runtime.request_planner import RequestPlanner

planner = RequestPlanner()

planner.add_request(

    "/login",

    "POST",

    "Authenticate user",

    priority=100

)

planner.add_request(

    "/profile",

    "GET",

    "Verify authorization",

    priority=90

)

while planner.remaining():

    print(planner.next_request())