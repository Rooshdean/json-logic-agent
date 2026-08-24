# CLAUDE.md

## Project

You are working on **JSON Logic Agent**: an agent that reads arbitrary JSON, explains its operational meaning in normal language, and optionally converts that meaning into Python or JavaScript.

## Non-negotiable architecture

Preserve:

`JSON -> semantic analysis -> LogicModel -> renderer -> output`

Never implement JSON-to-code as a direct shortcut. `LogicModel` is the canonical semantic intermediate representation.

## Behavior

When interpreting JSON:

- classify the JSON before assuming it represents executable logic;
- identify inputs, outputs, entities, conditions, actions, dependencies, and ordering;
- distinguish source facts from assumptions;
- never invent missing business rules;
- explicitly identify data-only JSON;
- preserve conditions and execution ordering;
- use TODOs/placeholders for external operations whose implementation is absent from the JSON.

## Development workflow

Before editing:

```bash
pytest -q
```

After editing:

```bash
pytest -q
```

Useful commands:

```bash
make test
make logic
make python
make javascript
```

## Key source files

- `src/json_logic_agent/models.py`: intermediate semantic model.
- `src/json_logic_agent/prompts.py`: analysis and rendering behavior.
- `src/json_logic_agent/agent.py`: model/API orchestration.
- `src/json_logic_agent/cli.py`: command-line interface.

## Coding style

Keep implementation small and explicit. Prefer typed models and testable functions. Avoid adding frameworks unless they solve a concrete requirement. Do not automatically execute generated code.

## Roadmap priority

When asked to improve the project without a more specific requirement, prioritize:

1. semantic reviewer/critic pass;
2. provider abstraction (OpenAI/Anthropic/local);
3. directory/batch mode;
4. TypeScript and Mermaid renderers;
5. MCP server mode;
6. interactive ambiguity clarification.
