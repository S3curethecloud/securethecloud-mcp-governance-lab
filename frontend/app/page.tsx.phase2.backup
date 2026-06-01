"use client";

import { useEffect, useMemo, useState } from "react";
import type { CSSProperties } from "react";

const API_BASE = "http://localhost:8000";

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
  const [status, setStatus] = useState("Loading MCP governance telemetry...");

  async function loadData() {
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

  useEffect(() => {
    loadData().catch((error) => setStatus(`Backend connection failed: ${error.message}`));
  }, []);

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

  return (
    <main style={styles.page}>
      <section style={styles.shell}>
        <header style={styles.hero}>
          <div>
            <div style={styles.brand}>🛡️ SecureTheCloud</div>
            <p style={styles.kicker}>MCP Governance Lab</p>
            <h1 style={styles.title}>SecureTheCloud MCP Governance Lab</h1>
            <p style={styles.subtitle}>
              Govern Model Context Protocol tool access before AI agents can retrieve sensitive information,
              invoke enterprise tools, execute workflows, or perform business actions.
            </p>
          </div>

          <div style={styles.doctrine}>
            <strong>Core Principle</strong>
            <span>AI can assist, recommend, and explain.</span>
            <span>AI cannot bypass governance.</span>
            <span>AI cannot invoke MCP tools without identity, policy, approval, and evidence validation.</span>
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
        </section>

        <section style={styles.layerSection}>
          <h2 style={styles.sectionTitle}>Platform Layers</h2>
          <div style={styles.layerGrid}>
            {platformLayers.map(([name, desc]) => (
              <div key={name} style={styles.layerCard}>
                <div style={styles.cube}>◇</div>
                <div>
                  <strong>{name}</strong>
                  <p>{desc}</p>
                  <span style={styles.ready}>Phase 2 Ready</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section style={styles.workspace}>
          <div style={styles.panel}>
            <p style={styles.kicker}>MCP Server Layer</p>
            <h2 style={styles.panelTitle}>Governed MCP Tools</h2>
            <p style={styles.muted}>V1 enterprise-style MCP tools exposed for governed demo requests.</p>

            <div style={styles.feed}>
              {tools.map((tool) => (
                <article key={tool.name} style={styles.record}>
                  <div style={styles.recordHead}>
                    <strong>{tool.name}</strong>
                    <span style={styles.badge}>{tool.default_risk_tier.replaceAll("_", " ").toUpperCase()}</span>
                  </div>
                  <p>{tool.description}</p>
                  <p>Sensitivity: <b>{tool.sensitivity}</b></p>
                </article>
              ))}
            </div>
          </div>

          <div style={styles.panel}>
            <p style={styles.kicker}>Evidence Preview</p>
            <h2 style={styles.panelTitle}>Seeded Governance Decisions</h2>
            <p style={styles.muted}>Live evidence records from the Phase 1 backend.</p>

            <div style={styles.feed}>
              {requests.map((request) => (
                <article key={request.request_id} style={styles.record}>
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
                  <p>{request.policy_result.reason}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <footer style={styles.footer}>
          MCP gives AI agents access to tools · SecureTheCloud governs those tools before they are used
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
  shell: { maxWidth: 1440, margin: "0 auto" },
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
  title: { fontSize: 58, lineHeight: 0.95, margin: "10px 0", fontWeight: 950 },
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
  fabricGrid: { display: "grid", gridTemplateColumns: "repeat(5,1fr)", gap: 16, marginTop: 18 },
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
  metrics: { display: "grid", gridTemplateColumns: "repeat(6,1fr)", gap: 14, marginTop: 18 },
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
  workspace: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, marginTop: 18 },
  panel: { border: "1px solid #334155", borderRadius: 22, padding: 24, background: "rgba(15,23,42,.86)" },
  panelTitle: { fontSize: 26, margin: "8px 0" },
  muted: { color: "#cbd5e1" },
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
