from .investigation_loop import InvestigationLoop


class AgentController:
    """
    Main controller of BugHunter AI.

    This is the entry point of the AI Agent.
    """

    def __init__(self, hypotheses):

        self.loop = InvestigationLoop(hypotheses)

    # --------------------------------------------------

    def start(self):

        print()

        print("="*70)
        print("BugHunter AI Agent Started")
        print("="*70)

        iteration = 1

        while True:

            result = self.loop.run_once()

            if result is None:

                break

            runtime = result["runtime"]

            print()

            print(f"Iteration : {iteration}")

            print(f"Goal      : {runtime['goal']}")

            print(f"Confidence: {runtime['confidence']}")

            print()

            iteration += 1

        print()

        print("="*70)

        print("Investigation Finished")

        print("="*70)