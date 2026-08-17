from .planner_service import PlannerService


def test_planner_service():

    service = PlannerService()

    plans = service.build(
        hypotheses=[
            {
                "title": "Authorization Review",
                "description": "Review ownership controls.",
                "risk": "High"
            }
        ]
    )

    assert isinstance(plans, list)

    assert len(plans) == 1

    assert plans[0].title == "Authorization Review"

    assert len(plans[0].steps) > 0