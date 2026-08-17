from typing import List, Dict


class WorkflowContextBuilder:
    """
    Converts reconstructed workflows and endpoint metadata
    into rich security investigation context.

    This is the bridge between:

        Workflow Engine
                ↓
        Security Reasoning Engine
    """

    def __init__(
        self,
        workflows,
        endpoint_metadata
    ):
        self.workflows = workflows

        self.endpoint_lookup = {
            endpoint.get("path"): endpoint
            for endpoint in endpoint_metadata
            if endpoint.get("path")
        }

    # ---------------------------------------------------
    # Build Security Investigation Context
    # ---------------------------------------------------

    def build(self) -> List[Dict]:

        contexts = []

        for workflow in self.workflows:

            endpoints = []

            authentication_boundaries = []

            models = set()
            functions = set()

            # -------------------------------------------
            # Collect endpoint intelligence
            # -------------------------------------------

            for path in workflow.endpoints:

                endpoint = self.endpoint_lookup.get(path)

                if endpoint is None:
                    continue

                endpoint_models = set(
                    endpoint.get("models", [])
                )

                endpoint_functions = set(
                    endpoint.get("calls", [])
                )

                models.update(endpoint_models)
                functions.update(endpoint_functions)

                authentication = endpoint.get(
                    "authentication",
                    False
                )

                if authentication:
                    authentication_boundaries.append({
                        "path": endpoint.get("path"),
                        "method": endpoint.get("method"),
                        "handler": endpoint.get("handler")
                    })

                endpoints.append({

                    "path": endpoint.get("path"),

                    "method": endpoint.get(
                        "method",
                        "UNKNOWN"
                    ),

                    "handler": endpoint.get(
                        "handler",
                        ""
                    ),

                    "models": list(
                        endpoint_models
                    ),

                    "calls": list(
                        endpoint_functions
                    ),

                    "authentication": authentication,

                    # Preserve additional endpoint
                    # intelligence if available.
                    "parameters": endpoint.get(
                        "parameters",
                        []
                    ),

                    "inputs": endpoint.get(
                        "inputs",
                        []
                    ),

                    "outputs": endpoint.get(
                        "outputs",
                        []
                    )
                })

            # -------------------------------------------
            # Security characteristics
            # -------------------------------------------

            unauthenticated_endpoints = [
                endpoint["path"]
                for endpoint in endpoints
                if not endpoint["authentication"]
            ]

            sensitive_models = [
                model
                for model in models
                if any(
                    keyword in model.lower()
                    for keyword in [
                        "user",
                        "account",
                        "admin",
                        "payment",
                        "order",
                        "transaction",
                        "invoice",
                        "profile",
                        "credential",
                        "session"
                    ]
                )
            ]

            sensitive_endpoints = [
                endpoint["path"]
                for endpoint in endpoints
                if any(
                    keyword in (
                        endpoint["path"] or ""
                    ).lower()
                    for keyword in [
                        "admin",
                        "user",
                        "account",
                        "payment",
                        "order",
                        "transaction",
                        "profile",
                        "upload",
                        "delete",
                        "update"
                    ]
                )
            ]

            # -------------------------------------------
            # Workflow context
            # -------------------------------------------

            context = {

                "workflow_name": workflow.name,

                "endpoint_count": len(
                    endpoints
                ),

                "endpoints": endpoints,

                "shared_models": sorted(
                    list(
                        getattr(
                            workflow,
                            "shared_models",
                            set()
                        )
                    )
                ),

                "shared_functions": sorted(
                    list(
                        getattr(
                            workflow,
                            "shared_functions",
                            set()
                        )
                    )
                ),

                "models": sorted(
                    list(models)
                ),

                "functions": sorted(
                    list(functions)
                ),

                "authentication_boundaries":
                    authentication_boundaries,

                "unauthenticated_endpoints":
                    unauthenticated_endpoints,

                "sensitive_models":
                    sensitive_models,

                "sensitive_endpoints":
                    sensitive_endpoints,

                # Useful high-level signals for
                # downstream reasoning.
                "security_signals": {

                    "has_authentication_boundary":
                        bool(
                            authentication_boundaries
                        ),

                    "has_unauthenticated_endpoints":
                        bool(
                            unauthenticated_endpoints
                        ),

                    "has_sensitive_models":
                        bool(
                            sensitive_models
                        ),

                    "has_sensitive_endpoints":
                        bool(
                            sensitive_endpoints
                        ),

                    "endpoint_count":
                        len(endpoints)
                }
            }

            contexts.append(context)

        return contexts