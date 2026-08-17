from dataclasses import dataclass, field
from typing import List, Dict
from uuid import uuid4

from .decision_engine import InvestigationTask


@dataclass
class AttackStep:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    step_number: int = 0

    action: str = ""

    request_template: Dict = field(
        default_factory=dict
    )

    expected_result: str = ""

    requires_human_review: bool = True


@dataclass
class AttackExecutionPlan:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    strategy_name: str = ""

    objective: str = ""

    priority: int = 0

    attack_steps: List[AttackStep] = field(
        default_factory=list
    )

    status: str = "PENDING_REVIEW"


class AttackExecutor:
    """
    Converts investigation tasks into structured validation plans.

    This component DOES NOT execute requests.

    Runtime execution happens separately through RuntimeEngine.

    Every generated plan requires human review before execution.
    """

    def __init__(
        self,
        tasks: List[InvestigationTask]
    ):

        self.tasks = tasks

    # =========================================================
    # BUILD VALIDATION PLANS
    # =========================================================

    def build(self):

        plans = []

        for task in self.tasks:

            strategy_name = (
                task.strategy_name or ""
            )

            plan = AttackExecutionPlan(

                strategy_name=strategy_name,

                objective=(
                    task.objective or
                    "Collect security validation evidence."
                ),

                priority=task.priority

            )

            strategy = strategy_name.lower()

            # -------------------------------------------------
            # Authentication
            # -------------------------------------------------

            if "authentication" in strategy:

                plan.attack_steps.extend([

                    AttackStep(

                        step_number=1,

                        action=(
                            "Identify the application's "
                            "authentication endpoint"
                        ),

                        request_template={
                            "method": "AUTO",
                            "path": "<login_endpoint>",
                            "headers": {},
                            "body": {}
                        },

                        expected_result=(
                            "Identify authentication request "
                            "and session mechanism."
                        )

                    ),

                    AttackStep(

                        step_number=2,

                        action=(
                            "Compare protected resource "
                            "behavior with and without "
                            "authentication context"
                        ),

                        request_template={
                            "method": "AUTO",
                            "path": "<protected_endpoint>",
                            "headers": {},
                            "body": {}
                        },

                        expected_result=(
                            "Protected resources should enforce "
                            "the expected authentication boundary."
                        )

                    ),

                    AttackStep(

                        step_number=3,

                        action=(
                            "Review session or token validation "
                            "behavior"
                        ),

                        request_template={
                            "authorization": "<test_token>"
                        },

                        expected_result=(
                            "Invalid or altered authentication "
                            "material should not grant unauthorized access."
                        )

                    )

                ])

            # -------------------------------------------------
            # Authorization
            # -------------------------------------------------

            elif "authorization" in strategy:

                plan.attack_steps.extend([

                    AttackStep(

                        step_number=1,

                        action=(
                            "Capture a baseline request for a "
                            "resource owned by the authorized test account"
                        ),

                        request_template={
                            "method": "AUTO",
                            "path": "<resource_endpoint>",
                            "resource_id": "<authorized_test_resource>"
                        },

                        expected_result=(
                            "Baseline request succeeds for the authorized resource."
                        )

                    ),

                    AttackStep(

                        step_number=2,

                        action=(
                            "Test access-control behavior using "
                            "a second authorized test identity"
                        ),

                        request_template={
                            "resource_id": "<second_test_resource>",
                            "identity": "<second_test_account>"
                        },

                        expected_result=(
                            "Access should remain restricted to resources "
                            "owned or explicitly authorized for the identity."
                        )

                    ),

                    AttackStep(

                        step_number=3,

                        action=(
                            "Compare authorization decisions across "
                            "related workflow endpoints"
                        ),

                        request_template={
                            "compare_related_endpoints": True
                        },

                        expected_result=(
                            "Related endpoints should apply consistent "
                            "ownership and authorization controls."
                        )

                    )

                ])

            # -------------------------------------------------
            # Financial workflow
            # -------------------------------------------------

            elif "financial" in strategy:

                plan.attack_steps.extend([

                    AttackStep(

                        step_number=1,

                        action=(
                            "Map the financial workflow and "
                            "identify state transitions"
                        ),

                        request_template={
                            "workflow": "<financial_workflow>"
                        },

                        expected_result=(
                            "Identify valid application states "
                            "and transitions."
                        )

                    ),

                    AttackStep(

                        step_number=2,

                        action=(
                            "Review server-side validation of "
                            "financial state changes"
                        ),

                        request_template={
                            "endpoint": "<state_change_endpoint>"
                        },

                        expected_result=(
                            "Sensitive state transitions should "
                            "be validated server-side."
                        )

                    ),

                    AttackStep(

                        step_number=3,

                        action=(
                            "Verify authorization and ownership "
                            "at each financial transition"
                        ),

                        request_template={
                            "identity": "<authorized_test_account>"
                        },

                        expected_result=(
                            "Only authorized transitions should be accepted."
                        )

                    )

                ])

            # -------------------------------------------------
            # Business logic
            # -------------------------------------------------

            elif "business logic" in strategy:

                plan.attack_steps.extend([

                    AttackStep(

                        step_number=1,

                        action=(
                            "Map valid business state transitions"
                        ),

                        request_template={
                            "workflow": "<workflow>"
                        },

                        expected_result=(
                            "Valid and invalid application states "
                            "are identified."
                        )

                    ),

                    AttackStep(

                        step_number=2,

                        action=(
                            "Identify client-controlled state values"
                        ),

                        request_template={
                            "fields": "<state_fields>"
                        },

                        expected_result=(
                            "Security-sensitive state should not "
                            "be trusted solely from client input."
                        )

                    ),

                    AttackStep(

                        step_number=3,

                        action=(
                            "Validate transition enforcement "
                            "using controlled test data"
                        ),

                        request_template={
                            "test_state": "<controlled_state>"
                        },

                        expected_result=(
                            "Invalid transitions should be rejected."
                        )

                    )

                ])

            # -------------------------------------------------
            # Input validation
            # -------------------------------------------------

            elif "input validation" in strategy:

                plan.attack_steps.extend([

                    AttackStep(

                        step_number=1,

                        action=(
                            "Identify accepted input parameters"
                        ),

                        request_template={
                            "endpoint": "<endpoint>"
                        },

                        expected_result=(
                            "Input surface is documented."
                        )

                    ),

                    AttackStep(

                        step_number=2,

                        action=(
                            "Review server-side validation rules"
                        ),

                        request_template={
                            "parameters": "<parameters>"
                        },

                        expected_result=(
                            "Inputs should be validated against "
                            "expected types and business rules."
                        )

                    ),

                    AttackStep(

                        step_number=3,

                        action=(
                            "Test boundary conditions using "
                            "controlled non-destructive values"
                        ),

                        request_template={
                            "test_values": "<controlled_values>"
                        },

                        expected_result=(
                            "Invalid values should be rejected safely."
                        )

                    )

                ])

            # -------------------------------------------------
            # Shared logic
            # -------------------------------------------------

            elif "shared logic" in strategy:

                plan.attack_steps.extend([

                    AttackStep(

                        step_number=1,

                        action=(
                            "Identify shared security-sensitive functions"
                        ),

                        request_template={
                            "functions": "<shared_functions>"
                        },

                        expected_result=(
                            "Shared security logic and callers are identified."
                        )

                    ),

                    AttackStep(

                        step_number=2,

                        action=(
                            "Compare security checks across callers"
                        ),

                        request_template={
                            "callers": "<callers>"
                        },

                        expected_result=(
                            "Equivalent security controls should "
                            "be applied across relevant callers."
                        )

                    )

                ])

            # -------------------------------------------------
            # Generic investigation
            # -------------------------------------------------

            else:

                plan.attack_steps.append(

                    AttackStep(

                        step_number=1,

                        action=(
                            task.next_action or
                            "Collect additional application evidence"
                        ),

                        request_template={},

                        expected_result=(
                            "Collect additional evidence "
                            "for human review."
                        )

                    )

                )

            plans.append(plan)

        return plans