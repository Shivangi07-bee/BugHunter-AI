from typing import List, Dict


class HypothesisGenerator:
    """
    Generates security investigation hypotheses from reconstructed
    application workflows.

    This engine does NOT claim that a vulnerability exists.

    It identifies security-relevant conditions that a human hunter
    should investigate and validate.
    """

    def __init__(self, workflow_contexts: List[Dict]):
        self.workflow_contexts = workflow_contexts

    # ============================================================
    # PUBLIC API
    # ============================================================

    def generate(self) -> List[Dict]:

        results = []

        for workflow in self.workflow_contexts:

            workflow_name = workflow.get(
                "workflow_name",
                "Unknown Workflow"
            )

            endpoints = workflow.get(
                "endpoints",
                []
            )

            security_signals = workflow.get(
                "security_signals",
                {}
            )

            shared_models = set(
                workflow.get(
                    "shared_models",
                    []
                )
            )

            sensitive_models = set(
                workflow.get(
                    "sensitive_models",
                    []
                )
            )

            sensitive_endpoints = set(
                workflow.get(
                    "sensitive_endpoints",
                    []
                )
            )

            # ----------------------------------------------------
            # Workflow-level reasoning
            # ----------------------------------------------------

            if len(endpoints) >= 2:

                results.append(
                    self._hypothesis(
                        title="Workflow Authorization Review",
                        description=(
                            f"Multiple endpoints participate in "
                            f"{workflow_name}. Review whether authorization "
                            f"requirements remain consistent across the "
                            f"workflow."
                        ),
                        reasoning=[
                            "The application exposes multiple related endpoints.",
                            "Related workflow steps may have different security boundaries.",
                            "Authorization should be validated at each sensitive state transition."
                        ],
                        evidence=[
                            endpoint.get("path")
                            for endpoint in endpoints
                            if endpoint.get("path")
                        ],
                        risk="Medium",
                        confidence=65,
                        workflow_name=workflow_name
                    )
                )

            # ----------------------------------------------------
            # Authentication boundary
            # ----------------------------------------------------

            if security_signals.get(
                "has_unauthenticated_endpoints"
            ):

                unauthenticated = workflow.get(
                    "unauthenticated_endpoints",
                    []
                )

                for path in unauthenticated:

                    results.append(
                        self._hypothesis(
                            title="Authentication Boundary Review",
                            description=(
                                f"{path} appears accessible without an "
                                f"authentication requirement."
                            ),
                            reasoning=[
                                "Endpoint metadata indicates no authentication requirement.",
                                "Determine whether public access is intentional.",
                                "If the endpoint accesses protected state, verify the authorization boundary."
                            ],
                            evidence=[path],
                            risk="Medium",
                            confidence=70,
                            workflow_name=workflow_name
                        )
                    )

            # ----------------------------------------------------
            # Sensitive endpoints
            # ----------------------------------------------------

            for endpoint in endpoints:

                path = endpoint.get(
                    "path",
                    ""
                )

                method = str(
                    endpoint.get(
                        "method",
                        ""
                    )
                ).upper()

                models = {
                    str(model).lower()
                    for model in endpoint.get(
                        "models",
                        []
                    )
                }

                calls = endpoint.get(
                    "calls",
                    []
                )

                authenticated = bool(
                    endpoint.get(
                        "authentication",
                        False
                    )
                )

                parameters = endpoint.get(
                    "parameters",
                    []
                )

                inputs = endpoint.get(
                    "inputs",
                    []
                )

                # ------------------------------------------------
                # Sensitive resource authorization
                # ------------------------------------------------

                if path in sensitive_endpoints:

                    results.append(
                        self._hypothesis(
                            title="Sensitive Resource Authorization Review",
                            description=(
                                f"{path} handles a potentially sensitive "
                                f"application resource."
                            ),
                            reasoning=[
                                "The endpoint name indicates a sensitive application operation.",
                                "Sensitive resources should enforce object-level authorization.",
                                "Review whether the requested resource is bound to the authenticated principal."
                            ],
                            evidence=[
                                path,
                                *list(models)
                            ],
                            risk="High",
                            confidence=72,
                            workflow_name=workflow_name
                        )
                    )

                # ------------------------------------------------
                # User / account resources
                # ------------------------------------------------

                user_related = any(
                    keyword in model
                    for model in models
                    for keyword in [
                        "user",
                        "account",
                        "profile",
                        "member"
                    ]
                )

                if user_related:

                    results.append(
                        self._hypothesis(
                            title="Object Ownership Review",
                            description=(
                                f"{path} interacts with a user or account "
                                f"related resource."
                            ),
                            reasoning=[
                                "User-owned resources require ownership validation.",
                                "Review whether resource identifiers are trusted from client input.",
                                "Compare authorization behavior across related workflow endpoints."
                            ],
                            evidence=[
                                path
                            ],
                            risk="High",
                            confidence=78,
                            workflow_name=workflow_name
                        )
                    )

                # ------------------------------------------------
                # Payment / transaction resources
                # ------------------------------------------------

                payment_related = any(
                    keyword in model
                    for model in models
                    for keyword in [
                        "payment",
                        "transaction",
                        "invoice",
                        "order"
                    ]
                )

                if payment_related:

                    results.append(
                        self._hypothesis(
                            title="Financial Workflow Integrity Review",
                            description=(
                                f"{path} participates in a financial or "
                                f"transaction-related workflow."
                            ),
                            reasoning=[
                                "Financial state transitions require strict server-side validation.",
                                "Review ownership, amount, state and authorization checks.",
                                "Compare preceding and following workflow steps for inconsistent validation."
                            ],
                            evidence=[
                                path
                            ],
                            risk="High",
                            confidence=82,
                            workflow_name=workflow_name
                        )
                    )

                # ------------------------------------------------
                # State-changing operations
                # ------------------------------------------------

                if method in {
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE"
                }:

                    results.append(
                        self._hypothesis(
                            title="State Transition Review",
                            description=(
                                f"{path} performs a state-changing operation."
                            ),
                            reasoning=[
                                "The endpoint can modify application state.",
                                "State transitions should enforce authorization and business invariants.",
                                "Review whether client-controlled values can bypass expected state transitions."
                            ],
                            evidence=[
                                path
                            ],
                            risk="Medium",
                            confidence=68,
                            workflow_name=workflow_name
                        )
                    )

                # ------------------------------------------------
                # Input handling
                # ------------------------------------------------

                if method in {
                    "POST",
                    "PUT",
                    "PATCH"
                } or parameters or inputs:

                    results.append(
                        self._hypothesis(
                            title="Input Validation Review",
                            description=(
                                f"{path} accepts or processes client-controlled input."
                            ),
                            reasoning=[
                                "Client input should be validated against server-side expectations.",
                                "Review type, range, format and business-rule validation.",
                                "Pay particular attention to fields affecting authorization or application state."
                            ],
                            evidence=[
                                path,
                                *self._string_values(parameters),
                                *self._string_values(inputs)
                            ],
                            risk="Medium",
                            confidence=70,
                            workflow_name=workflow_name
                        )
                    )

                # ------------------------------------------------
                # Shared application functions
                # ------------------------------------------------

                if calls:

                    results.append(
                        self._hypothesis(
                            title="Shared Logic Consistency Review",
                            description=(
                                f"{path} uses shared application logic."
                            ),
                            reasoning=[
                                "Shared functions may implement security-sensitive behavior.",
                                "Review whether every caller applies equivalent validation.",
                                "Look for differences between privileged and unprivileged call paths."
                            ],
                            evidence=[
                                path,
                                *self._string_values(calls)
                            ],
                            risk="Medium",
                            confidence=64,
                            workflow_name=workflow_name
                        )
                    )

            # ----------------------------------------------------
            # Sensitive workflow models
            # ----------------------------------------------------

            if sensitive_models:

                results.append(
                    self._hypothesis(
                        title="Sensitive Workflow Review",
                        description=(
                            f"{workflow_name} contains models associated "
                            f"with sensitive application state."
                        ),
                        reasoning=[
                            "Sensitive models increase the impact of authorization failures.",
                            "Review ownership and state transitions across the workflow.",
                            "Trace how these models move between endpoints."
                        ],
                        evidence=sorted(
                            sensitive_models
                        ),
                        risk="High",
                        confidence=75,
                        workflow_name=workflow_name
                    )
                )

            # ----------------------------------------------------
            # Remove duplicate hypotheses
            # ----------------------------------------------------

        return self._deduplicate(results)

    # ============================================================
    # HYPOTHESIS BUILDER
    # ============================================================

    def _hypothesis(
        self,
        title: str,
        description: str,
        reasoning: List[str],
        evidence: List,
        risk: str,
        confidence: int,
        workflow_name: str
    ) -> Dict:

        clean_evidence = []

        for item in evidence:

            if item is None:
                continue

            value = str(item).strip()

            if value and value not in clean_evidence:
                clean_evidence.append(value)

        return {

            "title": title,

            "description": description,

            "reasoning": reasoning,

            "evidence": clean_evidence,

            "risk": risk,

            "confidence": confidence,

            "workflow_name": workflow_name,

            "endpoints": [
                value
                for value in clean_evidence
                if value.startswith("/")
            ],

            "status": "Hypothesis",

            "requires_validation": True
        }

    # ============================================================
    # NORMALIZE VALUES
    # ============================================================

    def _string_values(self, values) -> List[str]:

        if not values:
            return []

        if isinstance(values, str):
            return [values]

        result = []

        for value in values:

            if isinstance(value, dict):

                for key in [
                    "name",
                    "key",
                    "parameter",
                    "field"
                ]:

                    if value.get(key):
                        result.append(
                            str(value[key])
                        )

                        break

            else:

                result.append(
                    str(value)
                )

        return result

    # ============================================================
    # DEDUPLICATION
    # ============================================================

    def _deduplicate(
        self,
        hypotheses: List[Dict]
    ) -> List[Dict]:

        unique = []
        seen = set()

        for hypothesis in hypotheses:

            key = (
                hypothesis.get("workflow_name"),
                hypothesis.get("title"),
                tuple(
                    sorted(
                        hypothesis.get(
                            "endpoints",
                            []
                        )
                    )
                )
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(hypothesis)

        return unique