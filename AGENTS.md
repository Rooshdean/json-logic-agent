# AGENTS.md

## Mission

JSON Logic Agent V5 reverse-engineers generic JSON and exported n8n workflows into normal logic, Python, JavaScript, TypeScript, or Mermaid.

## n8n contract

Detect n8n exports deterministically and analyze their graph locally before semantic interpretation.

Preserve:

`n8n JSON -> n8n analyzer -> Inspector -> Architect -> Critic -> LogicModel -> Generator -> Reviewer`

`jsonlogic n8n file.json --report-only` must not require an LLM/API call.

The deterministic report may inventory node/credential types but must never expose secret credential values. Risk findings are conservative review signals, not claims that a workflow is broken.

## Generic JSON contract

Preserve `JSON -> Inspector -> Architect -> Critic -> LogicModel -> Generator -> Reviewer`. Never bypass LogicModel.

## UX

`jsonlogic scan .` labels detected exports `[n8n-workflow]`. Interactive mode only auto-starts on TTYs; `--no-interactive`, `--json`, pipes, and CI remain deterministic.

## Development rules

- Python 3.10+.
- Keep deterministic n8n parsing in `n8n.py` separate from LLM prompts.
- Preserve n8n connection source, target, connection type, and output index.
- Treat expressions, Code nodes, AI nodes, HTTP calls, sub-workflows, and error settings as high-value analysis inputs.
- Never invent missing business behavior.
- Never auto-execute generated code.
- Add tests/fixtures for n8n parser changes.
- Run `pytest -q` before/after edits.

## Important files

- `src/json_logic_agent/n8n.py`
- `src/json_logic_agent/agent.py`
- `src/json_logic_agent/prompts.py`
- `src/json_logic_agent/scanner.py`
- `src/json_logic_agent/interactive.py`
- `src/json_logic_agent/cli.py`
- `docs/N8N_WORKFLOWS.md`

## Product direction

Prioritize richer node taxonomy, expression/data lineage, accurate branch labeling, n8n error workflows, Execute Workflow resolution, AI agent/tool graphs, and cross-workflow dependencies without weakening fidelity.
