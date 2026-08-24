# AGENTS.md

## Mission

This repository contains **JSON Logic Agent V2**. It converts arbitrary JSON into a normalized semantic logic model and renders that model as plain-language logic, Python, or JavaScript through a reviewable multi-agent pipeline.

## Core architecture

Always preserve:

`JSON -> Inspector -> Logic Architect -> Ambiguity Critic -> Code Generator -> Code Reviewer -> output`

`LogicModel` is the canonical semantic boundary. Do not bypass it by translating JSON directly to code.

## Stage contracts

- **Inspector** discovers structure, candidates, ambiguities, and confidence.
- **Architect** creates the draft `LogicModel` from source evidence.
- **Critic** checks the draft for unsupported inference, missing logic, and ordering errors.
- **Generator** renders the final model to the requested target.
- **Reviewer** compares output against both the original JSON and final model, scores fidelity, and may return corrected output.

## Development rules

- Use Python 3.10+.
- Keep stage outputs typed with Pydantic.
- Never invent missing business rules.
- Data-only JSON must be identified as data-only.
- New render targets must consume the final `LogicModel`.
- Keep CLI behavior backward compatible unless explicitly changing it.
- Do not execute generated Python or JavaScript automatically.
- Preserve source semantics over elegant-looking code.
- Add tests for schema and orchestration behavior changes.
- A reviewer correction must replace the complete generated output, not patch fragments blindly.

## Important files

- `src/json_logic_agent/agent.py` — V2 orchestration and stage methods.
- `src/json_logic_agent/models.py` — typed stage artifacts and canonical `LogicModel`.
- `src/json_logic_agent/prompts.py` — role-specific prompts.
- `src/json_logic_agent/cli.py` — CLI and trace inspection.
- `docs/V2_ARCHITECTURE.md` — detailed architecture contract.
- `examples/` — representative JSON inputs.
- `tests/` — tests.

## Before changing code

1. Read `README.md` and `docs/V2_ARCHITECTURE.md`.
2. Inspect the relevant source files.
3. Run `pytest -q`.
4. Explain any change that alters a stage contract or `LogicModel`.

## After changing code

1. Run `pytest -q`.
2. Run an example translation if an API key is available.
3. Inspect `--show-trace` when changing semantic behavior.
4. Update README/agent instructions when user-facing behavior changes.

## Product direction

Prefer improvements that strengthen fidelity, debuggability, and provider independence. Good next targets are provider abstraction, batch mode, TypeScript, Mermaid, semantic regression fixtures, MCP server mode, and interactive ambiguity clarification.
