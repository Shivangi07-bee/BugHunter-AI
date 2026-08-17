from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class InvestigationReasoning:

    investigation_goal: str = ""

    workflow_summary: str = ""

    attack_summary: str = ""

    observations: List[str] = field(default_factory=list)

    hypotheses: List[str] = field(default_factory=list)

    reasoning_prompt: str = ""


class InvestigationReasoner:
    """
    Combines Brain + Runtime before sending
    information to the LLM.
    """

    def __init__(

        self,

        runtime_snapshot: Dict,

        brain_output: Dict,

        prompt_builder

    ):

        self.runtime = runtime_snapshot

        self.brain = brain_output

        self.prompt_builder = prompt_builder

    # --------------------------------------------------

    def build(self):

        reasoning = InvestigationReasoning()

        reasoning.investigation_goal = self.runtime.get(

            "goal",

            ""

        )

        reasoning.workflow_summary = self.runtime.get(

            "workflow",

            ""

        )

        reasoning.attack_summary = (

            f"{len(self.brain['plans'])} attack plans generated."

        )

        reasoning.observations.append(

            f"{self.runtime['observations']} observations collected."

        )

        reasoning.observations.append(

            f"{self.runtime['evidence']} evidence collected."

        )

        for strategy in self.brain["strategies"]:

            reasoning.hypotheses.append(

                strategy.name

            )

        reasoning.reasoning_prompt = self.prompt_builder.build()

        return reasoning