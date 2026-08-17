from typing import List, Dict


class EvidenceCollector:
    """
    Collect supporting evidence for every hypothesis.
    """

    def __init__(
        self,
        workflow_contexts: List[Dict],
        hypotheses: List[Dict]
    ):

        self.workflow_contexts = workflow_contexts
        self.hypotheses = hypotheses

    # ----------------------------------------------------

    def collect(self) -> List[Dict]:

        workflow_lookup = {

            workflow["workflow_name"]: workflow

            for workflow in self.workflow_contexts

        }

        evidence = []

        for hypothesis in self.hypotheses:

            workflow = workflow_lookup.get(

                hypothesis.get(
                    "workflow_name",
                    ""
                )

            )

            endpoints = []

            if workflow:

                endpoints = workflow.get(
                    "endpoints",
                    []
                )

            evidence.append({

                "title": hypothesis.get(
                    "title"
                ),

                "workflow_name": hypothesis.get(
                    "workflow_name"
                ),

                "risk": hypothesis.get(
                    "risk"
                ),

                "score": hypothesis.get(
                    "score"
                ),

                "confidence": hypothesis.get(
                    "confidence"
                ),

                "description": hypothesis.get(
                    "description"
                ),

                "type": "Static Analysis",

                "location": ", ".join(

                    endpoint.get("path", "")

                    for endpoint in endpoints

                ),

                "endpoint_count": len(endpoints),

                "endpoints": endpoints,

                "reasoning": hypothesis.get(
                    "reasoning",
                    []
                ),

                "evidence": hypothesis.get(
                    "evidence",
                    []
                )

            })

        return evidence