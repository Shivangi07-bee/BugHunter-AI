import { useMemo, useState } from "react";

function KnowledgeGraph({ graph }) {
    const nodes = graph?.nodes || [];
    const edges = graph?.edges || [];

    const [selectedNode, setSelectedNode] = useState(null);

    const nodeMap = useMemo(() => {
        const map = new Map();

        nodes.forEach((node) => {
            map.set(node.id, node);
        });

        edges.forEach((edge) => {
            if (!map.has(edge.source)) {
                map.set(edge.source, {
                    id: edge.source,
                    label: edge.source,
                    type: "endpoint"
                });
            }

            if (!map.has(edge.target)) {
                map.set(edge.target, {
                    id: edge.target,
                    label: edge.target,
                    type: "model"
                });
            }
        });

        return Array.from(map.values());
    }, [nodes, edges]);

    const displayNodes = nodeMap.slice(0, 20);

    const nodePositions = useMemo(() => {
        const positions = {};

        const centerX = 50;
        const centerY = 50;

        displayNodes.forEach((node, index) => {
            if (index === 0) {
                positions[node.id] = {
                    x: centerX,
                    y: centerY
                };
                return;
            }

            const angle =
                ((index - 1) / Math.max(displayNodes.length - 1, 1)) *
                Math.PI *
                2;

            const radius = index % 2 === 0 ? 31 : 23;

            positions[node.id] = {
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius
            };
        });

        return positions;
    }, [displayNodes]);

    const getNodeType = (node) => {
        const type = String(node?.type || "").toLowerCase();

        if (type.includes("endpoint")) return "endpoint";
        if (type.includes("model")) return "model";
        if (type.includes("workflow")) return "workflow";

        return "component";
    };

    const getNodeColor = (node) => {
        const type = getNodeType(node);

        if (type === "endpoint") return "#16d9ff";
        if (type === "model") return "#8b7cff";
        if (type === "workflow") return "#20e39a";

        return "#f5b942";
    };

    const getConnectedEdges = (nodeId) => {
        return edges.filter(
            (edge) =>
                edge.source === nodeId ||
                edge.target === nodeId
        );
    };

    if (edges.length === 0 && nodes.length === 0) {
        return (
            <section className="kg-card">
                <div className="kg-header">
                    <div>
                        <span className="kg-eyebrow">
                            APPLICATION KNOWLEDGE
                        </span>

                        <h2>Knowledge Graph</h2>

                        <p>
                            No application relationships have been reconstructed yet.
                        </p>
                    </div>

                    <span className="kg-status kg-status-empty">
                        EMPTY
                    </span>
                </div>
            </section>
        );
    }

    return (
        <section className="kg-card">
            <div className="kg-header">
                <div>
                    <span className="kg-eyebrow">
                        APPLICATION KNOWLEDGE
                    </span>

                    <h2>Knowledge Graph</h2>

                    <p>
                        Relationships reconstructed from the application's
                        endpoints, models and workflow logic.
                    </p>
                </div>

                <div className="kg-summary">
                    <div>
                        <strong>{displayNodes.length}</strong>
                        <span>Nodes</span>
                    </div>

                    <div>
                        <strong>{edges.length}</strong>
                        <span>Relations</span>
                    </div>
                </div>
            </div>

            <div className="kg-workspace">
                <div className="kg-graph">
                    <div className="kg-grid" />

                    <svg
                        className="kg-lines"
                        viewBox="0 0 100 100"
                        preserveAspectRatio="none"
                    >
                        {edges.map((edge, index) => {
                            const source =
                                nodePositions[edge.source];

                            const target =
                                nodePositions[edge.target];

                            if (!source || !target) return null;

                            return (
                                <line
                                    key={`${edge.source}-${edge.target}-${index}`}
                                    x1={source.x}
                                    y1={source.y}
                                    x2={target.x}
                                    y2={target.y}
                                    stroke="rgba(35, 211, 255, 0.34)"
                                    strokeWidth="0.35"
                                    vectorEffect="non-scaling-stroke"
                                />
                            );
                        })}
                    </svg>

                    {displayNodes.map((node) => {
                        const position =
                            nodePositions[node.id];

                        const color =
                            getNodeColor(node);

                        const type =
                            getNodeType(node);

                        const selected =
                            selectedNode?.id === node.id;

                        return (
                            <button
                                key={node.id}
                                className={`kg-node ${
                                    selected ? "selected" : ""
                                }`}
                                style={{
                                    left: `${position.x}%`,
                                    top: `${position.y}%`,
                                    "--node-color": color
                                }}
                                onClick={() =>
                                    setSelectedNode(node)
                                }
                            >
                                <span
                                    className="kg-node-dot"
                                    style={{
                                        background: color,
                                        boxShadow: `0 0 18px ${color}`
                                    }}
                                />

                                <span className="kg-node-label">
                                    {node.label || node.id}
                                </span>

                                <span className="kg-node-type">
                                    {type}
                                </span>
                            </button>
                        );
                    })}

                    <div className="kg-center-label">
                        <span>APPLICATION</span>
                        <strong>RELATIONSHIP MODEL</strong>
                    </div>
                </div>

                <aside className="kg-inspector">
                    {selectedNode ? (
                        <>
                            <span className="kg-inspector-eyebrow">
                                SELECTED NODE
                            </span>

                            <h3>
                                {selectedNode.label ||
                                    selectedNode.id}
                            </h3>

                            <div className="kg-property">
                                <span>Type</span>
                                <strong>
                                    {getNodeType(selectedNode)}
                                </strong>
                            </div>

                            <div className="kg-property">
                                <span>Identifier</span>
                                <strong>
                                    {selectedNode.id}
                                </strong>
                            </div>

                            <div className="kg-property">
                                <span>Relationships</span>
                                <strong>
                                    {
                                        getConnectedEdges(
                                            selectedNode.id
                                        ).length
                                    }
                                </strong>
                            </div>

                            <div className="kg-related">
                                <span>CONNECTED THROUGH</span>

                                {getConnectedEdges(
                                    selectedNode.id
                                ).map((edge, index) => (
                                    <div
                                        className="kg-relation"
                                        key={index}
                                    >
                                        <span>
                                            {edge.source}
                                        </span>

                                        <b>
                                            {edge.relationship ||
                                                edge.reason ||
                                                "RELATED"}
                                        </b>

                                        <span>
                                            {edge.target}
                                        </span>
                                    </div>
                                ))}
                            </div>

                            <button
                                className="kg-clear"
                                onClick={() =>
                                    setSelectedNode(null)
                                }
                            >
                                Clear Selection
                            </button>
                        </>
                    ) : (
                        <div className="kg-empty-inspector">
                            <span className="kg-inspector-icon">
                                ◈
                            </span>

                            <h3>Relationship Inspector</h3>

                            <p>
                                Select a node to inspect its role
                                and relationships inside the
                                application model.
                            </p>
                        </div>
                    )}
                </aside>
            </div>

            <div className="kg-legend">
                <div>
                    <span
                        className="legend-dot"
                        style={{
                            background: "#16d9ff"
                        }}
                    />
                    Endpoint
                </div>

                <div>
                    <span
                        className="legend-dot"
                        style={{
                            background: "#8b7cff"
                        }}
                    />
                    Model
                </div>

                <div>
                    <span
                        className="legend-dot"
                        style={{
                            background: "#20e39a"
                        }}
                    />
                    Workflow
                </div>

                <div>
                    <span
                        className="legend-dot"
                        style={{
                            background: "#f5b942"
                        }}
                    />
                    Component
                </div>
            </div>

            <style>{`
                .kg-card {
                    width: 100%;
                    box-sizing: border-box;
                    margin-top: 25px;
                    padding: 28px;
                    border: 1px solid rgba(35, 211, 255, 0.16);
                    border-radius: 18px;
                    background:
                        linear-gradient(
                            145deg,
                            rgba(17, 29, 47, 0.98),
                            rgba(7, 15, 27, 0.98)
                        );
                    box-shadow:
                        0 20px 60px rgba(0, 0, 0, 0.25),
                        inset 0 1px rgba(255, 255, 255, 0.025);
                    color: #edf7ff;
                }

                .kg-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    gap: 24px;
                    margin-bottom: 24px;
                }

                .kg-eyebrow,
                .kg-inspector-eyebrow {
                    display: block;
                    margin-bottom: 8px;
                    color: #19d7ff;
                    font-size: 10px;
                    font-weight: 800;
                    letter-spacing: 0.18em;
                }

                .kg-header h2 {
                    margin: 0;
                    font-size: 26px;
                    letter-spacing: -0.02em;
                }

                .kg-header p {
                    max-width: 650px;
                    margin: 8px 0 0;
                    color: #7892ad;
                    font-size: 14px;
                    line-height: 1.6;
                }

                .kg-summary {
                    display: flex;
                    gap: 10px;
                }

                .kg-summary div {
                    min-width: 80px;
                    padding: 12px 16px;
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 12px;
                    background: rgba(255,255,255,0.025);
                    text-align: center;
                }

                .kg-summary strong {
                    display: block;
                    color: #19d7ff;
                    font-size: 20px;
                }

                .kg-summary span {
                    color: #6f879f;
                    font-size: 10px;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                }

                .kg-workspace {
                    display: grid;
                    grid-template-columns: minmax(0, 1fr) 280px;
                    min-height: 560px;
                    overflow: hidden;
                    border: 1px solid rgba(255,255,255,0.07);
                    border-radius: 15px;
                    background: #08111e;
                }

                .kg-graph {
                    position: relative;
                    min-height: 560px;
                    overflow: hidden;
                }

                .kg-grid {
                    position: absolute;
                    inset: 0;
                    background-image:
                        linear-gradient(
                            rgba(55, 121, 155, 0.08) 1px,
                            transparent 1px
                        ),
                        linear-gradient(
                            90deg,
                            rgba(55, 121, 155, 0.08) 1px,
                            transparent 1px
                        );
                    background-size: 38px 38px;
                    mask-image: radial-gradient(
                        circle,
                        black 25%,
                        transparent 85%
                    );
                }

                .kg-lines {
                    position: absolute;
                    inset: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                }

                .kg-node {
                    position: absolute;
                    transform: translate(-50%, -50%);
                    min-width: 115px;
                    padding: 10px 13px;
                    border: 1px solid rgba(255,255,255,0.10);
                    border-radius: 12px;
                    background: rgba(12, 25, 40, 0.96);
                    color: #eaf7ff;
                    cursor: pointer;
                    text-align: left;
                    transition:
                        transform 0.18s ease,
                        border-color 0.18s ease,
                        box-shadow 0.18s ease;
                    z-index: 3;
                }

                .kg-node:hover,
                .kg-node.selected {
                    transform: translate(-50%, -50%) scale(1.06);
                    border-color: var(--node-color);
                    box-shadow:
                        0 0 0 1px var(--node-color),
                        0 12px 30px rgba(0,0,0,0.35);
                }

                .kg-node-dot {
                    display: inline-block;
                    width: 7px;
                    height: 7px;
                    margin-right: 8px;
                    border-radius: 50%;
                }

                .kg-node-label {
                    font-size: 13px;
                    font-weight: 700;
                }

                .kg-node-type {
                    display: block;
                    margin-top: 5px;
                    margin-left: 15px;
                    color: #7089a2;
                    font-size: 9px;
                    text-transform: uppercase;
                    letter-spacing: 0.12em;
                }

                .kg-center-label {
                    position: absolute;
                    left: 50%;
                    top: 50%;
                    transform: translate(-50%, -50%);
                    width: 135px;
                    height: 135px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    border: 1px solid rgba(25,215,255,0.20);
                    border-radius: 50%;
                    background: radial-gradient(
                        circle,
                        rgba(17, 50, 70, 0.55),
                        rgba(7, 17, 29, 0.9)
                    );
                    box-shadow:
                        0 0 45px rgba(25,215,255,0.08);
                    z-index: 1;
                    pointer-events: none;
                }

                .kg-center-label span {
                    color: #5d7993;
                    font-size: 8px;
                    letter-spacing: 0.16em;
                }

                .kg-center-label strong {
                    margin-top: 6px;
                    color: #b9d9ea;
                    font-size: 10px;
                    text-align: center;
                    letter-spacing: 0.08em;
                }

                .kg-inspector {
                    padding: 22px;
                    border-left: 1px solid rgba(255,255,255,0.07);
                    background: rgba(12, 22, 36, 0.85);
                }

                .kg-inspector h3 {
                    margin: 0 0 20px;
                    font-size: 19px;
                    word-break: break-word;
                }

                .kg-property {
                    display: flex;
                    justify-content: space-between;
                    gap: 15px;
                    padding: 12px 0;
                    border-bottom: 1px solid rgba(255,255,255,0.06);
                }

                .kg-property span {
                    color: #6d849c;
                    font-size: 11px;
                }

                .kg-property strong {
                    max-width: 140px;
                    color: #d9edf8;
                    font-size: 11px;
                    text-align: right;
                    word-break: break-word;
                }

                .kg-related {
                    margin-top: 22px;
                }

                .kg-related > span {
                    color: #607990;
                    font-size: 9px;
                    letter-spacing: 0.14em;
                }

                .kg-relation {
                    margin-top: 8px;
                    padding: 9px;
                    border-radius: 8px;
                    background: rgba(255,255,255,0.035);
                    font-size: 9px;
                    line-height: 1.5;
                }

                .kg-relation b {
                    display: block;
                    margin: 3px 0;
                    color: #19d7ff;
                    font-size: 8px;
                    letter-spacing: 0.08em;
                }

                .kg-clear {
                    width: 100%;
                    margin-top: 20px;
                    padding: 10px;
                    border: 1px solid rgba(255,255,255,0.10);
                    border-radius: 8px;
                    background: transparent;
                    color: #9eb4c8;
                    cursor: pointer;
                }

                .kg-clear:hover {
                    border-color: #19d7ff;
                    color: #19d7ff;
                }

                .kg-empty-inspector {
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                }

                .kg-inspector-icon {
                    margin-bottom: 15px;
                    color: #19d7ff;
                    font-size: 25px;
                }

                .kg-empty-inspector h3 {
                    margin-bottom: 8px;
                }

                .kg-empty-inspector p {
                    color: #687f96;
                    font-size: 12px;
                    line-height: 1.6;
                }

                .kg-legend {
                    display: flex;
                    gap: 22px;
                    margin-top: 16px;
                    flex-wrap: wrap;
                }

                .kg-legend div {
                    display: flex;
                    align-items: center;
                    gap: 7px;
                    color: #7890a7;
                    font-size: 10px;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                }

                .legend-dot {
                    width: 7px;
                    height: 7px;
                    border-radius: 50%;
                    box-shadow: 0 0 8px currentColor;
                }

                .kg-status {
                    padding: 8px 12px;
                    border: 1px solid rgba(32,227,154,0.25);
                    border-radius: 8px;
                    color: #20e39a;
                    font-size: 9px;
                    font-weight: 800;
                    letter-spacing: 0.12em;
                }

                .kg-status-empty {
                    color: #7890a7;
                    border-color: rgba(255,255,255,0.1);
                }

                @media (max-width: 900px) {
                    .kg-workspace {
                        grid-template-columns: 1fr;
                    }

                    .kg-inspector {
                        min-height: 260px;
                        border-left: none;
                        border-top: 1px solid rgba(255,255,255,0.07);
                    }

                    .kg-header {
                        flex-direction: column;
                    }
                }
            `}</style>
        </section>
    );
}

export default KnowledgeGraph;