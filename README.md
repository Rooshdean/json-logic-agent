# JSON Logic Agent

JSON Logic Agent turns raw JSON into **human-readable operational logic** and can then translate that logic into **Python** or **JavaScript**.

The key architecture is:

```text
JSON file
   ↓
Semantic analysis
   ↓
Normalized Logic Model
   ├──→ Plain-language logic
   ├──→ Python
   └──→ JavaScript
```

The Logic Model is the core product. The agent does not simply pretty-print JSON or map keys directly to code; it first tries to understand what the JSON represents, then renders that interpretation into the requested target.

## What it can understand

- workflows and automations
- rules engines
- API request/response structures
- application configuration
- infrastructure configuration
- state machines
- access policies
- UI configuration
- schemas
- data records

If the input is data-only and does not contain executable logic, the agent should say that rather than inventing behavior.

## Quick start

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
./scripts/setup.sh
```

Add your OpenAI API key to `.env`, then run:

```bash
./scripts/run.sh examples/order_workflow.json logic
./scripts/run.sh examples/order_workflow.json python
./scripts/run.sh examples/order_workflow.json javascript
```

Or activate the environment and use the CLI directly:

```bash
source .venv/bin/activate
jsonlogic examples/order_workflow.json --to logic
jsonlogic examples/order_workflow.json --to python
jsonlogic examples/order_workflow.json --to javascript
```

## Claude Code

This repo contains a root `CLAUDE.md` so Claude Code immediately understands the architecture and development rules.

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
./scripts/setup.sh
claude
```

Recommended first prompt:

```text
Read CLAUDE.md, AGENTS.md, and README.md. Run the tests, explain the current JSON -> LogicModel -> renderer architecture, then help me continue developing the agent without bypassing the LogicModel.
```

A Claude project command also lives at `.claude/commands/translate-json.md`.

## Codex

The root `AGENTS.md` gives Codex repository-level operating instructions.

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
./scripts/setup.sh
codex
```

Recommended first prompt:

```text
Read AGENTS.md and README.md. Run the tests, inspect the JSON -> LogicModel -> renderer pipeline, and continue development while preserving the intermediate semantic model.
```

## CLI usage

### JSON → plain logic

```bash
jsonlogic workflow.json --to logic
```

### JSON → Python

```bash
jsonlogic workflow.json --to python
```

### JSON → JavaScript

```bash
jsonlogic workflow.json --to javascript
```

### Save generated output

```bash
jsonlogic workflow.json --to python --out generated.py
```

### Inspect the intermediate model

```bash
jsonlogic workflow.json --to logic --show-model
```

## Why there is an intermediate Logic Model

Direct JSON-to-code generation can produce convincing code that subtly changes the meaning of the source. JSON Logic Agent therefore uses two passes.

### Pass 1 — Understand

The agent extracts:

- summary
- JSON classification
- inputs
- outputs
- entities
- conditions
- actions
- dependencies
- ordered steps
- assumptions

### Pass 2 — Render

That same `LogicModel` is rendered into plain logic, Python, or JavaScript.

This also makes it easy to add TypeScript, Go, Mermaid, Terraform, SQL, pseudocode, or other targets later.

## Example

Input:

```json
{
  "workflow": "order-approval",
  "trigger": "order.created",
  "rules": [
    {
      "if": {
        "field": "order.total",
        "operator": ">",
        "value": 10000
      },
      "then": {
        "action": "request_manager_approval"
      }
    }
  ],
  "default_action": "auto_approve"
}
```

Possible plain-language interpretation:

```text
When a new order is created, inspect its total value.
If the order total is greater than 10,000, request manager approval.
If no rule redirects the order, auto-approve it.
```

Possible Python representation:

```python
def process_order(order):
    if order["total"] > 10_000:
        return request_manager_approval(order)

    return auto_approve(order)
```

If the JSON names an external action but does not define its implementation, generated code should use a TODO or placeholder rather than inventing infrastructure or side effects.

## Repository structure

```text
json-logic-agent/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── Makefile
├── pyproject.toml
├── .env.example
├── .claude/
│   └── commands/
│       └── translate-json.md
├── examples/
│   └── order_workflow.json
├── scripts/
│   ├── setup.sh
│   └── run.sh
├── src/json_logic_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── cli.py
│   ├── models.py
│   └── prompts.py
└── tests/
    └── test_models.py
```

## Development helpers

```bash
make setup
make test
make logic
make python
make javascript
```

## Programmatic usage

```python
from json_logic_agent import JsonLogicAgent

agent = JsonLogicAgent()
result = agent.translate_file("workflow.json", target="python")

print(result.rendered_output)
print(result.logic)
print(result.warnings)
```

## Agent rules

1. Do not simply describe JSON keys.
2. Infer execution semantics only when the source supports them.
3. Separate facts from assumptions.
4. Never silently invent missing business rules.
5. Preserve conditions and ordering.
6. Mark unresolved external operations with TODOs in generated code.
7. Say explicitly when JSON is data rather than logic.
8. Keep the pipeline `JSON -> LogicModel -> renderer` intact.

## Recommended roadmap

The next major evolution is a multi-agent pipeline:

```text
JSON Inspector
      ↓
Logic Architect
      ↓
Ambiguity Critic
      ↓
Code Generator
      ↓
Code Reviewer
```

High-value additions after that:

- Anthropic/provider abstraction
- recursive folder mode
- TypeScript output
- Mermaid workflow diagrams
- pseudocode output
- semantic reviewer pass
- interactive clarification mode
- REST API
- MCP server mode
- VS Code extension
- GitHub Action for changed JSON files
