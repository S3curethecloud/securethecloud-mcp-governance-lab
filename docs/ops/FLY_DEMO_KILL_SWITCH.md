# Fly Demo Kill Switch

## Purpose

This document explains how to turn the public Fly.io demo on, off, or permanently delete it while keeping the local Docker workflow available.

## Public Demo Apps

Frontend:

```text
securethecloud-mcp-governance-lab

Backend:

securethecloud-mcp-governance-lab-api
Recommended Temporary Shutdown

Use this when the demo should not be publicly accessible, but you may want to bring it back later.

./scripts/fly_demo_control.sh off

This scales both Fly apps to zero machines.

Turn Public Demo Back On
./scripts/fly_demo_control.sh on

This scales the backend and frontend back to one machine each.

Check Public Demo Status
./scripts/fly_demo_control.sh status
Run Locally Instead

Start local demo:

./scripts/fly_demo_control.sh local-up

Stop local demo:

./scripts/fly_demo_control.sh local-down

Local frontend:

http://localhost:3000

Local backend:

http://localhost:8000/health
Permanent Delete

Only use this when you are sure you no longer need the Fly public demo apps.

CONFIRM_DESTROY=I_UNDERSTAND_DELETE_PUBLIC_DEMO ./scripts/fly_demo_control.sh destroy

This permanently destroys the Fly frontend and backend apps.

Reverting to Local Only

After turning off or destroying Fly apps, the repo still works locally:

docker compose up --build -d

Then open:

http://localhost:3000
Boundary

The kill switch controls demo availability only. It does not delete the GitHub repository, local source code, release tags, documentation, or local Docker workflow.
