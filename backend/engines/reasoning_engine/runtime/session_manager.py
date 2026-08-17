from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict
from uuid import uuid4


@dataclass
class InvestigationSession:

    id: str = field(default_factory=lambda: str(uuid4()))

    project: str = ""

    started_at: datetime = field(default_factory=datetime.utcnow)

    last_updated: datetime = field(default_factory=datetime.utcnow)

    status: str = "RUNNING"

    completed_goals: int = 0

    evidence_count: int = 0

    observation_count: int = 0

    metadata: Dict = field(default_factory=dict)


class SessionManager:
    """
    Manages one BugHunter AI investigation session.
    """

    def __init__(self, project):

        self.session = InvestigationSession(
            project=project
        )

    # ------------------------------------------

    def touch(self):

        self.session.last_updated = datetime.utcnow()

    # ------------------------------------------

    def complete_goal(self):

        self.session.completed_goals += 1

        self.touch()

    # ------------------------------------------

    def add_evidence(self):

        self.session.evidence_count += 1

        self.touch()

    # ------------------------------------------

    def add_observation(self):

        self.session.observation_count += 1

        self.touch()

    # ------------------------------------------

    def update_metadata(self, key, value):

        self.session.metadata[key] = value

        self.touch()

    # ------------------------------------------

    def finish(self):

        self.session.status = "COMPLETED"

        self.touch()

    # ------------------------------------------

    def summary(self):

        return {

            "Session": self.session.id,

            "Project": self.session.project,

            "Status": self.session.status,

            "Goals": self.session.completed_goals,

            "Evidence": self.session.evidence_count,

            "Observations": self.session.observation_count,

            "Started": self.session.started_at,

            "Updated": self.session.last_updated

        }