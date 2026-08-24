# JSON Logic Agent V4 Command Reference

## Recommended command

```bash
jsonlogic scan .
```

In a real terminal this opens the V4 interactive file/action picker. Use arrow keys and Enter; you do not need to remember output flags.

## Scan options

Interactive scan of current directory:

```bash
jsonlogic scan .
```

Another directory:

```bash
jsonlogic scan /path/to/project
```

Traditional non-interactive file list:

```bash
jsonlogic scan . --no-interactive
```

Machine-readable scan result:

```bash
jsonlogic scan . --json
```

Maximum JSON size considered by scanner:

```bash
jsonlogic scan . --max-bytes 2000000
```

Use a specific model when you select a file from the interactive picker:

```bash
jsonlogic scan . --model <model-name>
```

`scan` automatically becomes non-interactive when stdin/stdout are not TTYs, making it safe for pipes and CI.

## Direct translation pattern

```bash
jsonlogic explain <file.json> --to <format>
```

Formats:

```text
logic
python
javascript
typescript
mermaid
```

`logic` is the default.

Normal logic:

```bash
jsonlogic explain file.json
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
jsonlogic explain file.json --to javascript --out generated.js
jsonlogic explain file.json --to typescript --out generated.ts
jsonlogic explain file.json --to mermaid --out diagram.mmd
```

## Inspect interpretation

Final LogicModel:

```bash
jsonlogic explain file.json --show-model
```

Full semantic trace:

```bash
jsonlogic explain file.json --show-trace
```

Save trace:

```bash
jsonlogic explain file.json --trace-out trace.json
```

## Model override

```bash
jsonlogic explain file.json --to python --model <model-name>
```

## Legacy syntax

Still supported:

```bash
jsonlogic file.json --to python
```

Prefer either interactive V4:

```bash
jsonlogic scan .
```

or explicit V3/V4 syntax:

```bash
jsonlogic explain file.json --to python
```
