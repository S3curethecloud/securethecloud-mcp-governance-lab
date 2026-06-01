# Phase 3 — MCP Access Request Portal

Status: Implementation Complete

## Goal

Add an interactive MCP Access Request Portal that allows users to submit governed MCP tool requests and immediately view policy decisions, risk tier, and evidence replay updates.

## Implemented

- MCP request form
- User identity field
- Role field
- Department field
- Business unit field
- Clearance level selector
- Agent identity field
- Service identity field
- Environment context selector
- Requested MCP tool selector
- Requested resource field
- Data classification selector
- Approval status selector
- Business purpose field
- Live policy decision result
- Live dashboard refresh after submission
- Live evidence replay refresh after submission

## Backend Endpoints Used

- GET /api/mcp/tools
- GET /api/mcp/requests
- GET /api/dashboard
- POST /api/mcp/requests

## Boundary

This is a lab request portal. It does not provide enterprise IAM, real MCP server integration, real enterprise data access, production authorization, SOC 2 certification, or production enforcement authority.
