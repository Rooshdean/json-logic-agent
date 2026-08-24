# JSON Logic Agent V5.2

> **Understand JSON — and deep-dive n8n workflows — without having to think in JSON.**

JSON Logic Agent helps developers turn unfamiliar JSON into normal logic, Python, JavaScript, TypeScript, Mermaid diagrams, Markdown reports, and PDFs. Exported n8n workflows are a first-class use case.

This README is written so a new user can go from **nothing installed** to a **successful analysis** without already knowing the project.

---

# 1. What you need

You need:

- Git
- Python **3.10 or newer**
- an OpenRouter API key for AI-assisted analysis

You do **not** need an API key for local scanning or the deterministic n8n report.

## Check your Python version

```bash
python3 --version
```

If you see Python 3.10, 3.11, 3.12, or newer, continue.

If you see Python 3.9.x on macOS, install a newer version:

```bash
brew install python@3.12
```

Then confirm:

```bash
python3.12 --version
```

---

# 2. Clone the project

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
```

---

# 3. Create the virtual environment

Recommended on macOS:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Your prompt should now show `(.venv)`.

Check which Python the virtual environment is using:

```bash
python --version
```

It must be Python 3.10+.

If you previously created `.venv` with Python 3.9, remove it and recreate it:

```bash
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
```

---

# 4. Install JSON Logic Agent

```bash
pip install --upgrade pip
pip install -e .
```

Confirm the CLI exists:

```bash
jsonlogic --help
```

If that command prints help, installation succeeded.

---

# 5. Configure OpenRouter

Create the local environment file:

```bash
cp .env.example .env
```

Open it with Nano:

```bash
nano .env
```

Add your key and model:

```text
OPENROUTER_API_KEY=your-openrouter-api-key
JSON_LOGIC_MODEL=anthropic/claude-sonnet-4
```

Save Nano with:

1. `Ctrl + O`
2. press `Enter`
3. `Ctrl + X`

Do **not** commit `.env` to GitHub.

`JSON_LOGIC_MODEL` can be changed to another model ID supported by OpenRouter.

---

# 6. First success: test without using OpenRouter

Run the included n8n example locally:

```bash
jsonlogic n8n examples/n8n_customer_workflow.json --report-only
```

You should see output similar to:

```text
N8N WORKFLOW INTELLIGENCE
=========================
Workflow: Customer Intake Example
Nodes: 4
Connections: 3
Triggers: Customer Webhook
Decision nodes: Has Email?
Integrations: HTTP/API
...
```

If this works, the installation and local n8n parser are working.

This command does **not** call OpenRouter.

---

# 7. Second success: test OpenRouter semantic analysis

Now run:

```bash
jsonlogic n8n examples/n8n_customer_workflow.json
```

This should produce:

1. the deterministic n8n workflow intelligence report
2. a semantic deep dive
3. source format
4. fidelity score
5. assumptions/warnings

If this succeeds, your OpenRouter configuration is working.

---

# 8. Use it on your own n8n workflow

Export a workflow from n8n as JSON.

For example, if it is in Downloads:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --report-only
```

Then run the full deep dive:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json
```

See it as JavaScript:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --to javascript
```

Python:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --to python
```

TypeScript:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --to typescript
```

Mermaid flowchart:

```bash
jsonlogic n8n ~/Downloads/my-workflow.json --to mermaid
```

---

# 9. Export the full analysis

## Markdown report

```bash
jsonlogic n8n ~/Downloads/my-workflow.json \
  --export my-workflow-report.md
```

## PDF report

```bash
jsonlogic n8n ~/Downloads/my-workflow.json \
  --export my-workflow-report.pdf
```

## Mermaid analysis as PDF

```bash
jsonlogic n8n ~/Downloads/my-workflow.json \
  --to mermaid \
  --export my-workflow-diagram.pdf
```

The full export includes:

- source format
- OpenRouter model/provider
- target view
- fidelity score
- n8n intelligence report
- semantic deep dive
- generated logic/code/Mermaid source
- assumptions/warnings
- pipeline metadata

### `--out` vs `--export`

Use `--out` to save only generated output:

```bash
jsonlogic n8n workflow.json --to mermaid --out workflow.mmd
```

Use `--export` for a complete human-readable report:

```bash
jsonlogic n8n workflow.json --to mermaid --export workflow-report.pdf
```

You can use both together.

---

# 10. Interactive mode

If you have a project containing several JSON files:

```bash
jsonlogic scan .
```

In a normal terminal you can use the arrow keys to select a file and choose:

```text
Explain in normal logic
Show as Python
Show as JavaScript
Show as TypeScript
Draw as Mermaid diagram
```

Detected n8n exports are marked `[n8n-workflow]` and use the n8n-aware analysis path.

For non-interactive output:

```bash
jsonlogic scan . --no-interactive
```

For machine-readable output:

```bash
jsonlogic scan . --json
```

Scanning is local. It does not send every discovered JSON file to OpenRouter.

---

# 11. Generic JSON files

JSON Logic Agent also works with non-n8n JSON:

```bash
jsonlogic explain config.json
jsonlogic explain config.json --to javascript
jsonlogic explain config.json --to python
jsonlogic explain config.json --to mermaid
jsonlogic explain config.json --export config-analysis.pdf
```

If `config.json` turns out to be an n8n workflow export, n8n analysis is enabled automatically.

---

# 12. Using the repo with Claude Code

Start from the project root:

```bash
cd ~/json-logic-agent
source .venv/bin/activate
claude
```

Then ask Claude Code:

```text
Read CLAUDE.md, AGENTS.md, README.md and docs/N8N_WORKFLOWS.md.
Run the tests first.

Then use JSON Logic Agent to analyze examples/n8n_customer_workflow.json.
Start with the deterministic report, then explain the semantic flow and show me the JavaScript representation.
```

For your own workflow:

```text
Use JSON Logic Agent V5.2 to deep-dive ~/Downloads/my-workflow.json.

Show me:
- purpose
- entry points
- execution flow
- branches
- integrations
- expressions
- error handling
- risks
- conceptual JavaScript
- Mermaid diagram
```

Claude Code can run the `jsonlogic` commands itself from the repository.

---

# 13. Using the repo with Codex

From the project root:

```bash
cd ~/json-logic-agent
source .venv/bin/activate
codex
```

Then ask:

```text
Read AGENTS.md, README.md and docs/N8N_WORKFLOWS.md.
Run pytest -q.

Then analyze examples/n8n_customer_workflow.json using JSON Logic Agent V5.2.
Start with the local deterministic report and then inspect the semantic deep dive.
```

---

# 14. Troubleshooting

## Error: Python 3.9 is not supported

Example:

```text
ERROR: Package 'json-logic-agent' requires a different Python: 3.9.6 not in '>=3.10'
```

Fix:

```bash
brew install python@3.12
cd ~/json-logic-agent
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Then confirm:

```bash
python --version
```

## `jsonlogic: command not found`

Activate the environment:

```bash
source .venv/bin/activate
```

Then reinstall:

```bash
pip install -e .
```

## OpenRouter key error

Check that `.env` exists:

```bash
ls -la .env
```

Open it:

```bash
nano .env
```

It should contain:

```text
OPENROUTER_API_KEY=your-key
JSON_LOGIC_MODEL=your-openrouter-model-id
```

Do not paste your real key into public issues, chat screenshots, or commits.

## I only want local analysis

Use:

```bash
jsonlogic n8n workflow.json --report-only
```

or:

```bash
jsonlogic scan . --no-interactive
```

## I pulled a new version and something is missing

After `git pull`, reinstall dependencies:

```bash
source .venv/bin/activate
pip install -e .
```

## My n8n workflow is not detected

A normal exported workflow should contain:

- a top-level `nodes` array
- a top-level `connections` object
- recognizable n8n node `type` values

Use `jsonlogic explain file.json` if it is not a standard n8n workflow export.

---

# 15. How the tool works

For n8n:

```text
n8n JSON
   ↓
Local deterministic n8n analyzer
   ↓
Nodes / graph / branches / expressions / risks
   ↓
OpenRouter model
   ↓
Inspector
   ↓
Logic Architect
   ↓
Ambiguity Critic
   ↓
LogicModel
   ↓
Generator
   ↓
Reviewer
   ↓
Logic / Python / JavaScript / TypeScript / Mermaid
   ↓
Terminal / Markdown / PDF
```

The generated Python/JavaScript/TypeScript is a conceptual representation of the workflow logic. It is not a drop-in replacement for the n8n runtime and is never automatically executed.

---

# Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [n8n Workflow Intelligence](docs/N8N_WORKFLOWS.md)
- [Command Reference](docs/COMMANDS.md)
- [Claude Code instructions](CLAUDE.md)
- [Codex instructions](AGENTS.md)

Current version: **0.5.2**

> **Understand first. Translate second. For n8n, reconstruct the workflow before explaining it.**
