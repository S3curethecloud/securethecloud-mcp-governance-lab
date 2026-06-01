#!/usr/bin/env bash
set -euo pipefail

echo "Starting SecureTheCloud MCP Governance Lab stack..."
docker compose up --build -d

echo "Waiting for services..."
sleep 15

echo "Checking backend health..."
curl -fsS http://localhost:8000/health
echo

echo "Checking MCP tools..."
curl -fsS http://localhost:8000/api/mcp/tools >/dev/null
echo "MCP tools endpoint ok"

echo "Checking dashboard..."
curl -fsS http://localhost:8000/api/dashboard
echo

echo "Checking executive summary..."
curl -fsS http://localhost:8000/api/executive/summary
echo

echo "Checking policy preview..."
curl -fsS -X POST http://localhost:8000/api/policy/preview \
  -H "Content-Type: application/json" \
  -d '{
    "user_identity": "Riley Brooks",
    "role": "Support Analyst",
    "department": "Customer Operations",
    "business_unit": "Customer Trust",
    "clearance_level": 4,
    "agent_identity": "securethecloud-demo-agent",
    "service_identity": "mcp-lab-service",
    "environment_context": "demo",
    "business_purpose": "Resolve customer escalation with governed MCP access",
    "requested_tool": "read_customer_record",
    "requested_resource": "customer profile",
    "data_classification": "restricted",
    "approval_status": "not_requested"
  }' >/dev/null
echo "Policy preview endpoint ok"

echo "Checking MCP firewall preview..."
curl -fsS -X POST http://localhost:8000/api/mcp/firewall/preview \
  -H "Content-Type: application/json" \
  -d '{
    "user_identity": "Riley Brooks",
    "role": "Support Analyst",
    "department": "Customer Operations",
    "business_unit": "Customer Trust",
    "clearance_level": 4,
    "agent_identity": "securethecloud-demo-agent",
    "service_identity": "mcp-lab-service",
    "environment_context": "demo",
    "business_purpose": "Resolve customer escalation with governed MCP access",
    "requested_tool": "read_customer_record",
    "requested_resource": "customer profile",
    "data_classification": "restricted",
    "approval_status": "not_requested"
  }' >/dev/null
echo "MCP firewall preview endpoint ok"

echo "Checking frontend..."
curl -fsSI http://localhost:3000 >/dev/null
echo "Frontend endpoint ok"

echo "Smoke test complete."
