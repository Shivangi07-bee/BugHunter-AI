from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List
from uuid import uuid4


@dataclass
class RuntimeState:

    session_id: str = field(default_factory=lambda: str(uuid4()))

    current_goal: str = ""

    current_strategy: str = ""

    current_action: str = ""

    completed_actions: List[str] = field(default_factory=list)

    pending_actions: List[str] = field(default_factory=list)

    observations: List[str] = field(default_factory=list)

    evidence: List[Dict] = field(default_factory=list)

    confidence: float = 0.0

    iteration: int = 0

    started_at: datetime = field(default_factory=datetime.utcnow)

    finished: bool = False


class RuntimeStateManager:
    """
    Maintains the current investigation state.
    """

    def __init__(self):

        self.state = RuntimeState()

    # --------------------------------------------------

    def set_goal(self, goal):

        self.state.current_goal = goal

    # --------------------------------------------------

    def set_strategy(self, strategy):

        self.state.current_strategy = strategy

    # --------------------------------------------------

    def set_action(self, action):

        self.state.current_action = action

    # --------------------------------------------------

    def add_pending_action(self, action):

        self.state.pending_actions.append(action)

    # --------------------------------------------------

    def complete_action(self, action):

        if action in self.state.pending_actions:

            self.state.pending_actions.remove(action)

        self.state.completed_actions.append(action)

    # --------------------------------------------------

    def add_observation(self, observation):

        self.state.observations.append(observation)

    # --------------------------------------------------

    def add_evidence(self, evidence):

        self.state.evidence.append(evidence)

    # --------------------------------------------------

    def increase_confidence(self, value):

        self.state.confidence = min(
            1.0,
            self.state.confidence + value
        )

    # --------------------------------------------------

    def next_iteration(self):

        self.state.iteration += 1

    # --------------------------------------------------

    def finish(self):

        self.state.finished = True

    # --------------------------------------------------

    def snapshot(self):

        return {

            "goal": self.state.current_goal,

            "strategy": self.state.current_strategy,

            "action": self.state.current_action,

            "iteration": self.state.iteration,

            "confidence": self.state.confidence,

            "completed_actions": len(self.state.completed_actions),

            "pending_actions": len(self.state.pending_actions),

            "observations": len(self.state.observations),

            "evidence": len(self.state.evidence),

            "finished": self.state.finished

        }