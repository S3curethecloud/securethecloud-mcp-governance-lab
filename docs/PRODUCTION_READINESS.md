# Production Readiness Scaffold

## Status

Lab readiness scaffold only.

This document prepares the SecureTheCloud MCP Governance Lab for public demo hardening and future deployment work. It does not claim production authorization, production enforcement, SOC 2 certification, real MCP server integration, or real enterprise data access.

## Current Readiness

- Dockerized FastAPI backend
- Dockerized Next.js frontend
- Docker Compose local stack
- Backend health endpoint
- Frontend build path
- CI validation workflow
- Local smoke test script
- Executive dashboard endpoint
- MCP request, policy preview, firewall preview, approval, and evidence replay endpoints

## Required Before Public Demo Deployment

- Configure public frontend API base URL
- Tighten CORS origins
- Add persistent database layer
- Add demo reset endpoint
- Add deployment-specific environment variables
- Add Fly.io app configuration
- Add public demo README section
- Confirm no secrets are committed
- Confirm lab boundary is visible in README

## Required Before Any Enterprise Production Claim

- Enterprise IAM integration
- Tenant boundary model
- Real MCP server integration
- Real authorization provider
- Real policy engine integration
- Real audit log storage
- Real evidence retention model
- Secrets management
- Managed database
- Observability
- Incident response plan
- Independent compliance review

## Boundary

This lab is production-shaped but not enterprise production. It demonstrates governance workflow concepts only.
