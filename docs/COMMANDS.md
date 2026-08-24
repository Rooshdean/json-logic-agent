# JSON Logic Agent Command Reference

## Basic pattern

```bash
jsonlogic explain <file.json> --to <format>
```

Available formats:

```text
logic
python
javascript
typescript
mermaid
```

`logic` is the default.

## Discover JSON files

Scan the current directory:

```bash
jsonlogic scan .
```

Scan another project:

```bash
jsonlogic scan /path/to/project
```

Machine-readable scan output:

```bash
jsonlogic scan . --json
```

Change the maximum file size inspected by the scanner:

```bash
jsonlogic scan . --max-bytes 2000000
```

## Explain a file

Normal logic:

```bash
jsonlogic explain file.json
```

Equivalent explicit command:

```bash
jsonlogic explain file.json --to logic
```

Python:

```bash
jsonlogic explain file.json --to python
```

JavaScript:

```bash
jsonlogic explain file.json --to javascript
```

TypeScript:

```bash
jsonlogic explain file.json --to typescript
```

Mermaid:

```bash
jsonlogic explain file.json --to mermaid
```

## Save output

```bash
jsonlogic explain file.json --to python --out generated.py
```

```bash
jsonlogic explain file.json --to javascript --out generated.js
```

```bash
jsonlogic explain file.json --to typescript --out generated.ts
```

```bash
jsonlogic explain file.json --to mermaid --out diagram.mmd
```

## Debug the interpretation

Show the final LogicModel:

```bash
jsonlogic explain file.json --show-model
```

Show the full pipeline trace:

```bash
jsonlogic explain file.json --show-trace
```

Save the trace:

```bash
jsonlogic explain file.json --trace-out trace.json
```

Combine options:

```bash
jsonlogic explain file.json \
  --to python \
  --out generated.py \
  --trace-out trace.json
```

## Choose a model

Override `JSON_LOGIC_MODEL` for one translation:

```bash
jsonlogic explain file.json --to python --model <model-name>
```

## Legacy syntax

V1/V2-style commands remain supported:

```bash
jsonlogic file.json --to python
```

For new usage, prefer:

```bash
jsonlogic explain file.json --to python
```
