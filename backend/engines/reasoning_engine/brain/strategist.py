from dataclasses import dataclass, field
from typing import List
from uuid import uuid4

from .memory import BrainMemory


@dataclass
class Strategy:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    objective: str = ""

    priority: int = 0

    reasoning: List[str] = field(
        default_factory=list
    )

    actions: List[str] = field(
        default_factory=list
    )


class Strategist:
    """
    Converts security hypotheses from Brain Memory into
    prioritized investigation strategies.

    The Strategist decides WHAT should be investigated
    and proposes HOW the investigation can begin.

    It does not execute attacks.
    """

    def __init__(
        self,
        memory: BrainMemory
    ):

        self.memory = memory

    # =========================================================
    # GENERATE STRATEGIES
    # =========================================================

    def generate(self):

        strategies = []

        hypotheses = (
            self.memory.recall_by_category(
                "Hypothesis"
            )
        )

        for hypothesis in hypotheses:

            strategy = self._build_strategy(
                hypothesis
            )

            if strategy is not None:

                strategies.append(
                    strategy
                )

        strategies.sort(
            key=lambda item: item.priority,
            reverse=True
        )

        return strategies

    # =========================================================
    # BUILD STRATEGY
    # =========================================================

    def _build_strategy(
        self,
        hypothesis
    ):

        title = str(
            hypothesis.title
        ).lower()

        data = getattr(
            hypothesis,
            "data",
            {}
        )

        description = str(
            data.get(
                "description",
                ""
            )
        ).lower()

        reasoning = " ".join(
            str(item)
            for item in data.get(
                "reasoning",
                []
            )
        ).lower()

        combined = " ".join([
            title,
            description,
            reasoning
        ])

        # -----------------------------------------------------
        # Authentication
        # -----------------------------------------------------

        if self._contains(
            combined,
            [
                "authentication",
                "unauthenticated",
                "login",
                "session",
                "auth boundary",
                "authentication boundary"
            ]
        ):

            return Strategy(

                name="Authentication Assessment",

                objective=(
                    "Verify authentication boundaries "
                    "and protected resource access."
                ),

                priority=100,

                reasoning=[
                    "An authentication boundary requires validation.",
                    "Protected resources should not be reachable without the expected identity context."
                ],

                actions=[
                    "Map the authentication boundary",
                    "Inspect login and session creation",
                    "Identify protected endpoints",
                    "Compare authenticated and unauthenticated behavior"
                ]
            )

        # -----------------------------------------------------
        # Authorization / ownership
        # -----------------------------------------------------

        if self._contains(
            combined,
            [
                "authorization",
                "ownership",
                "object ownership",
                "access control",
                "idor",
                "resource identifier"
            ]
        ):

            return Strategy(

                name="Authorization Assessment",

                objective=(
                    "Verify object ownership and "
                    "resource-level authorization."
                ),

                priority=95,

                reasoning=[
                    "User or account resources require ownership validation.",
                    "Related endpoints may expose inconsistent authorization boundaries."
                ],

                actions=[
                    "Identify resource identifiers",
                    "Trace ownership checks",
                    "Compare authorization across related endpoints",
                    "Validate access using an authorized test account"
                ]
            )

        # -----------------------------------------------------
        # Financial workflows
        # -----------------------------------------------------

        if self._contains(
            combined,
            [
                "payment",
                "financial",
                "transaction",
                "invoice",
                "financial workflow"
            ]
        ):

            return Strategy(

                name="Financial Workflow Assessment",

                objective=(
                    "Verify integrity and authorization "
                    "across financial state transitions."
                ),

                priority=94,

                reasoning=[
                    "Financial operations represent high-impact application state.",
                    "State changes should be validated server-side."
                ],

                actions=[
                    "Map the financial workflow",
                    "Identify state transitions",
                    "Trace server-side validation",
                    "Verify ownership and authorization at each transition"
                ]
            )

        # -----------------------------------------------------
        # State transitions
        # -----------------------------------------------------

        if self._contains(
            combined,
            [
                "state transition",
                "state-changing",
                "application state"
            ]
        ):

            return Strategy(

                name="Business Logic Assessment",

                objective=(
                    "Verify that application state "
                    "transitions follow expected business rules."
                ),

                priority=88,

                reasoning=[
                    "The endpoint changes application state.",
                    "Business invariants should be enforced server-side."
                ],

                actions=[
                    "Map valid state transitions",
                    "Identify client-controlled state fields",
                    "Review transition validation",
                    "Compare adjacent workflow states"
                ]
            )

        # -----------------------------------------------------
        # Input validation
        # -----------------------------------------------------

        if self._contains(
            combined,
            [
                "input validation",
                "client input",
                "client-controlled",
                "parameter",
                "input"
            ]
        ):

            return Strategy(

                name="Input Validation Assessment",

                objective=(
                    "Verify validation of "
                    "client-controlled input."
                ),

                priority=78,

                reasoning=[
                    "The application processes client-controlled data.",
                    "Security-sensitive fields require server-side validation."
                ],

                actions=[
                    "Identify accepted parameters",
                    "Trace validation logic",
                    "Review type and range enforcement",
                    "Test business-rule boundaries"
                ]
            )

        # -----------------------------------------------------
        # Shared logic
        # -----------------------------------------------------

        if self._contains(
            combined,
            [
                "shared logic",
                "shared function",
                "shared application logic"
            ]
        ):

            return Strategy(

                name="Shared Logic Consistency Assessment",

                objective=(
                    "Verify that shared application "
                    "logic applies consistent security controls."
                ),

                priority=75,

                reasoning=[
                    "Multiple endpoints depend on shared application logic.",
                    "Different callers may reach shared logic under different security contexts."
                ],

                actions=[
                    "Identify shared functions",
                    "Trace all callers",
                    "Compare security checks",
                    "Review privileged and unprivileged call paths"
                ]
            )

        # -----------------------------------------------------
        # Generic workflow investigation
        # -----------------------------------------------------

        return Strategy(

            name="Workflow Investigation",

            objective=(
                "Collect additional evidence about "
                "the application's reconstructed workflow."
            ),

            priority=50,

            reasoning=[
                "The available evidence does not yet map to a specialized security strategy.",
                "Additional application context is required."
            ],

            actions=[
                "Review workflow relationships",
                "Inspect related endpoints",
                "Collect additional application evidence"
            ]
        )

    # =========================================================
    # KEYWORD MATCHING
    # =========================================================

    def _contains(
        self,
        text,
        keywords
    ):

        return any(
            keyword in text
            for keyword in keywords
        )