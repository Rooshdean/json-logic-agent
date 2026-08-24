# Getting Started with JSON Logic Agent V5

JSON Logic Agent helps developers understand unfamiliar JSON and exported n8n workflows as normal logic or familiar code.

## 1. Install

Requirements: Python 3.10+, Git, and an OpenAI API key for semantic deep dives.

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
chmod +x scripts/*.sh
./scripts/setup.sh
source .venv/bin/activate
cp .env.example .env
```

Add to `.env`:

```text
OPENAI_API_KEY=your-api-key-here
```

## 2. Easiest workflow

```bash
jsonlogic scan .
```

Use arrow keys to choose a file, then choose Normal logic, Python, JavaScript, TypeScript, or Mermaid. n8n exports are detected automatically.

## 3. Deep-dive an n8n export

```bash
jsonlogic n8n workflow.json
```

Before semantic interpretation, V5 locally reconstructs the n8n workflow graph and inventories triggers, decisions, integrations, expressions, credentials types, code/AI nodes, disconnected nodes, terminal nodes, and review signals.

Try the included fixture:

```bash
jsonlogic n8n examples/n8n_customer_workflow.json --report-only
```

This command is local and makes no model/API call.

Then run the full deep dive:

```bash
jsonlogic n8n examples/n8n_customer_workflow.json
```

Or choose a developer representation:

```bash
jsonlogic n8n examples/n8n_customer_workflow.json --to javascript
jsonlogic n8n examples/n8n_customer_workflow.json --to python
jsonlogic n8n examples/n8n_customer_workflow.json --to typescript
jsonlogic n8n examples/n8n_customer_workflow.json --to mermaid
```

Read [n8n Workflow Intelligence](N8N_WORKFLOWS.md) for the full guide.

## 4. Generic JSON

```bash
jsonlogic explain config.json
jsonlogic explain config.json --to javascript
```

If the file is actually an n8n export, V5 detects it and activates the n8n-aware pipeline automatically.

## 5. Local vs AI-assisted operations

Local/no model call:

```bash
jsonlogic scan . --no-interactive
jsonlogic scan . --json
jsonlogic n8n workflow.json --report-only
```

AI-assisted semantic interpretation:

```bash
jsonlogic explain file.json
jsonlogic n8n workflow.json
```

This separation is intentional: discovering or structurally inspecting files should not require sending every file to a model.

## 6. Save output

```bash
jsonlogic n8n workflow.json --to javascript --out workflow.js
jsonlogic explain config.json --to python --out config_logic.py
```

Generated code is conceptual logic and is never automatically executed.

## 7. Inspect uncertainty

```bash
jsonlogic n8n workflow.json --show-trace
jsonlogic explain file.json --show-trace
```

The trace exposes the inspector, draft semantic model, critique, final LogicModel, and reviewer.

## 8. Troubleshooting

If `jsonlogic` is missing:

```bash
source .venv/bin/activate
```

After pulling a new version:

```bash
git pull
./scripts/setup.sh
```

If an n8n export is not detected, confirm it is a workflow export containing a top-level `nodes` array, `connections` object, and recognizable n8n node `type` values.

If you only want local n8n information and do not want an API call, always use `--report-only`.

## 9. Claude Code / Codex

Run `claude` or `codex` in the repo. Both have V5-specific repository instructions in `CLAUDE.md` and `AGENTS.md`.
