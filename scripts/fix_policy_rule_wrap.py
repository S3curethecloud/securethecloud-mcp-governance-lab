from pathlib import Path

p = Path("frontend/app/page.tsx")
s = p.read_text()

old = '<p>Rule: <b>{policyPreview.rule_id}</b></p>'
new = '''<p style={styles.ruleLine}>
                    Rule:<br />
                    <b style={styles.breakAnywhere}>{policyPreview.rule_id}</b>
                  </p>'''

if old not in s:
    raise SystemExit("Rule line marker not found")

s = s.replace(old, new)

if "breakAnywhere:" not in s:
    marker = '''  policyEngine: {
    border: "1px solid #22d3ee",
    borderRadius: 16,
    padding: 16,
    marginTop: 18,
    background: "rgba(8,47,73,.35)"
  },'''

    replacement = '''  policyEngine: {
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
  },'''

    if marker not in s:
        raise SystemExit("policyEngine style marker not found")

    s = s.replace(marker, replacement)

p.write_text(s)
print("Policy rule wrapping fix applied")
