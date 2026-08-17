from .models import RuntimeStep


class ResponseAnalyzer:
    """
    Analyzes HTTP responses returned by the Runtime Engine.

    This engine does NOT determine whether a vulnerability exists.

    It simply extracts observations that the Brain can reason about.
    """

    # --------------------------------------------------

    def analyze(self, response, attack_step):

        observations = []

        status = response.get(
            "status",
            0
        )

        body = response.get(
            "body",
            ""
        )

        headers = response.get(
            "headers",
            {}
        )

        # -----------------------------------------
        # Status Code
        # -----------------------------------------

        if status == 200:

            observations.append(
                "Request completed successfully."
            )

        elif status in [401, 403]:

            observations.append(
                "Authentication / Authorization enforced."
            )

        elif status == 404:

            observations.append(
                "Requested resource not found."
            )

        elif status >= 500:

            observations.append(
                "Server-side error detected."
            )

        # -----------------------------------------
        # Response Size
        # -----------------------------------------

        if len(body) > 5000:

            observations.append(
                "Large response body returned."
            )

        # -----------------------------------------
        # Interesting Headers
        # -----------------------------------------

        if "Set-Cookie" in headers:

            observations.append(
                "Server issued cookies."
            )

        if "Authorization" in headers:

            observations.append(
                "Authorization header present."
            )

        # -----------------------------------------
        # Runtime Result
        # -----------------------------------------

        return RuntimeStep(

            step_number=attack_step.step_number,

            action=attack_step.action,

            request=attack_step.request_template,

            response_status=status,

            response_headers=headers,

            response_body=body,

            observations=observations,

            success=status == 200

        )