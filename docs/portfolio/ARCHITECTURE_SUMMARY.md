# SecureTheCloud MCP Governance Lab — Architecture Summary

## Purpose

The SecureTheCloud MCP Governance Lab is a public, simulated AI governance product demo. It shows how Model Context Protocol style tool access can be governed before AI agents retrieve sensitive information, invoke enterprise tools, or perform business actions.

## Architecture

```text
Frontend Governance Console
        |
        v
Backend MCP Governance API
        |
        +--> Identity Context Evaluation
        +--> Data Classification
        +--> Risk Tiering
        +--> Policy Decision Engine
        +--> MCP Tool-Call Firewall
        +--> Human Approval Workspace
        +--> Mock MCP Execution Adapter
        +--> Evidence Replay Timeline
        +--> Executive Risk Summary
Frontend

The frontend is a Next.js interface that provides:

Public demo boundary
Shared trust fabric
Executive risk dashboard
MCP access request portal
MCP tool-call firewall console
Human approval workspace
Evidence replay timeline
Protected demo reset panel
Mock MCP execution adapter
Backend

The backend is a FastAPI service that provides:

Health endpoint
Dashboard and executive summary endpoints
MCP tool catalog
Governed MCP request creation
Policy preview and decisioning
Tool-call firewall evaluation
Human approval action handling
Evidence replay timeline
Protected demo reset
Mock MCP execution endpoint
Deployment

The lab is deployed publicly on Fly.io:

Frontend: https://securethecloud-mcp-governance-lab.fly.dev
Backend: https://securethecloud-mcp-governance-lab-api.fly.dev
Data Model

The lab uses deterministic seeded demo records and simulated execution outputs.

No real MCP servers, real customer records, regulated data, production credentials, or enterprise systems are connected.

Governance Flow
Request intake
→ identity context
→ data classification
→ risk tiering
→ policy decision
→ tool-call firewall
→ human approval when required
→ mock MCP execution or blocked outcome
→ evidence replay
→ executive visibility
Why It Matters

AI agents are increasingly able to invoke tools, retrieve context, and trigger workflows. Enterprises need a control layer that evaluates identity, data sensitivity, tool risk, approval status, and evidence capture before tool execution occurs.

This lab demonstrates that control layer safely.
