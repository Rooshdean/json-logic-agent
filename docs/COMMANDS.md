# JSON Logic Agent V5.2 Command Reference

## Interactive project browser

```bash
jsonlogic scan .
```

n8n exports are automatically labeled `[n8n-workflow]`.

## Generic JSON

```bash
jsonlogic explain file.json
jsonlogic explain file.json --to python
jsonlogic explain file.json --to javascript
jsonlogic explain file.json --to typescript
jsonlogic explain file.json --to mermaid
```

## n8n deep dive

```bash
jsonlogic n8n workflow.json
jsonlogic n8n workflow.json --to javascript
jsonlogic n8n workflow.json --to python
jsonlogic n8n workflow.json --to typescript
jsonlogic n8n workflow.json --to mermaid
```

## Local n8n report

```bash
jsonlogic n8n workflow.json --report-only
jsonlogic n8n workflow.json --report-only --report-json
```

## Export complete analysis

Markdown:

```bash
jsonlogic n8n workflow.json --export workflow-report.md
jsonlogic explain file.json --export analysis.md
```

PDF:

```bash
jsonlogic n8n workflow.json --export workflow-report.pdf
jsonlogic explain file.json --export analysis.pdf
```

Combine an output view with a report:

```bash
jsonlogic n8n workflow.json --to mermaid --export workflow-diagram.pdf
jsonlogic n8n workflow.json --to javascript --export workflow-code-review.md
```

The export includes the full report: metadata, n8n intelligence when applicable, semantic deep dive, target output, fidelity score, warnings, and pipeline metadata.

## Save only target output

`--out` intentionally differs from `--export`:

```bash
jsonlogic n8n workflow.json --to javascript --out workflow.js
jsonlogic n8n workflow.json --to mermaid --out workflow.mmd
```

Use `--out` for only the generated code/diagram source. Use `--export` for a complete `.md` or `.pdf` analysis report. Both flags can be used together.

## Semantic debugging

```bash
jsonlogic n8n workflow.json --show-trace
jsonlogic explain file.json --show-model
jsonlogic explain file.json --show-trace
jsonlogic explain file.json --trace-out trace.json
```

## Model override

```bash
jsonlogic n8n workflow.json --model <openrouter-model-id>
jsonlogic explain file.json --model <openrouter-model-id>
```
