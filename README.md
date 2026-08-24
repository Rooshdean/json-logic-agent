# JSON Logic Agent V5.1

> **Understand JSON — and deep-dive n8n workflows — without having to think in JSON.**

JSON Logic Agent is an interactive JSON/n8n reverse-engineering tool. V5.1 uses **OpenRouter** for standalone AI-assisted analysis, so you can choose from OpenRouter-supported model IDs instead of being tied to one model provider.

## Start here

```bash
jsonlogic scan .
```

Use arrow keys to choose a JSON file and view it as normal logic, Python, JavaScript, TypeScript, or Mermaid. n8n workflow exports are detected automatically.

## Installation

Python **3.10+** is required. On macOS, if the system Python is 3.9, install a newer Python first, for example with Homebrew:

```bash
brew install python@3.12
```

Then:

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
cp .env.example .env
```

## Configure OpenRouter

Create an API key in OpenRouter and put it in `.env`:

```text
OPENROUTER_API_KEY=your-openrouter-key
JSON_LOGIC_MODEL=anthropic/claude-sonnet-4
```

`JSON_LOGIC_MODEL` can be changed to another model ID available through OpenRouter. Model availability/IDs can change, so check OpenRouter's model catalog when choosing one.

The OpenRouter key is required only for **AI-assisted semantic analysis**. Local scanning and deterministic n8n reports do not require it.

## n8n deep dive

Local structural analysis — no API call:

```bash
jsonlogic n8n workflow.json --report-only
```

Full semantic deep dive through OpenRouter:

```bash
jsonlogic n8n workflow.json
```

Other representations:

```bash
jsonlogic n8n workflow.json --to javascript
jsonlogic n8n workflow.json --to python
jsonlogic n8n workflow.json --to typescript
jsonlogic n8n workflow.json --to mermaid
```

Override the configured OpenRouter model for one run:

```bash
jsonlogic n8n workflow.json --model <openrouter-model-id>
```

See [n8n Workflow Intelligence](docs/N8N_WORKFLOWS.md).

## Generic JSON

```bash
jsonlogic explain file.json
jsonlogic explain file.json --to python
jsonlogic explain file.json --to javascript
jsonlogic explain file.json --to typescript
jsonlogic explain file.json --to mermaid
```

If the file is an n8n export, V5.1 automatically activates n8n-aware analysis.

## Local vs OpenRouter

```text
JSON Logic Agent
      │
      ├── LOCAL
      │    ├── jsonlogic scan .
      │    └── jsonlogic n8n workflow.json --report-only
      │
      └── OPENROUTER
           ├── Inspector
           ├── Logic Architect
           ├── Ambiguity Critic
           ├── Generator
           └── Reviewer
```

The deterministic n8n analyzer runs before OpenRouter and provides grounded graph evidence: nodes, connections, branch indexes, triggers, decisions, integrations, expressions, credential types, Code/AI nodes, disconnected nodes, terminal paths, and conservative review signals.

## n8n architecture

```text
n8n JSON
   ↓
Format detection
   ↓
Local deterministic n8n analyzer
   ↓
Structured workflow context
   ↓
OpenRouter model
   ↓
Inspector → Architect → Critic → LogicModel
   ↓
Generator → Reviewer
   ↓
Logic / Python / JavaScript / TypeScript / Mermaid
```

Credential secret values must never be exposed. Generated code is conceptual and is never automatically executed.

## Interactive mode

```bash
jsonlogic scan .
```

n8n files appear as `[n8n-workflow]`. For scripts/CI:

```bash
jsonlogic scan . --no-interactive
jsonlogic scan . --json
```

Scanning remains local and does not upload every discovered file.

## Claude Code / Codex

You can still launch `claude` or `codex` from this repository to develop or inspect the project. The standalone `jsonlogic explain` / `jsonlogic n8n` semantic commands use the OpenRouter configuration above; `--report-only` remains local.

## Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [n8n Workflow Intelligence](docs/N8N_WORKFLOWS.md)
- [Command Reference](docs/COMMANDS.md)
- [CLAUDE.md](CLAUDE.md)
- [AGENTS.md](AGENTS.md)

## Development

```bash
pytest -q
```

Current package version: **0.5.1**.

> **Understand first. Translate second. For n8n, reconstruct the workflow before explaining it.**
