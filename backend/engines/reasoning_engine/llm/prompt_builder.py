from typing import Dict, List


class PromptBuilder:
    """
    Builds structured prompts for the AI Reasoning Engine.

    The LLM should never receive raw repositories.

    It receives:

        • Workflow
        • Attack Strategy
        • Attack Plan
        • Reflection
        • Evidence

    This dramatically improves reasoning quality.
    """

    def __init__(self, brain_output: Dict):

        self.output = brain_output

    # ---------------------------------------------------------

    def build(self):

        prompt = []

        prompt.append(
            "You are BugHunter AI, an expert Application Security Engineer."
        )

        prompt.append(
            "Analyze the following investigation."
        )

        prompt.append("")

        # -------------------------------------------------
        # Strategies
        # -------------------------------------------------

        prompt.append("=== Strategies ===")

        for strategy in self.output["strategies"]:

            prompt.append(

                f"""
Strategy:

Name: {strategy.name}

Objective:

{strategy.objective}

Reasoning:

{chr(10).join('- '+r for r in strategy.reasoning)}

"""
            )

        # -------------------------------------------------
        # Investigation Tasks
        # -------------------------------------------------

        prompt.append("")

        prompt.append("=== Investigation Tasks ===")

        for task in self.output["tasks"]:

            prompt.append(

                f"""

Priority: {task.priority}

Action:

{task.next_action}

"""
            )

        # -------------------------------------------------
        # Attack Plans
        # -------------------------------------------------

        prompt.append("")

        prompt.append("=== Attack Plans ===")

        for plan in self.output["plans"]:

            prompt.append(

                f"""

Strategy:

{plan.strategy_name}

Objective:

{plan.objective}

"""

            )

            for step in plan.attack_steps:

                prompt.append(

                    f"""

Step {step.step_number}

Action:

{step.action}

Expected:

{step.expected_result}

"""

                )

        # -------------------------------------------------
        # Reflection
        # -------------------------------------------------

        prompt.append("")

        prompt.append("=== Reflection ===")

        for reflection in self.output["reflections"]:

            prompt.append(

                f"""

Strategy:

{reflection.strategy}

Decision:

{reflection.decision}

Confidence Before:

{reflection.confidence_before}

Confidence After:

{reflection.confidence_after}

Outcome:

{reflection.outcome}

"""

            )

        # -------------------------------------------------

        prompt.append("""

================================================

Your Tasks

1. Explain the business workflow.

2. Explain possible attack paths.

3. Determine whether the evidence supports a vulnerability.

4. Explain why.

5. Assign confidence.

6. Recommend further investigation.

Return your answer in professional penetration testing style.

""")

        return "\n".join(prompt)