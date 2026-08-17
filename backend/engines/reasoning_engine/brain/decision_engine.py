from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

from .strategist import Strategy


@dataclass
class InvestigationTask:

    id: str = field(default_factory=lambda: str(uuid4()))

    strategy_id: str = ""

    strategy_name: str = ""

    objective: str = ""

    next_action: str = ""

    priority: int = 0

    reasoning: List[str] = field(default_factory=list)

    status: str = "PENDING"


class DecisionEngine:
    """
    Chooses the next investigation task.

    This is NOT an executor.

    It behaves like a junior bug hunter deciding:

    "What should I investigate first?"
    """

    def __init__(self, strategies: List[Strategy]):

        self.strategies = strategies

    # ---------------------------------------------------------

    def decide(self):

        tasks = []

        for strategy in self.strategies:

            if len(strategy.actions) == 0:
                continue

            task = InvestigationTask(

                strategy_id=strategy.id,

                strategy_name=strategy.name,

                objective=strategy.objective,

                next_action=strategy.actions[0],

                priority=strategy.priority,

                reasoning=strategy.reasoning.copy()

            )

            tasks.append(task)

        tasks.sort(

            key=lambda x: x.priority,

            reverse=True

        )

        return tasks