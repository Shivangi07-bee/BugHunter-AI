function AttackPlanPanel({ attackPlans }) {
  if (!attackPlans || attackPlans.length === 0) {
    return (
      <div className="cyber-card">
        <h2 className="section-title">AI Attack Plans</h2>

        <div className="empty-state">
          No attack plans generated.
        </div>
      </div>
    );
  }

  const getValue = (plan, keys, fallback = "Not available") => {
    for (const key of keys) {
      if (
        plan?.[key] !== undefined &&
        plan?.[key] !== null &&
        plan?.[key] !== ""
      ) {
        return plan[key];
      }
    }

    return fallback;
  };

  const formatStep = (step) => {
    if (!step || typeof step !== "object") {
      return {
        action: String(step),
        workflow: "",
        expected: "",
      };
    }

    return {
      action:
        step.action ||
        step.description ||
        step.operation ||
        "Investigate workflow",

      workflow:
        step.workflow ||
        step.target ||
        step.endpoint ||
        "",

      expected:
        step.expected_result ||
        step.expected ||
        step.outcome ||
        "",
    };
  };

  return (
    <div className="cyber-card attack-plan-card">

      <h2 className="section-title">
        AI Attack Plans
      </h2>

      <div className="attack-plan-grid">

        {attackPlans.map((plan, index) => {

          const strategy = getValue(
            plan,
            ["strategy", "name", "title", "type"],
            `Investigation Strategy ${index + 1}`
          );

          const risk = getValue(
            plan,
            ["risk", "risk_score", "score", "priority"],
            "N/A"
          );

          const confidence = getValue(
            plan,
            [
              "confidence",
              "confidence_score",
              "probability"
            ],
            "N/A"
          );

          const objective = getValue(
            plan,
            [
              "objective",
              "goal",
              "description",
              "reason"
            ],
            "Collect additional evidence."
          );

          const target = getValue(
            plan,
            [
              "target",
              "endpoint",
              "route",
              "target_endpoint"
            ],
            "Application workflow"
          );

          const steps = Array.isArray(plan?.steps)
            ? plan.steps
            : Array.isArray(plan?.attack_steps)
            ? plan.attack_steps
            : Array.isArray(plan?.actions)
            ? plan.actions
            : [];

          const rationale = getValue(
            plan,
            [
              "rationale",
              "reasoning",
              "explanation",
              "why"
            ],
            "Generated from the current application model."
          );

          const decision = getValue(
            plan,
            [
              "decision",
              "action",
              "next_action"
            ],
            "INVESTIGATE"
          );

          return (
            <div
              className="attack-plan"
              key={plan?.id || index}
            >

              {/* HEADER */}
              <div className="attack-plan-header">

                <div>
                  <span className="attack-plan-number">
                    PLAN {index + 1}
                  </span>

                  <h3>
                    {strategy}
                  </h3>
                </div>

                <div className="attack-risk">
                  {risk}
                </div>

              </div>


              {/* TARGET */}
              <div className="attack-section">

                <span className="attack-label">
                  TARGET
                </span>

                <div className="attack-value">
                  {target}
                </div>

              </div>


              {/* OBJECTIVE */}
              <div className="attack-section">

                <span className="attack-label">
                  OBJECTIVE
                </span>

                <div className="attack-value">
                  {objective}
                </div>

              </div>


              {/* METRICS */}
              <div className="attack-metrics">

                <div className="attack-metric">
                  <span>Risk</span>

                  <strong>
                    {risk}
                  </strong>
                </div>


                <div className="attack-metric">
                  <span>Confidence</span>

                  <strong>
                    {confidence}
                  </strong>
                </div>


                <div className="attack-metric">
                  <span>Decision</span>

                  <strong>
                    {decision}
                  </strong>
                </div>

              </div>


              {/* ATTACK SEQUENCE */}
              <div className="attack-section">

                <span className="attack-label">
                  ATTACK SEQUENCE
                </span>

                {steps.length > 0 ? (

                  <div className="attack-steps">

                    {steps.map((step, stepIndex) => {

                      const formatted =
                        formatStep(step);

                      return (
                        <div
                          className="attack-step-card"
                          key={
                            step?.id ||
                            stepIndex
                          }
                        >

                          <div className="step-number">
                            {stepIndex + 1}
                          </div>

                          <div className="step-content">

                            <div className="step-action">
                              {formatted.action}
                            </div>

                            {formatted.workflow && (
                              <div className="step-detail">

                                <span>
                                  WORKFLOW
                                </span>

                                {formatted.workflow}

                              </div>
                            )}

                            {formatted.expected && (
                              <div className="step-detail">

                                <span>
                                  EXPECTED RESULT
                                </span>

                                {formatted.expected}

                              </div>
                            )}

                          </div>

                        </div>
                      );
                    })}

                  </div>

                ) : (

                  <div className="attack-value">
                    No explicit attack sequence provided.
                  </div>

                )}

              </div>


              {/* REASONING */}
              <div className="attack-section">

                <span className="attack-label">
                  REASONING
                </span>

                <div className="attack-reasoning">
                  {rationale}
                </div>

              </div>

            </div>
          );
        })}

      </div>
    </div>
  );
}

export default AttackPlanPanel;