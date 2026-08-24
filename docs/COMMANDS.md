# JSON Logic Agent V5 Command Reference

## Interactive project browser

```bash
jsonlogic scan .
```

n8n exports are automatically labeled `[n8n-workflow]`.

Non-interactive:

```bash
jsonlogic scan . --no-interactive
jsonlogic scan . --json
```

## Generic JSON

```bash
jsonlogic explain file.json
jsonlogic explain file.json --to logic
jsonlogic explain file.json --to python
jsonlogic explain file.json --to javascript
jsonlogic explain file.json --to typescript
jsonlogic explain file.json --to mermaid
```

If the file is an n8n workflow, detection is automatic.

Print its n8n report before semantic output:

```bash
jsonlogic explain workflow.json --n8n-report
```

## n8n deep-dive command

Default normal-logic deep dive:

```bash
jsonlogic n8n workflow.json
```

JavaScript:

```bash
jsonlogic n8n workflow.json --to javascript
```

Python:

```bash
jsonlogic n8n workflow.json --to python
```

TypeScript:

```bash
jsonlogic n8n workflow.json --to typescript
```

Mermaid:

```bash
jsonlogic n8n workflow.json --to mermaid
```

## n8n local report — no model/API call

Human-readable:

```bash
jsonlogic n8n workflow.json --report-only
```

Machine-readable:

```bash
jsonlogic n8n workflow.json --report-only --report-json
```

## Save output

```bash
jsonlogic n8n workflow.json --to javascript --out workflow.js
jsonlogic explain file.json --to python --out generated.py
```

## Semantic debugging

```bash
jsonlogic n8n workflow.json --show-trace
jsonlogic explain file.json --show-model
jsonlogic explain file.json --show-trace
jsonlogic explain file.json --trace-out trace.json
```

## Model override

```bash
jsonlogic n8n workflow.json --model <model-name>
jsonlogic explain file.json --model <model-name>
jsonlogic scan . --model <model-name>
```

## Legacy syntax

Still supported:

```bash
jsonlogic file.json --to python
```

Recommended V5 entry points are `jsonlogic scan .`, `jsonlogic explain ...`, and `jsonlogic n8n ...`.
