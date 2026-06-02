#!/usr/bin/env bash
set -euo pipefail

FRONTEND_APP="${FRONTEND_APP:-securethecloud-mcp-governance-lab}"
API_APP="${API_APP:-securethecloud-mcp-governance-lab-api}"

export FLYCTL_INSTALL="${FLYCTL_INSTALL:-/home/cloudlab/.fly}"
export PATH="$FLYCTL_INSTALL/bin:$PATH"

usage() {
  cat <<USAGE
SecureTheCloud MCP Governance Lab Fly Demo Control

Usage:
  ./scripts/fly_demo_control.sh status
  ./scripts/fly_demo_control.sh off
  ./scripts/fly_demo_control.sh on
  ./scripts/fly_demo_control.sh local-up
  ./scripts/fly_demo_control.sh local-down
  CONFIRM_DESTROY=I_UNDERSTAND_DELETE_PUBLIC_DEMO ./scripts/fly_demo_control.sh destroy

Actions:
  status      Show Fly app status for frontend and backend
  off         Scale public Fly frontend and backend to zero
  on          Scale public Fly backend and frontend back to one machine
  local-up    Start local Docker Compose stack
  local-down  Stop local Docker Compose stack
  destroy     Permanently delete Fly frontend and backend apps

Apps:
  Frontend: $FRONTEND_APP
  Backend:  $API_APP
USAGE
}

require_fly() {
  if ! command -v fly >/dev/null 2>&1; then
    echo "fly CLI not found. Install or export PATH to flyctl first."
    exit 1
  fi
}

status_apps() {
  require_fly
  echo "Frontend status:"
  fly status -a "$FRONTEND_APP" || true
  echo
  echo "Backend status:"
  fly status -a "$API_APP" || true
}

turn_off() {
  require_fly
  echo "Scaling frontend to zero..."
  fly scale count 0 -a "$FRONTEND_APP" -y
  echo "Scaling backend to zero..."
  fly scale count 0 -a "$API_APP" -y
  echo "Public demo is off. Local repo and Docker workflow remain available."
}

turn_on() {
  require_fly
  echo "Scaling backend to one machine..."
  fly scale count 1 -a "$API_APP" -y
  echo "Scaling frontend to one machine..."
  fly scale count 1 -a "$FRONTEND_APP" -y
  echo "Waiting briefly before health checks..."
  sleep 10
  curl -fsS "https://$API_APP.fly.dev/health" || true
  echo
  curl -fsSI "https://$FRONTEND_APP.fly.dev" || true
  echo "Public demo should be back online."
}

local_up() {
  echo "Starting local Docker Compose stack..."
  docker compose up --build -d
  sleep 15
  curl -fsS http://localhost:8000/health || true
  echo
  curl -fsSI http://localhost:3000 || true
  echo "Local demo should be available at http://localhost:3000"
}

local_down() {
  echo "Stopping local Docker Compose stack..."
  docker compose down
}

destroy_apps() {
  require_fly

  if [ "${CONFIRM_DESTROY:-}" != "I_UNDERSTAND_DELETE_PUBLIC_DEMO" ]; then
    echo "Refusing to destroy Fly apps without explicit confirmation."
    echo "Run:"
    echo "CONFIRM_DESTROY=I_UNDERSTAND_DELETE_PUBLIC_DEMO ./scripts/fly_demo_control.sh destroy"
    exit 1
  fi

  echo "Permanently deleting frontend app: $FRONTEND_APP"
  fly apps destroy "$FRONTEND_APP" -y || true

  echo "Permanently deleting backend app: $API_APP"
  fly apps destroy "$API_APP" -y || true

  echo "Fly apps destroyed. Local repo remains available."
}

case "${1:-}" in
  status)
    status_apps
    ;;
  off)
    turn_off
    ;;
  on)
    turn_on
    ;;
  local-up)
    local_up
    ;;
  local-down)
    local_down
    ;;
  destroy)
    destroy_apps
    ;;
  *)
    usage
    exit 1
    ;;
esac
