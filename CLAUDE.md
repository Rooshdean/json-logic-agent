# CLAUDE.md

## Project

You are working on **JSON Logic Agent V2**: a multi-stage agent that reads arbitrary JSON, explains its operational meaning in normal language, and optionally converts that meaning into Python or JavaScript.

## Non-negotiable architecture

Preserve this pipeline:

`JSON -> Inspector -> Logic Architect -> Ambiguity Critic -> Code Generator -> Code Reviewer -> output`

The `LogicModel` remains the canonical semantic intermediate representation. Never implement JSON-to-code as a direct shortcut.

## Stage ownership

### JSON Inspector
- classifies the JSON;
- identifies structural signals and candidate semantics;
- records ambiguities and confidence;
- does not decide final business logic.

### Logic Architect
- creates the draft `LogicModel`;
- derives execution order, conditions, actions, inputs, outputs, entities, and dependencies;
- may use inspector observations only when supported by the original source.

### Ambiguity Critic
- challenges the draft against the original JSON;
- detects unsupported inference, missing logic, ordering problems, and semantic risks;
- returns `accept` or `revise`.

### Code Generator
- renders only from the final `LogicModel` plus original JSON for fidelity checking;
- supports `logic`, `python`, and `javascript`;
- uses TODOs for unresolved external behavior.

### Code Reviewer
- compares generated output with BOTH the original JSON and final `LogicModel`;
- scores fidelity from 0 to 100;
- may return a corrected complete output when revision is needed.

## Behavior

When interpreting JSON:

- classify before assuming executable behavior;
- distinguish source facts from assumptions;
- never invent missing business rules;
- explicitly identify data-only JSON;
- preserve conditions, defaults, branches, and execution ordering;
- use TODOs/placeholders for external operations whose implementation is absent;
- never automatically execute generated code.

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

Debug the entire reasoning pipeline with:

```bash
jsonlogic examples/order_workflow.json --to logic --show-trace
```

Or save it:

```bash
jsonlogic examples/order_workflow.json --to python --trace-out trace.json
```

## Key source files

- `src/json_logic_agent/models.py`: typed V2 pipeline artifacts and canonical `LogicModel`.
- `src/json_logic_agent/prompts.py`: role-specific prompts for all five stages.
- `src/json_logic_agent/agent.py`: V2 pipeline orchestration.
- `src/json_logic_agent/cli.py`: command-line interface and trace inspection.
- `docs/V2_ARCHITECTURE.md`: architecture contract.

## Coding style

Keep implementation small and explicit. Prefer typed models and testable stage methods. Avoid adding agent frameworks unless they solve a concrete requirement. Provider abstractions should not weaken the V2 stage boundaries.

## Roadmap priority

When asked to improve the project without a more specific requirement, prioritize:

1. provider abstraction (OpenAI/Anthropic/local);
2. directory/batch mode;
3. TypeScript and Mermaid renderers;
4. semantic regression fixtures;
5. MCP server mode;
6. interactive ambiguity clarification;
7. optional iterative reviewer loop with a strict max revision count.
