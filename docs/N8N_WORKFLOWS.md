# n8n Workflow Intelligence — V5

JSON Logic Agent V5 treats exported n8n workflows as a first-class format.

## Why

An n8n export can be difficult to review outside the visual editor. The JSON contains node definitions, parameters, expressions, credentials references, and a separate connection graph. V5 reconstructs that structure and then explains what the automation actually does.

## Fastest workflow

Export a workflow from n8n as JSON, then run:

```bash
jsonlogic n8n my-workflow.json
```

V5 automatically performs two layers of analysis:

```text
n8n JSON export
   ↓
Local deterministic n8n parser
   ├─ nodes
   ├─ connections
   ├─ triggers
   ├─ decisions
   ├─ integrations
   ├─ credentials types
   ├─ expressions
   ├─ disconnected nodes
   └─ review/risk signals
   ↓
Inspector → Architect → Critic → LogicModel → Generator → Reviewer
   ↓
Normal logic / Python / JavaScript / TypeScript / Mermaid
```

## Local report only

If you want to inspect the workflow without making an AI/API call:

```bash
jsonlogic n8n my-workflow.json --report-only
```

This produces a deterministic inventory similar to:

```text
N8N WORKFLOW INTELLIGENCE
=========================
Workflow: Customer Intake
Nodes: 12
Connections: 13
Triggers: Customer Webhook
Decision nodes: Has Email?, Existing Customer?
Code nodes: Normalize Payload
AI nodes: Customer Classifier
Integrations: HTTP/API, postgres, slack
Credential types referenced: httpHeaderAuth, postgresApi, slackApi
Disconnected nodes: Old Debug Node
Terminal nodes: Respond Success, Respond Error
```

For machine-readable output:

```bash
jsonlogic n8n my-workflow.json --report-only --report-json
```

The local report does not require the model to understand the workflow.

## Deep-dive views

Normal business/developer logic:

```bash
jsonlogic n8n my-workflow.json
```

Conceptual JavaScript equivalent:

```bash
jsonlogic n8n my-workflow.json --to javascript
```

Conceptual Python equivalent:

```bash
jsonlogic n8n my-workflow.json --to python
```

TypeScript:

```bash
jsonlogic n8n my-workflow.json --to typescript
```

Workflow diagram:

```bash
jsonlogic n8n my-workflow.json --to mermaid
```

## Automatic detection

You do not have to use the `n8n` command.

```bash
jsonlogic explain my-workflow.json
```

If the JSON has the characteristic exported n8n node/connection structure, V5 automatically activates n8n workflow intelligence.

You can ask to see the deterministic report too:

```bash
jsonlogic explain my-workflow.json --n8n-report
```

## Interactive mode

```bash
jsonlogic scan .
```

n8n exports appear as:

```text
customer-intake.json  [n8n-workflow]
```

Selecting one changes the action wording to **Deep-dive n8n workflow — ...** so it is obvious that V5 is using the n8n-aware path.

## What V5 looks for

### Workflow topology

- trigger/entry nodes
- outgoing and incoming connections
- branch output indexes
- terminal nodes
- disconnected nodes
- multiple entry points

### Logic

- IF/Switch/filter decisions
- node ordering
- transformations
- n8n expressions such as `{{$json...}}`
- custom Code/Function nodes
- sub-workflow execution

### Integrations

V5 inventories node types that appear to represent external services, HTTP/API calls, AI/model nodes, databases, and sub-workflows.

### Credentials

V5 records **credential types referenced by the export**. It must not expose credential secret values.

### Risk/review signals

The deterministic analyzer can flag review signals such as:

- disconnected nodes
- no obvious trigger
- multiple triggers
- external/integration nodes without explicit node-level error/retry settings
- custom Code nodes requiring manual review

These are review signals, not guarantees that the workflow is broken. n8n can implement behavior at workflow or platform level that is not obvious from a single exported node.

## Important limitation

Generated Python/JavaScript/TypeScript is a **conceptual equivalent of the workflow logic**, not a drop-in replacement for the n8n runtime. n8n nodes provide runtime behavior, credentials handling, retries, expression evaluation, binary-data handling, execution context, and integrations that ordinary generated code would need to implement separately.

## Security

Treat exported workflows as potentially sensitive. They may contain URLs, identifiers, expressions, sample payloads, or configuration. V5 deliberately inventories credential references rather than trying to reveal credential values.

## Debugging the interpretation

```bash
jsonlogic n8n my-workflow.json --show-trace
```

This exposes the semantic stages used after deterministic graph analysis and is useful when a complicated branch or expression was interpreted incorrectly.
