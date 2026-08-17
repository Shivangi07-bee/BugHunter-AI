from .models import InvestigationWorkspace


class Workspace:

    def __init__(self):

        self.workspace = InvestigationWorkspace()

    # --------------------------------------------------
    # Repository
    # --------------------------------------------------

    def repository(self, data):
        self.workspace.repository = data

    # --------------------------------------------------
    # Routes
    # --------------------------------------------------

    def routes(self, data):
        self.workspace.routes = data

    # --------------------------------------------------
    # Endpoints
    # --------------------------------------------------

    def endpoints(self, data):
        self.workspace.endpoints = data

    # --------------------------------------------------
    # Workflow
    # --------------------------------------------------

    def workflow(self, data):
        self.workspace.workflows = data

    # --------------------------------------------------
    # Knowledge Graph
    # --------------------------------------------------

    def knowledge_graph(self, data):
        self.workspace.knowledge_graph = data

   # --------------------------------------------------
# Timeline
# --------------------------------------------------

    def timeline(self, data):
        self.workspace.timeline = data

    # --------------------------------------------------
    # Hypotheses
    # --------------------------------------------------

    def hypotheses(self, data):
        self.workspace.hypotheses = data

    # --------------------------------------------------
    # Investigation Plan
    # --------------------------------------------------

    def investigation_plan(self, data):

        self.workspace.investigation_plan = data

        # Automatically expose attack plans
        if hasattr(data, "attack_plans"):
            self.workspace.attack_plans = data.attack_plans

        elif isinstance(data, dict):
            self.workspace.attack_plans = data.get(
                "attack_plans",
                []
            )

    # --------------------------------------------------
    # Evidence
    # --------------------------------------------------

    def evidence(self, data):
        self.workspace.evidence = data

    # --------------------------------------------------
    # Risk
    # --------------------------------------------------

    def risk(self, data):
        self.workspace.risk = data

    # Backward compatibility
    def risks(self, data):
        self.workspace.risk = data

    # --------------------------------------------------
    # Attack Plans
    # --------------------------------------------------

    def attack_plans(self, data):
        self.workspace.attack_plans = data

    def runtime(self, data):
         self.workspace.runtime = data

    # --------------------------------------------------
    # Findings
    # --------------------------------------------------

    def findings(self, data):
        self.workspace.findings = data
        # --------------------------------------------------
# Executive Summary
# --------------------------------------------------

    def executive_summary(self, data):
        self.workspace.executive_summary = data

    # --------------------------------------------------
    # Build Workspace
    # --------------------------------------------------

    def build(self):
        return self.workspace