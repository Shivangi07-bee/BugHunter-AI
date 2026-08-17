import {
    ReactFlow,
    Background,
    Controls,
    MiniMap
} from "reactflow";

import "reactflow/dist/style.css";

import "../styles/graph.css";

function InvestigationGraph({ graph }) {
console.log(graph);
const nodes = (graph.nodes || []).map((node, index) => ({

    id: node.id,

    position: {

        x: 150 + (index % 2) * 450,

        y: 100 + Math.floor(index / 2) * 180

    },

    data: {

        label: node.label

    },

    className:
        node.type === "endpoint"
            ? "endpoint-node"
            : "model-node"

}));

const edges = (graph.edges || []).map((edge, index) => ({

    id: `edge-${index}`,

    source: edge.source,

    target: edge.target,

    label: edge.relationship,

    animated: true

}));

    return (

        <div className="graph-card">

            <h2 className="section-title">

                AI Knowledge Graph

            </h2>

            <div className="graph-wrapper">

                <ReactFlow

                    nodes={nodes}

                    edges={edges}

                    fitView

                >

                    <Background />

                    <Controls />

                    <MiniMap />

                </ReactFlow>

            </div>

        </div>

    );

}

export default InvestigationGraph;