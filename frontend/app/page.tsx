"use client";

import { useEffect, useMemo, useState } from "react";
import type { CSSProperties, FormEvent } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  (typeof window !== "undefined" &&
  window.location.hostname !== "localhost" &&
  window.location.hostname !== "127.0.0.1"
    ? "https://securethecloud-mcp-governance-lab-api.fly.dev"
    : "http://localhost:8000");

type MCPTool = {
  name: string;
  label: string;
  description: string;
  sensitivity: string;
  default_risk_tier: string;
};

type PolicyResult = {
  decision: string;
  risk_tier: string;
  reason: string;
  approval_required: boolean;
  redaction_required: boolean;
  blocked: boolean;
};

type MCPRequest = {
  request_id: string;
  user_identity: string;
  role: string;
  department: string;
  business_unit: string;
  clearance_level: number;
  agent_identity: string;
  service_identity: string;
  environment_context: string;
  business_purpose: string;
  requested_tool: string;
  requested_resource: string;
  data_classification: string;
  approval_status: string;
  created_at: string;
  policy_result: PolicyResult;
  final_outcome: string;
  reviewer?: string | null;
  reviewer_action?: string | null;
  reviewer_note?: string | null;
  reviewed_at?: string | null;
};

type Dashboard = {
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
};

type MCPToolFirewallDecision = {
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
};

const initialForm = {
  user_identity: "Riley Brooks",
  role: "Support Analyst",
  department: "Customer Operations",
  business_unit: "Customer Trust",
  clearance_level: 4,
  agent_identity: "securethecloud-demo-agent",
  service_identity: "mcp-lab-service",
  environment_context: "demo",
  business_purpose: "Resolve customer escalation with governed MCP access",
  requested_tool: "read_customer_record",
  requested_resource: "customer profile",
  data_classification: "restricted",
  approval_status: "not_requested"
};

const fabricModules = [
  ["Governance & Policy", "Identity-aware MCP policy evaluation", "#22d3ee"],
  ["Evidence & Audit", "Replayable decision records for every MCP request", "#6ee75f"],
  ["Risk Intelligence", "Risk-tiered MCP tool access decisions", "#38bdf8"],
  ["Identity / Context", "User, agent, service, role, department, and environment", "#f59e0b"],
  ["MCP Tool Firewall", "Final checkpoint before enterprise tool execution", "#e879f9"]
];

const platformLayers = [
  ["AI Access Request Portal", "Entry point for governed AI and MCP requests"],
  ["MCP Server Layer", "Enterprise-style tools exposed through controlled interfaces"],
  ["Identity Context Engine", "Builds identity and agent context before policy evaluation"],
  ["Data Classification Layer", "Classifies public, internal, confidential, restricted, and regulated data"],
  ["Policy Decision Engine", "Returns allow, deny, redact, approval_required, or escalate"],
  ["Evidence Replay", "Auditor-ready reconstruction of request history"]
];

export default function Home() {
  const [tools, setTools] = useState<MCPTool[]>([]);
  const [requests, setRequests] = useState<MCPRequest[]>([]);
  const [dashboard, setDashboard] = useState<Dashboard | null>(null);
  const [executiveSummary, setExecutiveSummary] = useState<ExecutiveSummary | null>(null);
  const [form, setForm] = useState(initialForm);
  const [status, setStatus] = useState("Loading MCP governance telemetry...");
  const [lastDecision, setLastDecision] = useState<MCPRequest | null>(null);
  const [policyPreview, setPolicyPreview] = useState<PolicyPreview | null>(null);
  const [firewallPreview, setFirewallPreview] = useState<MCPToolFirewallDecision[]>([]);
  const [evidenceTimeline, setEvidenceTimeline] = useState<EvidenceTimeline | null>(null);
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string | null>(null);
  const [reviewer, setReviewer] = useState("Compliance Officer");

  async function loadData() {
    const [toolsRes, requestsRes, dashboardRes, executiveRes] = await Promise.all([
      fetch(`${API_BASE}/api/mcp/tools`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/mcp/requests`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/dashboard`, { cache: "no-store" }),
      fetch(`${API_BASE}/api/executive/summary`, { cache: "no-store" })
    ]);

    const nextRequests: MCPRequest[] = await requestsRes.json();

    setTools(await toolsRes.json());
    setRequests(nextRequests);
    setDashboard(await dashboardRes.json());
    setExecutiveSummary(await executiveRes.json());
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
  }

  useEffect(() => {
    loadData().catch((error) => setStatus(`Backend connection failed: ${error.message}`));
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadPolicyPreview().catch(() => undefined);
      loadFirewallPreview().catch(() => undefined);
    }, 200);

    return () => clearTimeout(timer);
  }, [form]);

  const selectedTool = useMemo(
    () => tools.find((tool) => tool.name === form.requested_tool),
    [tools, form.requested_tool]
  );

  const executivePosture = useMemo(() => {
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
  );

  async function submitRequest(event: FormEvent) {
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
    setSelectedEvidenceId(created.request_id);
    await loadEvidenceTimeline(created.request_id);
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
    setSelectedEvidenceId(updated.request_id);
    await loadEvidenceTimeline(updated.request_id);
    setStatus(`Human review complete: ${action.toUpperCase()} -> ${updated.policy_result.decision.toUpperCase()}`);

    await loadData();
  }

  return (
    <main style={styles.page}>
      <section style={styles.shell}>
        <header style={styles.hero}>
          <div>
            <div style={styles.brand}>🛡️ SecureTheCloud</div>
            <p style={styles.kicker}>MCP Governance Lab</p>
            <h1 style={styles.title}>SecureTheCloud MCP Governance Lab</h1>
            <p style={styles.subtitle}>
              Simulate governed Model Context Protocol tool access before AI agents can retrieve sensitive information,
              invoke enterprise-style tools, execute workflows, or perform business actions.
            </p>
          </div>

          <div style={styles.doctrine}>
            <strong>Core Principle</strong>
            <span>AI can assist, recommend, and explain.</span>
            <span>AI cannot bypass governance.</span>
            <span>AI cannot invoke MCP-style tools without identity, policy, approval, and evidence validation.</span>
          </div>
        </header>

        <section style={styles.fabric}>
          <h2 style={styles.sectionTitle}>Shared Trust Fabric</h2>
          <p style={styles.sectionSub}>Common governance services for MCP-enabled AI tool access.</p>

          <div style={styles.fabricGrid}>
            {fabricModules.map(([name, desc, color]) => (
              <div key={name} style={{ ...styles.fabricCard, borderColor: color }}>
                <div style={{ ...styles.hex, color }}>⬡</div>
                <strong>{name}</strong>
                <span>{desc}</span>
              </div>
            ))}
          </div>
        </section>

        <section style={styles.demoBoundary}>
          <div style={styles.boundaryCard}>
            <strong>Public Demo Boundary</strong>
            <span>Simulated MCP governance workflow. No real MCP servers, customer records, regulated data, or enterprise systems are connected.</span>
          </div>
          <div style={styles.boundaryCard}>
            <strong>Recruiter / Client Story</strong>
            <span>Shows identity-aware AI tool governance, policy decisions, approvals, firewall checks, evidence replay, and executive visibility.</span>
          </div>
          <div style={styles.boundaryCard}>
            <strong>Correct Claim</strong>
            <span>Production-shaped lab, not production enforcement. Demonstrates the control pattern safely and honestly.</span>
          </div>
        </section>

        {dashboard && (
          <section style={styles.metrics}>
            <Metric label="MCP Requests" value={dashboard.total_mcp_requests} />
            <Metric label="Allowed" value={dashboard.allowed_requests} />
            <Metric label="Denied" value={dashboard.denied_requests} />
            <Metric label="Approval Requests" value={dashboard.approval_requests} />
            <Metric label="Redacted" value={dashboard.redacted_responses} />
            <Metric label="Governance Coverage" value={`${dashboard.governance_coverage}%`} />
          </section>
        )}

        <section style={styles.executive}>
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
        )}

        <section style={styles.layerSection}>
          <h2 style={styles.sectionTitle}>Platform Layers</h2>
          <div style={styles.layerGrid}>
            {platformLayers.map(([name, desc]) => (
              <div key={name} style={styles.layerCard}>
                <div style={styles.cube}>◇</div>
                <div>
                  <strong>{name}</strong>
                  <p>{desc}</p>
                  <span style={styles.ready}>Demo Ready</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section style={styles.workspaceFive}>
          <form onSubmit={submitRequest} style={styles.panel}>
            <p style={styles.kicker}>Phase 3</p>
            <h2 style={styles.panelTitle}>MCP Access Request Portal</h2>
            <p style={styles.muted}>
              Submit a governed MCP tool request with identity, business purpose, classification, and approval context.
            </p>

            <Input label="User Identity" value={form.user_identity} onChange={(v) => setForm({ ...form, user_identity: v })} />
            <Input label="Role" value={form.role} onChange={(v) => setForm({ ...form, role: v })} />
            <Input label="Department" value={form.department} onChange={(v) => setForm({ ...form, department: v })} />
            <Input label="Business Unit" value={form.business_unit} onChange={(v) => setForm({ ...form, business_unit: v })} />

            <label style={styles.label}>Clearance Level</label>
            <select
              style={styles.input}
              value={form.clearance_level}
              onChange={(e) => setForm({ ...form, clearance_level: Number(e.target.value) })}
            >
              <option value={0}>0 - No clearance</option>
              <option value={1}>1 - Basic</option>
              <option value={2}>2 - Internal</option>
              <option value={3}>3 - Confidential</option>
              <option value={4}>4 - Restricted</option>
              <option value={5}>5 - Regulated/Admin</option>
            </select>

            <Input label="Agent Identity" value={form.agent_identity} onChange={(v) => setForm({ ...form, agent_identity: v })} />
            <Input label="Service Identity" value={form.service_identity} onChange={(v) => setForm({ ...form, service_identity: v })} />

            <label style={styles.label}>Environment Context</label>
            <select
              style={styles.input}
              value={form.environment_context}
              onChange={(e) => setForm({ ...form, environment_context: e.target.value })}
            >
              <option value="demo">demo</option>
              <option value="staging">staging</option>
              <option value="approved_lab">approved_lab</option>
              <option value="unknown">unknown</option>
              <option value="production">production</option>
            </select>

            <label style={styles.label}>Requested MCP Tool</label>
            <select
              style={styles.input}
              value={form.requested_tool}
              onChange={(e) => setForm({ ...form, requested_tool: e.target.value })}
            >
              {tools.map((tool) => (
                <option key={tool.name} value={tool.name}>
                  {tool.name}
                </option>
              ))}
            </select>

            <Input label="Requested Resource" value={form.requested_resource} onChange={(v) => setForm({ ...form, requested_resource: v })} />

            <label style={styles.label}>Data Classification</label>
            <select
              style={styles.input}
              value={form.data_classification}
              onChange={(e) => setForm({ ...form, data_classification: e.target.value })}
            >
              <option value="public">public</option>
              <option value="internal">internal</option>
              <option value="confidential">confidential</option>
              <option value="restricted">restricted</option>
              <option value="regulated">regulated</option>
            </select>

            <label style={styles.label}>Approval Status</label>
            <select
              style={styles.input}
              value={form.approval_status}
              onChange={(e) => setForm({ ...form, approval_status: e.target.value })}
            >
              <option value="not_requested">not_requested</option>
              <option value="approved">approved</option>
              <option value="rejected">rejected</option>
              <option value="escalated">escalated</option>
            </select>

            <label style={styles.label}>Business Purpose</label>
            <textarea
              style={{ ...styles.input, minHeight: 90 }}
              value={form.business_purpose}
              onChange={(e) => setForm({ ...form, business_purpose: e.target.value })}
            />

            <button style={styles.button}>Submit Governed MCP Request</button>

            {lastDecision && (
              <div style={styles.decisionCard}>
                <span>Latest Decision</span>
                <strong>{lastDecision.policy_result.decision.toUpperCase()}</strong>
                <small>{lastDecision.policy_result.reason}</small>
              </div>
            )}
          </form>

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
            <p style={styles.kicker}>MCP Server Layer</p>
            <h2 style={styles.panelTitle}>Selected Tool Context</h2>
            <p style={styles.muted}>The selected MCP tool is evaluated before execution is permitted.</p>

            {selectedTool && (
              <div style={styles.selectedTool}>
                <strong>{selectedTool.name}</strong>
                <p>{selectedTool.description}</p>
                <p>Sensitivity: <b>{selectedTool.sensitivity}</b></p>
                <p>Default risk: <b>{selectedTool.default_risk_tier.replaceAll("_", " ")}</b></p>
              </div>
            )}

            <div style={styles.policyPreview}>
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
                  <p style={styles.ruleLine}>
                    Rule:<br />
                    <b style={styles.breakAnywhere}>{policyPreview.rule_id}</b>
                  </p>
                  <p>{policyPreview.policy_result.reason}</p>
                  <div style={styles.controlGrid}>
                    {policyPreview.evaluated_controls.map((control) => (
                      <span key={control} style={styles.controlPill}>{control}</span>
                    ))}
                  </div>
                </div>
              </>
            )}
          </div>

          <div style={{ ...styles.panel, ...styles.evidenceWide }}>
            <p style={styles.kicker}>Evidence Replay</p>
            <h2 style={styles.panelTitle}>Latest MCP Governance Decisions</h2>
            <p style={styles.muted}>Every request is recorded as governance evidence. Select a record to replay the governed decision timeline.</p>

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

            <div style={styles.feed}>
              {requests.map((request) => (
                <article
                  key={request.request_id}
                  style={{ ...styles.record, ...(selectedEvidenceId === request.request_id ? styles.selectedEvidenceRecord : {}) }}
                  onClick={() => {
                    setSelectedEvidenceId(request.request_id);
                    loadEvidenceTimeline(request.request_id).catch(() => undefined);
                  }}
                >
                  <div style={styles.recordHead}>
                    <div>
                      <strong>{request.requested_tool}</strong>
                      <p>{request.request_id}</p>
                    </div>
                    <span style={decisionStyle(request.policy_result.decision)}>
                      {request.policy_result.decision.toUpperCase()}
                    </span>
                  </div>

                  <p>{request.user_identity} · {request.role} · {request.department}</p>
                  <p>
                    Resource: <b>{request.requested_resource}</b> · Classification: <b>{request.data_classification}</b>
                  </p>
                  <p>
                    Risk: <b>{request.policy_result.risk_tier.replaceAll("_", " ")}</b>
                  </p>
                  <p>{request.policy_result.reason}</p>

                  {request.reviewer_action && (
                    <p style={styles.reviewEvidence}>
                      Reviewer: {request.reviewer} · Action: {request.reviewer_action.toUpperCase()}
                    </p>
                  )}
                </article>
              ))}
            </div>
          </div>
        </section>

        <footer style={styles.footer}>
          Simulated MCP-style tools demonstrate AI governance · No real enterprise systems or customer data are connected
        </footer>
      </section>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
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
}

function Input({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) {
  return (
    <>
      <label style={styles.label}>{label}</label>
      <input style={styles.input} value={value} onChange={(e) => onChange(e.target.value)} />
    </>
  );
}

function firewallStatusStyle(status: string): CSSProperties {
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

function riskScoreStyle(score: number): CSSProperties {
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

function decisionStyle(decision: string): CSSProperties {
  if (decision === "allow") {
    return { ...styles.badge, borderColor: "#22c55e", color: "#86efac", background: "rgba(20,83,45,.45)" };
  }

  if (decision === "deny") {
    return { ...styles.badge, borderColor: "#ef4444", color: "#fca5a5", background: "rgba(127,29,29,.42)" };
  }

  if (decision === "approval_required") {
    return { ...styles.badge, borderColor: "#f59e0b", color: "#fcd34d", background: "rgba(69,26,3,.45)" };
  }

  return { ...styles.badge, borderColor: "#38bdf8", color: "#bae6fd", background: "rgba(8,47,73,.45)" };
}

const styles: Record<string, CSSProperties> = {
  page: {
    minHeight: "100vh",
    background: "radial-gradient(circle at top left,#132b46,#06111f 45%,#020617)",
    color: "#eaf2ff",
    fontFamily: "Inter, Arial, sans-serif",
    padding: 28
  },
  shell: { maxWidth: 1480, margin: "0 auto" },
  hero: {
    border: "1px solid #334155",
    borderRadius: 24,
    padding: 34,
    display: "flex",
    justifyContent: "space-between",
    gap: 24,
    background: "rgba(15,23,42,.78)",
    boxShadow: "0 24px 80px rgba(0,0,0,.35)"
  },
  brand: { fontSize: 24, fontWeight: 900, color: "#facc15", marginBottom: 18 },
  kicker: { color: "#67e8f9", textTransform: "uppercase", letterSpacing: 2, fontSize: 12, fontWeight: 800 },
  title: { fontSize: 54, lineHeight: 0.95, margin: "10px 0", fontWeight: 950 },
  subtitle: { color: "#cbd5e1", fontSize: 18, maxWidth: 820 },
  doctrine: {
    border: "1px solid #94a3b8",
    borderRadius: 16,
    padding: 18,
    minWidth: 340,
    display: "grid",
    gap: 10,
    background: "rgba(2,6,23,.6)"
  },
  fabric: {
    marginTop: 18,
    border: "1px solid #475569",
    borderRadius: 22,
    padding: 22,
    background: "rgba(2,6,23,.6)"
  },
  sectionTitle: { textAlign: "center", textTransform: "uppercase", letterSpacing: 5, fontSize: 24, margin: 0 },
  sectionTitleLeft: { textTransform: "uppercase", letterSpacing: 4, fontSize: 24, margin: "4px 0" },
  sectionSub: { textAlign: "center", color: "#cbd5e1", marginTop: 6 },
  sectionSubLeft: { color: "#cbd5e1", marginTop: 6, maxWidth: 760 },
  fabricGrid: { display: "grid", gridTemplateColumns: "repeat(5, minmax(0, 1fr))", gap: 16, marginTop: 18 },
  fabricCard: {
    border: "2px solid",
    borderRadius: 12,
    padding: 18,
    background: "linear-gradient(135deg,rgba(8,47,73,.55),rgba(2,6,23,.8))",
    minHeight: 126,
    display: "grid",
    gap: 8
  },
  hex: { fontSize: 34 },
  demoBoundary: {
    display: "grid",
    gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
    gap: 14,
    marginTop: 18
  },
  boundaryCard: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    background: "rgba(8,47,73,.28)",
    display: "grid",
    gap: 8
  },
  metrics: { display: "grid", gridTemplateColumns: "repeat(6, minmax(0, 1fr))", gap: 14, marginTop: 18 },
  metric: {
    border: "1px solid #334155",
    borderRadius: 18,
    padding: 18,
    background: "rgba(15,23,42,.8)",
    display: "grid",
    gap: 6
  },
  executive: {
    marginTop: 18,
    border: "1px solid #475569",
    borderRadius: 22,
    padding: 22,
    background: "linear-gradient(135deg,rgba(15,23,42,.9),rgba(2,6,23,.72))",
    display: "flex",
    justifyContent: "space-between",
    gap: 18
  },
  posture: {
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
  },
  layerSection: {
    marginTop: 18,
    border: "1px solid #475569",
    borderRadius: 22,
    padding: 22,
    background: "rgba(2,6,23,.6)"
  },
  layerGrid: { display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 14, marginTop: 18 },
  layerCard: {
    border: "1px solid #22d3ee",
    borderRadius: 14,
    padding: 18,
    display: "flex",
    gap: 14,
    background: "rgba(8,47,73,.28)"
  },
  cube: { color: "#6ee75f", fontSize: 36 },
  ready: {
    display: "inline-block",
    marginTop: 8,
    border: "1px solid #6ee75f",
    color: "#86efac",
    borderRadius: 999,
    padding: "4px 12px",
    fontSize: 12
  },
  workspaceThree: { display: "grid", gridTemplateColumns: "1fr 1fr 1.25fr", gap: 18, marginTop: 18 },
  workspaceFour: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1.2fr", gap: 18, marginTop: 18 },
  workspaceFive: {
    display: "grid",
    gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
    gap: 18,
    marginTop: 18,
    alignItems: "start"
  },
  panel: {
    border: "1px solid #334155",
    borderRadius: 22,
    padding: 24,
    background: "rgba(15,23,42,.86)",
    minWidth: 0,
    overflow: "hidden"
  },
  panelTitle: { fontSize: 26, margin: "8px 0" },
  evidenceWide: { gridColumn: "span 2" },
  muted: { color: "#cbd5e1" },
  label: { display: "block", marginTop: 12, marginBottom: 5, color: "#cbd5e1", fontSize: 13, fontWeight: 700 },
  input: {
    width: "100%",
    boxSizing: "border-box",
    borderRadius: 12,
    border: "1px solid #475569",
    background: "#020617",
    color: "#eaf2ff",
    padding: 12,
    minHeight: 42
  },
  button: {
    marginTop: 16,
    width: "100%",
    border: 0,
    borderRadius: 12,
    background: "#22d3ee",
    color: "#020617",
    padding: 14,
    fontWeight: 900,
    cursor: "pointer"
  },
  selectedTool: {
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
  },
  empty: {
    border: "1px dashed #475569",
    borderRadius: 16,
    padding: 18,
    color: "#cbd5e1",
    textAlign: "center"
  },
  ruleText: {
    color: "#94a3b8",
    fontSize: 12,
    borderTop: "1px solid #1e293b",
    paddingTop: 10,
    marginTop: 10
  },
  policyPreview: {
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
    background: "rgba(8,47,73,.35)",
    minWidth: 0,
    overflow: "hidden"
  },
  ruleLine: {
    minWidth: 0,
    overflowWrap: "anywhere",
    wordBreak: "break-word"
  },
  breakAnywhere: {
    overflowWrap: "anywhere",
    wordBreak: "break-word"
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
  },
  decisionCard: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "rgba(8,47,73,.45)",
    display: "grid",
    gap: 8
  },
  feed: { display: "grid", gap: 14, marginTop: 18 },
  record: { border: "1px solid #334155", borderRadius: 16, padding: 16, background: "#020617" },
  recordHead: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "start" },
  badge: {
    border: "1px solid #38bdf8",
    color: "#bae6fd",
    background: "rgba(8,47,73,.45)",
    borderRadius: 999,
    padding: "8px 12px",
    fontSize: 11,
    fontWeight: 900,
    whiteSpace: "nowrap"
  },
  footer: {
    marginTop: 18,
    border: "1px solid #334155",
    borderRadius: 14,
    padding: 14,
    textAlign: "center",
    color: "#cbd5e1",
    background: "rgba(15,23,42,.75)"
  }
};
