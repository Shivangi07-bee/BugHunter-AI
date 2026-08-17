from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import uuid4


@dataclass
class RuntimeContext:

    session_id: str = field(default_factory=lambda: str(uuid4()))

    repository: str = ""

    workflow: str = ""

    current_endpoint: str = ""

    current_goal: str = ""

    authentication_state: str = "UNKNOWN"

    current_strategy: str = ""

    current_action: str = ""

    discovered_endpoints: List[str] = field(default_factory=list)

    observations: List[str] = field(default_factory=list)

    evidence: List[Dict] = field(default_factory=list)

    visited_endpoints: List[str] = field(default_factory=list)

    attack_history: List[str] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    started_at: datetime = field(default_factory=datetime.utcnow)


class RuntimeContextManager:

    """
    Live investigation context.

    Represents everything BugHunter AI currently
    knows during an investigation.
    """

    def __init__(self):

        self.context = RuntimeContext()

    # -----------------------------------------------------

    def load_repository(self, repository):

        self.context.repository = repository

    # -----------------------------------------------------

    def set_workflow(self, workflow):

        self.context.workflow = workflow

    # -----------------------------------------------------

    def set_goal(self, goal):

        self.context.current_goal = goal

    # -----------------------------------------------------

    def set_strategy(self, strategy):

        self.context.current_strategy = strategy

    # -----------------------------------------------------

    def set_endpoint(self, endpoint):

        self.context.current_endpoint = endpoint

        if endpoint not in self.context.visited_endpoints:

            self.context.visited_endpoints.append(endpoint)

    # -----------------------------------------------------

    def set_authentication_state(self, state):

        self.context.authentication_state = state

    # -----------------------------------------------------

    def discover_endpoint(self, endpoint):

        if endpoint not in self.context.discovered_endpoints:

            self.context.discovered_endpoints.append(endpoint)

    # -----------------------------------------------------

    def add_observation(self, observation):

        self.context.observations.append(observation)

    # -----------------------------------------------------

    def add_evidence(self, evidence):

        self.context.evidence.append(evidence)

    # -----------------------------------------------------

    def add_attack(self, attack):

        self.context.attack_history.append(attack)

    # -----------------------------------------------------

    def update_metadata(self, key, value):

        self.context.metadata[key] = value

    # -----------------------------------------------------

    def snapshot(self):

        return {

            "repository": self.context.repository,

            "workflow": self.context.workflow,

            "goal": self.context.current_goal,

            "endpoint": self.context.current_endpoint,

            "authentication": self.context.authentication_state,

            "strategy": self.context.current_strategy,

            "visited": len(self.context.visited_endpoints),

            "discovered": len(self.context.discovered_endpoints),

            "evidence": len(self.context.evidence),

            "observations": len(self.context.observations),

            "attacks": len(self.context.attack_history)

        }