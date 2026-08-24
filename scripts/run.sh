#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d .venv ]; then
  echo "Missing .venv. Run ./scripts/setup.sh first." >&2
  exit 1
fi

. .venv/bin/activate

if [ ! -f .env ]; then
  echo "Missing .env. Run ./scripts/setup.sh first." >&2
  exit 1
fi

if [ "$#" -lt 1 ]; then
  cat <<'USAGE'
Usage:
  ./scripts/run.sh path/to/file.json [logic|python|javascript]

Examples:
  ./scripts/run.sh examples/order_workflow.json
  ./scripts/run.sh examples/order_workflow.json python
USAGE
  exit 1
fi

TARGET="${2:-logic}"
exec jsonlogic "$1" --to "$TARGET"
