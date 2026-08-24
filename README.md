# JSON Logic Agent V5

> **Understand JSON — and deep-dive n8n workflows — without having to think in JSON.**

JSON Logic Agent is for developers who understand code but do not want to mentally parse large JSON files. V5 adds first-class **n8n Workflow Intelligence** on top of the interactive V4 experience.

## Start here

```bash
jsonlogic scan .
```

Use arrow keys to select a JSON file and choose **Normal logic / Python / JavaScript / TypeScript / Mermaid**. Exported n8n workflows are detected automatically and shown as `[n8n-workflow]`.

## n8n deep dive

Export a workflow from n8n and run:

```bash
jsonlogic n8n workflow.json
```

V5 reconstructs the workflow graph before asking the semantic agents to explain it. It analyzes nodes, connections, triggers, branches, integrations, expressions, credential types, custom code, AI nodes, disconnected nodes, terminal paths, and review/risk signals.

Want only the local structural report with **no model/API call**?

```bash
jsonlogic n8n workflow.json --report-only
```

Want to understand the n8n workflow as JavaScript?

```bash
jsonlogic n8n workflow.json --to javascript
```

Or Python / TypeScript / diagram:

```bash
jsonlogic n8n workflow.json --to python
jsonlogic n8n workflow.json --to typescript
jsonlogic n8n workflow.json --to mermaid
```

See the complete [n8n Workflow Guide](docs/N8N_WORKFLOWS.md).

---

## Quick installation

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
chmod +x scripts/*.sh
./scripts/setup.sh
source .venv/bin/activate
cp .env.example .env
```

Add your API key to `.env`:

```text
OPENAI_API_KEY=your-api-key-here
```

Then try:

```bash
jsonlogic scan .
jsonlogic n8n examples/n8n_customer_workflow.json --report-only
jsonlogic n8n examples/n8n_customer_workflow.json
```

## Generic JSON still works

```bash
jsonlogic explain file.json
jsonlogic explain file.json --to python
jsonlogic explain file.json --to javascript
jsonlogic explain file.json --to typescript
jsonlogic explain file.json --to mermaid
```

If `file.json` is an n8n export, `explain` activates n8n intelligence automatically. To print the n8n structural report too:

```bash
jsonlogic explain workflow.json --n8n-report
```

## What V5 adds for n8n

| Capability | V5 behavior |
| --- | --- |
| n8n detection | Recognizes exported workflows from nodes/connections and n8n node types |
| Node graph | Reconstructs source → target connections and branch output indexes |
| Triggers | Identifies likely webhook/trigger entry points |
| Decisions | Identifies IF/Switch/filter-style nodes |
| Integrations | Inventories external/service node types and HTTP/API nodes |
| Expressions | Counts and surfaces n8n `{{...}}` expressions for semantic review |
| Custom code | Identifies Code/Function nodes for deeper manual review |
| AI nodes | Identifies common AI/agent/model node families |
| Credentials | Inventories credential **types/references**, never secret values |
| Graph health | Finds disconnected and terminal nodes |
| Risk signals | Flags missing obvious triggers, disconnected nodes, custom code, and external nodes without explicit node-level retry/error settings |

Risk findings are review signals, not proof that a workflow is broken; n8n behavior can also be configured outside an individual node/export.

## V5 architecture

Generic JSON:

```text
JSON → Inspector → Architect → Critic → LogicModel → Generator → Reviewer
```

n8n export:

```text
n8n JSON
   ↓
Format detection
   ↓
Deterministic n8n analyzer
   ├─ node inventory
   ├─ connection graph
   ├─ branch outputs
   ├─ integrations
   ├─ expressions
   └─ review signals
   ↓
Inspector
   ↓
Logic Architect
   ↓
Ambiguity Critic
   ↓
LogicModel
   ↓
Generator
   ↓
Reviewer
   ↓
Logic / Python / JavaScript / TypeScript / Mermaid
```

The deterministic n8n report gives the semantic agents grounded graph evidence before they interpret the business logic.

## Interactive mode

```bash
jsonlogic scan .
```

An n8n file appears like:

```text
❯ customer-onboarding.json  [n8n-workflow]
```

Selecting it presents n8n deep-dive views. Non-interactive behavior remains available:

```bash
jsonlogic scan . --no-interactive
jsonlogic scan . --json
```

Scanning is local. It does not upload every discovered file.

## Fidelity

V5 still uses `LogicModel` as the canonical semantic boundary and reports a reviewer fidelity score. For complex workflows:

```bash
jsonlogic n8n workflow.json --show-trace
```

Generated Python/JavaScript/TypeScript represents the **conceptual workflow logic**. It is not a drop-in replacement for the n8n runtime and is never automatically executed.

## Documentation

- [Getting Started](docs/GETTING_STARTED.md)
- [n8n Workflow Intelligence](docs/N8N_WORKFLOWS.md)
- [Command Reference](docs/COMMANDS.md)
- [V2 Fidelity Architecture](docs/V2_ARCHITECTURE.md)
- [CLAUDE.md](CLAUDE.md)
- [AGENTS.md](AGENTS.md)

## Development

```bash
pytest -q
```

Current package version: **0.5.0**.

## Core rule

> **Understand first. Translate second. For n8n, reconstruct the workflow before explaining it.**
