# JSON Logic Agent V3

**Understand JSON without having to think in JSON.**

JSON Logic Agent is for developers who are comfortable with code but may not be comfortable reading large or unfamiliar JSON structures. Give it a JSON file and ask to see the same meaning as normal logic, Python, JavaScript, TypeScript, or a Mermaid flow diagram.

```text
JSON → Inspector → Logic Architect → Critic → LogicModel → Generator → Reviewer
                                                        ├─ normal logic
                                                        ├─ Python
                                                        ├─ JavaScript
                                                        ├─ TypeScript
                                                        └─ Mermaid
```

The V2 fidelity pipeline remains underneath V3. `LogicModel` is still the semantic boundary: the tool does not simply rename JSON keys and pretend that is understanding.

## Quick start

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
chmod +x scripts/*.sh
./scripts/setup.sh
source .venv/bin/activate
```

Add `OPENAI_API_KEY` to `.env`.

## The V3 developer workflow

### I found a JSON file and just want to understand it

```bash
jsonlogic explain workflow.json
```

### Show me the same logic as JavaScript

```bash
jsonlogic explain workflow.json --to javascript
```

### Show it as Python

```bash
jsonlogic explain workflow.json --to python
```

### Show it as TypeScript

```bash
jsonlogic explain workflow.json --to typescript
```

### Draw the flow

```bash
jsonlogic explain workflow.json --to mermaid
```

### Save the result

```bash
jsonlogic explain workflow.json --to python --out workflow.py
jsonlogic explain workflow.json --to mermaid --out workflow.mmd
```

## Scan an unfamiliar project

V3 can discover JSON files before you decide which one to inspect:

```bash
jsonlogic scan .
```

Example output:

```text
package.json
  → node-package-manifest: Node.js package metadata, scripts, and dependencies

auth-rules.json
  → workflow-or-automation: Likely contains executable workflow or automation logic

permissions.json
  → access-policy: Likely describes roles, permissions, or policy rules
```

The scanner intentionally skips common generated/vendor directories such as `.git`, `.venv`, `node_modules`, `dist`, `build`, and `.next`.

For tooling or scripting:

```bash
jsonlogic scan . --json
```

The scan itself is local and deterministic; it does not send every discovered JSON file to the model. A file is sent through the semantic pipeline only when you choose to explain/translate it.

## Inspect the reasoning artifacts

```bash
jsonlogic explain workflow.json --to python --show-trace
```

Or save the trace:

```bash
jsonlogic explain workflow.json --to python --trace-out trace.json
```

Each translation receives a reviewer fidelity score.

## Backward compatibility

The old V1/V2 syntax still works:

```bash
jsonlogic workflow.json --to python
```

The recommended V3 syntax is:

```bash
jsonlogic explain workflow.json --to python
```

## What the five stages do

1. **JSON Inspector** — identifies structure, likely purpose, candidate inputs/outputs, conditions, actions, dependencies, ambiguity, and confidence.
2. **Logic Architect** — converts supported observations into the canonical `LogicModel`.
3. **Ambiguity Critic** — challenges unsupported assumptions, dropped branches, and ordering mistakes.
4. **Generator** — renders the reviewed model into the developer's preferred representation.
5. **Reviewer** — compares the output against both the original JSON and final LogicModel and can correct semantic drift.

See `docs/V2_ARCHITECTURE.md` for the underlying fidelity contracts.

## Claude Code

```bash
claude
```

Suggested first prompt:

```text
Read CLAUDE.md, AGENTS.md, README.md and the architecture docs. Run the tests. This is V3 of JSON Logic Agent: a developer-focused JSON reverse engineer. Preserve the Inspector -> Architect -> Critic -> LogicModel -> Generator -> Reviewer fidelity pipeline while improving the developer experience.
```

## Codex

```bash
codex
```

Suggested first prompt:

```text
Read AGENTS.md, README.md and the architecture docs. Run the tests. Preserve LogicModel as the canonical semantic boundary and keep scan/discovery local unless the user explicitly chooses a file to translate.
```

## Programmatic usage

```python
from json_logic_agent import JsonLogicAgent

agent = JsonLogicAgent()
result = agent.translate_file("workflow.json", target="typescript")

print(result.rendered_output)
print(result.metadata["fidelity_score"])
```

Project scanning:

```python
from json_logic_agent.scanner import scan_project

scan = scan_project(".")
for file in scan.files:
    print(file.path, file.likely_kind)
```

## Supported render targets

- `logic` — normal operational explanation
- `python` — Python 3.10+
- `javascript` — modern JavaScript
- `typescript` — typed JavaScript representation
- `mermaid` — flowchart source

## Safety and fidelity rules

- Never invent missing business rules.
- Do not turn candidate semantics into facts without source support.
- Preserve defaults, conditions, branches, and ordering.
- External operations absent from the JSON become TODOs/placeholders.
- Data-only JSON is identified as data rather than fabricated into a workflow.
- Generated code is never automatically executed.
- The reviewer checks output against both source JSON and `LogicModel`.

## Version

Current package version: **0.3.0**.

## Next useful V3.x work

- interactive terminal picker after `jsonlogic scan .`
- explain an entire selected folder as a system
- dependency graph across related JSON files
- provider abstraction for OpenAI / Anthropic / local models
- confidence-based clarification questions
- semantic regression fixtures
- MCP server mode
