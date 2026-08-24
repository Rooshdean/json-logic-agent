# JSON Logic Agent V4

> **Understand JSON without having to think in JSON.**

JSON Logic Agent is for developers who understand code but do not want to mentally parse large, nested, or unfamiliar JSON.

V4 adds an **interactive terminal browser**. You can scan a project, use your arrow keys to choose a JSON file, and then choose how you want to understand it — no command memorization required.

## The easiest way to use it

```bash
jsonlogic scan .
```

In a normal terminal, V4 opens an interactive picker:

```text
? Choose a JSON file:
❯ workflows/approval.json  [workflow-or-automation]
  permissions.json         [access-policy]
  config.json              [configuration]
  package.json             [node-package-manifest]
  Exit
```

Press **↑ / ↓** and **Enter**. Then choose:

```text
? What would you like to do with workflows/approval.json?
❯ Explain in normal logic
  Show as Python
  Show as JavaScript
  Show as TypeScript
  Draw as Mermaid diagram
  Choose another file
  Exit
```

After viewing the result, you can view the same file another way, choose another JSON file, or exit.

That is the main V4 workflow.

---

## Quick start

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
chmod +x scripts/*.sh
./scripts/setup.sh
source .venv/bin/activate
```

Copy the environment file:

```bash
cp .env.example .env
```

Add your OpenAI API key to `.env`:

```text
OPENAI_API_KEY=your-api-key-here
```

Then run:

```bash
jsonlogic scan .
```

For a detailed walkthrough, see [Getting Started](docs/GETTING_STARTED.md).

---

## You can still use direct commands

If you already know which file you want:

```bash
# Normal explanation
jsonlogic explain workflow.json

# Python
jsonlogic explain workflow.json --to python

# JavaScript
jsonlogic explain workflow.json --to javascript

# TypeScript
jsonlogic explain workflow.json --to typescript

# Flow diagram
jsonlogic explain workflow.json --to mermaid
```

Save output with:

```bash
jsonlogic explain workflow.json --to python --out workflow.py
```

---

## What V4 can show you

| View | What it is for |
| --- | --- |
| Normal logic | Understand what the JSON is doing without code |
| Python | See the behavior as familiar Python logic |
| JavaScript | See conditions and flow as modern JavaScript |
| TypeScript | JavaScript-style logic with useful inferred types |
| Mermaid | Visualize execution flow and branches |

## Example

Given:

```json
{
  "trigger": "order.created",
  "rules": [
    {
      "if": {"field": "order.total", "operator": ">", "value": 10000},
      "then": {"action": "request_manager_approval"}
    }
  ],
  "default_action": "auto_approve"
}
```

Normal logic might be represented as:

```text
When an order is created, check its total.

If the total is greater than 10,000:
  Request manager approval.

Otherwise:
  Auto-approve the order.
```

A JavaScript developer can instead choose **Show as JavaScript** and reason about the same behavior in familiar syntax.

---

## Interactive vs non-interactive scan

`jsonlogic scan .` is interactive only when running in a real terminal.

This means shell scripts, CI jobs, pipes, and redirected output remain predictable.

Force the traditional list view with:

```bash
jsonlogic scan . --no-interactive
```

Get machine-readable scan data with:

```bash
jsonlogic scan . --json
```

Project scanning itself is local and deterministic. The scanner does **not** upload every JSON file it discovers. A selected file enters the AI semantic pipeline only when you choose a view for it.

Common vendor/generated directories such as `.git`, `.venv`, `node_modules`, `dist`, `build`, and `.next` are ignored.

---

## Why the tool does not translate JSON directly to code

A direct AI conversion can produce code that looks good but subtly changes the meaning.

JSON Logic Agent uses this pipeline:

```text
JSON
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
Final view + fidelity score
```

`LogicModel` is the semantic boundary. The agent first determines what the JSON appears to mean, challenges that interpretation, and only then renders Python, JavaScript, TypeScript, normal logic, or Mermaid.

The reviewer compares the final representation against both the original JSON and `LogicModel`.

## Fidelity score

Each semantic translation reports a score such as:

```text
Fidelity score: 96/100
```

This is the reviewer's estimate of how closely the output preserves the meaning supported by the source JSON. It is not a mathematical guarantee, and generated code should be reviewed before production use.

For difficult files, inspect the pipeline:

```bash
jsonlogic explain file.json --show-trace
```

Or save it:

```bash
jsonlogic explain file.json --trace-out trace.json
```

---

## What JSON can it help with?

- workflows and automations
- rules engines
- application configuration
- permissions and access policies
- schemas
- API structures
- state machines
- infrastructure configuration
- ordinary JSON data

If a JSON file is simply data, the agent should say that rather than inventing executable logic.

---

## Claude Code

```bash
claude
```

Suggested prompt:

```text
Read CLAUDE.md, AGENTS.md and README.md. Run the tests and explain JSON Logic Agent V4 before making changes. Preserve the interactive scan UX and the LogicModel fidelity pipeline.
```

## Codex

```bash
codex
```

Suggested prompt:

```text
Read AGENTS.md and README.md. Run the tests and explain JSON Logic Agent V4 before making changes. Preserve the interactive scan UX and the LogicModel fidelity pipeline.
```

---

## Documentation

- [Getting Started](docs/GETTING_STARTED.md) — installation and first use
- [Command Reference](docs/COMMANDS.md) — CLI commands and options
- [V2 Architecture](docs/V2_ARCHITECTURE.md) — underlying semantic fidelity architecture
- [CLAUDE.md](CLAUDE.md) — Claude Code instructions
- [AGENTS.md](AGENTS.md) — Codex/coding-agent instructions

## Development

```bash
pytest -q
```

Current package version: **0.4.0**.

## Core rule

> **Understand first. Translate second.**
