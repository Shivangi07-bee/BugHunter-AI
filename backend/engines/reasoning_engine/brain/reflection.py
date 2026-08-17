from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

from .attack_executor import AttackExecutionPlan
from .memory import BrainMemory


@dataclass
class Reflection:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    strategy: str = ""

    confidence_before: float = 0.0

    confidence_after: float = 0.0

    outcome: str = ""

    decision: str = ""

    observations: List[str] = field(
        default_factory=list
    )

    next_steps: List[str] = field(
        default_factory=list
    )


class ReflectionEngine:
    """
    Evaluates investigation plans and determines
    the next reasoning direction.

    Reflection does not claim that a vulnerability exists.

    It evaluates investigation quality and decides whether
    the investigation should:

        CONTINUE
        PIVOT
        ESCALATE
        STOP
    """

    def __init__(
        self,
        plans: List[AttackExecutionPlan],
        memory: BrainMemory
    ):

        self.plans = plans
        self.memory = memory

    # =========================================================
    # EVALUATE
    # =========================================================

    def evaluate(self):

        reflections = []

        for plan in self.plans:

            before = self._initial_confidence(
                plan
            )

            observations = []

            observations.append(
                f"{len(plan.attack_steps)} validation "
                f"steps prepared."
            )

            observations.append(
                "Validation plan requires runtime evidence "
                "before a security conclusion can be reached."
            )

            # -------------------------------------------------
            # Check existing evidence
            # -------------------------------------------------

            evidence_records = (
                self.memory.recall_by_category(
                    "Evidence"
                )
            )

            reflection_records = (
                self.memory.recall_by_category(
                    "Reflection"
                )
            )

            if evidence_records:

                observations.append(
                    f"{len(evidence_records)} evidence "
                    f"record(s) already available."
                )

            # -------------------------------------------------
            # Determine decision
            # -------------------------------------------------

            if evidence_records:

                decision = "ESCALATE"

                outcome = (
                    "Runtime evidence is available. "
                    "Review the evidence and determine "
                    "whether the hypothesis warrants escalation."
                )

                after = min(
                    before + 0.05,
                    1.0
                )

                next_steps = [
                    "Review collected evidence",
                    "Correlate evidence with the hypothesis",
                    "Determine whether additional validation is required"
                ]

            elif len(plan.attack_steps) >= 3:

                decision = "CONTINUE"

                outcome = (
                    "A structured validation path exists, "
                    "but runtime evidence is still required."
                )

                after = before

                next_steps = [
                    "Execute approved validation steps",
                    "Collect runtime responses",
                    "Record evidence",
                    "Re-evaluate the hypothesis"
                ]

            elif len(plan.attack_steps) == 0:

                decision = "PIVOT"

                outcome = (
                    "No meaningful validation path was generated."
                )

                after = max(
                    before - 0.05,
                    0.0
                )

                next_steps = [
                    "Revisit the workflow",
                    "Generate additional evidence",
                    "Create an alternative investigation strategy"
                ]

            else:

                decision = "CONTINUE"

                outcome = (
                    "Initial investigation path is available, "
                    "but additional context is required."
                )

                after = before

                next_steps = [
                    "Collect additional application context",
                    "Review related endpoints",
                    "Perform controlled validation"
                ]

            # -------------------------------------------------
            # Avoid artificial confidence inflation
            # -------------------------------------------------

            if reflection_records:

                observations.append(
                    f"{len(reflection_records)} previous "
                    f"reflection record(s) available."
                )

            # -------------------------------------------------
            # Build reflection
            # -------------------------------------------------

            reflection = Reflection(

                strategy=plan.strategy_name,

                confidence_before=before,

                confidence_after=after,

                outcome=outcome,

                decision=decision,

                observations=observations,

                next_steps=next_steps

            )

            # -------------------------------------------------
            # Persist reflection in Brain Memory
            # -------------------------------------------------

            self.memory.remember(

                category="Reflection",

                title=plan.strategy_name,

                data={

                    "decision": decision,

                    "confidence_before": before,

                    "confidence_after": after,

                    "outcome": outcome,

                    "observations": observations,

                    "next_steps": next_steps

                },

                confidence=after,

                tags=[
                    "reflection",
                    decision.lower()
                ]

            )

            reflections.append(
                reflection
            )

        return reflections

    # =========================================================
    # INITIAL CONFIDENCE
    # =========================================================

    def _initial_confidence(
        self,
        plan
    ):

        strategy = str(
            plan.strategy_name
        ).lower()

        # Existing memory can provide context.
        relevant_records = []

        if (
            "authentication"
            in strategy
        ):

            relevant_records.extend(
                self.memory.recall_by_tag(
                    "auth"
                )
            )

        if (
            "authorization"
            in strategy
        ):

            relevant_records.extend(
                self.memory.recall_by_tag(
                    "idor"
                )
            )

        if relevant_records:

            return 0.80

        # Higher-priority investigation paths
        # begin with stronger investigation confidence,
        # but this is NOT a vulnerability confidence score.

        if getattr(
            plan,
            "priority",
            0
        ) >= 90:

            return 0.70

        if getattr(
            plan,
            "priority",
            0
        ) >= 70:

            return 0.60

        return 0.50