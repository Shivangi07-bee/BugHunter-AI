from .attack_planner import AttackPlanner


class PlannerService:
    """
    Single integration point for the planning layer.

    Converts the existing investigation state into
    structured validation plans.

    Does NOT execute anything.
    """

    def build(
        self,
        investigation_plan=None,
        hypotheses=None,
        workflows=None
    ):
        planner = AttackPlanner(
            investigation_plan=investigation_plan,
            hypotheses=hypotheses,
            workflows=workflows
        )

        return planner.build()