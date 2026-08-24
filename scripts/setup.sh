#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Python 3 is required." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  "$PYTHON_BIN" -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

if [ ! -f .env ]; then
  cp .env.example .env
fi

cat <<'MSG'

Setup complete.

Next:
  1. Put your OPENAI_API_KEY in .env
  2. source .venv/bin/activate
  3. jsonlogic examples/order_workflow.json --to logic

For Claude Code:
  claude

For Codex:
  codex
MSG
