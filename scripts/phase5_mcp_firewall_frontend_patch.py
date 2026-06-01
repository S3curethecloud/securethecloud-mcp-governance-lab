from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

if "type MCPToolFirewallDecision" not in s:
    marker = '''type PolicyPreview = {
  requested_tool: string;
  requested_resource: string;
  data_classification: string;
  risk_evaluation: RiskEvaluation;
  policy_result: PolicyResult;
  evaluated_controls: string[];
  rule_id: string;
};'''
    replacement = '''type PolicyPreview = {
  requested_tool: string;
  requested_resource: string;
  data_classification: string;
  risk_evaluation: RiskEvaluation;
  policy_result: PolicyResult;
  evaluated_controls: string[];
  rule_id: string;
};

type MCPToolFirewallDecision = {
  tool: string;
  status: "allowed" | "blocked" | "requires_approval" | "redacted" | "escalated";
  risk_tier: string;
  reason: string;
  rule_id: string;
};'''
    if marker not in s:
        raise SystemExit("PolicyPreview type marker not found")
    s = s.replace(marker, replacement)

if "const [firewallPreview" not in s:
    marker = '''  const [status, setStatus] = useState("Loading MCP governance telemetry...");
  const [lastDecision, setLastDecision] = useState<MCPRequest | null>(null);
  const [policyPreview, setPolicyPreview] = useState<PolicyPreview | null>(null);'''
    replacement = '''  const [status, setStatus] = useState("Loading MCP governance telemetry...");
  const [lastDecision, setLastDecision] = useState<MCPRequest | null>(null);
  const [policyPreview, setPolicyPreview] = useState<PolicyPreview | null>(null);
  const [firewallPreview, setFirewallPreview] = useState<MCPToolFirewallDecision[]>([]);'''
    if marker not in s:
        raise SystemExit("state marker not found")
    s = s.replace(marker, replacement)

if "async function loadFirewallPreview" not in s:
    marker = '''  async function loadPolicyPreview() {
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
    replacement = '''  async function loadPolicyPreview() {
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
  }

  async function loadFirewallPreview() {
    const res = await fetch(`${API_BASE}/api/mcp/firewall/preview`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    if (res.ok) {
      setFirewallPreview(await res.json());
    }
  }'''
    if marker not in s:
      raise SystemExit("loadPolicyPreview marker not found")
    s = s.replace(marker, replacement)

s = s.replace(
'''  useEffect(() => {
    const timer = setTimeout(() => {
      loadPolicyPreview().catch(() => undefined);
    }, 200);

    return () => clearTimeout(timer);
  }, [form]);''',
'''  useEffect(() => {
    const timer = setTimeout(() => {
      loadPolicyPreview().catch(() => undefined);
      loadFirewallPreview().catch(() => undefined);
    }, 200);

    return () => clearTimeout(timer);
  }, [form]);'''
)

s = s.replace(
'''        <section style={styles.workspaceThree}>''',
'''        <section style={styles.workspaceFour}>'''
)

if "MCP Tool-Call Firewall" not in s:
    marker = '''          </form>

          <div style={styles.panel}>
            <p style={styles.kicker}>MCP Server Layer</p>'''
    replacement = '''          </form>

          <div style={styles.panel}>
            <p style={styles.kicker}>Phase 5</p>
            <h2 style={styles.panelTitle}>MCP Tool-Call Firewall</h2>
            <p style={styles.muted}>
              Every MCP tool is inspected before execution. The firewall applies identity, classification,
              risk, approval, and policy checks before access is allowed.
            </p>

            <div style={styles.firewallDoctrine}>
              AI can reason and recommend. AI cannot invoke MCP tools until policy, approval,
              and evidence checks pass.
            </div>

            <div style={styles.feed}>
              {firewallPreview.map((item) => (
                <article key={item.tool} style={styles.firewallCard}>
                  <div style={styles.recordHead}>
                    <strong>{item.tool}</strong>
                    <span style={firewallStatusStyle(item.status)}>
                      {item.status.replace("_", " ").toUpperCase()}
                    </span>
                  </div>
                  <p>Risk: <b>{item.risk_tier.replaceAll("_", " ")}</b></p>
                  <p>{item.reason}</p>
                  <p style={styles.ruleText}>{item.rule_id}</p>
                </article>
              ))}
            </div>
          </div>

          <div style={styles.panel}>
            <p style={styles.kicker}>MCP Server Layer</p>'''
    if marker not in s:
        raise SystemExit("form closing marker not found")
    s = s.replace(marker, replacement)

if "function firewallStatusStyle" not in s:
    marker = '''function riskScoreStyle(score: number): CSSProperties {'''
    replacement = '''function firewallStatusStyle(status: string): CSSProperties {
  if (status === "allowed") {
    return { ...styles.badge, borderColor: "#22c55e", color: "#86efac", background: "rgba(20,83,45,.45)" };
  }

  if (status === "blocked") {
    return { ...styles.badge, borderColor: "#ef4444", color: "#fca5a5", background: "rgba(127,29,29,.42)" };
  }

  if (status === "requires_approval") {
    return { ...styles.badge, borderColor: "#f59e0b", color: "#fcd34d", background: "rgba(69,26,3,.45)" };
  }

  if (status === "redacted") {
    return { ...styles.badge, borderColor: "#38bdf8", color: "#bae6fd", background: "rgba(8,47,73,.45)" };
  }

  return { ...styles.badge, borderColor: "#e879f9", color: "#f5d0fe", background: "rgba(88,28,135,.35)" };
}

function riskScoreStyle(score: number): CSSProperties {'''
    if marker not in s:
        raise SystemExit("riskScoreStyle marker not found")
    s = s.replace(marker, replacement)

if "workspaceFour:" not in s:
    s = s.replace(
'''  workspaceThree: { display: "grid", gridTemplateColumns: "1fr 1fr 1.25fr", gap: 18, marginTop: 18 },''',
'''  workspaceThree: { display: "grid", gridTemplateColumns: "1fr 1fr 1.25fr", gap: 18, marginTop: 18 },
  workspaceFour: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1.2fr", gap: 18, marginTop: 18 },'''
    )

if "firewallDoctrine:" not in s:
    marker = '''  selectedTool: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "#020617"
  },'''
    replacement = '''  selectedTool: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "#020617"
  },
  firewallDoctrine: {
    border: "1px solid #e879f9",
    borderRadius: 16,
    padding: 14,
    marginTop: 18,
    background: "rgba(88,28,135,.22)",
    color: "#f5d0fe",
    fontWeight: 800
  },
  firewallCard: {
    border: "1px solid #334155",
    borderRadius: 16,
    padding: 16,
    background: "#020617"
  },
  ruleText: {
    color: "#94a3b8",
    fontSize: 12,
    borderTop: "1px solid #1e293b",
    paddingTop: 10,
    marginTop: 10
  },'''
    if marker not in s:
        raise SystemExit("selectedTool style marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 5 frontend MCP firewall patch applied")
