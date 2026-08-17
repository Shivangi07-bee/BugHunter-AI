function EvidencePanel({ evidence }) {

    return (

        <div
            style={{
                background: "#242424",
                padding: 20,
                borderRadius: 10,
                marginTop: 25
            }}
        >

            <h2>Evidence Collected</h2>

            {

                !evidence || evidence.length === 0 ? (

                    <p>No evidence collected.</p>

                ) : (

                    evidence.map((item, index) => (

                        <div
                            key={index}
                            style={{
                                background: "#2f2f2f",
                                padding: 18,
                                marginBottom: 15,
                                borderRadius: 10,
                                borderLeft: "5px solid #4CAF50"
                            }}
                        >

                            <h3
                                style={{
                                    color: "#81C784",
                                    marginBottom: 12
                                }}
                            >
                                Evidence {index + 1}
                            </h3>

                            <div style={{ marginBottom: 8 }}>
                                <strong>Type</strong>
                                <div>
                                    {item.type || "Unknown"}
                                </div>
                            </div>

                            <div style={{ marginBottom: 8 }}>
                                <strong>Location</strong>
                                <div>
                                    {item.location || "Unknown"}
                                </div>
                            </div>

                            <div style={{ marginBottom: 8 }}>
                                <strong>Description</strong>
                                <div>
                                    {item.description || "No description available."}
                                </div>
                            </div>

                            <div style={{ marginBottom: 8 }}>
                                <strong>Severity</strong>
                                <div>
                                    {item.severity || "Unknown"}
                                </div>
                            </div>

                            <div style={{ marginBottom: 8 }}>
                                <strong>Confidence</strong>
                                <div>
                                    {item.confidence ?? "N/A"}
                                </div>
                            </div>

                            <div style={{ marginBottom: 8 }}>
                                <strong>Related Endpoint</strong>
                                <div>
                                    {item.endpoint || "None"}
                                </div>
                            </div>

                        </div>

                    ))

                )

            }

        </div>

    );

}

export default EvidencePanel;