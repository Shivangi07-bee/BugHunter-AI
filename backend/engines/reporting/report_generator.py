from datetime import datetime


class ReportGenerator:
    """
    Generates the final BugHunter AI report from the InvestigationWorkspace.
    """

    def __init__(self, workspace):

        self.workspace = workspace

    # --------------------------------------------------

    def generate(self):

        return {

            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "repository": self.workspace.repository,

            "routes": self.workspace.routes,

            "endpoints": self.workspace.endpoints,

            "workflows": self.workspace.workflows,

            "knowledge_graph": self.workspace.knowledge_graph,

            "hypotheses": self.workspace.hypotheses,

            "risk": self.workspace.risk,

            "evidence": self.workspace.evidence,

            "investigation_plan": self.workspace.investigation_plan,

            "attack_plans": self.workspace.attack_plans,

            "runtime": getattr(
                self.workspace,
                "runtime",
                []
            ),

            "findings": self.workspace.findings

        }