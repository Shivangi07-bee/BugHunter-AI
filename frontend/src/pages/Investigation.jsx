import React, { useMemo, useState } from "react";

import Navbar from "../components/Navbar";
import KnowledgeGraph from "../components/KnowledgeGraph";
import "../styles/dashboard.css";


function Investigation() {

    // ============================================================
    // LOAD INVESTIGATION
    // ============================================================

    const stored = localStorage.getItem("investigation");

    let result = null;

    try {
        result = stored ? JSON.parse(stored) : null;
    } catch (error) {
        console.error("Failed to parse investigation:", error);
        result = null;
    }


    if (!result || !result.workspace) {
        return (
            <div className="app-layout">


                <div className="main-content">

                    <Navbar />

                    <div className="page">

                        <div className="cyber-card">

                            <h2 className="section-title">
                                Investigation Not Available
                            </h2>

                            <p>
                                Run a repository analysis first.
                            </p>

                        </div>

                    </div>

                </div>

            </div>
        );
    }


    const workspace = result.workspace || {};


    // ============================================================
    // NORMALIZE DATA
    // ============================================================

    const safeArray = (value) => {

        if (Array.isArray(value)) {
            return value;
        }

        return [];
    };


    const safeObject = (value) => {

        if (
            value &&
            typeof value === "object" &&
            !Array.isArray(value)
        ) {
            return value;
        }

        return {};
    };


    // ============================================================
    // REPOSITORY
    // ============================================================

    const repo =
        workspace.repository ||
        workspace.project ||
        result.project ||
        {};


    // ============================================================
    // WORKFLOW NORMALIZATION
    //
    // IMPORTANT:
    // Backend currently calls:
    //
    //     workspace.workflow(context)
    //
    // NOT:
    //
    //     workspace.workflows(workflows)
    //
    // Therefore we support BOTH forms.
    // ============================================================

    const workflowSource =
        workspace.workflows ??
        workspace.workflow ??
        result.workflows_data ??
        [];


    let workflows = [];


    if (Array.isArray(workflowSource)) {

        workflows = workflowSource;

    } else if (
        workflowSource &&
        typeof workflowSource === "object"
    ) {

        // Possible context shapes

        if (Array.isArray(workflowSource.workflows)) {

            workflows = workflowSource.workflows;

        } else if (
            Array.isArray(workflowSource.items)
        ) {

            workflows = workflowSource.items;

        } else if (
            Array.isArray(workflowSource.context)
        ) {

            workflows = workflowSource.context;

        } else if (
            Array.isArray(workflowSource.data)
        ) {

            workflows = workflowSource.data;

        } else {

            // Single workflow object

            if (
                workflowSource.endpoints ||
                workflowSource.name ||
                workflowSource.workflow_id ||
                workflowSource.id
            ) {

                workflows = [workflowSource];

            }

        }

    }


    // ============================================================
    // NORMALIZE EACH WORKFLOW
    // ============================================================

    workflows = workflows.map(
        (workflow, index) => {

            const item = safeObject(workflow);


            let endpoints =
                item.endpoints ??
                item.endpoint_paths ??
                item.routes ??
                item.nodes ??
                [];


            endpoints = safeArray(endpoints);


            // Endpoint objects → readable strings

            endpoints = endpoints.map(
                (endpoint) => {

                    if (
                        endpoint &&
                        typeof endpoint === "object"
                    ) {

                        return (
                            endpoint.path ||
                            endpoint.route ||
                            endpoint.endpoint ||
                            endpoint.url ||
                            endpoint.name ||
                            JSON.stringify(endpoint)
                        );

                    }

                    return String(endpoint);
                }
            );


            return {

                ...item,

                id:
                    item.id ||
                    item.workflow_id ||
                    `workflow-${index + 1}`,

                name:
                    item.name ||
                    item.workflow_name ||
                    item.title ||
                    `Workflow ${index + 1}`,

                endpoints,

                shared_models:
                    safeArray(
                        item.shared_models ??
                        item.models
                    ),

                shared_functions:
                    safeArray(
                        item.shared_functions ??
                        item.functions
                    ),

            };

        }
    );


    // ============================================================
    // OTHER WORKSPACE DATA
    // ============================================================

    const hypotheses =
        safeArray(workspace.hypotheses);

    const evidence =
        safeArray(workspace.evidence);

    const findings =
        safeArray(workspace.findings);

    const attackPlans =
        safeArray(workspace.attack_plans);

    const runtime =
        safeArray(workspace.runtime);

    const investigationPlan =
        safeArray(workspace.investigation_plan);

    const graph =
        safeObject(workspace.knowledge_graph);

    const risk =
        safeObject(workspace.risk);

    const timeline =
        safeArray(workspace.timeline);


    // ============================================================
    // DEBUG
    //
    // This will tell us EXACTLY what frontend receives.
    // ============================================================

    console.log(
        "=========================================="
    );

    console.log(
        "BUG HUNTER AI - INVESTIGATION DATA"
    );

    console.log(
        "Backend workflow count:",
        result.workflows
    );

    console.log(
        "Workspace workflow:",
        workspace.workflow
    );

    console.log(
        "Workspace workflows:",
        workspace.workflows
    );

    console.log(
        "Normalized workflows:",
        workflows
    );

    console.log(
        "=========================================="
    );


    // ============================================================
    // STATE
    // ============================================================

    const [activeSection, setActiveSection] =
        useState("overview");

    const [selectedIndex, setSelectedIndex] =
        useState(0);

    const [selectedWorkflowIndex, setSelectedWorkflowIndex] =
        useState(0);


    // ============================================================
    // SELECTED DATA
    // ============================================================

    const selectedFinding =
        findings[selectedIndex] ||
        null;


    const selectedHypothesis =
        hypotheses[selectedIndex] ||
        null;


    const selectedPlan =
        attackPlans[selectedIndex] ||
        null;


    const selectedWorkflow =
        workflows[selectedWorkflowIndex] ||
        workflows[0] ||
        null;


    const selectedRuntime =
        runtime[selectedIndex] ||
        runtime[0] ||
        null;


    const planSteps =
        selectedPlan
            ? safeArray(
                selectedPlan.attack_steps ??
                selectedPlan.steps
            )
            : [];


    const runtimeSteps =
        selectedRuntime
            ? safeArray(
                selectedRuntime.steps
            )
            : [];


    // ============================================================
    // CURRENT INVESTIGATION
    // ============================================================

    const currentTitle =
        selectedFinding?.title ||
        selectedHypothesis?.title ||
        selectedPlan?.strategy_name ||
        "Investigation";


    const currentObjective =
        selectedPlan?.objective ||
        selectedFinding?.description ||
        selectedHypothesis?.description ||
        "Review the application's security behavior.";


    const currentRisk =
        selectedFinding?.risk ??
        selectedHypothesis?.score ??
        risk?.score ??
        0;


    const currentConfidence =
        selectedFinding?.confidence ??
        selectedHypothesis?.confidence ??
        "N/A";


    const currentDecision =
        selectedFinding?.decision ||
        "INVESTIGATE";


    // ============================================================
    // NAVIGATION
    // ============================================================

    const sections = [

        {
            id: "overview",
            label: "Overview",
        },

        {
            id: "workflows",
            label: "Workflows",
        },

        {
            id: "investigate",
            label: "Investigate",
        },

        {
            id: "evidence",
            label: "Evidence",
        },

        {
            id: "graph",
            label: "Knowledge Graph",
        },

        {
            id: "timeline",
            label: "Timeline",
        },

        {
            id: "report",
            label: "Report",
        },

    ];


    // ============================================================
    // INVESTIGATION SELECTOR
    // ============================================================

    const selectInvestigation = (index) => {

        setSelectedIndex(index);

        setActiveSection("investigate");

    };


    // ============================================================
    // WORKFLOW SELECTOR
    // ============================================================

    const selectWorkflow = (index) => {

        setSelectedWorkflowIndex(index);

    };


    // ============================================================
    // RENDER
    // ============================================================

    return (
    <div className="app-layout">

        <div className="investigation-content">
            <Navbar />

                <div className="page">


                    {/* =====================================================
                        HEADER
                    ====================================================== */}

                    <div
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            gap: "20px",
                            marginBottom: "24px",
                            flexWrap: "wrap",
                        }}
                    >

                        <div>

                            <div
                                style={{
                                    color: "#20d9ff",
                                    fontSize: "12px",
                                    letterSpacing: "2px",
                                    fontWeight: 700,
                                    marginBottom: "8px",
                                }}
                            >
                            
                                <img
                                    src="/bughunter-logo.png"
                                    alt="BugHunter AI"
                                    style={{
                                          width: "58px",
                                          height: "58px",
                                          objectFit: "contain",
                                          display: "block",
                                           marginBottom: "8px",
                                     }}
                                  />

                                   BUG HUNTER AI
                                 </div>


                            <h1 className="page-title">

                                {repo.project_name ||
                                    repo.name ||
                                    "Application Investigation"}

                            </h1>


                            <p className="page-subtitle">
                                Security reasoning workspace
                            </p>

                        </div>


                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                gap: "10px",
                            }}
                        >

                            <span
                                style={{
                                    padding: "9px 15px",
                                    borderRadius: "20px",
                                    border:
                                        "1px solid rgba(0,220,180,.35)",
                                    color: "#39e6b0",
                                    background:
                                        "rgba(0,220,180,.08)",
                                    fontSize: "13px",
                                    fontWeight: 700,
                                }}
                            >
                                ● INVESTIGATION ACTIVE
                            </span>

                        </div>

                    </div>


                    {/* =====================================================
                        NAVIGATION
                    ====================================================== */}

                    <div
                        style={{
                            display: "flex",
                            gap: "8px",
                            overflowX: "auto",
                            paddingBottom: "18px",
                            marginBottom: "4px",
                        }}
                    >

                        {sections.map(
                            (section) => (

                                <button
                                    key={section.id}
                                    onClick={() =>
                                        setActiveSection(
                                            section.id
                                        )
                                    }
                                    style={{
                                        border:
                                            activeSection ===
                                            section.id
                                                ? "1px solid #16d9ff"
                                                : "1px solid rgba(255,255,255,.10)",

                                        background:
                                            activeSection ===
                                            section.id
                                                ? "rgba(0,190,255,.12)"
                                                : "rgba(255,255,255,.025)",

                                        color:
                                            activeSection ===
                                            section.id
                                                ? "#20d9ff"
                                                : "#aab7c9",

                                        padding:
                                            "10px 16px",

                                        borderRadius: "8px",

                                        cursor: "pointer",

                                        whiteSpace:
                                            "nowrap",

                                        fontWeight: 700,

                                        fontSize: "13px",
                                    }}
                                >
                                    {section.label}
                                </button>

                            )
                        )}

                    </div>


                    {/* =====================================================
                        OVERVIEW
                    ====================================================== */}

                    {activeSection === "overview" && (

                        <>

                            <div
                                style={{
                                    display: "grid",
                                    gridTemplateColumns:
                                        "repeat(auto-fit,minmax(170px,1fr))",
                                    gap: "14px",
                                    marginBottom: "20px",
                                }}
                            >

                                {[
                                    [
                                        "WORKFLOWS",
                                        workflows.length,
                                    ],

                                    [
                                        "HYPOTHESES",
                                        hypotheses.length,
                                    ],

                                    [
                                        "EVIDENCE",
                                        evidence.length,
                                    ],

                                    [
                                        "FINDINGS",
                                        findings.length,
                                    ],

                                    [
                                        "ATTACK PLANS",
                                        attackPlans.length,
                                    ],

                                ].map(
                                    ([label, value]) => (

                                        <div
                                            className="cyber-card"
                                            key={label}
                                            style={{
                                                margin: 0,
                                                textAlign:
                                                    "center",
                                            }}
                                        >

                                            <div
                                                style={{
                                                    fontSize: "11px",
                                                    color: "#71839c",
                                                    letterSpacing:
                                                        "1.5px",
                                                }}
                                            >
                                                {label}
                                            </div>


                                            <div
                                                style={{
                                                    fontSize: "30px",
                                                    fontWeight: 800,
                                                    color: "#20d9ff",
                                                    marginTop: "8px",
                                                }}
                                            >
                                                {value}
                                            </div>

                                        </div>

                                    )
                                )}

                            </div>


                            <div className="cyber-card">

                                <div className="card-heading">

                                    <div>

                                        <span className="card-eyebrow">
                                            APPLICATION MODEL
                                        </span>

                                        <h2 className="section-title">
                                            {repo.project_name ||
                                                "Application"}
                                        </h2>

                                    </div>

                                    <span className="card-indicator">
                                        ANALYZED
                                    </span>

                                </div>


                                <div
                                    style={{
                                        display: "grid",
                                        gridTemplateColumns:
                                            "repeat(auto-fit,minmax(160px,1fr))",
                                        gap: "18px",
                                    }}
                                >

                                    <Stat
                                        label="Language"
                                        value={repo.language}
                                    />

                                    <Stat
                                        label="Framework"
                                        value={repo.framework}
                                    />

                                    <Stat
                                        label="Entry Point"
                                        value={repo.entry_point}
                                    />

                                    <Stat
                                        label="Source Files"
                                        value={
                                            repo.source_files ??
                                            repo.source_file_count
                                        }
                                    />

                                    <Stat
                                        label="Risk Score"
                                        value={
                                            risk?.score ??
                                            0
                                        }
                                    />

                                </div>

                            </div>


                            <div className="cyber-card">

                                <span className="card-eyebrow">
                                    RECONSTRUCTED ATTACK SURFACE
                                </span>

                                <h2 className="section-title">
                                    Workflows
                                </h2>

                                <p>
                                    BugHunter AI reconstructed{" "}
                                    <strong>
                                        {workflows.length}
                                    </strong>{" "}
                                    application workflow
                                    {workflows.length === 1
                                        ? ""
                                        : "s"}.
                                </p>


                                {workflows.length > 0 ? (

                                    <div
                                        style={{
                                            display: "grid",
                                            gap: "10px",
                                            marginTop: "16px",
                                        }}
                                    >

                                        {workflows.map(
                                            (
                                                workflow,
                                                index
                                            ) => (

                                                <button
                                                    key={
                                                        workflow.id ||
                                                        index
                                                    }
                                                    onClick={() => {

                                                        selectWorkflow(
                                                            index
                                                        );

                                                        setActiveSection(
                                                            "workflows"
                                                        );

                                                    }}
                                                    style={{
                                                        textAlign:
                                                            "left",

                                                        width: "100%",

                                                        padding:
                                                            "14px",

                                                        borderRadius:
                                                            "8px",

                                                        border:
                                                            "1px solid rgba(255,255,255,.08)",

                                                        background:
                                                            "rgba(255,255,255,.025)",

                                                        color:
                                                            "#dce8f5",

                                                        cursor:
                                                            "pointer",
                                                    }}
                                                >

                                                    <strong>
                                                        {workflow.name}
                                                    </strong>

                                                    <div
                                                        style={{
                                                            marginTop:
                                                                "6px",

                                                            color:
                                                                "#71839c",

                                                            fontSize:
                                                                "12px",
                                                        }}
                                                    >
                                                        {
                                                            workflow.endpoints
                                                                .length
                                                        }{" "}
                                                        endpoint
                                                        {
                                                            workflow
                                                                .endpoints
                                                                .length ===
                                                            1
                                                                ? ""
                                                                : "s"
                                                        }
                                                    </div>

                                                </button>

                                            )
                                        )}

                                    </div>

                                ) : (

                                    <p
                                        style={{
                                            color:
                                                "#71839c",
                                        }}
                                    >
                                        No workflows were
                                        returned by the
                                        analysis engine.
                                    </p>

                                )}

                            </div>


                            <div className="cyber-card">

                                <span className="card-eyebrow">
                                    NEXT INVESTIGATION
                                </span>

                                <h2 className="section-title">
                                    Choose an investigation
                                </h2>

                                <p>
                                    Select an investigation
                                    to inspect reasoning,
                                    evidence and validation.
                                </p>

                                <InvestigationList
                                    items={
                                        findings.length
                                            ? findings
                                            : hypotheses
                                    }
                                    activeIndex={
                                        selectedIndex
                                    }
                                    onSelect={
                                        selectInvestigation
                                    }
                                />

                            </div>

                        </>

                    )}


                    {/* =====================================================
                        WORKFLOWS
                    ====================================================== */}

                    {activeSection === "workflows" && (

                        <div className="cyber-card">

                            <div
                                style={{
                                    display: "flex",
                                    justifyContent:
                                        "space-between",
                                    alignItems:
                                        "flex-start",
                                    gap: "15px",
                                    marginBottom:
                                        "18px",
                                }}
                            >

                                <div>

                                    <span className="card-eyebrow">
                                        APPLICATION WORKFLOWS
                                    </span>

                                    <h2 className="section-title">
                                        Reconstructed Workflows
                                    </h2>

                                    <p
                                        style={{
                                            marginBottom: 0,
                                        }}
                                    >
                                        Business flows
                                        reconstructed from
                                        endpoint
                                        relationships.
                                    </p>

                                </div>


                                <span className="card-indicator">

                                    {workflows.length}{" "}
                                    WORKFLOW
                                    {workflows.length ===
                                    1
                                        ? ""
                                        : "S"}

                                </span>

                            </div>


                            {workflows.length === 0 ? (

                                <div
                                    style={{
                                        padding: "20px",
                                        borderRadius: "8px",
                                        border:
                                            "1px dashed rgba(255,255,255,.12)",
                                        color:
                                            "#71839c",
                                    }}
                                >
                                    No workflows discovered
                                    in the returned
                                    investigation
                                    workspace.
                                </div>

                            ) : (

                                <div
                                    style={{
                                        display: "grid",
                                        gap: "12px",
                                    }}
                                >

                                    {workflows.map(
                                        (
                                            workflow,
                                            index
                                        ) => {

                                            const active =
                                                selectedWorkflowIndex ===
                                                index;

                                            const endpoints =
                                                workflow.endpoints;

                                            const models =
                                                workflow.shared_models;

                                            const functions =
                                                workflow.shared_functions;


                                            return (

                                                <button
                                                    key={
                                                        workflow.id ||
                                                        index
                                                    }
                                                    onClick={() =>
                                                        selectWorkflow(
                                                            index
                                                        )
                                                    }
                                                    style={{
                                                        textAlign:
                                                            "left",

                                                        border:
                                                            active
                                                                ? "1px solid #20d9ff"
                                                                : "1px solid rgba(255,255,255,.08)",

                                                        background:
                                                            active
                                                                ? "rgba(0,205,255,.08)"
                                                                : "rgba(255,255,255,.025)",

                                                        padding:
                                                            "18px",

                                                        borderRadius:
                                                            "10px",

                                                        color:
                                                            "#dbe7f5",

                                                        cursor:
                                                            "pointer",

                                                        width:
                                                            "100%",
                                                    }}
                                                >

                                                    <div
                                                        style={{
                                                            display:
                                                                "flex",

                                                            justifyContent:
                                                                "space-between",

                                                            alignItems:
                                                                "center",

                                                            gap:
                                                                "12px",
                                                        }}
                                                    >

                                                        <strong
                                                            style={{
                                                                fontSize:
                                                                    "16px",
                                                            }}
                                                        >
                                                            {
                                                                workflow.name
                                                            }
                                                        </strong>


                                                        <span
                                                            style={{
                                                                color:
                                                                    "#20d9ff",

                                                                fontSize:
                                                                    "12px",

                                                                fontWeight:
                                                                    700,
                                                            }}
                                                        >

                                                            {
                                                                endpoints.length
                                                            }{" "}
                                                            endpoint
                                                            {endpoints.length ===
                                                            1
                                                                ? ""
                                                                : "s"}

                                                        </span>

                                                    </div>


                                                    {endpoints.length >
                                                        0 && (

                                                        <div
                                                            style={{
                                                                display:
                                                                    "flex",

                                                                flexWrap:
                                                                    "wrap",

                                                                gap:
                                                                    "8px",

                                                                marginTop:
                                                                    "14px",
                                                            }}
                                                        >

                                                            {endpoints.map(
                                                                (
                                                                    endpoint,
                                                                    endpointIndex
                                                                ) => (

                                                                    <span
                                                                        key={
                                                                            endpointIndex
                                                                        }
                                                                        style={{
                                                                            padding:
                                                                                "7px 10px",

                                                                            borderRadius:
                                                                                "6px",

                                                                            border:
                                                                                "1px solid rgba(0,205,255,.18)",

                                                                            background:
                                                                                "rgba(0,205,255,.05)",

                                                                            color:
                                                                                "#9edff0",

                                                                            fontSize:
                                                                                "12px",

                                                                            fontFamily:
                                                                                "monospace",
                                                                        }}
                                                                    >
                                                                        {
                                                                            endpoint
                                                                        }
                                                                    </span>

                                                                )
                                                            )}

                                                        </div>

                                                    )}


                                                    {(
                                                        models.length >
                                                        0 ||
                                                        functions.length >
                                                        0
                                                    ) && (

                                                        <div
                                                            style={{
                                                                display:
                                                                    "flex",

                                                                flexWrap:
                                                                    "wrap",

                                                                gap:
                                                                    "14px",

                                                                marginTop:
                                                                    "14px",

                                                                color:
                                                                    "#71839c",

                                                                fontSize:
                                                                    "11px",
                                                            }}
                                                        >

                                                            {models.length >
                                                                0 && (

                                                                <span>
                                                                    Models:{" "}
                                                                    {
                                                                        models.join(
                                                                            ", "
                                                                        )
                                                                    }
                                                                </span>

                                                            )}


                                                            {functions.length >
                                                                0 && (

                                                                <span>
                                                                    Functions:{" "}
                                                                    {
                                                                        functions.join(
                                                                            ", "
                                                                        )
                                                                    }
                                                                </span>

                                                            )}

                                                        </div>

                                                    )}

                                                </button>

                                            );

                                        }
                                    )}

                                </div>

                            )}

                        </div>

                    )}


                    {/* =====================================================
                        INVESTIGATION
                    ====================================================== */}

                    {activeSection === "investigate" && (

                        <>

                            <div
                                style={{
                                    display: "grid",
                                    gridTemplateColumns:
                                        "290px minmax(0,1fr)",
                                    gap: "18px",
                                    alignItems:
                                        "start",
                                }}
                            >


                                {/* CASE QUEUE */}

                                <div
                                    className="cyber-card"
                                    style={{
                                        position:
                                            "sticky",
                                        top: "20px",
                                    }}
                                >

                                    <span className="card-eyebrow">
                                        HUNTER QUEUE
                                    </span>

                                    <h3 className="section-title">
                                        Investigations
                                    </h3>

                                    <p
                                        style={{
                                            fontSize:
                                                "12px",
                                            color:
                                                "#71839c",
                                            lineHeight:
                                                1.6,
                                        }}
                                    >
                                        Security cases
                                        prioritized from
                                        the application's
                                        attack surface.
                                    </p>


                                    <div
                                        style={{
                                            display:
                                                "flex",
                                            gap: "8px",
                                            marginBottom:
                                                "14px",
                                        }}
                                    >

                                        <span
                                            style={{
                                                padding:
                                                    "5px 8px",
                                                borderRadius:
                                                    "5px",
                                                background:
                                                    "rgba(255,180,0,.10)",
                                                color:
                                                    "#ffc857",
                                                fontSize:
                                                    "10px",
                                                fontWeight:
                                                    800,
                                            }}
                                        >
                                            {findings.length}{" "}
                                            FINDINGS
                                        </span>


                                        <span
                                            style={{
                                                padding:
                                                    "5px 8px",
                                                borderRadius:
                                                    "5px",
                                                background:
                                                    "rgba(0,205,255,.08)",
                                                color:
                                                    "#20d9ff",
                                                fontSize:
                                                    "10px",
                                                fontWeight:
                                                    800,
                                            }}
                                        >
                                            {hypotheses.length}{" "}
                                            HYPOTHESES
                                        </span>

                                    </div>


                                    <InvestigationList
                                        items={
                                            findings.length
                                                ? findings
                                                : hypotheses
                                        }
                                        activeIndex={
                                            selectedIndex
                                        }
                                        onSelect={
                                            selectInvestigation
                                        }
                                    />

                                </div>


                                {/* MAIN CASE */}

                                <div
                                    style={{
                                        display:
                                            "grid",
                                        gap:
                                            "18px",
                                    }}
                                >


                                    {/* CASE HEADER */}

                                    <div className="cyber-card">

                                        <span className="card-eyebrow">
                                            ACTIVE SECURITY CASE
                                        </span>


                                        <h2 className="section-title">
                                            {currentTitle}
                                        </h2>


                                        <div
                                            style={{
                                                color:
                                                    "#71839c",
                                                fontSize:
                                                    "12px",
                                                fontFamily:
                                                    "monospace",
                                            }}
                                        >

                                            TARGET ·{" "}

                                            {selectedWorkflow
                                                ?.endpoints?.[0] ||
                                                repo.entry_point ||
                                                "APPLICATION"}

                                        </div>


                                        <p
                                            style={{
                                                marginTop:
                                                    "18px",
                                                color:
                                                    "#a9b8ca",
                                                lineHeight:
                                                    1.7,
                                            }}
                                        >
                                            {currentObjective}
                                        </p>


                                        <div
                                            style={{
                                                display:
                                                    "grid",
                                                gridTemplateColumns:
                                                    "repeat(3,minmax(0,1fr))",
                                                gap:
                                                    "12px",
                                                marginTop:
                                                    "20px",
                                            }}
                                        >

                                            <Metric
                                                label="RISK SCORE"
                                                value={
                                                    currentRisk
                                                }
                                            />

                                            <Metric
                                                label="CONFIDENCE"
                                                value={
                                                    currentConfidence
                                                }
                                            />

                                            <Metric
                                                label="DECISION"
                                                value={
                                                    currentDecision
                                                }
                                            />

                                        </div>

                                    </div>


                                    {/* WORKFLOW CONTEXT */}

                                    <div className="cyber-card">

                                        <span className="card-eyebrow">
                                            ATTACK SURFACE CONTEXT
                                        </span>

                                        <h3 className="section-title">
                                            Workflow Under Investigation
                                        </h3>


                                        {selectedWorkflow ? (

                                            <>

                                                <strong>
                                                    {
                                                        selectedWorkflow.name
                                                    }
                                                </strong>


                                                <div
                                                    style={{
                                                        display:
                                                            "flex",
                                                        flexWrap:
                                                            "wrap",
                                                        gap:
                                                            "8px",
                                                        marginTop:
                                                            "15px",
                                                    }}
                                                >

                                                    {selectedWorkflow.endpoints.map(
                                                        (
                                                            endpoint,
                                                            index
                                                        ) => (

                                                            <span
                                                                key={
                                                                    index
                                                                }
                                                                style={{
                                                                    padding:
                                                                        "8px 11px",
                                                                    borderRadius:
                                                                        "6px",
                                                                    border:
                                                                        "1px solid rgba(0,205,255,.18)",
                                                                    background:
                                                                        "rgba(0,205,255,.05)",
                                                                    color:
                                                                        "#9edff0",
                                                                    fontFamily:
                                                                        "monospace",
                                                                    fontSize:
                                                                        "12px",
                                                                }}
                                                            >
                                                                {
                                                                    endpoint
                                                                }
                                                            </span>

                                                        )
                                                    )}

                                                </div>

                                            </>

                                        ) : (

                                            <p
                                                style={{
                                                    color:
                                                        "#71839c",
                                                }}
                                            >
                                                No workflow is
                                                associated
                                                with this
                                                investigation.
                                            </p>

                                        )}

                                    </div>


                                    {/* VALIDATION PLAN */}

                                    <div className="cyber-card">

                                        <span className="card-eyebrow">
                                            REASONING PLAN
                                        </span>

                                        <h3 className="section-title">
                                            Validation Path
                                        </h3>


                                        {planSteps.length ===
                                        0 ? (

                                            <p
                                                style={{
                                                    color:
                                                        "#71839c",
                                                }}
                                            >
                                                No validation
                                                steps are
                                                currently
                                                associated
                                                with this
                                                case.
                                            </p>

                                        ) : (

                                            <div
                                                style={{
                                                    display:
                                                        "grid",
                                                    gap:
                                                        "10px",
                                                }}
                                            >

                                                {planSteps.map(
                                                    (
                                                        step,
                                                        index
                                                    ) => (

                                                        <div
                                                            key={
                                                                index
                                                            }
                                                            style={{
                                                                padding:
                                                                    "15px",
                                                                border:
                                                                    "1px solid rgba(255,255,255,.07)",
                                                                borderRadius:
                                                                    "8px",
                                                            }}
                                                        >

                                                            <strong>
                                                                Step{" "}
                                                                {
                                                                    step.step_number ||
                                                                    index +
                                                                        1
                                                                }
                                                            </strong>


                                                            <div
                                                                style={{
                                                                    marginTop:
                                                                        "6px",
                                                                    color:
                                                                        "#8ea0b6",
                                                                    fontSize:
                                                                        "12px",
                                                                }}
                                                            >
                                                                {
                                                                    step.action ||
                                                                    "Investigation step"
                                                                }
                                                            </div>


                                                            <div
                                                                style={{
                                                                    marginTop:
                                                                        "6px",
                                                                    color:
                                                                        "#71839c",
                                                                    fontSize:
                                                                        "12px",
                                                                }}
                                                            >
                                                                Expected evidence:{" "}
                                                                {
                                                                    step.expected_result ||
                                                                    "Collect and evaluate evidence"
                                                                }
                                                            </div>

                                                        </div>

                                                    )
                                                )}

                                            </div>

                                        )}

                                    </div>


                                    {/* RUNTIME */}

                                    <div className="cyber-card">

                                        <span className="card-eyebrow">
                                            VALIDATION STATE
                                        </span>

                                        <h3 className="section-title">
                                            Runtime Evidence
                                        </h3>


                                        {runtimeSteps.length ===
                                        0 ? (

                                            <p
                                                style={{
                                                    color:
                                                        "#71839c",
                                                }}
                                            >
                                                Runtime
                                                validation has
                                                not produced
                                                observations
                                                for this case
                                                yet.
                                            </p>

                                        ) : (

                                            <div
                                                style={{
                                                    display:
                                                        "grid",
                                                    gap:
                                                        "9px",
                                                }}
                                            >

                                                {runtimeSteps.map(
                                                    (
                                                        step,
                                                        index
                                                    ) => (

                                                        <div
                                                            key={
                                                                index
                                                            }
                                                            style={{
                                                                padding:
                                                                    "14px",
                                                                border:
                                                                    "1px solid rgba(255,255,255,.07)",
                                                                borderRadius:
                                                                    "8px",
                                                            }}
                                                        >

                                                            <strong>
                                                                Step{" "}
                                                                {
                                                                    step.step_number ||
                                                                    index +
                                                                        1
                                                                }
                                                            </strong>


                                                            <div
                                                                style={{
                                                                    marginTop:
                                                                        "6px",
                                                                    color:
                                                                        "#8ea0b6",
                                                                    fontSize:
                                                                        "12px",
                                                                }}
                                                            >
                                                                {
                                                                    step.action ||
                                                                    "Runtime observation"
                                                                }
                                                            </div>

                                                        </div>

                                                    )
                                                )}

                                            </div>

                                        )}

                                    </div>

                                </div>

                            </div>

                        </>

                    )}


                    {/* =====================================================
                        EVIDENCE
                    ====================================================== */}

                    {activeSection === "evidence" && (

                        <div className="cyber-card">

                            <span className="card-eyebrow">
                                INVESTIGATION DATA
                            </span>

                            <h2 className="section-title">
                                Evidence
                            </h2>


                            {evidence.length === 0 ? (

                                <p
                                    style={{
                                        color:
                                            "#71839c",
                                    }}
                                >
                                    No evidence records
                                    available.
                                </p>

                            ) : (

                                <div
                                    style={{
                                        display:
                                            "grid",
                                        gap:
                                            "10px",
                                    }}
                                >

                                    {evidence.map(
                                        (
                                            item,
                                            index
                                        ) => (

                                            <div
                                                key={
                                                    index
                                                }
                                                style={{
                                                    padding:
                                                        "15px",
                                                    border:
                                                        "1px solid rgba(255,255,255,.08)",
                                                    borderRadius:
                                                        "9px",
                                                    background:
                                                        "rgba(255,255,255,.02)",
                                                }}
                                            >

                                                <strong>
                                                    {
                                                        item.title ||
                                                        item.type ||
                                                        item.source ||
                                                        `Evidence ${index + 1}`
                                                    }
                                                </strong>


                                                <p
                                                    style={{
                                                        color:
                                                            "#8ea0b6",
                                                        marginBottom:
                                                            0,
                                                    }}
                                                >
                                                    {
                                                        item.description ||
                                                        item.message ||
                                                        item.observation ||
                                                        JSON.stringify(
                                                            item
                                                        )
                                                    }
                                                </p>

                                            </div>

                                        )
                                    )}

                                </div>

                            )}

                        </div>

                    )}


                    {/* =====================================================
    KNOWLEDGE GRAPH
====================================================== */}

{activeSection === "graph" && (
    <KnowledgeGraph graph={graph} />
)}


                    {/* =====================================================
                        TIMELINE
                    ====================================================== */}

                    {activeSection === "timeline" && (

                        <div className="cyber-card">

                            <span className="card-eyebrow">
                                INVESTIGATION HISTORY
                            </span>

                            <h2 className="section-title">
                                Investigation Timeline
                            </h2>


                            {timeline.length > 0 ? (

                                <div
                                    style={{
                                        display:
                                            "grid",
                                        gap:
                                            "10px",
                                    }}
                                >

                                    {timeline.map(
                                        (
                                            event,
                                            index
                                        ) => (

                                            <div
                                                key={
                                                    index
                                                }
                                                style={{
                                                    padding:
                                                        "13px",
                                                    borderLeft:
                                                        "2px solid #20d9ff",
                                                    background:
                                                        "rgba(255,255,255,.02)",
                                                }}
                                            >

                                                {typeof event ===
                                                "string"
                                                    ? event
                                                    : JSON.stringify(
                                                        event
                                                    )}

                                            </div>

                                        )
                                    )}

                                </div>

                            ) : (

                                <div
                                    style={{
                                        display:
                                            "grid",
                                        gap:
                                            "10px",
                                    }}
                                >

                                    {[
                                        "Application analyzed",
                                        "Workflows reconstructed",
                                        "Security hypotheses generated",
                                        "Investigation strategies created",
                                        "Attack plans prepared",
                                        "Runtime validation performed",
                                        "Findings generated",
                                    ].map(
                                        (
                                            event,
                                            index
                                        ) => (

                                            <div
                                                key={
                                                    event
                                                }
                                                style={{
                                                    display:
                                                        "flex",
                                                    gap:
                                                        "15px",
                                                    alignItems:
                                                        "center",
                                                    padding:
                                                        "13px",
                                                    borderLeft:
                                                        "2px solid #20d9ff",
                                                    background:
                                                        "rgba(255,255,255,.02)",
                                                }}
                                            >

                                                <span
                                                    style={{
                                                        color:
                                                            "#20d9ff",
                                                        fontWeight:
                                                            800,
                                                    }}
                                                >
                                                    0
                                                    {index +
                                                        1}
                                                </span>

                                                <span>
                                                    {event}
                                                </span>

                                            </div>

                                        )
                                    )}

                                </div>

                            )}

                        </div>

                    )}


                    {/* =====================================================
                        REPORT
                    ====================================================== */}

                    {activeSection === "report" && (

                        <div className="cyber-card">

                            <span className="card-eyebrow">
                                FINAL OUTPUT
                            </span>

                            <h2 className="section-title">
                                Investigation Report
                            </h2>

                            <p>
                                The complete
                                investigation has
                                been reconstructed by
                                BugHunter AI.
                            </p>


                            <div
                                style={{
                                    display:
                                        "grid",
                                    gap:
                                        "12px",
                                    marginTop:
                                        "20px",
                                }}
                            >

                                <Stat
                                    label="Workflows"
                                    value={
                                        workflows.length
                                    }
                                />

                                <Stat
                                    label="Hypotheses"
                                    value={
                                        hypotheses.length
                                    }
                                />

                                <Stat
                                    label="Findings"
                                    value={
                                        findings.length
                                    }
                                />

                                <Stat
                                    label="Attack Plans"
                                    value={
                                        attackPlans.length
                                    }
                                />

                            </div>

                        </div>

                    )}

                </div>

            </div>

        </div>
    );
}


// ================================================================
// SMALL UI COMPONENTS
// ================================================================

function Stat({
    label,
    value,
}) {

    return (

        <div>

            <div
                style={{
                    color:
                        "#71839c",
                    fontSize:
                        "11px",
                    letterSpacing:
                        "1px",
                    marginBottom:
                        "6px",
                }}
            >
                {label}
            </div>

            <strong>
                {value ??
                    "Unknown"}
            </strong>

        </div>
    );
}


function Metric({
    label,
    value,
}) {

    return (

        <div
            style={{
                padding:
                    "15px",
                borderRadius:
                    "9px",
                background:
                    "rgba(255,255,255,.025)",
                border:
                    "1px solid rgba(255,255,255,.08)",
            }}
        >

            <div
                style={{
                    fontSize:
                        "10px",
                    color:
                        "#71839c",
                    letterSpacing:
                        "1.5px",
                }}
            >
                {label}
            </div>

            <strong
                style={{
                    display:
                        "block",
                    marginTop:
                        "7px",
                    color:
                        "#20d9ff",
                    fontSize:
                        "18px",
                }}
            >
                {value}
            </strong>

        </div>
    );
}


function InvestigationList({
    items,
    activeIndex,
    onSelect,
}) {

    if (
        !items ||
        items.length === 0
    ) {

        return (

            <p
                style={{
                    color:
                        "#71839c",
                }}
            >
                No investigations
                available.
            </p>

        );
    }


    return (

        <div
            style={{
                display:
                    "grid",
                gap:
                    "8px",
            }}
        >

            {items.map(
                (
                    item,
                    index
                ) => {

                    const title =
                        item.title ||
                        item.strategy_name ||
                        item.name ||
                        `Investigation ${index + 1}`;


                    const active =
                        activeIndex ===
                        index;


                    return (

                        <button
                            key={
                                item.id ||
                                index
                            }
                            onClick={() =>
                                onSelect(
                                    index
                                )
                            }
                            style={{
                                textAlign:
                                    "left",

                                width:
                                    "100%",

                                padding:
                                    "13px",

                                borderRadius:
                                    "8px",

                                border:
                                    active
                                        ? "1px solid #20d9ff"
                                        : "1px solid rgba(255,255,255,.07)",

                                background:
                                    active
                                        ? "rgba(0,205,255,.10)"
                                        : "rgba(255,255,255,.02)",

                                color:
                                    "#dce8f5",

                                cursor:
                                    "pointer",
                            }}
                        >

                            <strong
                                style={{
                                    fontSize:
                                        "13px",
                                }}
                            >
                                {title}
                            </strong>


                            <div
                                style={{
                                    marginTop:
                                        "5px",
                                    fontSize:
                                        "11px",
                                    color:
                                        "#71839c",
                                }}
                            >
                                {
                                    item.decision ||
                                    item.risk ||
                                    "INVESTIGATE"
                                }
                            </div>

                        </button>

                    );
                }
            )}

        </div>
    );
}


export default Investigation;