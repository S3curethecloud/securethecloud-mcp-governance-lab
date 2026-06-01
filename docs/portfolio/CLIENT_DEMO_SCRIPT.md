# SecureTheCloud MCP Governance Lab — Client Demo Script

## Demo URL

https://securethecloud-mcp-governance-lab.fly.dev

## One-Sentence Summary

This lab demonstrates how AI tool access can be governed before an agent invokes MCP-style enterprise tools, retrieves sensitive data, or performs business actions.

## Correct Positioning

This is a production-shaped simulated governance lab.

It does not connect to real MCP servers, customer records, regulated data, or enterprise systems. It safely demonstrates the control pattern: identity, classification, policy, firewall, approval, execution gating, and evidence replay.

## 90-Second Walkthrough

1. Start at the top of the page and point out the core principle:

   AI can assist, recommend, and explain. AI cannot bypass governance or invoke MCP-style tools without identity, policy, approval, and evidence validation.

2. Explain the Shared Trust Fabric:

   The lab models governance and policy, evidence and audit, risk intelligence, identity context, and an MCP tool firewall.

3. Show the Public Demo Boundary:

   The page clearly states this is simulated and does not connect to real enterprise systems.

4. Show the Executive Risk & Control Center:

   This gives leadership-level visibility into risk distribution, decision distribution, firewall posture, governance health, sensitive access attempts, and readiness posture.

5. Use the MCP Access Request Portal:

   Submit or review a governed request for a sensitive tool such as read_customer_record.

6. Show the MCP Tool-Call Firewall:

   Each tool receives an allowed, blocked, redacted, or requires-approval decision with a reason.

7. Show Human Approval Workspace:

   Sensitive requests route to review before execution is allowed.

8. Show Evidence Replay:

   Every request can be reconstructed through a timeline: intake, identity, classification, risk tiering, policy decision, approval status, and final outcome.

9. Show Mock MCP Execution Adapter:

   The lab demonstrates the final checkpoint before execution. A request can execute only when policy, firewall, approval, and evidence checks pass.

10. Close with the value:

   This is the control-plane pattern companies need before AI agents are allowed to use enterprise tools.

## Interview Talking Points

- Built as a full-stack Dockerized governance lab.
- Deployed publicly on Fly.io.
- Includes backend APIs, frontend governance console, executive dashboard, evidence replay, human approval workflow, and resettable demo state.
- Shows safe AI governance patterns without exposing real customer data or production systems.
- Demonstrates product thinking, security architecture, backend design, frontend UX, deployment, CI readiness, and demo packaging.

## Strong Closing Statement

The goal of this lab is not to claim production enforcement. The goal is to show the architecture, workflow, and governance controls that would be required before AI agents can safely interact with enterprise tools.
