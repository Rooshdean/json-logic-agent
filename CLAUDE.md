# CLAUDE.md

## Project

You are working on **JSON Logic Agent V5**: an interactive JSON reverse engineer with first-class n8n Workflow Intelligence.

## Product promise

A developer should be able to export an n8n workflow JSON and ask: what does this automation actually do, what calls what, where does data branch, what integrations/credentials types does it depend on, what deserves review, and what would the conceptual logic look like in Python/JavaScript/TypeScript or a diagram?

## n8n architecture

Preserve:

`n8n JSON -> deterministic detection/analyzer -> Inspector -> Architect -> Critic -> LogicModel -> Generator -> Reviewer`

The deterministic analyzer lives in `src/json_logic_agent/n8n.py`. It must remain usable without an LLM via `jsonlogic n8n file.json --report-only`.

It should derive graph facts locally: nodes, connections, output indexes, triggers, decisions, integrations, expressions, credential types, code/AI nodes, disconnected/terminal nodes, and conservative review signals.

Never expose credential secret values. Never claim a risk signal proves a workflow is broken.

## Generic JSON

Generic JSON continues through `Inspector -> Architect -> Critic -> LogicModel -> Generator -> Reviewer`. Do not weaken this path while adding n8n features.

## Interactive UX

`jsonlogic scan .` is interactive only on TTY stdin/stdout. n8n files are labeled `[n8n-workflow]` and get n8n deep-dive wording. `--no-interactive` and `--json` remain deterministic/local.

## Commands

```bash
jsonlogic scan .
jsonlogic explain file.json
jsonlogic n8n workflow.json
jsonlogic n8n workflow.json --report-only
jsonlogic n8n workflow.json --to javascript
jsonlogic n8n workflow.json --to mermaid
```

## Development rules

- Python 3.10+.
- Run `pytest -q` before/after edits.
- Keep deterministic parsing separate from AI semantic interpretation.
- Preserve branch output indexes in n8n graph analysis.
- Treat Code nodes and expressions as important semantic evidence.
- Generated code is conceptual and never auto-executed.
- New render targets consume final LogicModel.
- Add fixtures/tests for new n8n node families or topology behavior.

## Important files

- `src/json_logic_agent/n8n.py` — V5 deterministic n8n intelligence.
- `src/json_logic_agent/agent.py` — n8n context injection + semantic pipeline.
- `src/json_logic_agent/scanner.py` — n8n detection during project discovery.
- `src/json_logic_agent/interactive.py` — V5 picker.
- `src/json_logic_agent/cli.py` — `n8n`, `scan`, `explain` commands.
- `docs/N8N_WORKFLOWS.md` — user-facing n8n contract.

## Next priorities

Improve node-type taxonomy, expression/data lineage analysis, branch labels, error-workflow semantics, sub-workflow resolution, AI-agent/tool topology, and cross-workflow dependency graphs while remaining conservative about unsupported behavior.
