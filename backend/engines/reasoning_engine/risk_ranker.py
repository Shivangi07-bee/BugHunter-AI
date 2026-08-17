from typing import List, Dict


class RiskRanker:
    """
    Prioritizes security investigation hypotheses.

    The ranker does not determine whether a vulnerability exists.
    It estimates investigation priority from available evidence,
    confidence, impact indicators and application context.
    """

    def __init__(self, hypotheses: List[Dict]):
        self.hypotheses = hypotheses

    # =========================================================
    # PUBLIC API
    # =========================================================

    def rank(self) -> List[Dict]:

        ranked = []

        for hypothesis in self.hypotheses:

            score = self._calculate_score(hypothesis)

            level = self._risk_level(score)

            enriched = dict(hypothesis)

            enriched["score"] = score
            enriched["risk"] = level

            enriched["priority"] = self._priority(score)

            enriched["ranking_factors"] = self._ranking_factors(
                hypothesis
            )

            ranked.append(enriched)

        ranked.sort(
            key=lambda item: (
                item["score"],
                item.get("confidence", 0)
            ),
            reverse=True
        )

        return ranked

    # =========================================================
    # SCORE
    # =========================================================

    def _calculate_score(
        self,
        hypothesis: Dict
    ) -> int:

        confidence = self._number(
            hypothesis.get("confidence", 0)
        )

        score = confidence * 0.45

        title = str(
            hypothesis.get("title", "")
        ).lower()

        description = str(
            hypothesis.get("description", "")
        ).lower()

        reasoning = " ".join(
            str(item)
            for item in hypothesis.get(
                "reasoning",
                []
            )
        ).lower()

        evidence = " ".join(
            str(item)
            for item in hypothesis.get(
                "evidence",
                []
            )
        ).lower()

        combined = " ".join([
            title,
            description,
            reasoning,
            evidence
        ])

        # -----------------------------------------------------
        # Security boundary
        # -----------------------------------------------------

        if any(
            term in combined
            for term in [
                "authentication",
                "unauthenticated",
                "authorization",
                "ownership",
                "access control"
            ]
        ):
            score += 15

        # -----------------------------------------------------
        # Sensitive resources
        # -----------------------------------------------------

        if any(
            term in combined
            for term in [
                "payment",
                "financial",
                "transaction",
                "invoice",
                "credential",
                "account",
                "user data",
                "sensitive"
            ]
        ):
            score += 15

        # -----------------------------------------------------
        # State-changing behavior
        # -----------------------------------------------------

        if any(
            term in combined
            for term in [
                "state transition",
                "state-changing",
                "modify application state",
                "delete",
                "update"
            ]
        ):
            score += 10

        # -----------------------------------------------------
        # Workflow reasoning
        # -----------------------------------------------------

        if any(
            term in combined
            for term in [
                "workflow",
                "related endpoints",
                "state transition",
                "preceding",
                "following"
            ]
        ):
            score += 8

        # -----------------------------------------------------
        # Client-controlled input
        # -----------------------------------------------------

        if any(
            term in combined
            for term in [
                "client-controlled",
                "client input",
                "parameter",
                "input validation"
            ]
        ):
            score += 7

        # -----------------------------------------------------
        # Shared security-sensitive logic
        # -----------------------------------------------------

        if any(
            term in combined
            for term in [
                "shared function",
                "shared logic",
                "security-sensitive behavior"
            ]
        ):
            score += 6

        # -----------------------------------------------------
        # Explicit high-impact indicators
        # -----------------------------------------------------

        if any(
            term in combined
            for term in [
                "financial",
                "ownership",
                "privileged",
                "sensitive resource"
            ]
        ):
            score += 8

        # -----------------------------------------------------
        # Confidence penalty / reward
        # -----------------------------------------------------

        if confidence >= 90:
            score += 5
        elif confidence < 50:
            score -= 5

        # -----------------------------------------------------
        # Clamp
        # -----------------------------------------------------

        return max(
            0,
            min(
                100,
                round(score)
            )
        )

    # =========================================================
    # RISK LEVEL
    # =========================================================

    def _risk_level(
        self,
        score: int
    ) -> str:

        if score >= 85:
            return "Critical"

        if score >= 70:
            return "High"

        if score >= 45:
            return "Medium"

        return "Low"

    # =========================================================
    # PRIORITY
    # =========================================================

    def _priority(
        self,
        score: int
    ) -> str:

        if score >= 85:
            return "Immediate"

        if score >= 70:
            return "High"

        if score >= 45:
            return "Normal"

        return "Low"

    # =========================================================
    # EXPLAINABLE RANKING
    # =========================================================

    def _ranking_factors(
        self,
        hypothesis: Dict
    ) -> List[str]:

        factors = []

        text = " ".join([
            str(hypothesis.get("title", "")),
            str(hypothesis.get("description", "")),
            " ".join(
                str(x)
                for x in hypothesis.get(
                    "reasoning",
                    []
                )
            )
        ]).lower()

        if any(
            x in text
            for x in [
                "authentication",
                "authorization",
                "ownership",
                "access control"
            ]
        ):
            factors.append(
                "security boundary"
            )

        if any(
            x in text
            for x in [
                "payment",
                "financial",
                "transaction",
                "sensitive"
            ]
        ):
            factors.append(
                "sensitive application state"
            )

        if any(
            x in text
            for x in [
                "state transition",
                "state-changing"
            ]
        ):
            factors.append(
                "state-changing operation"
            )

        if any(
            x in text
            for x in [
                "client input",
                "client-controlled",
                "parameter"
            ]
        ):
            factors.append(
                "client-controlled input"
            )

        if any(
            x in text
            for x in [
                "workflow",
                "related endpoints"
            ]
        ):
            factors.append(
                "workflow relationship"
            )

        if not factors:
            factors.append(
                "application reasoning"
            )

        return factors

    # =========================================================
    # SAFE NUMBER CONVERSION
    # =========================================================

    def _number(
        self,
        value
    ) -> float:

        try:
            return float(value)
        except (
            TypeError,
            ValueError
        ):
            return 0.0