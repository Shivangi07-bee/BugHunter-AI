class ExecutiveSummaryEngine:
    """
    Builds a concise executive-level summary of an investigation.

    The engine accepts both dataclass/object based results and
    dictionary based results so the service pipeline remains stable
    when data crosses API/serialization boundaries.
    """

    # ---------------------------------------------------------
    # Safe value extraction
    # ---------------------------------------------------------

    @staticmethod
    def _get(item, key, default=None):
        """
        Read a value from either:
        - an object/dataclass
        - a dictionary
        """
        if item is None:
            return default

        if isinstance(item, dict):
            return item.get(key, default)

        return getattr(item, key, default)

    # ---------------------------------------------------------
    # List normalization
    # ---------------------------------------------------------

    @staticmethod
    def _as_list(value):
        if value is None:
            return []

        if isinstance(value, list):
            return value

        if isinstance(value, tuple):
            return list(value)

        if isinstance(value, set):
            return list(value)

        return [value]

    # ---------------------------------------------------------
    # Build executive summary
    # ---------------------------------------------------------

    def build(
        self,
        profile=None,
        routes=None,
        workflows=None,
        hypotheses=None,
        evidence=None,
        attack_plans=None,
        risk=None,
    ):
        routes = self._as_list(routes)
        workflows = self._as_list(workflows)
        hypotheses = self._as_list(hypotheses)
        evidence = self._as_list(evidence)
        attack_plans = self._as_list(attack_plans)

        # -----------------------------------------------------
        # Project information
        # -----------------------------------------------------

        project_name = self._get(
            profile,
            "project_name",
            self._get(profile, "name", "Unknown Project")
        )

        language = self._get(
            profile,
            "language",
            "Unknown"
        )

        # -----------------------------------------------------
        # Risk information
        # -----------------------------------------------------

        risk_value = risk

        if risk_value is None:
            risk_value = "Unknown"

        # If risk is an object/dict, normalize it.
        if isinstance(risk_value, dict):
            risk_value = (
                risk_value.get("level")
                or risk_value.get("risk")
                or risk_value.get("overall")
                or "Unknown"
            )

        # -----------------------------------------------------
        # Hypothesis summary
        # -----------------------------------------------------

        hypothesis_summary = []

        for hypothesis in hypotheses:

            hypothesis_summary.append({
                "title": self._get(
                    hypothesis,
                    "title",
                    "Investigation Hypothesis"
                ),

                "risk": self._get(
                    hypothesis,
                    "risk",
                    "Unknown"
                ),

                "confidence": self._get(
                    hypothesis,
                    "confidence",
                    0
                ),

                "score": self._get(
                    hypothesis,
                    "score",
                    0
                ),

                "description": self._get(
                    hypothesis,
                    "description",
                    ""
                )
            })

        # -----------------------------------------------------
        # Attack plan summary
        # -----------------------------------------------------

        attack_plan_summary = []

        for plan in attack_plans:

            strategy_name = self._get(
                plan,
                "strategy_name",
                "Investigation Strategy"
            )

            objective = self._get(
                plan,
                "objective",
                ""
            )

            priority = self._get(
                plan,
                "priority",
                0
            )

            attack_steps = self._get(
                plan,
                "attack_steps",
                []
            )

            # Some serialized results may use "steps".
            if not attack_steps:
                attack_steps = self._get(
                    plan,
                    "steps",
                    []
                )

            attack_steps = self._as_list(
                attack_steps
            )

            attack_plan_summary.append({

                "strategy": strategy_name,

                "objective": objective,

                "priority": priority,

                "step_count": len(attack_steps)

            })

        # -----------------------------------------------------
        # Evidence summary
        # -----------------------------------------------------

        evidence_summary = []

        for item in evidence:

            evidence_summary.append({

                "type": self._get(
                    item,
                    "type",
                    "evidence"
                ),

                "description": self._get(
                    item,
                    "description",
                    self._get(
                        item,
                        "title",
                        ""
                    )
                )

            })

        # -----------------------------------------------------
        # Determine overall status
        # -----------------------------------------------------

        if not hypotheses:
            status = "NO_HYPOTHESES"

        elif attack_plans:
            status = "INVESTIGATION_READY"

        else:
            status = "ANALYSIS_COMPLETE"

        # -----------------------------------------------------
        # Final executive summary
        # -----------------------------------------------------

        return {

            "status": status,

            "project": {

                "name": project_name,

                "language": language

            },

            "overview": {

                "routes": len(routes),

                "workflows": len(workflows),

                "hypotheses": len(hypotheses),

                "evidence_items": len(evidence),

                "attack_plans": len(attack_plans)

            },

            "risk": risk_value,

            "hypotheses": hypothesis_summary,

            "investigation_paths": attack_plan_summary,

            "evidence": evidence_summary,

            "summary": (
                f"{project_name} was analyzed across "
                f"{len(routes)} routes and "
                f"{len(workflows)} reconstructed workflows. "
                f"{len(hypotheses)} investigation hypotheses "
                f"and {len(attack_plans)} investigation paths "
                f"were generated."
            )

        }