function HypothesisPanel({ hypotheses }) {

    if (!Array.isArray(hypotheses) || hypotheses.length === 0) {

        return (

            <div className="cyber-card">

                <h2 className="section-title">
                    AI Attack Hypotheses
                </h2>

                <div className="empty-state">
                    No hypotheses generated.
                </div>

            </div>

        );

    }

    return (

        <div className="cyber-card">

            <h2 className="section-title">
                AI Attack Hypotheses
            </h2>

            {

                hypotheses.map((h, index) => (

                    <div
                        key={index}
                        className="hypothesis-card"
                    >

                        <div className="hypothesis-header">

                            <div>

                                <div className="hypothesis-title">

                                    {h.title}

                                </div>

                                <div className="hypothesis-confidence">

                                    Confidence : {h.confidence}%

                                </div>

                            </div>

                            <div
                                className={`risk-badge ${String(h.risk).toLowerCase()}`}
                            >

                                {h.risk}

                            </div>

                        </div>

                        <div className="hypothesis-block">

                            <span className="label">

                                Description

                            </span>

                            <p>

                                {h.description}

                            </p>

                        </div>

                        <div className="hypothesis-block">

                            <span className="label">

                                AI Reasoning

                            </span>

                            <p>

                                {h.reasoning}

                            </p>

                        </div>

                        <div className="hypothesis-block">

                            <span className="label">

                                Evidence

                            </span>

                            <div className="chips">

                                {

                                    h.evidence?.length

                                        ?

                                        h.evidence.map(

                                            (item, i) => (

                                                <span
                                                    key={i}
                                                    className="chip"
                                                >

                                                    {item}

                                                </span>

                                            )

                                        )

                                        :

                                        <span className="chip">

                                            None

                                        </span>

                                }

                            </div>

                        </div>

                        <div className="hypothesis-block">

                            <span className="label">

                                Affected Endpoints

                            </span>

                            <div className="chips">

                                {

                                    h.affected_endpoints?.map(

                                        (ep, i) => (

                                            <span
                                                key={i}
                                                className="chip blue"
                                            >

                                                {ep}

                                            </span>

                                        )

                                    )

                                }

                            </div>

                        </div>

                    </div>

                ))

            }

        </div>

    );

}

export default HypothesisPanel;