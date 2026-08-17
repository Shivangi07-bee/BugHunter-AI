from dataclasses import dataclass, field
from typing import List
from uuid import uuid4


@dataclass
class InvestigationGoal:

    id: str = field(default_factory=lambda: str(uuid4()))

    name: str = ""

    description: str = ""

    priority: int = 0

    completed: bool = False

    success_criteria: List[str] = field(default_factory=list)

    observations: List[str] = field(default_factory=list)


class GoalManager:
    """
    Defines what BugHunter AI is trying to achieve.

    A junior bug hunter always has goals,
    not just vulnerabilities.

    Example:

    Goal:
        Verify Authentication

    Goal:
        Verify Authorization

    Goal:
        Verify Business Logic

    Goal:
        Verify Payment Integrity
    """

    def __init__(self):

        self.goals = []

    # ----------------------------------------------------

    def create_default_goals(self):

        self.goals = [

            InvestigationGoal(

                name="Authentication",

                description="Verify authentication boundaries.",

                priority=100,

                success_criteria=[

                    "Authentication workflow understood",

                    "Session handling analyzed",

                    "JWT handling analyzed"

                ]

            ),

            InvestigationGoal(

                name="Authorization",

                description="Verify authorization controls.",

                priority=95,

                success_criteria=[

                    "Object ownership checked",

                    "Privilege boundaries checked"

                ]

            ),

            InvestigationGoal(

                name="Business Logic",

                description="Understand business workflow abuse.",

                priority=90,

                success_criteria=[

                    "Workflow reconstructed",

                    "Critical transitions analyzed"

                ]

            ),

            InvestigationGoal(

                name="Input Validation",

                description="Review input trust boundaries.",

                priority=80,

                success_criteria=[

                    "Parameters analyzed",

                    "Validation points identified"

                ]

            )

        ]

    # ----------------------------------------------------

    def next_goal(self):

        remaining = [

            goal

            for goal in self.goals

            if not goal.completed

        ]

        if not remaining:

            return None

        remaining.sort(

            key=lambda g: g.priority,

            reverse=True

        )

        return remaining[0]

    # ----------------------------------------------------

    def complete(self, goal_name):

        for goal in self.goals:

            if goal.name == goal_name:

                goal.completed = True

                return True

        return False

    # ----------------------------------------------------

    def add_observation(

        self,

        goal_name,

        observation

    ):

        for goal in self.goals:

            if goal.name == goal_name:

                goal.observations.append(

                    observation

                )

                return

    # ----------------------------------------------------

    def summary(self):

        return [

            {

                "Goal": g.name,

                "Priority": g.priority,

                "Completed": g.completed,

                "Observations": len(g.observations)

            }

            for g in self.goals

        ]