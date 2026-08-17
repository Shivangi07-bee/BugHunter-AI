from collections import defaultdict


class InvestigationIdentityEngine:
    """
    Converts raw reasoning strategies into unique investigations.

    Responsibilities:
    - Remove truly duplicate investigations.
    - Preserve investigations that target different endpoints.
    - Preserve investigations with different objectives.
    - Give duplicate display titles meaningful names.
    - Attach a stable investigation_id.

    This is NOT a vulnerability scanner.
    It only organizes the reasoning produced by the Brain.
    """

    def normalize(self, value):
        if value is None:
            return ""

        if isinstance(value, list):
            return " | ".join(
                self.normalize(item)
                for item in value
            )

        if isinstance(value, dict):
            return " | ".join(
                f"{key}:{self.normalize(value[key])}"
                for key in sorted(value.keys())
            )

        return " ".join(
            str(value).lower().strip().split()
        )

    def extract_endpoints(self, item):
        endpoints = item.get(
            "endpoints",
            item.get("endpoint", [])
        )

        if endpoints is None:
            return []

        if not isinstance(endpoints, list):
            endpoints = [endpoints]

        result = []

        for endpoint in endpoints:
            if isinstance(endpoint, dict):
                method = endpoint.get(
                    "method",
                    ""
                )

                path = endpoint.get(
                    "path",
                    endpoint.get(
                        "route",
                        ""
                    )
                )

                value = f"{method} {path}".strip()

                if value:
                    result.append(value)

            else:
                value = str(endpoint).strip()

                if value:
                    result.append(value)

        return sorted(
            set(result)
        )

    def identity_key(self, item):
        """
        Two investigations are considered identical only when
        their actual security target is the same.
        """

        workflow = self.normalize(
            item.get(
                "workflow",
                item.get(
                    "workflow_name",
                    ""
                )
            )
        )

        objective = self.normalize(
            item.get(
                "objective",
                item.get(
                    "description",
                    ""
                )
            )
        )

        attack_type = self.normalize(
            item.get(
                "attack_type",
                item.get(
                    "category",
                    item.get(
                        "type",
                        ""
                    )
                )
            )
        )

        endpoints = tuple(
            self.extract_endpoints(item)
        )

        reasoning = self.normalize(
            item.get(
                "reasoning",
                []
            )
        )

        return (
            workflow,
            attack_type,
            objective,
            endpoints,
            reasoning
        )

    def deduplicate(self, investigations):
        """
        Remove exact reasoning duplicates while preserving
        meaningful investigations.
        """

        unique = []
        seen = set()

        for investigation in investigations or []:

            if not isinstance(
                investigation,
                dict
            ):
                continue

            key = self.identity_key(
                investigation
            )

            if key in seen:
                continue

            seen.add(key)

            investigation = dict(
                investigation
            )

            unique.append(
                investigation
            )

        return unique

    def _focus_from_strategy(self, item):
        """
        Extract a useful human-readable security focus.
        """

        attack_type = item.get(
            "attack_type",
            item.get(
                "category",
                item.get(
                    "type",
                    ""
                )
            )
        )

        if attack_type:
            return str(
                attack_type
            ).replace(
                "_",
                " "
            ).title()

        reasoning = item.get(
            "reasoning",
            []
        )

        if isinstance(
            reasoning,
            list
        ) and reasoning:

            text = str(
                reasoning[0]
            ).strip()

            if text:
                return text[:70]

        description = item.get(
            "description",
            item.get(
                "objective",
                ""
            )
        )

        if description:
            return str(
                description
            ).strip()[:70]

        endpoints = self.extract_endpoints(
            item
        )

        if endpoints:
            return endpoints[0]

        return "Security Assessment"

    def assign_display_titles(self, investigations):
        """
        Prevent ugly repeated UI titles.

        Example:

        Authorization Assessment
        Authorization Assessment

        becomes:

        Authorization Assessment
        Authorization Assessment — Payment Endpoint
        """

        title_groups = defaultdict(list)

        for item in investigations:

            title = item.get(
                "title",
                item.get(
                    "name",
                    "Security Investigation"
                )
            )

            title = str(
                title
            ).strip()

            title_groups[
                title.lower()
            ].append(item)

        for title_key, items in title_groups.items():

            if len(items) == 1:

                item = items[0]

                item["title"] = (
                    item.get(
                        "title",
                        "Security Investigation"
                    )
                )

                continue

            used_titles = set()

            for item in items:

                base_title = str(
                    item.get(
                        "title",
                        "Security Investigation"
                    )
                ).strip()

                focus = self._focus_from_strategy(
                    item
                )

                candidate = (
                    f"{base_title} — {focus}"
                )

                candidate_key = (
                    candidate.lower()
                )

                if candidate_key in used_titles:

                    endpoints = (
                        self.extract_endpoints(
                            item
                        )
                    )

                    if endpoints:

                        candidate = (
                            f"{base_title} — "
                            f"{endpoints[0]}"
                        )

                used_titles.add(
                    candidate.lower()
                )

                item["title"] = candidate

        return investigations

    def enrich(self, investigations):
        """
        Final processing pipeline.
        """

        investigations = (
            self.deduplicate(
                investigations
            )
        )

        investigations = (
            self.assign_display_titles(
                investigations
            )
        )

        for index, investigation in enumerate(
            investigations,
            start=1
        ):

            investigation[
                "investigation_id"
            ] = (
                investigation.get(
                    "investigation_id"
                )
                or f"investigation-{index}"
            )

        return investigations