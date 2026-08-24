# JSON Logic Agent V2

JSON Logic Agent V2 turns raw JSON into **human-readable operational logic** and can translate that logic into **Python** or **JavaScript** through a reviewed multi-agent pipeline.

## V2 pipeline

```text
JSON
 ↓
JSON Inspector
 ↓
Logic Architect
 ↓
Ambiguity Critic
 ↓
(optional revision)
 ↓
Code Generator
 ↓
Code Reviewer
 ↓
Final output + fidelity score
```

The `LogicModel` is the canonical semantic representation. V2 does not directly map JSON keys to code.

## Why V2 is different

The stages have separate responsibilities:

- **Inspector** discovers structure, likely semantics, ambiguities, and confidence.
- **Architect** creates the draft `LogicModel`.
- **Critic** challenges unsupported inference, missing branches, and ordering errors.
- **Generator** produces plain logic, Python, or JavaScript from the final model.
- **Reviewer** compares generated output against both the source JSON and final model, assigns a fidelity score, and can replace the output if revision is required.

See [`docs/V2_ARCHITECTURE.md`](docs/V2_ARCHITECTURE.md) for the full contract.

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
chmod +x scripts/*.sh
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

## Inspect the whole V2 reasoning pipeline

```bash
jsonlogic examples/order_workflow.json --to logic --show-trace
```

Save the trace for debugging or regression analysis:

```bash
jsonlogic examples/order_workflow.json --to python --trace-out trace.json
```

Each normal run also prints the reviewer fidelity score.

## Claude Code

The root `CLAUDE.md` describes the V2 stage contracts and development rules.

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
./scripts/setup.sh
claude
```

Recommended first prompt:

```text
Read CLAUDE.md, AGENTS.md, README.md, and docs/V2_ARCHITECTURE.md. Run the tests. Explain the Inspector -> Architect -> Critic -> Generator -> Reviewer pipeline, then continue development without bypassing LogicModel.
```

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
Read AGENTS.md and docs/V2_ARCHITECTURE.md. Run the tests and inspect the V2 pipeline. Preserve the typed stage contracts and keep LogicModel as the canonical semantic boundary.
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

### Show only the final LogicModel

```bash
jsonlogic workflow.json --to logic --show-model
```

### Show all V2 stage artifacts

```bash
jsonlogic workflow.json --to logic --show-trace
```

## Programmatic usage

```python
from json_logic_agent import JsonLogicAgent

agent = JsonLogicAgent()
result = agent.translate_file("workflow.json", target="python")

print(result.rendered_output)
print(result.logic)
print(result.metadata["fidelity_score"])
print(result.trace)
```

You can also call individual stages directly:

```python
inspection = agent.inspect(data)
draft = agent.architect(data, inspection)
critique = agent.critique(data, inspection, draft)
final_logic = agent.revise(data, draft, critique)
code = agent.render(data, final_logic, "python")
review = agent.review(data, final_logic, "python", code)
```

## Example input

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

The agent should infer logic equivalent to:

```text
When an order is created, inspect its total.
If the total is greater than 10,000, request manager approval.
Otherwise, use the configured default action and auto-approve the order.
```

A Python rendering may resemble:

```python
def process_order(order):
    if order["total"] > 10_000:
        return request_manager_approval(order)  # TODO: implementation is external

    return auto_approve(order)  # TODO: implementation is external
```

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
├── .github/workflows/
├── docs/
│   └── V2_ARCHITECTURE.md
├── examples/
├── scripts/
├── src/json_logic_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── cli.py
│   ├── models.py
│   └── prompts.py
└── tests/
```

## Development helpers

```bash
make setup
make test
make logic
make python
make javascript
```

## V2 fidelity rules

1. Do not simply describe JSON keys.
2. Infer execution semantics only when the source supports them.
3. Candidate semantics from the Inspector are not automatically facts.
4. Separate facts from assumptions.
5. Never silently invent missing business rules.
6. Preserve conditions, defaults, branches, and ordering.
7. Mark unresolved external operations with TODOs/placeholders.
8. Say explicitly when JSON is data rather than logic.
9. Generated code must never be auto-executed.
10. Keep the complete pipeline inspectable.

## Current roadmap

High-value V3 candidates:

- provider abstraction for OpenAI / Anthropic / local models
- recursive folder and batch mode
- TypeScript output
- Mermaid diagrams
- semantic regression fixtures
- interactive ambiguity clarification
- MCP server mode
- optional bounded reviewer revision loop
