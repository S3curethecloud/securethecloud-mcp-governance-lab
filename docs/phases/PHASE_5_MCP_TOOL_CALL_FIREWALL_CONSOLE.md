# Phase 5 — MCP Tool-Call Firewall Console

Status: Implementation Complete

## Goal

Add a visible MCP Tool-Call Firewall Console that evaluates each MCP tool before execution and explains whether access is allowed, blocked, redacted, escalated, or requires approval.

## Implemented

- MCP firewall decision model
- Firewall status mapping
- Backend firewall preview endpoint
- Frontend MCP Tool-Call Firewall panel
- Per-tool status display
- Per-tool risk tier display
- Per-tool policy reason display
- Per-tool rule identifier display
- Live firewall preview refresh as request context changes

## Backend Endpoint Added

- POST /api/mcp/firewall/preview

## Firewall Statuses

- allowed
- blocked
- requires_approval
- redacted
- escalated

## Boundary

This is a lab firewall console. It does not provide production authorization, real MCP server integration, real OPA enforcement, real enterprise data access, SOC 2 certification, or production enforcement authority.
