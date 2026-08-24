# AGENTS.md

## Mission

JSON Logic Agent V3 helps developers understand unfamiliar JSON by translating its supported semantics into normal logic, Python, JavaScript, TypeScript, or Mermaid.

## Core architecture

Always preserve:

`JSON -> Inspector -> Logic Architect -> Ambiguity Critic -> LogicModel -> Generator -> Reviewer -> output`

Never bypass `LogicModel`.

## V3 CLI contract

```bash
jsonlogic scan .
jsonlogic explain file.json [--to logic|python|javascript|typescript|mermaid]
```

Preserve legacy `jsonlogic file.json --to ...` behavior where practical.

`scan` is local discovery. Do not turn it into implicit bulk LLM ingestion. Multi-file semantic analysis should require an explicit user action/selection.

## Development rules

- Python 3.10+.
- Typed Pydantic stage outputs.
- Never invent missing business rules.
- Preserve conditions, defaults, branches, and ordering.
- Data-only JSON remains data-only.
- New renderers consume final `LogicModel`.
- Never execute generated code automatically.
- Add tests for scanner, schema, CLI, or orchestration changes.
- Keep generated explanations useful to a developer, not merely descriptive of JSON syntax.

## Important files

- `src/json_logic_agent/agent.py` — semantic orchestration.
- `src/json_logic_agent/models.py` — stage models and LogicModel.
- `src/json_logic_agent/prompts.py` — prompts/render targets.
- `src/json_logic_agent/scanner.py` — deterministic local project scanner.
- `src/json_logic_agent/cli.py` — V3 UX.
- `docs/V2_ARCHITECTURE.md` — underlying fidelity contract.

## Workflow

Before and after edits run `pytest -q`. For semantic changes inspect `--show-trace`. For discovery changes test `jsonlogic scan .` and ensure vendor/generated directories remain excluded.

## Product direction

Prioritize interactive file selection, explicitly selected multi-file/system understanding, dependency graphs, provider abstraction, confidence-based clarification, and MCP mode while keeping the fidelity pipeline inspectable.
