function StatsCard({ risk }) {
    const rawScore =
        risk?.score ??
        risk?.risk_score ??
        risk?.overall_score ??
        0;

    const score = Math.max(
        0,
        Math.min(100, Number(rawScore) || 0)
    );

    let level =
        risk?.level ??
        risk?.severity ??
        risk?.overall_risk;

    if (!level || level === "Unknown") {
        if (score >= 80) level = "Critical";
        else if (score >= 60) level = "High";
        else if (score >= 40) level = "Medium";
        else if (score > 0) level = "Low";
        else level = "No Risk";
    }

    const normalizedLevel = String(level).toLowerCase();

    let severityClass = "risk-safe";

    if (normalizedLevel === "critical") {
        severityClass = "risk-critical";
    } else if (normalizedLevel === "high") {
        severityClass = "risk-high";
    } else if (normalizedLevel === "medium") {
        severityClass = "risk-medium";
    } else if (normalizedLevel === "low") {
        severityClass = "risk-low";
    }

    return (
        <section className={`risk-card ${severityClass}`}>

            <div className="risk-header">

                <div className="risk-title-block">
                    <span className="risk-eyebrow">
                        SECURITY POSTURE
                    </span>

                    <h2>Risk Assessment</h2>
                </div>

                <div className="risk-status">
                    <span className="risk-status-dot"></span>
                    {level}
                </div>

            </div>

            <div className="risk-content">

                <div className="risk-box">

                    <span className="risk-label">
                        OVERALL RISK
                    </span>

                    <h1 className="risk-level">
                        {level}
                    </h1>

                    <span className="risk-description">
                        Derived from application reasoning
                    </span>

                </div>

                <div className="risk-divider"></div>

                <div className="risk-box">

                    <span className="risk-label">
                        RISK SCORE
                    </span>

                    <div className="risk-score">
                        <strong>{score}</strong>
                        <span>/100</span>
                    </div>

                    <div className="risk-progress">
                        <div
                            className="risk-progress-fill"
                            style={{
                                width: `${score}%`
                            }}
                        />
                    </div>

                </div>

            </div>

        </section>
    );
}

export default StatsCard;