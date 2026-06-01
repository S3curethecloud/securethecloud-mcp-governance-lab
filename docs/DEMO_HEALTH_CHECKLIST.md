
Public Demo Health Checklist
Before Sharing the URL

Run:

curl https://securethecloud-mcp-governance-lab-api.fly.dev/health
curl https://securethecloud-mcp-governance-lab-api.fly.dev/api/executive/summary
curl -I https://securethecloud-mcp-governance-lab.fly.dev
Reset Demo State

Run:

curl -X POST https://securethecloud-mcp-governance-lab-api.fly.dev/api/demo/reset \
  -H "X-Demo-Reset-Token: $DEMO_RESET_TOKEN"
UI Walkthrough

Confirm:

Public Demo Boundary appears
Executive dashboard loads metrics
MCP Access Request Portal submits requests
Tool-call Firewall updates
Human Approval Workspace handles approval-required requests
Evidence Replay Timeline updates
Demo Operations reset console appears
Correct Claim

This is a simulated MCP governance lab and production-shaped demo. It is not production enforcement or real enterprise MCP authorization.
