function normalizeArray(value) {
  if (Array.isArray(value)) return value;

  if (value && typeof value === "object") {
    if (Array.isArray(value.items)) return value.items;
    if (Array.isArray(value.findings)) return value.findings;
    if (Array.isArray(value.evidence)) return value.evidence;
    if (Array.isArray(value.results)) return value.results;

    return Object.values(value);
  }

  return [];
}

function getText(value, fallback = "Not available") {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }

  if (typeof value === "string" || typeof value === "number") {
    return String(value);
  }

  return JSON.stringify(value, null, 2);
}

function FindingCard({ finding, index }) {
  const title =
    finding.title ||
    finding.name ||
    finding.type ||
    finding.category ||
    `Security Finding ${index + 1}`;

  const description =
    finding.description ||
    finding.reason ||
    finding.explanation ||
    finding.message ||
    finding.outcome ||
    "Potential security-relevant behavior identified during investigation.";

  const risk =
    finding.risk ??
    finding.score ??
    finding.risk_score ??
    finding.severity ??
    "N/A";

  const confidence =
    finding.confidence ??
    finding.confidence_score ??
    "N/A";

  const decision =
    finding.decision ||
    finding.status ||
    finding.result ||
    "INVESTIGATE";

  return (
    <div className="finding-card">

      <div className="finding-top">
        <div>
          <span className="finding-number">
            FINDING {index + 1}
          </span>

          <h3>{getText(title)}</h3>
        </div>

        <div className="finding-risk">
          {getText(risk)}
        </div>
      </div>

      <div className="finding-description">
        {getText(description)}
      </div>

      <div className="finding-metrics">

        <div className="finding-metric">
          <span>RISK</span>
          <strong>{getText(risk)}</strong>
        </div>

        <div className="finding-metric">
          <span>CONFIDENCE</span>
          <strong>{getText(confidence)}</strong>
        </div>

        <div className="finding-metric">
          <span>DECISION</span>
          <strong>{getText(decision)}</strong>
        </div>

      </div>

      {(finding.route ||
        finding.endpoint ||
        finding.workflow ||
        finding.target) && (

        <div className="finding-context">

          {finding.route && (
            <div>
              <span>ROUTE</span>
              <code>{getText(finding.route)}</code>
            </div>
          )}

          {finding.endpoint && (
            <div>
              <span>ENDPOINT</span>
              <code>{getText(finding.endpoint)}</code>
            </div>
          )}

          {finding.workflow && (
            <div>
              <span>WORKFLOW</span>
              <p>{getText(finding.workflow)}</p>
            </div>
          )}

          {finding.target && (
            <div>
              <span>TARGET</span>
              <p>{getText(finding.target)}</p>
            </div>
          )}

        </div>
      )}

    </div>
  );
}

function EvidenceCard({ evidence, index }) {
  const type =
    evidence.type ||
    evidence.category ||
    evidence.kind ||
    "Observation";

  const source =
    evidence.source ||
    evidence.route ||
    evidence.endpoint ||
    evidence.file ||
    "Application model";

  const description =
    evidence.description ||
    evidence.reason ||
    evidence.observation ||
    evidence.message ||
    evidence.value ||
    evidence.result ||
    evidence.outcome ||
    evidence;

  return (
    <div className="evidence-card">

      <div className="evidence-index">
        {String(index + 1).padStart(2, "0")}
      </div>

      <div className="evidence-body">

        <div className="evidence-header">
          <span>{getText(type)}</span>
          <code>{getText(source)}</code>
        </div>

        <p>
          {getText(description)}
        </p>

      </div>

    </div>
  );
}

function FindingsEvidencePanel({
  findings = [],
  evidence = []
}) {

  const normalizedFindings = normalizeArray(findings);
  const normalizedEvidence = normalizeArray(evidence);

  return (
    <section className="cyber-card findings-evidence-panel">

      {/* ================= FINDINGS ================= */}

      <div className="section-title-row">

        <div>
          <span className="section-kicker">
            SECURITY REASONING
          </span>

          <h2>AI Findings</h2>

          <p className="section-description">
            Security-relevant conclusions produced from the
            application model, workflow analysis and reasoning engine.
          </p>
        </div>

        <div className="section-count">
          {normalizedFindings.length}
        </div>

      </div>

      {normalizedFindings.length === 0 ? (

        <div className="empty-state">
          No confirmed findings yet. Investigation evidence is still
          being evaluated.
        </div>

      ) : (

        <div className="findings-list">

          {normalizedFindings.map((finding, index) => (

            <FindingCard
              key={finding.id || index}
              finding={finding}
              index={index}
            />

          ))}

        </div>

      )}


      {/* ================= EVIDENCE ================= */}

      <div className="subsection-heading">

        <div>
          <span className="section-kicker">
            INVESTIGATION DATA
          </span>

          <h2>Evidence</h2>

          <p className="section-description">
            Observations collected while reconstructing application
            behavior and evaluating security hypotheses.
          </p>
        </div>

        <div className="section-count">
          {normalizedEvidence.length}
        </div>

      </div>

      {normalizedEvidence.length === 0 ? (

        <div className="empty-state">
          No evidence records were produced.
        </div>

      ) : (

        <div className="evidence-list">

          {normalizedEvidence.map((item, index) => (

            <EvidenceCard
              key={item.id || index}
              evidence={item}
              index={index}
            />

          ))}

        </div>

      )}

    </section>
  );
}

export default FindingsEvidencePanel;