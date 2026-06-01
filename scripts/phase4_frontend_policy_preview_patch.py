from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

if "type RiskEvaluation" not in s:
    marker = '''type Dashboard = {
  total_mcp_requests: number;
  allowed_requests: number;
  denied_requests: number;
  approval_requests: number;
  redacted_responses: number;
  sensitive_access_attempts: number;
  high_risk_activities: number;
  policy_violations: number;
  governance_coverage: number;
};'''
    replacement = '''type Dashboard = {
  total_mcp_requests: number;
  allowed_requests: number;
  denied_requests: number;
  approval_requests: number;
  redacted_responses: number;
  sensitive_access_attempts: number;
  high_risk_activities: number;
  policy_violations: number;
  governance_coverage: number;
};

type RiskEvaluation = {
  risk_tier: string;
  risk_score: number;
  risk_factors: string[];
  protected_data: boolean;
  action_type: string;
};

type PolicyPreview = {
  requested_tool: string;
  requested_resource: string;
  data_classification: string;
  risk_evaluation: RiskEvaluation;
  policy_result: PolicyResult;
  evaluated_controls: string[];
  rule_id: string;
};'''
    if marker not in s:
        raise SystemExit("Dashboard type marker not found")
    s = s.replace(marker, replacement)

if "const [policyPreview" not in s:
    marker = '''  const [form, setForm] = useState(initialForm);
  const [status, setStatus] = useState("Loading MCP governance telemetry...");
  const [lastDecision, setLastDecision] = useState<MCPRequest | null>(null);'''
    replacement = '''  const [form, setForm] = useState(initialForm);
  const [status, setStatus] = useState("Loading MCP governance telemetry...");
  const [lastDecision, setLastDecision] = useState<MCPRequest | null>(null);
  const [policyPreview, setPolicyPreview] = useState<PolicyPreview | null>(null);'''
    if marker not in s:
        raise SystemExit("state marker not found")
    s = s.replace(marker, replacement)

if "async function loadPolicyPreview" not in s:
    marker = '''  async function loadData() {
    const [toolsRes, requestsRes, dashboardRes] = await Promise.all([
      fetch(`${API_BASE}/api/mcp/tools`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/mcp/requests`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/dashboard`, { cache: "no-store" })
    ]);

    setTools(await toolsRes.json());
    setRequests(await requestsRes.json());
    setDashboard(await dashboardRes.json());
    setStatus("Live backend connected");
  }'''
    replacement = '''  async function loadData() {
    const [toolsRes, requestsRes, dashboardRes] = await Promise.all([
      fetch(`${API_BASE}/api/mcp/tools`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/mcp/requests`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/dashboard`, { cache: "no-store" })
    ]);

    setTools(await toolsRes.json());
    setRequests(await requestsRes.json());
    setDashboard(await dashboardRes.json());
    setStatus("Live backend connected");
  }

  async function loadPolicyPreview() {
    const res = await fetch(`${API_BASE}/api/policy/preview`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    if (res.ok) {
      setPolicyPreview(await res.json());
    }
  }'''
    if marker not in s:
        raise SystemExit("loadData marker not found")
    s = s.replace(marker, replacement)

if "loadPolicyPreview().catch" not in s:
    marker = '''  useEffect(() => {
    loadData().catch((error) => setStatus(`Backend connection failed: ${error.message}`));
  }, []);'''
    replacement = '''  useEffect(() => {
    loadData().catch((error) => setStatus(`Backend connection failed: ${error.message}`));
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadPolicyPreview().catch(() => undefined);
    }, 200);

    return () => clearTimeout(timer);
  }, [form]);'''
    if marker not in s:
        raise SystemExit("useEffect marker not found")
    s = s.replace(marker, replacement)

if "Risk Tiering Engine" not in s:
    marker = '''            <div style={styles.policyPreview}>
              <strong>Governance Evaluation Inputs</strong>
              <span>User: {form.user_identity}</span>
              <span>Role: {form.role}</span>
              <span>Clearance: {form.clearance_level}</span>
              <span>Tool: {form.requested_tool}</span>
              <span>Resource: {form.requested_resource}</span>
              <span>Classification: {form.data_classification}</span>
              <span>Approval: {form.approval_status}</span>
            </div>
          </div>'''
    replacement = '''            <div style={styles.policyPreview}>
              <strong>Governance Evaluation Inputs</strong>
              <span>User: {form.user_identity}</span>
              <span>Role: {form.role}</span>
              <span>Clearance: {form.clearance_level}</span>
              <span>Tool: {form.requested_tool}</span>
              <span>Resource: {form.requested_resource}</span>
              <span>Classification: {form.data_classification}</span>
              <span>Approval: {form.approval_status}</span>
            </div>

            {policyPreview && (
              <>
                <div style={styles.riskEngine}>
                  <div style={styles.recordHead}>
                    <strong>Risk Tiering Engine</strong>
                    <span style={riskScoreStyle(policyPreview.risk_evaluation.risk_score)}>
                      {policyPreview.risk_evaluation.risk_score}/100
                    </span>
                  </div>
                  <p>Tier: <b>{policyPreview.risk_evaluation.risk_tier.replaceAll("_", " ")}</b></p>
                  <p>Action Type: <b>{policyPreview.risk_evaluation.action_type}</b></p>
                  <p>Protected Data: <b>{policyPreview.risk_evaluation.protected_data ? "yes" : "no"}</b></p>
                  <ul style={styles.compactList}>
                    {policyPreview.risk_evaluation.risk_factors.map((factor) => (
                      <li key={factor}>{factor}</li>
                    ))}
                  </ul>
                </div>

                <div style={styles.policyEngine}>
                  <div style={styles.recordHead}>
                    <strong>Policy Decision Engine</strong>
                    <span style={decisionStyle(policyPreview.policy_result.decision)}>
                      {policyPreview.policy_result.decision.toUpperCase()}
                    </span>
                  </div>
                  <p>Rule: <b>{policyPreview.rule_id}</b></p>
                  <p>{policyPreview.policy_result.reason}</p>
                  <div style={styles.controlGrid}>
                    {policyPreview.evaluated_controls.map((control) => (
                      <span key={control} style={styles.controlPill}>{control}</span>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>'''
    if marker not in s:
        raise SystemExit("policyPreview block marker not found")
    s = s.replace(marker, replacement)

if "function riskScoreStyle" not in s:
    marker = '''function decisionStyle(decision: string): CSSProperties {'''
    replacement = '''function riskScoreStyle(score: number): CSSProperties {
  if (score >= 80) {
    return { ...styles.badge, borderColor: "#ef4444", color: "#fca5a5", background: "rgba(127,29,29,.42)" };
  }

  if (score >= 50) {
    return { ...styles.badge, borderColor: "#f59e0b", color: "#fcd34d", background: "rgba(69,26,3,.45)" };
  }

  if (score >= 20) {
    return { ...styles.badge, borderColor: "#38bdf8", color: "#bae6fd", background: "rgba(8,47,73,.45)" };
  }

  return { ...styles.badge, borderColor: "#22c55e", color: "#86efac", background: "rgba(20,83,45,.45)" };
}

function decisionStyle(decision: string): CSSProperties {'''
    if marker not in s:
        raise SystemExit("decisionStyle marker not found")
    s = s.replace(marker, replacement)

if "riskEngine:" not in s:
    marker = '''  policyPreview: {
    border: "1px solid #334155",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "#020617",
    display: "grid",
    gap: 8
  },'''
    replacement = '''  policyPreview: {
    border: "1px solid #334155",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "#020617",
    display: "grid",
    gap: 8
  },
  riskEngine: {
    border: "1px solid #f59e0b",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "rgba(69,26,3,.22)"
  },
  policyEngine: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "rgba(8,47,73,.35)"
  },
  compactList: {
    marginTop: 10,
    paddingLeft: 18,
    color: "#cbd5e1"
  },
  controlGrid: {
    display: "flex",
    flexWrap: "wrap",
    gap: 8,
    marginTop: 12
  },
  controlPill: {
    border: "1px solid #334155",
    borderRadius: 999,
    padding: "5px 9px",
    color: "#cbd5e1",
    fontSize: 11,
    background: "#020617"
  },'''
    if marker not in s:
        raise SystemExit("styles marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 4 frontend patch applied")
