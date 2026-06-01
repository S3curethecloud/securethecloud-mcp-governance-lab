# Deployment Readiness Notes

## Local

Run:

```bash
docker compose up --build -d
./scripts/local_smoke_test.sh
Future Public Demo Deployment

Target model:

Frontend: Fly.io or Cloudflare Pages
Backend: Fly.io, Cloud Run, App Runner, Render, or equivalent
Database: Managed PostgreSQL
DNS: Cloudflare
Secrets: platform secret manager
Environment Variables

Backend candidates:

LAB_MODE=true
DATABASE_URL=
CORS_ORIGINS=
DEMO_RESET_TOKEN=

Frontend candidates:

NEXT_PUBLIC_API_BASE_URL=
Boundary

Deployment readiness does not mean production enforcement readiness. This lab must not be represented as enterprise IAM, production authorization, SOC 2 certification, real MCP execution authority, or real regulated data processing.
