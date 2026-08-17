from .request_executor import RequestExecutor
from .response_analyzer import ResponseAnalyzer
from .session_manager import SessionManager


class RuntimeEngine:
    """
    Executes investigation plans.

    It never exploits vulnerabilities.
    It only executes safe validation requests.
    """

    def __init__(self):

        self.session = SessionManager()
        self.executor = RequestExecutor()
        self.analyzer = ResponseAnalyzer()

    # --------------------------------------------------

    def execute(self, attack_plans):

        runtime_results = []

        session = self.session.get_session()

        for plan in attack_plans:

            plan_result = {

                "strategy": plan.strategy_name,

                "objective": plan.objective,

                "steps": []

            }

            for step in plan.attack_steps:

                response = self.executor.execute(

                    session=session,

                    request_template=step.request_template

                )

                analysis = self.analyzer.analyze(

                    response,

                    step

                )

                plan_result["steps"].append({

                    "step_number": analysis.step_number,

                    "action": analysis.action,

                    "status": analysis.response_status,

                    "success": analysis.success,

                    "observations": analysis.observations

                })

            runtime_results.append(plan_result)

        return runtime_results