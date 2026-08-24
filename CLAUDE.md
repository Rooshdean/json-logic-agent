# CLAUDE.md

## Project

You are working on **JSON Logic Agent V4**: an interactive developer-focused JSON reverse engineer for people who understand programming but do not want to mentally parse complex JSON.

## Primary V4 experience

The default human workflow is:

```text
jsonlogic scan .
      ↓
arrow-key file picker
      ↓
Explain / Python / JavaScript / TypeScript / Mermaid
      ↓
result
      ↓
another view / another file / exit
```

Interactive mode must only auto-start when stdin and stdout are TTYs. Scripts, CI, pipes, and `--no-interactive` must retain deterministic list output. `--json` must always remain machine-readable and non-interactive.

Project scanning remains local. Do not send all discovered files to a model merely to populate the picker.

## Non-negotiable semantic architecture

Preserve:

`JSON -> Inspector -> Logic Architect -> Ambiguity Critic -> LogicModel -> Generator -> Reviewer -> output`

`LogicModel` is canonical. Never implement direct JSON-to-code conversion.

## Supported targets

`logic`, `python`, `javascript`, `typescript`, `mermaid`.

## Important files

- `src/json_logic_agent/interactive.py` — V4 terminal menus and action mapping.
- `src/json_logic_agent/cli.py` — TTY detection and CLI orchestration.
- `src/json_logic_agent/scanner.py` — local deterministic JSON discovery.
- `src/json_logic_agent/agent.py` — semantic pipeline.
- `src/json_logic_agent/models.py` — typed contracts and LogicModel.
- `src/json_logic_agent/prompts.py` — semantic/render prompts.

## Development rules

- Python 3.10+.
- Run `pytest -q` before and after edits.
- Keep the interactive layer thin; it should select a file and target, then call the existing semantic pipeline.
- Do not duplicate semantic logic inside the UI.
- Preserve direct `jsonlogic explain ...` commands and legacy syntax.
- Never auto-execute generated code.
- Never invent missing business rules.
- New output views must consume final LogicModel.

## V4.x priorities

1. search/filter inside the interactive file picker;
2. optional preview panel with file classification/keys before selection;
3. explicit multi-select for related JSON files and system-level explanation;
4. dependency graph across selected files;
5. provider abstraction;
6. confidence-based clarification;
7. MCP mode.
