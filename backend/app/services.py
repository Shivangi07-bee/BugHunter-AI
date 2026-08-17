from pathlib import Path

from investigation.workspace import Workspace

from engines.application_understanding.repository_loader import RepositoryLoader
from engines.application_understanding.project_profiler import ProjectProfiler
from engines.application_understanding.route_discovery import RouteDiscovery
from engines.application_understanding.endpoint_analyzer import EndpointAnalyzer

from engines.workflow_engine.relationship_builder import RelationshipBuilder
from engines.workflow_engine.workflow_detector import WorkflowDetector
from engines.workflow_engine.context_builder import WorkflowContextBuilder

from engines.reasoning_engine.knowledge_graph_builder import KnowledgeGraphBuilder
from engines.reasoning_engine.hypothesis_generator import HypothesisGenerator
from engines.reasoning_engine.risk_ranker import RiskRanker
from engines.reasoning_engine.evidence_collector import EvidenceCollector
from engines.reasoning_engine.brain.orchestrator import BugHunterBrain
from engines.reasoning_engine.brain.attack_executor import (
    AttackExecutionPlan,
    AttackStep,
)
from engines.reasoning_engine.brain.reflection import ReflectionEngine

from engines.planner.investigation_planner import InvestigationPlanner

from engines.runtime.runtime_engine import RuntimeEngine

from engines.reporting.json_exporter import JsonExporter
from engines.reporting.report_generator import ReportGenerator

from investigation.timeline_engine import TimelineEngine
from investigation.executive_summary_engine import ExecutiveSummaryEngine

from reports.report_builder import ReportBuilder


class BugHunterService:

    def analyze(self, repository):

        # ==================================================
        # NORMALIZE REPOSITORY PATH
        # ==================================================

        # The frontend may send a Windows path such as:
        # D:\\bughunter-ai\\sample_projects\\shopping_app
        #
        # Inside Docker/Linux, Windows "\" is not treated as
        # a path separator. Normalize both Windows and Linux
        # paths before resolving the mounted repository.

        repository_value = str(repository).strip()

        repository_name = (
            repository_value
            .replace("\\", "/")
            .rstrip("/")
            .split("/")[-1]
        )

        repository_path = (
           Path(__file__).resolve().parents[2]
        / "sample_projects"
         / repository_name
        )

        if not repository_path.is_dir():
            raise FileNotFoundError(
                f"Repository not found in Docker mount: "
                f"{repository_path}"
            )

        # ==================================================
        # REPOSITORY LOADER
        # ==================================================

        loader = RepositoryLoader(
            str(repository_path)
        )
        source_files = loader.load_repository()
        root_files = loader.get_root_files()

        workspace = Workspace()

        # ==================================================
        # PROJECT PROFILER
        # ==================================================

        profiler = ProjectProfiler(
            source_files,
            root_files
        )

        profile = profiler.build_profile()

        workspace.repository(
            profile
        )

        # ==================================================
        # ROUTE DISCOVERY
        # ==================================================

        discovery = RouteDiscovery(
            source_files
        )

        routes = discovery.discover_routes()

        workspace.routes(
            routes
        )

        # ==================================================
        # ENDPOINT ANALYZER
        # ==================================================

        analyzer = EndpointAnalyzer(
            source_files,
            routes
        )

        endpoint_metadata = analyzer.analyze()

        workspace.endpoints(
            endpoint_metadata
        )

        # ==================================================
        # RELATIONSHIP BUILDER
        # ==================================================

        relationship_builder = RelationshipBuilder(
            endpoint_metadata
        )

        edges = (
            relationship_builder
            .build_relationships()
        )

        adjacency = (
            relationship_builder
            .build_graph()
        )

        # ==================================================
        # KNOWLEDGE GRAPH
        # ==================================================

        graph = KnowledgeGraphBuilder(
            endpoint_metadata,
            edges
        ).build()

        workspace.knowledge_graph(
            graph
        )

        # ==================================================
        # WORKFLOW DETECTION
        # ==================================================

        detector = WorkflowDetector(
            adjacency
        )

        workflows = detector.detect()

        # ==================================================
        # WORKFLOW CONTEXT
        # ==================================================

        context = WorkflowContextBuilder(
            workflows,
            endpoint_metadata
        ).build()

        workspace.workflow(
            context
        )

        # ==================================================
        # HYPOTHESIS GENERATION
        # ==================================================

        hypotheses = HypothesisGenerator(
            context
        ).generate()

        # ==================================================
        # RISK RANKING
        # ==================================================

        hypotheses = RiskRanker(
            hypotheses
        ).rank()

        workspace.hypotheses(
            hypotheses
        )

        workspace.risks(
            hypotheses
        )

        risk = workspace.build().risk

        # ==================================================
        # STATIC EVIDENCE
        # ==================================================

        evidence = EvidenceCollector(
            context,
            hypotheses
        ).collect()

        workspace.evidence(
            evidence
        )

        # ==================================================
        # INVESTIGATION PLANNER
        # ==================================================

        planner = InvestigationPlanner(
            workflows,
            hypotheses,
            graph
        )

        investigation_plan = (
            planner.build()
        )

        workspace.investigation_plan(
            investigation_plan
        )

        # ==================================================
        # BUGHUNTER BRAIN
        # ==================================================

        brain = BugHunterBrain()

        brain.load_hypotheses(
            hypotheses
        )

        brain_result = brain.run()

        findings = brain_result.get(
            "findings",
            []
        )

        workspace.findings(
            findings
        )

        # ==================================================
        # ATTACK PLANS
        # ==================================================

        serialized_attack_plans = (
            brain_result.get(
                "plans",
                []
            )
        )

        workspace.attack_plans(
            serialized_attack_plans
        )

        # ==================================================
        # RESTORE ATTACK PLAN OBJECTS
        #
        # Brain exposes dictionaries for the API.
        # Runtime works with AttackExecutionPlan objects.
        # ==================================================

        attack_plans = (
            self._restore_attack_plans(
                serialized_attack_plans
            )
        )

        # ==================================================
        # RUNTIME EXECUTION
        # ==================================================

        runtime = RuntimeEngine()

        runtime_results = runtime.execute(
            attack_plans
        )

        workspace.runtime(
            runtime_results
        )

        # ==================================================
        # RUNTIME → INVESTIGATION EVIDENCE
        # ==================================================

        runtime_evidence = []

        for plan_result in runtime_results:

            strategy = plan_result.get(
                "strategy",
                "Unknown Strategy"
            )

            for step in plan_result.get(
                "steps",
                []
            ):

                runtime_evidence.append({

                    "source": "runtime",

                    "strategy": strategy,

                    "step": step.get(
                        "step_number"
                    ),

                    "action": step.get(
                        "action",
                        ""
                    ),

                    "status": step.get(
                        "status",
                        0
                    ),

                    "success": step.get(
                        "success",
                        False
                    ),

                    "observations": step.get(
                        "observations",
                        []
                    )

                })

        # Preserve static evidence and
        # append runtime observations.

        evidence = (
            evidence +
            runtime_evidence
        )

        workspace.evidence(
            evidence
        )

        workspace.workspace.metadata[
            "runtime"
        ] = runtime_results

        # ==================================================
        # RUNTIME EVIDENCE → BRAIN MEMORY
        # ==================================================

        for item in runtime_evidence:

            brain.memory.remember(

                category="Evidence",

                title=item.get(
                    "strategy",
                    "Runtime Validation"
                ),

                data=item,

                confidence=(
                    1.0
                    if item.get(
                        "success",
                        False
                    )
                    else 0.5
                ),

                tags=[
                    "runtime",
                    "evidence"
                ]

            )

        # ==================================================
        # POST-RUNTIME REFLECTION
        #
        # The Brain now reflects on actual runtime
        # observations rather than only generated plans.
        # ==================================================

        post_runtime_reflections = []

        if attack_plans:

            reflection_engine = ReflectionEngine(
                attack_plans,
                brain.memory
            )

            post_runtime_reflections = (
                reflection_engine.evaluate()
            )

        serialized_reflections = []

        for reflection in post_runtime_reflections:

            if hasattr(
                reflection,
                "__dataclass_fields__"
            ):

                from dataclasses import asdict

                serialized_reflections.append(
                    asdict(
                        reflection
                    )
                )

            elif isinstance(
                reflection,
                dict
            ):

                serialized_reflections.append(
                    reflection
                )

        brain_result[
            "post_runtime_reflections"
        ] = serialized_reflections

        # ==================================================
        # ENRICH FINDINGS WITH REFLECTION
        # ==================================================

        for index, reflection in enumerate(
            serialized_reflections
        ):

            if index >= len(findings):
                break

            finding = findings[index]

            if not isinstance(
                finding,
                dict
            ):
                continue

            decision = reflection.get(
                "decision"
            )

            outcome = reflection.get(
                "outcome"
            )

            confidence = reflection.get(
                "confidence_after"
            )

            if decision:
                finding[
                    "decision"
                ] = decision

            if outcome:
                finding[
                    "runtime_outcome"
                ] = outcome

            if confidence is not None:

                finding[
                    "runtime_confidence"
                ] = round(
                    float(confidence) * 100,
                    2
                )

            finding[
                "runtime_validated"
            ] = True

        workspace.findings(
            findings
        )

        # ==================================================
        # EXECUTIVE SUMMARY
        # ==================================================

        summary_engine = (
            ExecutiveSummaryEngine()
        )

        summary = summary_engine.build(

            profile=profile,

            routes=routes,

            workflows=workflows,

            hypotheses=hypotheses,

            evidence=evidence,

            attack_plans=serialized_attack_plans,

            risk=risk
        )

        workspace.executive_summary(
            summary
        )

        # ==================================================
        # TIMELINE
        # ==================================================

        timeline_engine = (
            TimelineEngine()
        )

        timeline = timeline_engine.build(

            profile=profile,

            routes=routes,

            workflows=workflows,

            hypotheses=hypotheses,

            evidence=evidence,

            attack_plans=serialized_attack_plans,

            findings=findings
        )

        workspace.timeline(
            timeline
        )

        # ==================================================
        # BUILD FINAL INVESTIGATION WORKSPACE
        # ==================================================

        investigation = workspace.build()

        # ==================================================
        # REPORT GENERATION
        # ==================================================

        report = ReportGenerator(
            investigation
        ).generate()

        # ==================================================
        # WORKSPACE REPORT
        # ==================================================

        report_builder = ReportBuilder()

        workspace_report = (
            report_builder.build(
                investigation
            )
        )

        # ==================================================
        # JSON EXPORT
        # ==================================================

        json_report = JsonExporter(
            report
        ).export()

        # ==================================================
        # FINAL RESULT
        # ==================================================

        return {

            "workspace": investigation,

            "workspace_report": workspace_report,

            "report": report,

            "json_report": json_report,

            "project": profile,

            "routes": len(routes),

            "workflows": len(workflows),

            "hypotheses": len(hypotheses),

            "brain": brain_result,

            "runtime": runtime_results,

            "evidence": evidence,

            "findings": findings,

        }

    # ======================================================
    # ATTACK PLAN RESTORATION
    # ======================================================

    def _restore_attack_plans(
        self,
        serialized_plans
    ):

        plans = []

        for plan_data in (
            serialized_plans or []
        ):

            if isinstance(
                plan_data,
                AttackExecutionPlan
            ):

                plans.append(
                    plan_data
                )

                continue

            if not isinstance(
                plan_data,
                dict
            ):
                continue

            steps = []

            for step_data in plan_data.get(
                "attack_steps",
                []
            ):

                if isinstance(
                    step_data,
                    AttackStep
                ):

                    steps.append(
                        step_data
                    )

                    continue

                if not isinstance(
                    step_data,
                    dict
                ):
                    continue

                steps.append(

                    AttackStep(

                        id=step_data.get(
                            "id",
                            ""
                        ),

                        step_number=step_data.get(
                            "step_number",
                            0
                        ),

                        action=step_data.get(
                            "action",
                            ""
                        ),

                        request_template=step_data.get(
                            "request_template",
                            {}
                        ),

                        expected_result=step_data.get(
                            "expected_result",
                            ""
                        )

                    )

                )

            plans.append(

                AttackExecutionPlan(

                    id=plan_data.get(
                        "id",
                        ""
                    ),

                    strategy_name=plan_data.get(
                        "strategy_name",
                        ""
                    ),

                    objective=plan_data.get(
                        "objective",
                        ""
                    ),

                    priority=plan_data.get(
                        "priority",
                        0
                    ),

                    attack_steps=steps

                )

            )

        return plans