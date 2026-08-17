from .models import InvestigationTask


class InvestigationPlanner:
    """
    Creates a prioritized security investigation plan.

    The planner converts reconstructed workflows, knowledge-graph
    relationships and ranked hypotheses into an ordered queue for
    human validation.
    """

    def __init__(
        self,
        workflows,
        hypotheses,
        knowledge_graph,
    ):
        self.workflows = workflows
        self.hypotheses = hypotheses
        self.knowledge_graph = knowledge_graph

    # =========================================================
    # BUILD PLAN
    # =========================================================

    def build(self):

        candidates = []

        # -----------------------------------------------------
        # 1. Security hypotheses
        # -----------------------------------------------------

        for hypothesis in self.hypotheses:

            score = self._score_hypothesis(
                hypothesis
            )

            candidates.append({
                "kind": "hypothesis",
                "score": score,
                "title": hypothesis.get(
                    "title",
                    "Security Hypothesis"
                ),
                "reason": self._hypothesis_reason(
                    hypothesis
                )
            })

        # -----------------------------------------------------
        # 2. Knowledge graph relationships
        # -----------------------------------------------------

        for edge in self.knowledge_graph.get(
            "edges",
            []
        ):

            relationship = edge.get(
                "relationship",
                edge.get(
                    "reason",
                    "Application relationship"
                )
            )

            score = self._score_relationship(
                relationship
            )

            candidates.append({
                "kind": "relationship",
                "score": score,
                "title": (
                    f"Review "
                    f"{edge.get('source', 'unknown')} "
                    f"→ "
                    f"{edge.get('target', 'unknown')}"
                ),
                "reason": relationship
            })

        # -----------------------------------------------------
        # 3. Workflows
        # -----------------------------------------------------

        for workflow in self.workflows:

            name = getattr(
                workflow,
                "name",
                "Unknown Workflow"
            )

            endpoint_count = len(
                getattr(
                    workflow,
                    "endpoints",
                    []
                )
            )

            # Larger workflows generally deserve
            # earlier structural review.
            score = min(
                55,
                25 + endpoint_count * 5
            )

            candidates.append({
                "kind": "workflow",
                "score": score,
                "title": f"Investigate {name}",
                "reason": (
                    "Business workflow reconstructed "
                    "from related application endpoints."
                )
            })

        # -----------------------------------------------------
        # Sort by investigation value
        # -----------------------------------------------------

        candidates.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        # -----------------------------------------------------
        # Convert into InvestigationTask objects
        # -----------------------------------------------------

        tasks = []

        for priority, candidate in enumerate(
            candidates,
            start=1
        ):

            tasks.append(
                InvestigationTask(
                    priority=priority,
                    title=candidate["title"],
                    reason=candidate["reason"]
                )
            )

        return tasks

    # =========================================================
    # HYPOTHESIS SCORING
    # =========================================================

    def _score_hypothesis(
        self,
        hypothesis
    ):

        score = 50

        confidence = self._number(
            hypothesis.get(
                "confidence",
                0
            )
        )

        risk = str(
            hypothesis.get(
                "risk",
                ""
            )
        ).lower()

        existing_score = self._number(
            hypothesis.get(
                "score",
                0
            )
        )

        # Prefer the already calculated RiskRanker score.
        if existing_score:
            score = existing_score

        else:
            score += confidence * 0.25

        if risk == "critical":
            score += 25

        elif risk == "high":
            score += 15

        elif risk == "medium":
            score += 5

        # Hypotheses requiring validation are useful
        # investigation candidates.
        if hypothesis.get(
            "requires_validation",
            False
        ):
            score += 5

        return min(
            100,
            round(score)
        )

    # =========================================================
    # RELATIONSHIP SCORING
    # =========================================================

    def _score_relationship(
        self,
        relationship
    ):

        text = str(
            relationship
        ).lower()

        score = 35

        if any(
            keyword in text
            for keyword in [
                "auth",
                "authorization",
                "ownership",
                "access"
            ]
        ):
            score += 25

        if any(
            keyword in text
            for keyword in [
                "payment",
                "transaction",
                "user",
                "account",
                "admin"
            ]
        ):
            score += 20

        if any(
            keyword in text
            for keyword in [
                "shared_model",
                "shared_function"
            ]
        ):
            score += 10

        return min(
            100,
            score
        )

    # =========================================================
    # HYPOTHESIS REASON
    # =========================================================

    def _hypothesis_reason(
        self,
        hypothesis
    ):

        risk = hypothesis.get(
            "risk",
            "Unknown"
        )

        factors = hypothesis.get(
            "ranking_factors",
            []
        )

        if factors:

            return (
                f"Risk: {risk}. "
                f"Factors: "
                f"{', '.join(factors)}."
            )

        return (
            f"Risk: {risk}. "
            f"Security hypothesis requires "
            f"human validation."
        )

    # =========================================================
    # SAFE NUMBER
    # =========================================================

    def _number(
        self,
        value
    ):

        try:
            return float(value)

        except (
            TypeError,
            ValueError
        ):
            return 0