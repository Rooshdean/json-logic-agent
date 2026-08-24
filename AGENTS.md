# AGENTS.md

## Mission

JSON Logic Agent V4 lets developers browse JSON files interactively and view supported semantics as normal logic, Python, JavaScript, TypeScript, or Mermaid.

## V4 UX contract

`jsonlogic scan .` should open the arrow-key picker only when stdin/stdout are TTYs.

`jsonlogic scan . --no-interactive`, `jsonlogic scan . --json`, CI, pipes, and redirected output must remain non-interactive.

The interactive layer selects a file and target only. It must reuse the normal semantic pipeline rather than implementing separate interpretation logic.

Project scanning remains local and must not implicitly send every discovered JSON file to an LLM.

## Semantic architecture

Always preserve:

`JSON -> Inspector -> Logic Architect -> Ambiguity Critic -> LogicModel -> Generator -> Reviewer -> output`

Never bypass `LogicModel`.

## Development rules

- Python 3.10+.
- Typed Pydantic semantic outputs.
- Keep `questionary` usage isolated to the interactive UX.
- Preserve direct `jsonlogic explain` and legacy commands.
- Never invent missing business rules.
- Never execute generated code automatically.
- New render targets consume final LogicModel.
- Add tests for interactive helper logic, scanner behavior, CLI changes, and semantic contracts.

## Important files

- `src/json_logic_agent/interactive.py` — V4 picker.
- `src/json_logic_agent/cli.py` — CLI/TTY behavior.
- `src/json_logic_agent/scanner.py` — local discovery.
- `src/json_logic_agent/agent.py` — semantic orchestration.
- `src/json_logic_agent/models.py` — typed contracts.
- `src/json_logic_agent/prompts.py` — prompts/render targets.

## Workflow

Run `pytest -q` before and after edits. Test both interactive-terminal behavior and `--no-interactive`/`--json` behavior when changing the V4 UX.

## Product direction

Prioritize picker search/filter, previews, explicit multi-file selection, cross-file dependency graphs, provider abstraction, confidence-based clarification, and MCP mode without weakening semantic fidelity.
