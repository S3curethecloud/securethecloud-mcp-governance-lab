from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

s = s.replace("clearance_level: 3,", "clearance_level: 4,", 1)

if "reviewer_action?: string | null;" not in s:
    marker = '''  created_at: string;
  policy_result: PolicyResult;
  final_outcome: string;
};'''
    replacement = '''  created_at: string;
  policy_result: PolicyResult;
  final_outcome: string;
  reviewer?: string | null;
  reviewer_action?: string | null;
  reviewer_note?: string | null;
  reviewed_at?: string | null;
};'''
    if marker not in s:
        raise SystemExit("MCPRequest type marker not found")
    s = s.replace(marker, replacement)

if 'const [reviewer, setReviewer]' not in s:
    marker = '''  const [lastDecision, setLastDecision] = useState<MCPRequest | null>(null);
  const [policyPreview, setPolicyPreview] = useState<PolicyPreview | null>(null);
  const [firewallPreview, setFirewallPreview] = useState<MCPToolFirewallDecision[]>([]);'''
    replacement = '''  const [lastDecision, setLastDecision] = useState<MCPRequest | null>(null);
  const [policyPreview, setPolicyPreview] = useState<PolicyPreview | null>(null);
  const [firewallPreview, setFirewallPreview] = useState<MCPToolFirewallDecision[]>([]);
  const [reviewer, setReviewer] = useState("Compliance Officer");'''
    if marker not in s:
        raise SystemExit("state marker not found")
    s = s.replace(marker, replacement)

if "const pendingApprovals" not in s:
    marker = '''  const executivePosture = useMemo(() => {
    if (!dashboard) {
      return "Loading";
    }

    if (dashboard.approval_requests > 0) {
      return "Review Required";
    }

    if (dashboard.policy_violations > 0) {
      return "Guarded";
    }

    return "Demo Ready";
  }, [dashboard]);'''
    replacement = '''  const executivePosture = useMemo(() => {
    if (!dashboard) {
      return "Loading";
    }

    if (dashboard.approval_requests > 0) {
      return "Review Required";
    }

    if (dashboard.policy_violations > 0) {
      return "Guarded";
    }

    return "Demo Ready";
  }, [dashboard]);

  const pendingApprovals = useMemo(
    () => requests.filter((request) => request.policy_result.decision === "approval_required"),
    [requests]
  );'''
    if marker not in s:
        raise SystemExit("executivePosture marker not found")
    s = s.replace(marker, replacement)

if "async function reviewRequest" not in s:
    marker = '''  async function submitRequest(event: FormEvent) {
    event.preventDefault();

    setStatus("Submitting governed MCP request...");

    const res = await fetch(`${API_BASE}/api/mcp/requests`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    if (!res.ok) {
      setStatus(`MCP request failed: ${res.status}`);
      return;
    }

    const created: MCPRequest = await res.json();
    setLastDecision(created);
    setStatus(`Decision recorded: ${created.policy_result.decision.toUpperCase()} / ${created.policy_result.risk_tier.replaceAll("_", " ").toUpperCase()}`);

    await loadData();
  }'''
    replacement = '''  async function submitRequest(event: FormEvent) {
    event.preventDefault();

    setStatus("Submitting governed MCP request...");

    const res = await fetch(`${API_BASE}/api/mcp/requests`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    if (!res.ok) {
      setStatus(`MCP request failed: ${res.status}`);
      return;
    }

    const created: MCPRequest = await res.json();
    setLastDecision(created);
    setStatus(`Decision recorded: ${created.policy_result.decision.toUpperCase()} / ${created.policy_result.risk_tier.replaceAll("_", " ").toUpperCase()}`);

    await loadData();
  }

  async function reviewRequest(requestId: string, action: "approve" | "reject" | "escalate") {
    setStatus(`${action.toUpperCase()} review submitted for ${requestId}...`);

    const res = await fetch(`${API_BASE}/api/mcp/requests/${requestId}/approval`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        action,
        reviewer,
        note: `Phase 6 reviewer action: ${action}`
      })
    });

    if (!res.ok) {
      setStatus(`Human review failed: ${res.status}`);
      return;
    }

    const updated: MCPRequest = await res.json();
    setLastDecision(updated);
    setStatus(`Human review complete: ${action.toUpperCase()} -> ${updated.policy_result.decision.toUpperCase()}`);

    await loadData();
  }'''
    if marker not in s:
        raise SystemExit("submitRequest marker not found")
    s = s.replace(marker, replacement)

s = s.replace(
    '<section style={styles.workspaceFour}>',
    '<section style={styles.workspaceFive}>'
)

if "Human Approval Workspace" not in s:
    marker = '''          <div style={styles.panel}>
            <p style={styles.kicker}>MCP Server Layer</p>'''
    replacement = '''          <div style={styles.panel}>
            <p style={styles.kicker}>Phase 6</p>
            <h2 style={styles.panelTitle}>Human Approval Workspace</h2>
            <p style={styles.muted}>
              High-risk MCP requests are routed for reviewer approval before tool execution is allowed.
            </p>

            <label style={styles.label}>Reviewer</label>
            <select
              style={styles.input}
              value={reviewer}
              onChange={(e) => setReviewer(e.target.value)}
            >
              <option>Compliance Officer</option>
              <option>Security Officer</option>
              <option>Data Steward</option>
              <option>Risk Executive</option>
              <option>System Owner</option>
            </select>

            <div style={styles.feed}>
              {pendingApprovals.length === 0 && (
                <div style={styles.empty}>No pending approval requests.</div>
              )}

              {pendingApprovals.map((request) => (
                <article key={request.request_id} style={styles.approvalCard}>
                  <div style={styles.recordHead}>
                    <div>
                      <strong>{request.requested_tool}</strong>
                      <p>{request.request_id}</p>
                    </div>
                    <span style={styles.approvalBadge}>APPROVAL REQUIRED</span>
                  </div>

                  <p>{request.user_identity} · {request.role} · {request.department}</p>
                  <p>Resource: <b>{request.requested_resource}</b></p>
                  <p>Classification: <b>{request.data_classification}</b> · Risk: <b>{request.policy_result.risk_tier.replaceAll("_", " ")}</b></p>
                  <p>{request.policy_result.reason}</p>

                  <div style={styles.reviewActions}>
                    <button type="button" style={styles.approveButton} onClick={() => reviewRequest(request.request_id, "approve")}>
                      Approve
                    </button>
                    <button type="button" style={styles.rejectButton} onClick={() => reviewRequest(request.request_id, "reject")}>
                      Reject
                    </button>
                    <button type="button" style={styles.escalateButton} onClick={() => reviewRequest(request.request_id, "escalate")}>
                      Escalate
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </div>

          <div style={styles.panel}>
            <p style={styles.kicker}>MCP Server Layer</p>'''
    if marker not in s:
        raise SystemExit("selected tool panel marker not found")
    s = s.replace(marker, replacement)

if "{request.reviewer_action &&" not in s:
    marker = '''                  <p>{request.policy_result.reason}</p>
                </article>'''
    replacement = '''                  <p>{request.policy_result.reason}</p>

                  {request.reviewer_action && (
                    <p style={styles.reviewEvidence}>
                      Reviewer: {request.reviewer} · Action: {request.reviewer_action.toUpperCase()}
                    </p>
                  )}
                </article>'''
    if marker not in s:
        raise SystemExit("evidence reviewer marker not found")
    s = s.replace(marker, replacement, 1)

if "workspaceFive:" not in s:
    marker = '''  workspaceFour: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1.2fr", gap: 18, marginTop: 18 },'''
    replacement = '''  workspaceFour: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1.2fr", gap: 18, marginTop: 18 },
  workspaceFive: { display: "grid", gridTemplateColumns: ".9fr 1fr 1fr 1fr 1.2fr", gap: 18, marginTop: 18 },'''
    if marker not in s:
        raise SystemExit("workspaceFour style marker not found")
    s = s.replace(marker, replacement)

if "approvalCard:" not in s:
    marker = '''  firewallCard: {
    border: "1px solid #334155",
    borderRadius: 16,
    padding: 16,
    background: "#020617"
  },'''
    replacement = '''  firewallCard: {
    border: "1px solid #334155",
    borderRadius: 16,
    padding: 16,
    background: "#020617"
  },
  approvalCard: {
    border: "1px solid #f59e0b",
    borderRadius: 16,
    padding: 16,
    background: "rgba(69,26,3,.22)"
  },
  approvalBadge: {
    border: "1px solid #f59e0b",
    color: "#fcd34d",
    background: "rgba(69,26,3,.45)",
    borderRadius: 999,
    padding: "8px 12px",
    fontSize: 10,
    fontWeight: 900,
    whiteSpace: "nowrap"
  },
  reviewActions: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: 8,
    marginTop: 14
  },
  approveButton: {
    border: 0,
    borderRadius: 10,
    padding: 10,
    background: "#22c55e",
    color: "#052e16",
    fontWeight: 900,
    cursor: "pointer"
  },
  rejectButton: {
    border: 0,
    borderRadius: 10,
    padding: 10,
    background: "#f87171",
    color: "#450a0a",
    fontWeight: 900,
    cursor: "pointer"
  },
  escalateButton: {
    border: 0,
    borderRadius: 10,
    padding: 10,
    background: "#f59e0b",
    color: "#451a03",
    fontWeight: 900,
    cursor: "pointer"
  },
  reviewEvidence: {
    marginTop: 10,
    color: "#86efac",
    borderTop: "1px solid #334155",
    paddingTop: 10
  },
  empty: {
    border: "1px dashed #475569",
    borderRadius: 16,
    padding: 18,
    color: "#cbd5e1",
    textAlign: "center"
  },'''
    if marker not in s:
        raise SystemExit("firewallCard style marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 6 frontend approval patch applied")
