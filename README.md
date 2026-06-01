# SecureTheCloud MCP Governance Lab

**Status:** Lab Platform / Phase 0 Baseline

A governed Model Context Protocol access, policy, approval, and evidence platform for enterprise AI workflows.

This lab demonstrates how MCP-enabled AI agents can be governed before accessing enterprise systems, retrieving sensitive information, invoking tools, executing workflows, or performing business actions.

## Core Principle

AI can assist.

AI can recommend.

AI can explain.

AI cannot bypass governance, access sensitive resources, invoke enterprise tools, mutate critical systems, or execute business actions without explicit authorization, policy validation, approval controls, and evidence capture.

## What It Demonstrates

- MCP tool governance
- AI agent action control
- Identity-aware policy evaluation
- Data classification
- Risk-tiering
- Human approval gates
- AI tool-call firewall
- Evidence capture
- Evidence replay
- Executive governance visibility

## V1 MCP Tools

- `search_internal_docs`
- `query_database`
- `read_customer_record`
- `create_ticket`

## Future MCP Tools

- `create_change_request`
- `deploy_application`
- `access_hr_record`
- `retrieve_financial_report`
- `invoke_cloud_action`
- `submit_purchase_request`
- `execute_workflow`
- `access_customer_case`
- `query_vector_database`
- `invoke_agent_workflow`

## Phase Model

All lab work is tracked under `docs/phases/`.

- Phase 0: Repository and doctrine baseline
- Phase 1: Backend MCP governance API
- Phase 2: Frontend platform shell
- Phase 3: MCP access request portal
- Phase 4: Risk tiering and policy decision engine
- Phase 5: MCP tool-call firewall
- Phase 6: Human approval workspace
- Phase 7: Evidence replay
- Phase 8: Executive governance dashboard
- Phase 9: Docker and CI readiness
- Phase 10: Public demo polish
- Phase 11: Fly.io public deployment
- Phase 12: Managed persistence and demo hardening

## Lab Boundary

This is a production-shaped lab, not an enterprise-grade authorization system.

It does not provide enterprise IAM, production authorization, real regulated-system access, real customer data processing, SOC 2 certification, production audit assurance, or production enforcement authority.

## Public Demo Positioning

SecureTheCloud MCP Governance Lab is a production-shaped portfolio lab that demonstrates how MCP-style AI tool access can be governed before execution.

This lab is intentionally simulated. It does not connect to real MCP servers, real enterprise systems, real customer data, real regulated data, or production authorization infrastructure.

## Demo Narrative

Model Context Protocol gives AI agents a way to interact with tools.

SecureTheCloud MCP Governance Lab demonstrates a governance pattern for those tool calls:

- capture the request
- validate identity context
- classify the data/resource
- calculate risk tier
- evaluate policy
- inspect tool-call firewall decisions
- require approval for sensitive activity
- capture evidence
- replay the decision timeline
- summarize executive readiness

## Recruiter / Client Demo

Use `docs/DEMO_SCRIPT.md` for the recommended walkthrough.

## Correct Claim

This is a simulated MCP governance lab and production-shaped demo.

It is not production enforcement, real enterprise MCP authorization, SOC 2 certification, or real regulated data processing.

## Public Demo Links

Frontend:

```text
https://securethecloud-mcp-governance-lab.fly.dev

Backend health:

https://securethecloud-mcp-governance-lab-api.fly.dev/health

Backend executive summary:

https://securethecloud-mcp-governance-lab-api.fly.dev/api/executive/summary
Demo Reset

The public demo can be restored to seeded records with the protected reset endpoint:

curl -X POST https://securethecloud-mcp-governance-lab-api.fly.dev/api/demo/reset \
  -H "X-Demo-Reset-Token: $DEMO_RESET_TOKEN"

Never commit the reset token.
