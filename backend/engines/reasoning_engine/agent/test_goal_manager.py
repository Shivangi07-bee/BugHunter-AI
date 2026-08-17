from pprint import pprint

from engines.reasoning_engine.agent.goal_manager import GoalManager

manager = GoalManager()

manager.create_default_goals()

goal = manager.next_goal()

print()

print("Current Goal")

print(goal.name)

print()

manager.add_observation(

    goal.name,

    "JWT generation detected."

)

manager.add_observation(

    goal.name,

    "Protected endpoint discovered."

)

manager.complete(

    goal.name

)

print()

print("Next Goal")

print(

    manager.next_goal().name

)

print()

pprint(

    manager.summary()

)