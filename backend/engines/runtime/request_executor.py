import requests


class RequestExecutor:
    """
    Executes controlled HTTP validation requests.

    The executor only performs requests explicitly supplied by
    the Runtime Engine and uses an explicit target base URL.

    It does not discover targets or generate exploit payloads.
    """

    def __init__(
        self,
        base_url=None,
        timeout=10
    ):

        self.base_url = (
            base_url.rstrip("/")
            if base_url
            else None
        )

        self.timeout = timeout

    # =========================================================
    # EXECUTE REQUEST
    # =========================================================

    def execute(
        self,
        session,
        request_template
    ):

        request_template = (
            request_template
            if isinstance(
                request_template,
                dict
            )
            else {}
        )

        method = str(
            request_template.get(
                "method",
                "GET"
            )
        ).upper()

        url = request_template.get(
            "url"
        )

        path = request_template.get(
            "path"
        )

        # -----------------------------------------------------
        # Resolve target
        # -----------------------------------------------------

        if not url:

            if not self.base_url:

                return {
                    "status": 0,
                    "headers": {},
                    "body": "",
                    "error": (
                        "No runtime target configured."
                    )
                }

            if path:

                path = str(path)

                if not path.startswith("/"):
                    path = "/" + path

                url = (
                    self.base_url +
                    path
                )

            else:

                return {
                    "status": 0,
                    "headers": {},
                    "body": "",
                    "error": (
                        "Request has no target path."
                    )
                }

        # -----------------------------------------------------
        # Request components
        # -----------------------------------------------------

        headers = request_template.get(
            "headers",
            {}
        )

        params = request_template.get(
            "params",
            {}
        )

        body = request_template.get(
            "body",
            {}
        )

        # -----------------------------------------------------
        # Execute
        # -----------------------------------------------------

        try:

            response = session.request(

                method=method,

                url=url,

                headers=headers,

                params=params,

                json=body,

                timeout=self.timeout

            )

            return {

                "status": response.status_code,

                "headers": dict(
                    response.headers
                ),

                "body": response.text,

                "url": url,

                "method": method

            }

        except requests.RequestException as exc:

            return {

                "status": 0,

                "headers": {},

                "body": "",

                "url": url,

                "method": method,

                "error": str(exc)

            }

        except Exception as exc:

            return {

                "status": 0,

                "headers": {},

                "body": "",

                "url": url,

                "method": method,

                "error": str(exc)

            }