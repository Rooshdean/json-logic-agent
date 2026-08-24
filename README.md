# JSON Logic Agent V5.2

> **Understand JSON — and deep-dive n8n workflows — without having to think in JSON.**

JSON Logic Agent is an interactive JSON/n8n reverse-engineering tool. It uses local deterministic analysis for n8n structure and OpenRouter for AI-assisted semantic analysis. V5.2 adds complete **Markdown and PDF report exports**.

## Start here

```bash
jsonlogic scan .
```

Use arrow keys to choose a JSON file and view it as normal logic, Python, JavaScript, TypeScript, or Mermaid. n8n workflow exports are detected automatically.

## Installation

Python **3.10+** is required. On macOS:

```bash
brew install python@3.12

git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
cp .env.example .env
```

After pulling V5.2 into an existing clone, run `pip install -e .` again so the PDF dependency is installed.

## Configure OpenRouter

Put your OpenRouter key and preferred model in `.env`:

```text
OPENROUTER_API_KEY=your-openrouter-key
JSON_LOGIC_MODEL=anthropic/claude-sonnet-4
```

The key is needed only for AI-assisted semantic analysis. `scan` and `n8n --report-only` remain local.

## n8n deep dive

```bash
jsonlogic n8n workflow.json --report-only
jsonlogic n8n workflow.json
jsonlogic n8n workflow.json --to javascript
jsonlogic n8n workflow.json --to python
jsonlogic n8n workflow.json --to typescript
jsonlogic n8n workflow.json --to mermaid
```

## Export a complete report

V5.2 uses `--export` for a complete report. The file extension selects the format.

Markdown:

```bash
jsonlogic n8n workflow.json --export workflow-report.md
```

PDF:

```bash
jsonlogic n8n workflow.json --export workflow-report.pdf
```

Mermaid analysis inside Markdown:

```bash
jsonlogic n8n workflow.json --to mermaid --export workflow-diagram.md
```

Mermaid analysis inside PDF:

```bash
jsonlogic n8n workflow.json --to mermaid --export workflow-diagram.pdf
```

The complete report contains the source format, provider/model, target view, fidelity score, n8n intelligence report, semantic deep dive, generated logic/code/Mermaid source, assumptions/warnings, and pipeline metadata.

`--out` is different: it saves **only the rendered target output**. For example:

```bash
jsonlogic n8n workflow.json --to mermaid --out workflow.mmd
```

Use `--export` when you want a human-readable analysis report and `--out` when you want only the generated artifact/source.

## Generic JSON

The same export feature works for generic JSON:

```bash
jsonlogic explain config.json --export config-analysis.md
jsonlogic explain config.json --to python --export config-analysis.pdf
```

If the file is an n8n export, n8n-aware analysis activates automatically.

## Architecture

```text
n8n JSON
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
   ↓
Terminal / Markdown report / PDF report
```

Credential secret values must never be exposed. Generated code is conceptual and is never automatically executed.

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

Current package version: **0.5.2**.

> **Understand first. Translate second. For n8n, reconstruct the workflow before explaining it.**
