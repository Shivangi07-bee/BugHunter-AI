function WorkflowPanel({ workflows }) {
    if (!Array.isArray(workflows) || workflows.length === 0) {
        return (
            <div className="cyber-card">
                <h2 className="section-title">
                    Workflow Reconstruction
                </h2>

                <div className="empty-state">
                    No workflow reconstructed.
                </div>
            </div>
        );
    }

    return (
        <div className="cyber-card">

            <h2 className="section-title">
                Workflow Reconstruction
            </h2>

            {

                workflows.map((workflow, index) => (

                    <div
                        key={index}
                        className="workflow-card"
                    >

                        <div className="workflow-header">

                            <div>

                                <div className="workflow-title">

                                    {workflow.workflow_name ||
                                        `Workflow ${index + 1}`}

                                </div>

                                <div className="workflow-count">

                                    {workflow.endpoint_count || 0} Endpoints

                                </div>

                            </div>

                            <div className="workflow-badge">

                                ACTIVE

                            </div>

                        </div>

                        {

                            workflow.endpoints?.map((endpoint, i) => (

                                <div
                                    key={i}
                                    className="endpoint-card"
                                >

                                    <div className="endpoint-path">

                                        {endpoint.method}

                                        <span
                                            style={{
                                                color: "#00e5ff",
                                                marginLeft: 12
                                            }}
                                        >
                                            {endpoint.path}
                                        </span>

                                    </div>

                                    <div className="endpoint-grid">

                                        <div>

                                            <span className="label">

                                                Handler

                                            </span>

                                            <p>

                                                {endpoint.handler}

                                            </p>

                                        </div>

                                        <div>

                                            <span className="label">

                                                Authentication

                                            </span>

                                            <p>

                                                {

                                                    endpoint.authentication

                                                        ? "Required"

                                                        : "Public"

                                                }

                                            </p>

                                        </div>

                                    </div>

                                    <div className="workflow-section">

                                        <span className="label">

                                            Models

                                        </span>

                                        <div className="chips">

                                            {

                                                endpoint.models?.length

                                                    ?

                                                    endpoint.models.map(

                                                        (m, index) => (

                                                            <span
                                                                key={index}
                                                                className="chip"
                                                            >
                                                                {m}
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

                                    <div className="workflow-section">

                                        <span className="label">

                                            Function Calls

                                        </span>

                                        <div className="chips">

                                            {

                                                endpoint.calls?.length

                                                    ?

                                                    endpoint.calls.map(

                                                        (call, index) => (

                                                            <span
                                                                key={index}
                                                                className="chip blue"
                                                            >
                                                                {call}
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

                                </div>

                            ))

                        }

                    </div>

                ))

            }

        </div>
    );
}

export default WorkflowPanel;