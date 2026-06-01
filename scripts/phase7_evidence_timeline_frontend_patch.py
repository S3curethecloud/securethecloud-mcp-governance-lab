from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

if "type EvidenceTimelineStep" not in s:
    marker = '''type MCPToolFirewallDecision = {
  tool: string;
  status: "allowed" | "blocked" | "requires_approval" | "redacted" | "escalated";
  risk_tier: string;
  reason: string;
  rule_id: string;
};'''
    replacement = '''type MCPToolFirewallDecision = {
  tool: string;
  status: "allowed" | "blocked" | "requires_approval" | "redacted" | "escalated";
  risk_tier: string;
  reason: string;
  rule_id: string;
};

type EvidenceTimelineStep = {
  step: string;
  label: string;
  status: string;
  detail: string;
  timestamp?: string | null;
};

type EvidenceTimeline = {
  request_id: string;
  requested_tool: string;
  final_outcome: string;
  steps: EvidenceTimelineStep[];
};'''
    if marker not in s:
        raise SystemExit("MCPToolFirewallDecision marker not found")
    s = s.replace(marker, replacement)

if "const [evidenceTimeline" not in s:
    marker = '''  const [policyPreview, setPolicyPreview] = useState<PolicyPreview | null>(null);
  const [firewallPreview, setFirewallPreview] = useState<MCPToolFirewallDecision[]>([]);
  const [reviewer, setReviewer] = useState("Compliance Officer");'''
    replacement = '''  const [policyPreview, setPolicyPreview] = useState<PolicyPreview | null>(null);
  const [firewallPreview, setFirewallPreview] = useState<MCPToolFirewallDecision[]>([]);
  const [evidenceTimeline, setEvidenceTimeline] = useState<EvidenceTimeline | null>(null);
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string | null>(null);
  const [reviewer, setReviewer] = useState("Compliance Officer");'''
    if marker not in s:
        raise SystemExit("state marker not found")
    s = s.replace(marker, replacement)

if "async function loadEvidenceTimeline" not in s:
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

    const nextRequests: MCPRequest[] = await requestsRes.json();

    setTools(await toolsRes.json());
    setRequests(nextRequests);
    setDashboard(await dashboardRes.json());
    setStatus("Live backend connected");

    const nextEvidenceId = selectedEvidenceId ?? nextRequests[0]?.request_id;
    if (nextEvidenceId) {
      setSelectedEvidenceId(nextEvidenceId);
      loadEvidenceTimeline(nextEvidenceId).catch(() => undefined);
    }
  }

  async function loadEvidenceTimeline(requestId: string) {
    const res = await fetch(`${API_BASE}/api/mcp/evidence/${requestId}/timeline`, {
      cache: "no-store"
    });

    if (res.ok) {
      setEvidenceTimeline(await res.json());
    }
  }'''
    if marker not in s:
        raise SystemExit("loadData marker not found")
    s = s.replace(marker, replacement)

s = s.replace(
'''    const created: MCPRequest = await res.json();
    setLastDecision(created);
    setStatus(`Decision recorded: ${created.policy_result.decision.toUpperCase()} / ${created.policy_result.risk_tier.replaceAll("_", " ").toUpperCase()}`);

    await loadData();''',
'''    const created: MCPRequest = await res.json();
    setLastDecision(created);
    setSelectedEvidenceId(created.request_id);
    await loadEvidenceTimeline(created.request_id);
    setStatus(`Decision recorded: ${created.policy_result.decision.toUpperCase()} / ${created.policy_result.risk_tier.replaceAll("_", " ").toUpperCase()}`);

    await loadData();'''
)

s = s.replace(
'''    const updated: MCPRequest = await res.json();
    setLastDecision(updated);
    setStatus(`Human review complete: ${action.toUpperCase()} -> ${updated.policy_result.decision.toUpperCase()}`);

    await loadData();''',
'''    const updated: MCPRequest = await res.json();
    setLastDecision(updated);
    setSelectedEvidenceId(updated.request_id);
    await loadEvidenceTimeline(updated.request_id);
    setStatus(`Human review complete: ${action.toUpperCase()} -> ${updated.policy_result.decision.toUpperCase()}`);

    await loadData();'''
)

if "Evidence Timeline" not in s:
    marker = '''            <p style={styles.muted}>Every request is recorded as governance evidence.</p>

            <div style={styles.feed}>'''
    replacement = '''            <p style={styles.muted}>Every request is recorded as governance evidence. Select a record to replay the governed decision timeline.</p>

            {evidenceTimeline && (
              <div style={styles.timelinePanel}>
                <div style={styles.recordHead}>
                  <div>
                    <strong>Evidence Timeline</strong>
                    <p>{evidenceTimeline.request_id} · {evidenceTimeline.requested_tool}</p>
                  </div>
                  <span style={decisionStyle(evidenceTimeline.final_outcome)}>
                    {evidenceTimeline.final_outcome.toUpperCase()}
                  </span>
                </div>

                <div style={styles.timelineSteps}>
                  {evidenceTimeline.steps.map((step) => (
                    <div key={`${step.step}-${step.label}`} style={styles.timelineStep}>
                      <div style={styles.timelineDot}>{step.step}</div>
                      <div>
                        <strong>{step.label}</strong>
                        <p>Status: <b>{step.status.replaceAll("_", " ")}</b></p>
                        <p>{step.detail}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div style={styles.feed}>'''
    if marker not in s:
        raise SystemExit("evidence muted marker not found")
    s = s.replace(marker, replacement)

s = s.replace(
'''                <article key={request.request_id} style={styles.record}>''',
'''                <article
                  key={request.request_id}
                  style={{ ...styles.record, ...(selectedEvidenceId === request.request_id ? styles.selectedEvidenceRecord : {}) }}
                  onClick={() => {
                    setSelectedEvidenceId(request.request_id);
                    loadEvidenceTimeline(request.request_id).catch(() => undefined);
                  }}
                >'''
)

if "timelinePanel:" not in s:
    marker = '''  reviewEvidence: {
    marginTop: 10,
    color: "#86efac",
    borderTop: "1px solid #334155",
    paddingTop: 10
  },'''
    replacement = '''  reviewEvidence: {
    marginTop: 10,
    color: "#86efac",
    borderTop: "1px solid #334155",
    paddingTop: 10
  },
  selectedEvidenceRecord: {
    borderColor: "#22d3ee",
    boxShadow: "0 0 0 1px rgba(34,211,238,.35)"
  },
  timelinePanel: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "rgba(8,47,73,.28)"
  },
  timelineSteps: {
    display: "grid",
    gap: 12,
    marginTop: 14
  },
  timelineStep: {
    display: "grid",
    gridTemplateColumns: "42px 1fr",
    gap: 12,
    borderTop: "1px solid #1e293b",
    paddingTop: 12
  },
  timelineDot: {
    height: 34,
    width: 34,
    borderRadius: 999,
    display: "grid",
    placeItems: "center",
    border: "1px solid #22d3ee",
    color: "#67e8f9",
    fontWeight: 900,
    background: "#020617"
  },'''
    if marker not in s:
        raise SystemExit("reviewEvidence style marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 7 frontend evidence timeline patch applied")
