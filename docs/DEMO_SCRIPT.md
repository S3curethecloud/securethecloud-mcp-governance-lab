# SecureTheCloud MCP Governance Lab — Recruiter / Client Demo Script

## Demo Positioning

SecureTheCloud MCP Governance Lab is a production-shaped portfolio lab that demonstrates how AI agent access to MCP-style tools can be governed before execution.

This is a simulated MCP governance lab. It does not connect to real enterprise systems, real MCP servers, real customer records, real regulated data, or production authorization infrastructure.

## Demo Story

Model Context Protocol gives AI agents a way to interact with tools and systems.

This lab shows how an enterprise could place governance in front of those tool calls:

1. Capture an MCP access request.
2. Build identity and agent context.
3. Classify the requested data/resource.
4. Score the risk tier.
5. Apply policy.
6. Inspect MCP tool-call firewall decisions.
7. Route sensitive requests to human approval.
8. Record evidence.
9. Replay the decision timeline.
10. Present executive governance posture.

## Recommended Walkthrough

### 1. Open the Executive Governance Dashboard

Explain that leaders can see:

- MCP request volume
- risk distribution
- decision distribution
- firewall posture
- approval queue health
- sensitive access attempts
- policy violations
- readiness posture

### 2. Submit a governed MCP request

Use:

- Tool: `read_customer_record`
- Classification: `restricted`
- Clearance: `4 - Restricted`
- Approval status: `not_requested`

Expected result:

- Policy requires approval.
- Tool-call firewall marks sensitive tools as requiring approval.
- Evidence replay records the decision.

### 3. Approve the request

Use the Human Approval Workspace.

Expected result:

- Reviewer action is recorded.
- Policy re-evaluates.
- Evidence replay updates.
- Final outcome changes to allow when approval evidence exists.

### 4. Reject or escalate another request

Expected result:

- Final decision changes to deny or escalate.
- Reviewer evidence is captured.
- Executive dashboard updates.

### 5. Show Evidence Replay Timeline

Explain that the platform can reconstruct:

- Request intake
- identity context
- data classification
- risk tiering
- policy decision
- human approval
- final outcome

## Demo Doctrine

AI can assist, recommend, and explain.

AI cannot invoke MCP-style tools, access sensitive resources, execute workflows, mutate systems, or perform business actions without identity, policy, approval, and evidence validation.

## Lab Boundary

This is a portfolio/demo lab.

It does not provide:

- real enterprise IAM
- real MCP server integration
- real customer data access
- real regulated data processing
- real production authorization
- real production enforcement
- SOC 2 certification
- production audit assurance
