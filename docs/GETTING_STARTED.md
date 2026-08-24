# Getting Started — JSON Logic Agent V5.2

This is the short first-run checklist. For the full walkthrough and troubleshooting, see the main README.

## Step 1 — Check Python

```bash
python3 --version
```

Python 3.10+ is required. macOS users with Python 3.9 can install 3.12:

```bash
brew install python@3.12
```

## Step 2 — Clone

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
```

## Step 3 — Create and activate the virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python --version
```

The final command must report Python 3.10+.

## Step 4 — Install

```bash
pip install --upgrade pip
pip install -e .
jsonlogic --help
```

## Step 5 — Configure OpenRouter

```bash
cp .env.example .env
nano .env
```

Add:

```text
OPENROUTER_API_KEY=your-openrouter-key
JSON_LOGIC_MODEL=anthropic/claude-sonnet-4
```

Save Nano with `Ctrl+O`, Enter, `Ctrl+X`.

Never commit `.env` or share the real key.

## Step 6 — Verify local n8n analysis

```bash
jsonlogic n8n examples/n8n_customer_workflow.json --report-only
```

This does not use OpenRouter.

Expected signs of success include:

```text
Workflow: Customer Intake Example
Nodes: 4
Triggers: Customer Webhook
Decision nodes: Has Email?
```

## Step 7 — Verify OpenRouter

```bash
jsonlogic n8n examples/n8n_customer_workflow.json
```

You should receive the local workflow intelligence followed by `SEMANTIC DEEP DIVE`, a fidelity score, and warnings.

## Step 8 — Analyze your workflow

```bash
jsonlogic n8n ~/Downloads/my-workflow.json
```

Alternative views:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --to javascript
jsonlogic n8n ~/Downloads/my-workflow.json --to python
jsonlogic n8n ~/Downloads/my-workflow.json --to typescript
jsonlogic n8n ~/Downloads/my-workflow.json --to mermaid
```

## Step 9 — Export it

Markdown:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --export workflow-report.md
```

PDF:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --export workflow-report.pdf
```

Mermaid PDF report:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --to mermaid --export workflow-diagram.pdf
```

## Step 10 — Browse a whole project

```bash
jsonlogic scan .
```

Use arrow keys to select discovered JSON files and choose the representation you want.

## Step 11 — Claude Code

```bash
cd ~/json-logic-agent
source .venv/bin/activate
claude
```

Suggested first prompt:

```text
Read CLAUDE.md, README.md and docs/N8N_WORKFLOWS.md.
Run pytest -q first.
Then use JSON Logic Agent to analyze examples/n8n_customer_workflow.json.
```

## Step 12 — Codex

```bash
cd ~/json-logic-agent
source .venv/bin/activate
codex
```

Suggested first prompt:

```text
Read AGENTS.md, README.md and docs/N8N_WORKFLOWS.md.
Run pytest -q first.
Then use JSON Logic Agent to analyze examples/n8n_customer_workflow.json.
```

## Updating later

```bash
cd ~/json-logic-agent
git pull
source .venv/bin/activate
pip install -e .
```

## Common Python 3.9 fix

```bash
brew install python@3.12
cd ~/json-logic-agent
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

For detailed troubleshooting, architecture, security notes, `--out` vs `--export`, generic JSON usage, and examples, return to the main README.
