from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

if "type ExecutiveSummary" not in s:
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

type ExecutiveSummary = {
  readiness_posture: string;
  readiness_reason: string;
  total_mcp_requests: number;
  sensitive_access_attempts: number;
  high_risk_activities: number;
  policy_violations: number;
  pending_approvals: number;
  completed_human_reviews: number;
  risk_tier_1_low: number;
  risk_tier_2_moderate: number;
  risk_tier_3_high: number;
  risk_tier_4_critical: number;
  decisions_allow: number;
  decisions_deny: number;
  decisions_redact: number;
  decisions_approval_required: number;
  decisions_escalate: number;
  firewall_allowed: number;
  firewall_blocked: number;
  firewall_requires_approval: number;
  firewall_redacted: number;
  firewall_escalated: number;
};'''
    if marker not in s:
        raise SystemExit("Dashboard type marker not found")
    s = s.replace(marker, replacement)

if "const [executiveSummary" not in s:
    marker = '''  const [requests, setRequests] = useState<MCPRequest[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [form, setForm] = useState(initialForm);'''
    replacement = '''  const [requests, setRequests] = useState<MCPRequest[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [executiveSummary, setExecutiveSummary] = useState<ExecutiveSummary | null>(null);
  const [form, setForm] = useState(initialForm);'''
    if marker not in s:
        raise SystemExit("state marker not found")
    s = s.replace(marker, replacement)

s = s.replace(
'''    const [toolsRes, requestsRes, dashboardRes] = await Promise.all([
      fetch(`${API_BASE}/api/mcp/tools`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/mcp/requests`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/dashboard`, { cache: "no-store" })
    ]);''',
'''    const [toolsRes, requestsRes, dashboardRes, executiveRes] = await Promise.all([
      fetch(`${API_BASE}/api/mcp/tools`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/mcp/requests`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/dashboard`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/executive/summary`, { cache: "no-store" })
    ]);'''
)

s = s.replace(
'''    setRequests(nextRequests);
    setDashboard(await dashboardRes.json());
    setStatus("Live backend connected");''',
'''    setRequests(nextRequests);
    setDashboard(await dashboardRes.json());
    setExecutiveSummary(await executiveRes.json());
    setStatus("Live backend connected");'''
)

# Replace old executive section with richer dashboard.
old = '''        <section style={styles.executive}>
          <div>
            <p style={styles.kicker}>Executive Governance View</p>
            <h2 style={styles.sectionTitleLeft}>MCP Risk & Control Center</h2>
            <p style={styles.sectionSubLeft}>
              Leadership visibility into MCP tool access, policy effectiveness, sensitive access attempts,
              high-risk activities, and governance posture.
            </p>
          </div>

          <div style={styles.posture}>
            <span>Readiness Posture</span>
            <strong>{executivePosture}</strong>
            <small>{status}</small>
          </div>
        </section>'''

new = '''        <section style={styles.executive}>
          <div>
            <p style={styles.kicker}>Phase 8 · Executive Governance Dashboard</p>
            <h2 style={styles.sectionTitleLeft}>MCP Risk & Control Center</h2>
            <p style={styles.sectionSubLeft}>
              Leadership visibility into MCP tool access, policy effectiveness, firewall posture,
              sensitive access attempts, high-risk activities, human review pressure, and governance readiness.
            </p>
          </div>

          <div style={styles.posture}>
            <span>Readiness Posture</span>
            <strong>{executiveSummary?.readiness_posture ?? executivePosture}</strong>
            <small>{executiveSummary?.readiness_reason ?? status}</small>
          </div>
        </section>

        {executiveSummary && (
          <section style={styles.executiveGrid}>
            <div style={styles.executiveCard}>
              <h3>Risk Distribution</h3>
              <Bar label="Tier 1 Low" value={executiveSummary.risk_tier_1_low} total={executiveSummary.total_mcp_requests} />
              <Bar label="Tier 2 Moderate" value={executiveSummary.risk_tier_2_moderate} total={executiveSummary.total_mcp_requests} />
              <Bar label="Tier 3 High" value={executiveSummary.risk_tier_3_high} total={executiveSummary.total_mcp_requests} />
              <Bar label="Tier 4 Critical" value={executiveSummary.risk_tier_4_critical} total={executiveSummary.total_mcp_requests} />
            </div>

            <div style={styles.executiveCard}>
              <h3>Decision Distribution</h3>
              <LineMetric label="Allowed" value={executiveSummary.decisions_allow} />
              <LineMetric label="Denied" value={executiveSummary.decisions_deny} />
              <LineMetric label="Approval Required" value={executiveSummary.decisions_approval_required} />
              <LineMetric label="Redacted" value={executiveSummary.decisions_redact} />
              <LineMetric label="Escalated" value={executiveSummary.decisions_escalate} />
            </div>

            <div style={styles.executiveCard}>
              <h3>Tool-Call Firewall Summary</h3>
              <LineMetric label="Allowed tools" value={executiveSummary.firewall_allowed} />
              <LineMetric label="Blocked tools" value={executiveSummary.firewall_blocked} />
              <LineMetric label="Requires approval" value={executiveSummary.firewall_requires_approval} />
              <LineMetric label="Redacted tools" value={executiveSummary.firewall_redacted} />
              <LineMetric label="Escalated tools" value={executiveSummary.firewall_escalated} />
            </div>

            <div style={styles.executiveCard}>
              <h3>Governance Health</h3>
              <LineMetric label="Sensitive attempts" value={executiveSummary.sensitive_access_attempts} />
              <LineMetric label="High-risk activities" value={executiveSummary.high_risk_activities} />
              <LineMetric label="Policy violations" value={executiveSummary.policy_violations} />
              <LineMetric label="Pending approvals" value={executiveSummary.pending_approvals} />
              <LineMetric label="Human reviews" value={executiveSummary.completed_human_reviews} />
            </div>
          </section>
        )}'''

if old not in s:
    raise SystemExit("executive section marker not found")
s = s.replace(old, new)

if "function Bar" not in s:
    marker = '''function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div style={styles.metric}>
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}'''
    replacement = '''function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div style={styles.metric}>
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

function LineMetric({ label, value }: { label: string; value: number | string }) {
  return (
    <div style={styles.lineMetric}>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Bar({ label, value, total }: { label: string; value: number; total: number }) {
  const width = total > 0 ? Math.max(4, Math.round((value / total) * 100)) : 0;

  return (
    <div style={styles.barRow}>
      <div style={styles.lineMetric}>
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
      <div style={styles.barTrack}>
        <div style={{ ...styles.barFill, width: `${width}%` }} />
      </div>
    </div>
  );
}'''
    if marker not in s:
        raise SystemExit("Metric function marker not found")
    s = s.replace(marker, replacement)

if "executiveGrid:" not in s:
    marker = '''  posture: {
    minWidth: 300,
    border: "1px solid #6ee75f",
    borderRadius: 16,
    padding: 18,
    background: "rgba(20,83,45,.22)",
    display: "grid",
    gap: 8
  },'''
    replacement = '''  posture: {
    minWidth: 300,
    border: "1px solid #6ee75f",
    borderRadius: 16,
    padding: 18,
    background: "rgba(20,83,45,.22)",
    display: "grid",
    gap: 8
  },
  executiveGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
    gap: 14,
    marginTop: 18
  },
  executiveCard: {
    border: "1px solid #334155",
    borderRadius: 18,
    padding: 18,
    background: "rgba(2,6,23,.78)"
  },
  lineMetric: {
    display: "flex",
    justifyContent: "space-between",
    gap: 10,
    borderTop: "1px solid #1e293b",
    paddingTop: 9,
    marginTop: 9
  },
  barRow: {
    display: "grid",
    gap: 6
  },
  barTrack: {
    height: 8,
    borderRadius: 999,
    background: "#0f172a",
    border: "1px solid #334155",
    overflow: "hidden"
  },
  barFill: {
    height: "100%",
    borderRadius: 999,
    background: "#22d3ee"
  },'''
    if marker not in s:
        raise SystemExit("posture style marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 8 frontend executive dashboard patch applied")
