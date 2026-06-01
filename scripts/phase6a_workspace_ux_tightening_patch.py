from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

# Keep the current JSX structure but make the workspace flow into 3 readable columns instead of 5 squeezed columns.
s = s.replace(
'''  workspaceFive: { display: "grid", gridTemplateColumns: ".9fr 1fr 1fr 1fr 1.2fr", gap: 18, marginTop: 18 },''',
'''  workspaceFive: {
    display: "grid",
    gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
    gap: 18,
    marginTop: 18,
    alignItems: "start"
  },'''
)

# Make evidence replay span two columns on the second row.
s = s.replace(
'''          <div style={styles.panel}>
            <p style={styles.kicker}>Evidence Replay</p>
            <h2 style={styles.panelTitle}>Latest MCP Governance Decisions</h2>''',
'''          <div style={{ ...styles.panel, ...styles.evidenceWide }}>
            <p style={styles.kicker}>Evidence Replay</p>
            <h2 style={styles.panelTitle}>Latest MCP Governance Decisions</h2>'''
)

# Make phase labels current in the platform layer cards.
s = s.replace("Phase 3 Ready", "Phase 6 Ready")

# Make the hero and workspace slightly more comfortable on common laptop screens.
s = s.replace(
'''  shell: { maxWidth: 1500, margin: "0 auto" },''',
'''  shell: { maxWidth: 1480, margin: "0 auto" },'''
)

# Reduce title slightly to avoid oversized hero on smaller displays.
s = s.replace(
'''  title: { fontSize: 58, lineHeight: 0.95, margin: "10px 0", fontWeight: 950 },''',
'''  title: { fontSize: 54, lineHeight: 0.95, margin: "10px 0", fontWeight: 950 },'''
)

# Improve panel readability and prevent internal content from forcing horizontal overflow.
s = s.replace(
'''  panel: { border: "1px solid #334155", borderRadius: 22, padding: 24, background: "rgba(15,23,42,.86)" },''',
'''  panel: {
    border: "1px solid #334155",
    borderRadius: 22,
    padding: 24,
    background: "rgba(15,23,42,.86)",
    minWidth: 0,
    overflow: "hidden"
  },'''
)

# Add evidence-wide style.
if "evidenceWide:" not in s:
    s = s.replace(
'''  panelTitle: { fontSize: 26, margin: "8px 0" },''',
'''  panelTitle: { fontSize: 26, margin: "8px 0" },
  evidenceWide: { gridColumn: "span 2" },'''
    )

# Improve input readability now that columns are wider.
s = s.replace(
'''    padding: 12
  },''',
'''    padding: 12,
    minHeight: 42
  },''',
1
)

# Reduce very large card text pressure in narrow panels.
s = s.replace(
'''  fabricGrid: { display: "grid", gridTemplateColumns: "repeat(5,1fr)", gap: 16, marginTop: 18 },''',
'''  fabricGrid: { display: "grid", gridTemplateColumns: "repeat(5, minmax(0, 1fr))", gap: 16, marginTop: 18 },'''
)

# Make the metric row safer.
s = s.replace(
'''  metrics: { display: "grid", gridTemplateColumns: "repeat(6,1fr)", gap: 14, marginTop: 18 },''',
'''  metrics: { display: "grid", gridTemplateColumns: "repeat(6, minmax(0, 1fr))", gap: 14, marginTop: 18 },'''
)

p.write_text(s)
print("Phase 6A workspace UX tightening patch applied")
