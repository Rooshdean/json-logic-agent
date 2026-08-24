# CLAUDE.md

## Project

You are working on **JSON Logic Agent V3**: a developer-focused JSON reverse engineer for people who understand programming but do not necessarily want to read or mentally parse complex JSON.

A user should be able to say: "show me what this JSON does as normal logic, Python, JavaScript, TypeScript, or a diagram."

## Non-negotiable fidelity architecture

Preserve:

`JSON -> Inspector -> Logic Architect -> Ambiguity Critic -> LogicModel -> Generator -> Code Reviewer -> output`

`LogicModel` is canonical. Never implement a direct JSON-to-code shortcut.

## V3 developer experience

Primary commands:

```bash
jsonlogic scan .
jsonlogic explain file.json
jsonlogic explain file.json --to python
jsonlogic explain file.json --to javascript
jsonlogic explain file.json --to typescript
jsonlogic explain file.json --to mermaid
```

The old `jsonlogic file.json --to ...` syntax should remain compatible.

Project scanning must remain local/deterministic by default. Do not send every discovered project file to a model merely to list/classify files.

## Stage ownership

- Inspector: structure, candidates, ambiguity, confidence.
- Architect: evidence-backed canonical LogicModel.
- Critic: challenge assumptions, missing branches, and ordering.
- Generator: render only from final LogicModel, using source for fidelity context.
- Reviewer: compare output with source + LogicModel and correct semantic drift.

## Supported targets

`logic`, `python`, `javascript`, `typescript`, `mermaid`.

New targets must consume the final LogicModel.

## Behavior

- Optimize explanations for developers who understand code but may dislike JSON.
- Explain purpose and flow, not just keys.
- Never invent missing business rules.
- Preserve conditions, defaults, branches, and order.
- Mark unresolved external behavior with TODOs/placeholders.
- Identify data-only JSON honestly.
- Never auto-execute generated code.

## Development workflow

Before and after edits:

```bash
pytest -q
```

Useful debugging:

```bash
jsonlogic scan .
jsonlogic explain examples/order_workflow.json --show-trace
```

## Important files

- `src/json_logic_agent/agent.py` — five-stage orchestration.
- `src/json_logic_agent/models.py` — canonical semantic/stage models.
- `src/json_logic_agent/prompts.py` — role prompts and render targets.
- `src/json_logic_agent/scanner.py` — local project discovery/classification.
- `src/json_logic_agent/cli.py` — V3 developer UX.
- `docs/V2_ARCHITECTURE.md` — fidelity-stage contract inherited by V3.

## V3.x priorities

1. interactive terminal picker after project scan;
2. multi-file/system explanation with explicit user selection;
3. dependency graph across related JSON files;
4. provider abstraction;
5. confidence-based clarification;
6. MCP server mode.
