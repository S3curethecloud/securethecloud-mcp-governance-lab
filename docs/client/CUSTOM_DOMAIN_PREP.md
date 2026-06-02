# Custom Domain Preparation

## Current Public Demo

https://securethecloud-mcp-governance-lab.fly.dev

## Optional Future Custom Domain Candidates

Recommended client-facing options:

- https://mcp-governance.securethecloud.dev
- https://mcp-lab.securethecloud.dev
- https://demo.securethecloud.dev/mcp-governance

## Recommended Choice

Use:

```text
mcp-governance.securethecloud.dev

Reason:

It is specific, professional, and clearly tied to the demo's purpose.

Deployment Model

Current deployment:

Frontend: Fly.io app
Backend: Fly.io app
DNS provider: Cloudflare
Current frontend app: securethecloud-mcp-governance-lab
Current backend app: securethecloud-mcp-governance-lab-api
Future Custom Domain Steps

Do not run these until ready to attach the domain.

fly certs add mcp-governance.securethecloud.dev -a securethecloud-mcp-governance-lab
fly certs show mcp-governance.securethecloud.dev -a securethecloud-mcp-governance-lab

Then add the required DNS record in Cloudflare.

Boundary

Custom domain attachment is optional. The Fly.io URL is already valid for public demo sharing.
