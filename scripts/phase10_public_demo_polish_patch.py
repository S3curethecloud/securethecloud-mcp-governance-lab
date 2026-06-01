from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

# Honest public demo positioning.
s = s.replace(
    "Govern Model Context Protocol tool access before AI agents can retrieve sensitive information,\n              invoke enterprise tools, execute workflows, or perform business actions.",
    "Simulate governed Model Context Protocol tool access before AI agents can retrieve sensitive information,\n              invoke enterprise-style tools, execute workflows, or perform business actions."
)

s = s.replace(
    "AI cannot invoke MCP tools without identity, policy, approval, and evidence validation.",
    "AI cannot invoke MCP-style tools without identity, policy, approval, and evidence validation."
)

s = s.replace(
    "MCP gives AI agents access to tools · SecureTheCloud governs those tools before they are used",
    "Simulated MCP-style tools demonstrate AI governance · No real enterprise systems or customer data are connected"
)

s = s.replace("Phase 6 Ready", "Demo Ready")
s = s.replace("Phase 3 Ready", "Demo Ready")
s = s.replace("Phase 5", "Phase 5")
s = s.replace("Phase 6", "Phase 6")

# Add a public demo boundary strip after the Shared Trust Fabric section.
if "Public Demo Boundary" not in s:
    marker = '''        {dashboard && (
          <section style={styles.metrics}>'''
    insert = '''        <section style={styles.demoBoundary}>
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
          <section style={styles.metrics}>'''
    if marker not in s:
        raise SystemExit("metrics marker not found")
    s = s.replace(marker, insert)

# Add styles.
if "demoBoundary:" not in s:
    marker = '''  metrics: { display: "grid", gridTemplateColumns: "repeat(6, minmax(0, 1fr))", gap: 14, marginTop: 18 },'''
    replacement = '''  demoBoundary: {
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
  metrics: { display: "grid", gridTemplateColumns: "repeat(6, minmax(0, 1fr))", gap: 14, marginTop: 18 },'''
    if marker not in s:
        raise SystemExit("metrics style marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 10 public demo polish applied")
