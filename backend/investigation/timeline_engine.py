from dataclasses import dataclass


@dataclass
class TimelineEvent:

    stage: str

    title: str

    description: str

    status: str


class TimelineEngine:

    def build(
        self,
        profile,
        routes,
        workflows,
        hypotheses,
        evidence,
        attack_plans,
        findings
    ):

        timeline = []

        timeline.append(
            TimelineEvent(
                stage="Repository",
                title="Repository Loaded",
                description=f"Loaded {profile.get('project_name', 'Unknown')} project.",
                status="completed"
            ).__dict__
        )

        timeline.append(
            TimelineEvent(
                stage="Routes",
                title="Routes Discovered",
                description=f"{len(routes)} routes identified.",
                status="completed"
            ).__dict__
        )

        timeline.append(
            TimelineEvent(
                stage="Workflow",
                title="Workflow Reconstructed",
                description=f"{len(workflows)} workflows reconstructed.",
                status="completed"
            ).__dict__
        )

        timeline.append(
            TimelineEvent(
                stage="Reasoning",
                title="Hypotheses Generated",
                description=f"{len(hypotheses)} attack hypotheses generated.",
                status="completed"
            ).__dict__
        )

        timeline.append(
            TimelineEvent(
                stage="Evidence",
                title="Evidence Collected",
                description=f"{len(evidence)} evidence objects collected.",
                status="completed"
            ).__dict__
        )

        timeline.append(
            TimelineEvent(
                stage="Attack Planning",
                title="Attack Plans Created",
                description=f"{len(attack_plans)} attack plans prepared.",
                status="completed"
            ).__dict__
        )

        timeline.append(
            TimelineEvent(
                stage="Findings",
                title="Investigation Completed",
                description=f"{len(findings)} findings produced.",
                status="completed"
            ).__dict__
        )

        return timeline