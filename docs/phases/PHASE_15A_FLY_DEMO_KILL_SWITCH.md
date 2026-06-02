# Phase 15A — Fly Demo Kill Switch

Status: Implementation Complete

## Goal

Add a safe control script and documentation for turning the public Fly.io demo off, turning it back on, permanently deleting the Fly apps, or reverting to local-only demo mode.

## Implemented

- Fly demo control script
- Public demo off command
- Public demo on command
- Public demo status command
- Local Docker up command
- Local Docker down command
- Protected permanent destroy command
- Kill switch operations documentation
- README kill switch section

## Script

```text
scripts/fly_demo_control.sh
Safe Temporary Shutdown
./scripts/fly_demo_control.sh off
Restore Public Demo
./scripts/fly_demo_control.sh on
Permanent Destroy
CONFIRM_DESTROY=I_UNDERSTAND_DELETE_PUBLIC_DEMO ./scripts/fly_demo_control.sh destroy
Boundary

This phase controls demo availability only. It does not delete the GitHub repository, local source code, release tags, documentation, or local Docker workflow.
