from pathlib import Path

# Rename portfolio doc if present.
old = Path("docs/portfolio/RECRUITER_DEMO_SCRIPT.md")
new = Path("docs/portfolio/CLIENT_DEMO_SCRIPT.md")
if old.exists() and not new.exists():
    old.rename(new)

# Rename phase doc if present.
old_phase = Path("docs/phases/PHASE_14_RECRUITER_DEMO_SCRIPT_PORTFOLIO_PACKAGING.md")
new_phase = Path("docs/phases/PHASE_14_CLIENT_DEMO_SCRIPT_PORTFOLIO_PACKAGING.md")
if old_phase.exists() and not new_phase.exists():
    old_phase.rename(new_phase)

paths = [
    Path("frontend/app/page.tsx"),
    Path("README.md"),
    Path("docs/portfolio/CLIENT_DEMO_SCRIPT.md"),
    Path("docs/portfolio/SCREENSHOT_GUIDE.md"),
    Path("docs/portfolio/ARCHITECTURE_SUMMARY.md"),
    Path("docs/portfolio/CORRECT_CLAIMS.md"),
    Path("docs/portfolio/WHY_THIS_MATTERS.md"),
    Path("docs/releases/v0.13.0-mock-mcp-execution-adapter.md"),
    Path("docs/phases/PHASE_14_CLIENT_DEMO_SCRIPT_PORTFOLIO_PACKAGING.md"),
    Path("docs/phases/PHASE_12_DEMO_RESET_PERSISTENCE_RECRUITER_HARDENING.md"),
]

replacements = {
    "Recruiter / Client Story": "Client Story",
    "Recruiter / Client Walkthrough": "Client Walkthrough",
    "Phase 12 · Recruiter Demo Hardening": "Phase 12 · Client Demo Hardening",
    "recruiter/client": "client",
    "recruiter or client": "client",
    "recruiter/client-ready": "client-ready",
    "recruiter/client demo": "client demo",
    "recruiter/client demos": "client demos",
    "recruiter/client walkthroughs": "client walkthroughs",
    "recruiters, clients, and portfolio reviewers": "clients and portfolio reviewers",
    "recruiters and clients": "clients",
    "recruiter, portfolio, and client-style": "client and portfolio",
    "recruiter, portfolio, and client": "client and portfolio",
    "recruiter-friendly": "client-friendly",
    "recruiter-ready": "client-ready",
    "recruiter walkthrough": "client walkthrough",
    "recruiter demo": "client demo",
    "recruiter demos": "client demos",
    "recruiter": "client",
    "Recruiter/Client": "Client",
    "Recruiter / Client": "Client",
    "Recruiter": "Client",
}

for path in paths:
    if not path.exists():
        continue

    s = path.read_text()

    # Preserve existing historical tag name if it appears.
    protected = "v0.14.0-recruiter-demo-packaging"
    s = s.replace(protected, "__PHASE14_TAG_PROTECTED__")

    for a, b in replacements.items():
        s = s.replace(a, b)

    s = s.replace("__PHASE14_TAG_PROTECTED__", protected)

    # Fix renamed doc references.
    s = s.replace(
        "docs/portfolio/RECRUITER_DEMO_SCRIPT.md",
        "docs/portfolio/CLIENT_DEMO_SCRIPT.md",
    )
    s = s.replace(
        "PHASE_14_RECRUITER_DEMO_SCRIPT_PORTFOLIO_PACKAGING.md",
        "PHASE_14_CLIENT_DEMO_SCRIPT_PORTFOLIO_PACKAGING.md",
    )

    path.write_text(s)

print("Phase 14A client positioning polish applied")
