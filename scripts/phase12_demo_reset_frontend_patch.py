from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

if "const [demoResetToken" not in s:
    s = s.replace(
        '  const [reviewer, setReviewer] = useState("Compliance Officer");',
        '''  const [reviewer, setReviewer] = useState("Compliance Officer");
  const [demoResetToken, setDemoResetToken] = useState("");
  const [demoResetStatus, setDemoResetStatus] = useState("Owner reset token required.");'''
    )

s = s.replace(
'''    const nextEvidenceId = selectedEvidenceId ?? nextRequests[0]?.request_id;
    if (nextEvidenceId) {''',
'''    const nextEvidenceId = nextRequests.some((request) => request.request_id === selectedEvidenceId)
      ? selectedEvidenceId
      : nextRequests[0]?.request_id;

    if (nextEvidenceId) {'''
)

if "async function resetDemo" not in s:
    marker = "  return (\n"
    reset_function = '''  async function resetDemo() {
    if (!demoResetToken.trim()) {
      setDemoResetStatus("Enter the owner reset token first.");
      return;
    }

    setDemoResetStatus("Resetting seeded demo records...");

    const res = await fetch(`${API_BASE}/api/demo/reset`, {
      method: "POST",
      headers: {
        "X-Demo-Reset-Token": demoResetToken.trim()
      }
    });

    if (!res.ok) {
      setDemoResetStatus(`Reset failed: ${res.status}`);
      return;
    }

    const result = await res.json();
    setDemoResetToken("");
    setSelectedEvidenceId(null);
    setEvidenceTimeline(null);
    setDemoResetStatus(`${result.message}. Records restored: ${result.reset_records}`);

    await loadData();
  }

'''
    if marker not in s:
        raise SystemExit("return marker not found")
    s = s.replace(marker, reset_function + marker, 1)

if "Demo Operations" not in s:
    marker = '''        <section style={styles.layerSection}>'''
    demo_ops = '''        <section style={styles.demoOps}>
          <div>
            <p style={styles.kicker}>Phase 12 · Recruiter Demo Hardening</p>
            <h2 style={styles.sectionTitleLeft}>Demo Operations</h2>
            <p style={styles.sectionSubLeft}>
              Restore the seeded demo state before interviews or client walkthroughs. The reset requires an owner token and does not expose real data.
            </p>
          </div>

          <div style={styles.demoResetCard}>
            <strong>Protected Demo Reset</strong>
            <input
              style={styles.input}
              type="password"
              value={demoResetToken}
              placeholder="Owner reset token"
              onChange={(e) => setDemoResetToken(e.target.value)}
            />
            <button type="button" style={styles.button} onClick={resetDemo}>
              Restore Seeded Demo
            </button>
            <small>{demoResetStatus}</small>
          </div>
        </section>

'''
    if marker not in s:
        raise SystemExit("layerSection marker not found")
    s = s.replace(marker, demo_ops + marker)

if "demoOps:" not in s:
    marker = '''  layerSection: {
    marginTop: 18,
    border: "1px solid #475569",
    borderRadius: 22,
    padding: 22,
    background: "rgba(2,6,23,.6)"
  },'''
    replacement = '''  demoOps: {
    marginTop: 18,
    border: "1px solid #22d3ee",
    borderRadius: 22,
    padding: 22,
    background: "rgba(8,47,73,.28)",
    display: "grid",
    gridTemplateColumns: "1.5fr 1fr",
    gap: 18,
    alignItems: "center"
  },
  demoResetCard: {
    border: "1px solid #334155",
    borderRadius: 16,
    padding: 16,
    background: "rgba(2,6,23,.78)",
    display: "grid",
    gap: 10
  },
  layerSection: {
    marginTop: 18,
    border: "1px solid #475569",
    borderRadius: 22,
    padding: 22,
    background: "rgba(2,6,23,.6)"
  },'''
    if marker not in s:
        raise SystemExit("layerSection style marker not found")
    s = s.replace(marker, replacement)

p.write_text(s)
print("Phase 12 frontend demo reset console patch applied")
