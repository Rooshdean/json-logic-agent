# AGENTS.md

## Mission

This repository contains **JSON Logic Agent**. It converts arbitrary JSON into a normalized semantic logic model and can render that model as plain-language logic, Python, or JavaScript.

## Core architecture

Always preserve this pipeline:

`JSON -> analysis -> LogicModel -> renderer -> target output`

Do not bypass `LogicModel` by translating source JSON directly to code. The intermediate representation is the main fidelity and safety boundary.

## Development rules

- Use Python 3.10+.
- Keep provider-specific API code isolated in `src/json_logic_agent/agent.py` or future provider modules.
- Never invent missing business rules. Surface uncertainty as assumptions or TODOs.
- Data-only JSON must be identified as data-only rather than falsely interpreted as executable behavior.
- New render targets should consume `LogicModel`.
- Add tests for schema or translation behavior changes.
- Keep the CLI backward compatible unless a task explicitly requires a breaking change.
- Do not execute generated Python or JavaScript automatically.
- Preserve source semantics over producing elegant-looking code.

## Important files

- `src/json_logic_agent/agent.py` — analysis and rendering orchestration.
- `src/json_logic_agent/models.py` — normalized intermediate representation.
- `src/json_logic_agent/prompts.py` — semantic-analysis and renderer prompts.
- `src/json_logic_agent/cli.py` — CLI entry point.
- `examples/` — representative JSON inputs.
- `tests/` — tests.

## Before changing code

1. Read `README.md`.
2. Inspect the relevant source files.
3. Run `pytest -q`.
4. Explain any architecture change that would alter `LogicModel`.

## After changing code

1. Run `pytest -q`.
2. Run an example translation if an API key is available.
3. Update README/agent instructions when user-facing behavior changes.

## Product direction

Prefer additions that strengthen semantic understanding and fidelity. Useful next targets include TypeScript, Mermaid, pseudocode, recursive directory processing, provider abstraction, a reviewer pass, and MCP server mode.
