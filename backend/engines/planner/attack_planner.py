from dataclasses import dataclass, field
from typing import Any, Dict, List
from uuid import uuid4


@dataclass
class PlannedAttackStep:
    id: str = field(default_factory=lambda: str(uuid4()))

    step_number: int = 0

    action: str = ""

    objective: str = ""

    target: str = ""

    expected_result: str = ""

    evidence_required: List[str] = field(
        default_factory=list
    )


@dataclass
class AttackPlan:
    id: str = field(default_factory=lambda: str(uuid4()))

    title: str = ""

    objective: str = ""

    priority: int = 0

    hypothesis: str = ""

    workflow: str = ""

    steps: List[PlannedAttackStep] = field(
        default_factory=list
    )

    status: str = "PLANNED"


class AttackPlanner:
    """
    Converts investigation plans and hypotheses into
    structured security validation plans.

    This component DOES NOT execute requests.

    Responsibility:
        Investigation Plan
              ↓
        Attack Strategy
              ↓
        Ordered Validation Steps

    Execution belongs to the Runtime Engine.
    """

    def __init__(
        self,
        investigation_plan=None,
        hypotheses=None,
        workflows=None
    ):
        self.investigation_plan = (
            investigation_plan or []
        )

        self.hypotheses = (
            hypotheses or []
        )

        self.workflows = (
            workflows or []
        )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def build(self) -> List[AttackPlan]:

        plans = []

        sources = self._collect_sources()

        for index, source in enumerate(sources):

            plan = self._build_plan(
                source,
                index
            )

            if plan.steps:
                plans.append(plan)

        plans.sort(
            key=lambda item: item.priority,
            reverse=True
        )

        return plans

    # =========================================================
    # SOURCE NORMALIZATION
    # =========================================================

    def _collect_sources(self):

        sources = []

        if isinstance(
            self.investigation_plan,
            list
        ):
            sources.extend(
                self.investigation_plan
            )

        elif self.investigation_plan:
            sources.append(
                self.investigation_plan
            )

        if not sources:

            sources.extend(
                self.hypotheses
            )

        return sources

    # =========================================================
    # PLAN BUILDER
    # =========================================================

    def _build_plan(
        self,
        source,
        index
    ):

        data = self._to_dict(source)

        title = str(
            data.get(
                "title",
                data.get(
                    "name",
                    data.get(
                        "strategy_name",
                        "Security Validation"
                    )
                )
            )
        )

        objective = str(
            data.get(
                "objective",
                data.get(
                    "description",
                    "Validate security-relevant application behavior."
                )
            )
        )

        hypothesis = str(
            data.get(
                "hypothesis",
                data.get(
                    "title",
                    title
                )
            )
        )

        workflow = str(
            data.get(
                "workflow",
                data.get(
                    "workflow_name",
                    "Application workflow"
                )
            )
        )

        priority = self._priority(
            data
        )

        plan = AttackPlan(

            title=title,

            objective=objective,

            priority=priority,

            hypothesis=hypothesis,

            workflow=workflow

        )

        category = self._category(
            title,
            objective
        )

        if category == "authorization":

            plan.steps = (
                self._authorization_steps()
            )

        elif category == "authentication":

            plan.steps = (
                self._authentication_steps()
            )

        elif category == "injection":

            plan.steps = (
                self._injection_steps()
            )

        elif category == "workflow":

            plan.steps = (
                self._workflow_steps()
            )

        else:

            plan.steps = (
                self._general_steps()
            )

        return plan

    # =========================================================
    # AUTHORIZATION
    # =========================================================

    def _authorization_steps(self):

        return [

            PlannedAttackStep(
                step_number=1,

                action=(
                    "Identify a protected resource "
                    "within the authorized workflow."
                ),

                objective=(
                    "Establish the expected authorization boundary."
                ),

                target="Protected resource",

                expected_result=(
                    "A baseline authorized request is identified."
                ),

                evidence_required=[
                    "Request",
                    "Response status",
                    "Authenticated identity"
                ]
            ),

            PlannedAttackStep(
                step_number=2,

                action=(
                    "Compare access decisions for a "
                    "different authorized test identity."
                ),

                objective=(
                    "Determine whether ownership checks "
                    "are consistently enforced."
                ),

                target="Resource authorization",

                expected_result=(
                    "Access is restricted according to ownership "
                    "or assigned permissions."
                ),

                evidence_required=[
                    "Identity",
                    "Resource identifier",
                    "Authorization response"
                ]
            ),

            PlannedAttackStep(
                step_number=3,

                action=(
                    "Review authorization enforcement across "
                    "related workflow endpoints."
                ),

                objective=(
                    "Validate authorization consistency."
                ),

                target="Related endpoints",

                expected_result=(
                    "Every sensitive transition applies "
                    "appropriate authorization."
                ),

                evidence_required=[
                    "Endpoint",
                    "Identity",
                    "Authorization decision"
                ]
            )

        ]

    # =========================================================
    # AUTHENTICATION
    # =========================================================

    def _authentication_steps(self):

        return [

            PlannedAttackStep(
                step_number=1,

                action=(
                    "Map the authentication workflow."
                ),

                objective=(
                    "Identify login and session boundaries."
                ),

                target="Authentication workflow",

                expected_result=(
                    "Authentication state transitions are identified."
                ),

                evidence_required=[
                    "Login endpoint",
                    "Session mechanism"
                ]
            ),

            PlannedAttackStep(
                step_number=2,

                action=(
                    "Review protected endpoint behavior "
                    "without an authenticated session."
                ),

                objective=(
                    "Validate enforcement of authentication boundaries."
                ),

                target="Protected endpoint",

                expected_result=(
                    "Unauthenticated access is rejected."
                ),

                evidence_required=[
                    "Request",
                    "Response status"
                ]
            ),

            PlannedAttackStep(
                step_number=3,

                action=(
                    "Review session or token validation logic."
                ),

                objective=(
                    "Determine whether authentication state "
                    "is validated server-side."
                ),

                target="Session/token validation",

                expected_result=(
                    "Invalid authentication state is rejected."
                ),

                evidence_required=[
                    "Token/session state",
                    "Validation result"
                ]
            )

        ]

    # =========================================================
    # INJECTION
    # =========================================================

    def _injection_steps(self):

        return [

            PlannedAttackStep(
                step_number=1,

                action=(
                    "Locate user-controlled input reaching "
                    "database or command processing."
                ),

                objective=(
                    "Identify the relevant input-to-sink path."
                ),

                target="Input processing",

                expected_result=(
                    "The data flow into the sensitive sink is identified."
                ),

                evidence_required=[
                    "Input source",
                    "Processing function",
                    "Sink"
                ]
            ),

            PlannedAttackStep(
                step_number=2,

                action=(
                    "Review parameterization and validation "
                    "at the identified sink."
                ),

                objective=(
                    "Determine whether untrusted input is safely handled."
                ),

                target="Sensitive sink",

                expected_result=(
                    "Input is parameterized or safely validated."
                ),

                evidence_required=[
                    "Query construction",
                    "Validation logic"
                ]
            ),

            PlannedAttackStep(
                step_number=3,

                action=(
                    "Perform controlled validation using "
                    "non-destructive test input."
                ),

                objective=(
                    "Validate the observed data-flow behavior."
                ),

                target="Input boundary",

                expected_result=(
                    "Application behavior remains safely constrained."
                ),

                evidence_required=[
                    "Test input",
                    "Response",
                    "Application behavior"
                ]
            )

        ]

    # =========================================================
    # WORKFLOW
    # =========================================================

    def _workflow_steps(self):

        return [

            PlannedAttackStep(
                step_number=1,

                action=(
                    "Map the workflow state transitions."
                ),

                objective=(
                    "Identify valid and sensitive application states."
                ),

                target="Application workflow",

                expected_result=(
                    "Workflow states and transitions are identified."
                ),

                evidence_required=[
                    "Endpoints",
                    "State transitions"
                ]
            ),

            PlannedAttackStep(
                step_number=2,

                action=(
                    "Review server-side validation at "
                    "sensitive state transitions."
                ),

                objective=(
                    "Determine whether invalid transitions "
                    "are rejected."
                ),

                target="State-changing endpoints",

                expected_result=(
                    "Invalid state transitions are rejected."
                ),

                evidence_required=[
                    "State",
                    "Transition",
                    "Validation result"
                ]
            ),

            PlannedAttackStep(
                step_number=3,

                action=(
                    "Verify authorization and ownership "
                    "at sensitive workflow transitions."
                ),

                objective=(
                    "Ensure only permitted transitions occur."
                ),

                target="Sensitive transition",

                expected_result=(
                    "Only authorized transitions are accepted."
                ),

                evidence_required=[
                    "Identity",
                    "Transition",
                    "Authorization decision"
                ]
            )

        ]

    # =========================================================
    # GENERAL
    # =========================================================

    def _general_steps(self):

        return [

            PlannedAttackStep(
                step_number=1,

                action=(
                    "Review the relevant application workflow."
                ),

                objective=(
                    "Collect additional security evidence."
                ),

                target="Application workflow",

                expected_result=(
                    "Relevant application behavior is documented."
                ),

                evidence_required=[
                    "Workflow",
                    "Endpoints"
                ]
            ),

            PlannedAttackStep(
                step_number=2,

                action=(
                    "Validate security controls at "
                    "identified sensitive boundaries."
                ),

                objective=(
                    "Determine whether expected controls are enforced."
                ),

                target="Security boundary",

                expected_result=(
                    "Expected security controls are observed."
                ),

                evidence_required=[
                    "Control",
                    "Response",
                    "Observed behavior"
                ]
            )

        ]

    # =========================================================
    # CATEGORY
    # =========================================================

    def _category(
        self,
        title,
        objective
    ):

        text = (
            f"{title} {objective}"
        ).lower()

        if any(
            word in text
            for word in [
                "idor",
                "authorization",
                "ownership",
                "access control",
                "permission"
            ]
        ):
            return "authorization"

        if any(
            word in text
            for word in [
                "authentication",
                "auth",
                "login",
                "session",
                "jwt"
            ]
        ):
            return "authentication"

        if any(
            word in text
            for word in [
                "sql",
                "sqli",
                "injection",
                "query"
            ]
        ):
            return "injection"

        if any(
            word in text
            for word in [
                "workflow",
                "payment",
                "transaction",
                "state"
            ]
        ):
            return "workflow"

        return "general"

    # =========================================================
    # PRIORITY
    # =========================================================

    def _priority(
        self,
        data
    ):

        value = data.get(
            "priority",
            data.get(
                "risk",
                data.get(
                    "risk_score",
                    0
                )
            )
        )

        if isinstance(
            value,
            str
        ):

            mapping = {
                "critical": 100,
                "high": 90,
                "medium": 60,
                "moderate": 60,
                "low": 30,
                "informational": 10
            }

            return mapping.get(
                value.lower(),
                40
            )

        try:

            return int(
                float(value)
            )

        except (
            ValueError,
            TypeError
        ):

            return 40

    # =========================================================
    # NORMALIZATION
    # =========================================================

    def _to_dict(
        self,
        value
    ):

        if isinstance(
            value,
            dict
        ):
            return value

        if hasattr(
            value,
            "__dict__"
        ):
            return vars(
                value
            )

        return {}