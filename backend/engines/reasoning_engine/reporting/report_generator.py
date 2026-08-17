from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import uuid4


@dataclass
class SecurityFinding:

    title: str

    severity: str

    confidence: float

    reasoning: str

    recommendation: str


@dataclass
class InvestigationReport:

    id: str = field(default_factory=lambda: str(uuid4()))

    generated_at: datetime = field(default_factory=datetime.utcnow)

    project: str = ""

    workflow: str = ""

    summary: str = ""

    findings: List[SecurityFinding] = field(default_factory=list)


class ReportGenerator:

    """
    Generates the final investigation report.

    This report is generated after:

        Brain
            ↓
        Agent
            ↓
        Runtime
            ↓
        AI Reasoning
    """

    def __init__(

        self,

        runtime,

        reasoning

    ):

        self.runtime = runtime

        self.reasoning = reasoning

    # ---------------------------------------------------

    def generate(self):

        report = InvestigationReport()

        report.project = self.runtime.get(

            "repository",

            "Unknown"

        )

        report.workflow = self.runtime.get(

            "workflow",

            "Unknown"

        )

        report.summary = (

            "BugHunter AI completed the investigation."

        )

        report.findings.append(

            SecurityFinding(

                title="Authentication Investigation",

                severity="High",

                confidence=0.91,

                reasoning=self.reasoning.attack_analysis,

                recommendation=self.reasoning.recommendations

            )

        )

        return report