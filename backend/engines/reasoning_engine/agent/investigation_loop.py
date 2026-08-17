from ..brain.orchestrator import BugHunterBrain
from .goal_manager import GoalManager
from .runtime_state import RuntimeStateManager


class InvestigationLoop:
    """
    Controls the investigation lifecycle.

    Flow:

        Goal
          ↓
        Brain
          ↓
        Runtime State
          ↓
        Result
          ↓
        Next Goal

    The loop coordinates existing reasoning components.
    It does not perform vulnerability detection itself.
    """

    def __init__(self, hypotheses):

        self.goal_manager = GoalManager()
        self.goal_manager.create_default_goals()

        self.runtime = RuntimeStateManager()

        self.brain = BugHunterBrain()

        self.brain.load_hypotheses(
            hypotheses or []
        )

    # =========================================================
    # RUN ONE INVESTIGATION ITERATION
    # =========================================================

    def run_once(self):

        # -----------------------------------------------------
        # Get next investigation goal
        # -----------------------------------------------------

        goal = self.goal_manager.next_goal()

        if goal is None:

            self.runtime.finish()

            return {
                "status": "finished",
                "goal": None,
                "brain_output": None,
                "runtime": self.runtime.snapshot()
            }

        # -----------------------------------------------------
        # Register active goal
        # -----------------------------------------------------

        self.runtime.set_goal(
            goal.name
        )

        # -----------------------------------------------------
        # Execute reasoning
        # -----------------------------------------------------

        try:

            result = self.brain.run()

        except Exception as exc:

            return {
                "status": "error",
                "goal": goal,
                "brain_output": None,
                "error": str(exc),
                "runtime": self.runtime.snapshot()
            }

        # -----------------------------------------------------
        # Determine whether reasoning produced a result
        # -----------------------------------------------------

        successful = result is not None

        if isinstance(result, dict):

            successful = (
                result.get(
                    "success",
                    True
                )
                is not False
            )

        # -----------------------------------------------------
        # Complete goal only after successful reasoning
        # -----------------------------------------------------

        if successful:

            self.goal_manager.complete(
                goal.name
            )

            self.runtime.next_iteration()

            # -------------------------------------------------
            # Use actual confidence when available.
            # Never invent confidence improvement.
            # -------------------------------------------------

            confidence = self._extract_confidence(
                result
            )

            if confidence is not None:

                self.runtime.increase_confidence(
                    confidence
                )

        # -----------------------------------------------------
        # Return investigation state
        # -----------------------------------------------------

        return {

            "status": (
                "completed"
                if successful
                else "incomplete"
            ),

            "goal": goal,

            "brain_output": result,

            "runtime": self.runtime.snapshot()

        }

    # =========================================================
    # CONFIDENCE EXTRACTION
    # =========================================================

    def _extract_confidence(
        self,
        result
    ):

        if not isinstance(
            result,
            dict
        ):
            return None

        confidence = result.get(
            "confidence"
        )

        if confidence is None:
            return None

        try:

            value = float(
                confidence
            )

        except (
            TypeError,
            ValueError
        ):

            return None

        # Accept both:
        #
        # 0.0 - 1.0
        # 0   - 100
        #
        # Runtime currently works with
        # incremental confidence values.

        if value > 1:

            value = value / 100

        return max(
            0.0,
            min(
                value,
                1.0
            )
        )

    # =========================================================
    # FINISHED
    # =========================================================

    def finished(self):

        return self.runtime.state.finished