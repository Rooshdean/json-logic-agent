# JSON Logic Agent V3

> **Understand JSON without having to think in JSON.**

JSON Logic Agent helps developers understand large, nested, or unfamiliar JSON files by translating their meaning into something easier to read.

You can turn JSON into:

- plain English logic
- Python
- JavaScript
- TypeScript
- Mermaid flow diagrams

## The simplest example

You have this:

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

Instead of manually working through the JSON, run:

```bash
jsonlogic explain workflow.json
```

The goal is an explanation similar to:

```text
When an order is created, check its total.

If the total is greater than 10,000:
  Request manager approval.

Otherwise:
  Auto-approve the order.
```

Or ask to see the same meaning as code:

```bash
jsonlogic explain workflow.json --to javascript
jsonlogic explain workflow.json --to python
```

That is the core purpose of JSON Logic Agent.

---

## Quick start

### 1. Clone

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
```

### 2. Set up

```bash
chmod +x scripts/*.sh
./scripts/setup.sh
source .venv/bin/activate
```

### 3. Configure your API key

```bash
cp .env.example .env
```

Open `.env` and add your OpenAI API key:

```text
OPENAI_API_KEY=your-api-key-here
```

Never commit your real API key.

### 4. Test it

```bash
jsonlogic explain examples/order_workflow.json
```

For a full beginner walkthrough, read [Getting Started](docs/GETTING_STARTED.md).

---

## What do you want to do?

| I want to... | Run this |
| --- | --- |
| Find JSON files in a project | `jsonlogic scan .` |
| Understand a JSON file normally | `jsonlogic explain file.json` |
| See the logic as Python | `jsonlogic explain file.json --to python` |
| See the logic as JavaScript | `jsonlogic explain file.json --to javascript` |
| See the logic as TypeScript | `jsonlogic explain file.json --to typescript` |
| Draw the workflow | `jsonlogic explain file.json --to mermaid` |
| Save generated output | `jsonlogic explain file.json --to python --out output.py` |
| See how the agent interpreted it | `jsonlogic explain file.json --show-trace` |

See the full [Command Reference](docs/COMMANDS.md).

---

## Start with an unfamiliar project

If you do not even know which JSON file matters, run:

```bash
cd some-project
jsonlogic scan .
```

You may see something like:

```text
package.json
  → node-package-manifest

config.json
  → configuration

permissions.json
  → access-policy

workflows/approval.json
  → workflow-or-automation
```

Then inspect the file you care about:

```bash
jsonlogic explain workflows/approval.json
```

Or translate its logic into the language you are more comfortable with:

```bash
jsonlogic explain workflows/approval.json --to javascript
```

`scan` is local and deterministic. It does **not** automatically upload every JSON file in the project to the model.

---

## Output formats

### Normal logic

```bash
jsonlogic explain file.json
```

Best when you simply want to know what the file is doing.

### Python

```bash
jsonlogic explain file.json --to python
```

Best when Python is easier for you to reason about than JSON.

### JavaScript

```bash
jsonlogic explain file.json --to javascript
```

Best for JavaScript developers who want to see conditions and flow represented as familiar code.

### TypeScript

```bash
jsonlogic explain file.json --to typescript
```

Similar to JavaScript, with useful types/interfaces where the JSON supports them.

### Mermaid

```bash
jsonlogic explain file.json --to mermaid
```

Produces Mermaid flowchart source so you can visualize workflows and branches.

---

## Why not just ask an AI to convert JSON directly to code?

Because a direct conversion can look convincing while changing the meaning.

JSON Logic Agent uses a reviewed semantic pipeline:

```text
                     ┌─────────────────┐
JSON ──► Inspector ─►│ Logic Architect │
                     └────────┬────────┘
                              ▼
                           Critic
                              ▼
                         LogicModel
                              ▼
                          Generator
                              ▼
                           Reviewer
                              ▼
              Logic / Python / JS / TS / Mermaid
```

The important part is `LogicModel`.

The agent first tries to understand what the JSON means. Only after that interpretation has been challenged does it generate your preferred representation.

The final reviewer checks the generated output against both the original JSON and the semantic model and reports a **fidelity score**.

---

## What the fidelity score means

A translation ends with a score such as:

```text
Fidelity score: 96/100
```

This is the reviewer's estimate of how faithfully the generated representation preserves the meaning supported by the source JSON.

It is not a mathematical guarantee. Generated output should still be reviewed before being used as production code.

---

## When the JSON is ambiguous

JSON does not always contain enough information to know exactly what an application does.

JSON Logic Agent is designed to expose that uncertainty instead of quietly inventing missing behavior.

Run:

```bash
jsonlogic explain file.json --show-trace
```

This lets you inspect:

```text
InspectionReport
      ↓
Draft LogicModel
      ↓
CritiqueReport
      ↓
Final LogicModel
      ↓
ReviewReport
```

Save it with:

```bash
jsonlogic explain file.json --trace-out trace.json
```

---

## What JSON can it help with?

Examples include:

- workflows and automations
- rules engines
- application configuration
- permissions and access policies
- schemas
- API structures
- state machines
- infrastructure configuration
- ordinary JSON data

Not every JSON file contains logic. If a file is just data, the agent should say so rather than inventing executable behavior.

---

## Using it with Claude Code

After cloning and setting up the repository:

```bash
claude
```

Suggested first prompt:

```text
Read CLAUDE.md, AGENTS.md and README.md. Run the tests. Explain how JSON Logic Agent V3 works before making changes.
```

`CLAUDE.md` contains project-specific instructions for Claude Code.

---

## Using it with Codex

```bash
codex
```

Suggested first prompt:

```text
Read AGENTS.md and README.md. Run the tests. Explain how JSON Logic Agent V3 works before making changes.
```

`AGENTS.md` contains repository instructions for Codex.

---

## Programmatic usage

```python
from json_logic_agent import JsonLogicAgent

agent = JsonLogicAgent()

result = agent.translate_file(
    "workflow.json",
    target="javascript",
)

print(result.rendered_output)
print(result.metadata["fidelity_score"])
```

Project scanning:

```python
from json_logic_agent.scanner import scan_project

result = scan_project(".")

for file in result.files:
    print(file.path, file.likely_kind)
```

---

## Documentation

- [Getting Started](docs/GETTING_STARTED.md) — installation and first use
- [Command Reference](docs/COMMANDS.md) — CLI commands and options
- [V2 Architecture](docs/V2_ARCHITECTURE.md) — detailed fidelity pipeline inherited by V3
- [CLAUDE.md](CLAUDE.md) — instructions for Claude Code
- [AGENTS.md](AGENTS.md) — instructions for Codex and coding agents

---

## Development

Run tests:

```bash
pytest -q
```

Or:

```bash
make test
```

Current package version: **0.3.0**.

## Core rule

> **Understand first. Translate second.**

JSON Logic Agent should never produce nicer-looking code at the expense of changing what the JSON actually says.
