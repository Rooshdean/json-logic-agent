# Getting Started with JSON Logic Agent V5.1

JSON Logic Agent helps developers understand unfamiliar JSON and exported n8n workflows. Standalone AI-assisted analysis uses OpenRouter; local scanning and n8n structural reports require no API key.

## 1. Install Python 3.10+

Check:

```bash
python3 --version
```

If macOS reports Python 3.9.x and you use Homebrew:

```bash
brew install python@3.12
```

## 2. Install JSON Logic Agent

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## 3. Configure OpenRouter

```bash
cp .env.example .env
```

Edit `.env`:

```text
OPENROUTER_API_KEY=your-openrouter-key
JSON_LOGIC_MODEL=anthropic/claude-sonnet-4
```

Use any currently available OpenRouter model ID you prefer.

## 4. Verify local functionality first

```bash
jsonlogic --help
jsonlogic n8n examples/n8n_customer_workflow.json --report-only
```

The second command performs deterministic n8n analysis locally and does not use OpenRouter.

## 5. Run AI-assisted analysis

```bash
jsonlogic n8n examples/n8n_customer_workflow.json
```

Or:

```bash
jsonlogic n8n workflow.json --to javascript
jsonlogic n8n workflow.json --to python
jsonlogic n8n workflow.json --to typescript
jsonlogic n8n workflow.json --to mermaid
```

Override the OpenRouter model per run:

```bash
jsonlogic n8n workflow.json --model <openrouter-model-id>
```

## 6. Interactive project mode

```bash
jsonlogic scan .
```

Use arrow keys to choose a file and representation. n8n exports are detected automatically.

## 7. Generic JSON

```bash
jsonlogic explain config.json
jsonlogic explain config.json --to javascript
```

## 8. Local vs OpenRouter

Local/no API call:

```bash
jsonlogic scan . --no-interactive
jsonlogic scan . --json
jsonlogic n8n workflow.json --report-only
```

OpenRouter semantic analysis:

```bash
jsonlogic explain file.json
jsonlogic n8n workflow.json
```

## 9. Claude Code / Codex

From the repo:

```bash
claude
```

or:

```bash
codex
```

Claude Code/Codex can inspect and develop the repository. When they invoke the standalone `jsonlogic n8n` or `jsonlogic explain` semantic commands, those commands use your OpenRouter configuration.

## Troubleshooting

If installation says Python 3.9 is unsupported, rebuild the virtual environment explicitly with Python 3.12:

```bash
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

If semantic analysis reports `OPENROUTER_API_KEY is required`, check that `.env` exists in the repo root and contains your key.

If you do not want an API call, use `--report-only` for n8n structural analysis.
