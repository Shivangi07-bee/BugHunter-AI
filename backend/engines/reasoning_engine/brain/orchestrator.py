from dataclasses import asdict, is_dataclass

from .memory import BrainMemory
from .strategist import Strategist
from .decision_engine import DecisionEngine
from .attack_executor import AttackExecutor
from .reflection import ReflectionEngine
from .investigation_identity import InvestigationIdentityEngine

class BugHunterBrain:
    """
    Main Brain Controller.

    Memory
        ↓
    Strategy
        ↓
    Decision
        ↓
    Attack Planning
        ↓
    Reflection
        ↓
    Security Findings
    """

    def __init__(self):
        self.memory = BrainMemory()

    # =========================================================
    # LOAD HYPOTHESES
    # =========================================================

    def load_hypotheses(self, hypotheses):

        for hypothesis in hypotheses:

            self.memory.remember(
                category="Hypothesis",

                title=hypothesis.get(
                    "title",
                    "Unnamed Hypothesis"
                ),

                data={
                    "description": hypothesis.get(
                        "description",
                        ""
                    ),

                    "workflow": hypothesis.get(
                        "workflow_name",
                        hypothesis.get(
                            "workflow",
                            "Unknown Workflow"
                        )
                    ),

                    "risk": hypothesis.get(
                        "risk",
                        "Unknown"
                    ),

                    "confidence": hypothesis.get(
                        "confidence",
                        0
                    ),

                    "evidence": hypothesis.get(
                        "evidence",
                        []
                    ),

                    "endpoints": hypothesis.get(
                        "endpoints",
                        []
                    ),

                    "reasoning": hypothesis.get(
                        "reasoning",
                        []
                    )
                },

                confidence=self._normalize_confidence(
                    hypothesis.get(
                        "confidence",
                        80
                    )
                ),

                tags=self._infer_tags(
                    hypothesis.get(
                        "title",
                        ""
                    )
                )
            )

    # =========================================================
    # RUN BRAIN
    # =========================================================

    def run(self):

        print()
        print("=" * 70)
        print("BugHunter AI Brain")
        print("=" * 70)

        # -----------------------------------------------------
        # -----------------------------------------------------
        # 1. STRATEGY
        # -----------------------------------------------------

        strategist = Strategist(
            self.memory
        )

        strategies = strategist.generate()

        print(
            f"Strategies Generated : {len(strategies)}"
        )

        # -----------------------------------------------------
        # 2. DECISION
        # -----------------------------------------------------

        decision_engine = DecisionEngine(
            strategies
        )

        tasks = decision_engine.decide()

        print(
            f"Investigation Tasks : {len(tasks)}"
        )

        # 3. ATTACK PLANNING
        # -----------------------------------------------------

        attack_executor = AttackExecutor(
            tasks
        )

        plans = attack_executor.build()

        print(
            f"Attack Plans : {len(plans)}"
        )

        # -----------------------------------------------------
        # 4. REFLECTION
        # -----------------------------------------------------

        reflector = ReflectionEngine(
            plans,
            self.memory
        )

        reflections = reflector.evaluate()

        print(
            f"Reflection Records : {len(reflections)}"
        )

        # -----------------------------------------------------
        # 5. SECURITY FINDINGS
        # -----------------------------------------------------

        findings = self._build_findings(
            strategies=strategies,
            tasks=tasks,
            plans=plans,
            reflections=reflections
        )

        print(
            f"Security Findings : {len(findings)}"
        )

        # -----------------------------------------------------
        # SERIALIZE DATACLASSES
        #
        # Keep the real objects internally.
        # Convert only the final API result into dictionaries.
        # -----------------------------------------------------

        return {
            "memory": self.memory,

            "strategies": self._serialize_list(
                strategies
            ),

            "tasks": self._serialize_list(
                tasks
            ),

            "plans": self._serialize_list(
                plans
            ),

            "reflections": self._serialize_list(
                reflections
            ),

            "findings": findings
        }

    # =========================================================
    # BUILD FINDINGS
    # =========================================================

    def _build_findings(
        self,
        strategies,
        tasks,
        plans,
        reflections
    ):

        findings = []

        # -----------------------------------------------------
        # Strategy findings
        # -----------------------------------------------------

        for index, strategy in enumerate(
            strategies or []
        ):

            data = self._to_dict(
                strategy
            )

            title = data.get(
                "name",
                f"Security Finding {index + 1}"
            )

            description = data.get(
                "objective",
                "Security-relevant behavior identified during investigation."
            )

            risk = self._extract_risk(
                data
            )

            confidence = self._extract_confidence(
                data
            )

            reasoning = self._extract_list(
                data,
                "reasoning"
            )

            finding = {
                "id": f"finding-{index + 1}",

                "title": self._clean_title(
                    title,
                    index
                ),

                "description": str(
                    description
                ),

                "workflow": str(
                    data.get(
                        "workflow",
                        "Application workflow"
                    )
                ),

                "risk": risk,

                "confidence": confidence,

                "decision": "INVESTIGATE",

                "evidence": [],

                "reasoning": reasoning,

                "endpoints": [],

                "severity": self._risk_level(
                    risk
                ),

                "source": "BugHunter AI Reasoning Engine"
            }

            findings.append(
                finding
            )

        # -----------------------------------------------------
        # If strategies are unavailable, use tasks
        # -----------------------------------------------------

        if not findings:

            for index, task in enumerate(
                tasks or []
            ):

                data = self._to_dict(
                    task
                )

                finding = {
                    "id": f"finding-{index + 1}",

                    "title": self._clean_title(
                        data.get(
                            "strategy_name",
                            data.get(
                                "title",
                                "Security Investigation"
                            )
                        ),
                        index
                    ),

                    "description": str(
                        data.get(
                            "objective",
                            "Security-relevant behavior requires investigation."
                        )
                    ),

                    "workflow": "Application workflow",

                    "risk": self._extract_risk(
                        data
                    ),

                    "confidence": self._extract_confidence(
                        data
                    ),

                    "decision": "INVESTIGATE",

                    "evidence": [],

                    "reasoning": self._extract_list(
                        data,
                        "reasoning"
                    ),

                    "endpoints": [],

                    "severity": self._risk_level(
                        self._extract_risk(
                            data
                        )
                    ),

                    "source": "BugHunter AI Reasoning Engine"
                }

                findings.append(
                    finding
                )

        # -----------------------------------------------------
        # Reflection enrichment
        # -----------------------------------------------------

        self._apply_reflections(
            findings,
            reflections
        )

        return findings

    # =========================================================
    # REFLECTION ENRICHMENT
    # =========================================================

    def _apply_reflections(
        self,
        findings,
        reflections
    ):

        if not findings:
            return

        for index, reflection in enumerate(
            reflections or []
        ):

            if index >= len(findings):
                break

            data = self._to_dict(
                reflection
            )

            finding = findings[index]

            outcome = data.get(
                "outcome",
                ""
            )

            decision = data.get(
                "decision",
                ""
            )

            confidence_after = data.get(
                "confidence_after",
                None
            )

            observations = data.get(
                "observations",
                []
            )

            next_steps = data.get(
                "next_steps",
                []
            )

            if outcome:

                finding["description"] = str(
                    outcome
                )

            if decision:

                finding["decision"] = str(
                    decision
                ).upper()

            if confidence_after is not None:

                finding["confidence"] = (
                    self._normalize_confidence(
                        confidence_after
                    ) * 100
                )

            if observations:

                finding["evidence"] = (
                    self._merge_lists(
                        finding.get(
                            "evidence",
                            []
                        ),
                        observations
                    )
                )

            if next_steps:

                finding["next_steps"] = [
                    str(step)
                    for step in next_steps
                ]

    # =========================================================
    # DATACLASS / DICT NORMALIZATION
    # =========================================================

    def _to_dict(self, value):

        if isinstance(
            value,
            dict
        ):
            return value

        if is_dataclass(
            value
        ):
            return asdict(
                value
            )

        return {}

    def _serialize_list(
        self,
        values
    ):

        result = []

        for value in values or []:

            if isinstance(
                value,
                dict
            ):
                result.append(
                    value
                )

            elif is_dataclass(
                value
            ):
                result.append(
                    asdict(
                        value
                    )
                )

            else:
                result.append(
                    value
                )

        return result

    # =========================================================
    # RISK
    # =========================================================

    def _extract_risk(
        self,
        data
    ):

        if not isinstance(
            data,
            dict
        ):
            return 0

        risk = data.get(
            "risk",
            data.get(
                "risk_score",
                data.get(
                    "score",
                    0
                )
            )
        )

        if isinstance(
            risk,
            (int, float)
        ):

            return round(
                float(risk),
                2
            )

        mapping = {
            "critical": 95,
            "high": 80,
            "medium": 60,
            "moderate": 60,
            "low": 30,
            "info": 10,
            "informational": 10
        }

        risk_text = str(
            risk
        ).strip().lower()

        if risk_text in mapping:

            return mapping[
                risk_text
            ]

        try:

            return float(
                risk_text
            )

        except (
            ValueError,
            TypeError
        ):

            return 0

    # =========================================================
    # CONFIDENCE
    # =========================================================

    def _extract_confidence(
        self,
        data
    ):

        if not isinstance(
            data,
            dict
        ):
            return 0

        confidence = data.get(
            "confidence",
            data.get(
                "confidence_after",
                0
            )
        )

        return round(
            self._normalize_confidence(
                confidence
            ) * 100,
            2
        )

    def _normalize_confidence(
        self,
        value
    ):

        try:

            value = float(
                value
            )

        except (
            ValueError,
            TypeError
        ):

            return 0.0

        if 0 <= value <= 1:

            return value

        if 0 <= value <= 100:

            return value / 100.0

        return 0.0

    # =========================================================
    # LIST HELPERS
    # =========================================================

    def _extract_list(
        self,
        data,
        key
    ):

        if not isinstance(
            data,
            dict
        ):
            return []

        value = data.get(
            key,
            []
        )

        if value is None:
            return []

        if isinstance(
            value,
            list
        ):

            return [
                item
                if isinstance(
                    item,
                    dict
                )
                else str(item)
                for item in value
            ]

        if isinstance(
            value,
            tuple
        ):

            return [
                str(item)
                for item in value
            ]

        return [
            str(value)
        ]

    def _merge_lists(
        self,
        first,
        second
    ):

        result = []

        for item in (
            first or []
        ) + (
            second or []
        ):

            if item not in result:

                result.append(
                    item
                )

        return result

    # =========================================================
    # RISK LEVEL
    # =========================================================

    def _risk_level(
        self,
        risk
    ):

        try:

            score = float(
                risk
            )

        except (
            ValueError,
            TypeError
        ):

            score = 0

        if score >= 90:
            return "CRITICAL"

        if score >= 70:
            return "HIGH"

        if score >= 40:
            return "MEDIUM"

        if score > 0:
            return "LOW"

        return "INFORMATIONAL"

    # =========================================================
    # TITLE
    # =========================================================

    def _clean_title(
        self,
        title,
        index
    ):

        title = str(
            title
        ).strip()

        if not title:

            return (
                f"Security Finding {index + 1}"
            )

        generic_titles = {
            "security finding",
            "finding",
            "investigation strategy",
            "security investigation"
        }

        if title.lower() in generic_titles:

            return (
                f"Security Finding {index + 1}"
            )

        return title

    # =========================================================
    # TAG INFERENCE
    # =========================================================

    def _infer_tags(
        self,
        text
    ):

        title = str(
            text
        ).lower()

        tags = []

        keywords = [
            "auth",
            "authorization",
            "idor",
            "jwt",
            "sql",
            "csrf",
            "xss",
            "ssrf",
            "sqli",
            "payment",
            "admin",
            "upload",
            "file",
            "graphql",
            "api",
            "session",
            "permission",
            "access",
            "token",
            "workflow"
        ]

        for keyword in keywords:

            if keyword in title:

                tags.append(
                    keyword
                )

        return tags