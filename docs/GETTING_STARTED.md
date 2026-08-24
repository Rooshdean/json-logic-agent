# Getting Started with JSON Logic Agent V4

JSON Logic Agent is for developers who can understand code but find large or unfamiliar JSON difficult to reason about.

V4 makes the normal workflow interactive: **scan → choose a file → choose how you want to see it**.

## 1. Install

You need Python 3.10+, Git, and an OpenAI API key.

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
chmod +x scripts/*.sh
./scripts/setup.sh
source .venv/bin/activate
```

## 2. Configure the API key

```bash
cp .env.example .env
```

Edit `.env`:

```text
OPENAI_API_KEY=your-api-key-here
```

Never commit your real API key.

## 3. Start V4

Move into a project containing JSON and run:

```bash
jsonlogic scan .
```

Use **↑ / ↓** to select a file and press **Enter**.

You will then see:

```text
Explain in normal logic
Show as Python
Show as JavaScript
Show as TypeScript
Draw as Mermaid diagram
Choose another file
Exit
```

Choose the representation that makes the JSON easiest for you to understand.

After the result, V4 lets you:

- view the same file another way
- choose another JSON file
- exit

## 4. Example workflow

Suppose a project contains:

```text
my-project/
├── package.json
├── config.json
├── permissions.json
└── workflows/
    └── approval.json
```

Run:

```bash
cd my-project
jsonlogic scan .
```

Select `workflows/approval.json`, then choose **Show as JavaScript**.

If JavaScript still does not make the flow obvious, choose **Use another view for this file** and then **Draw as Mermaid diagram**.

You do not need to remember the individual `--to` commands when using interactive mode.

## 5. Direct commands are still available

```bash
jsonlogic explain approval.json
jsonlogic explain approval.json --to python
jsonlogic explain approval.json --to javascript
jsonlogic explain approval.json --to typescript
jsonlogic explain approval.json --to mermaid
```

These are useful for scripts, repeatable workflows, or when you already know exactly what you want.

## 6. Non-interactive scanning

If you only want the discovered file list:

```bash
jsonlogic scan . --no-interactive
```

For JSON output:

```bash
jsonlogic scan . --json
```

When stdin/stdout are not attached to a real terminal — for example in CI or a shell pipe — `scan` automatically uses non-interactive output.

## 7. Save generated output

```bash
jsonlogic explain approval.json --to python --out approval.py
jsonlogic explain approval.json --to mermaid --out approval.mmd
```

Generated code is an aid for understanding semantics. JSON Logic Agent never automatically executes it.

## 8. Fidelity and uncertainty

The semantic pipeline is:

```text
JSON
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
Final output + fidelity score
```

The reviewer reports a fidelity score estimating how closely the generated representation preserves the meaning supported by the JSON.

For difficult files:

```bash
jsonlogic explain approval.json --show-trace
```

Save the trace with:

```bash
jsonlogic explain approval.json --trace-out trace.json
```

The trace exposes assumptions and ambiguity instead of hiding them.

## 9. What kinds of JSON can it help with?

- workflow definitions
- automation rules
- configuration
- permissions/access policies
- schemas
- API structures
- state machines
- infrastructure configuration
- ordinary data

Not every JSON file represents executable logic. The agent should identify data-only JSON rather than invent behavior.

## 10. Troubleshooting

### `jsonlogic: command not found`

```bash
source .venv/bin/activate
```

If needed:

```bash
./scripts/setup.sh
```

### The interactive menu does not appear

Make sure you are running in a normal interactive terminal and did not pass `--no-interactive` or `--json`.

Update your installation after pulling V4 so the `questionary` dependency is installed:

```bash
git pull
./scripts/setup.sh
```

### API authentication error

Check `.env` contains a valid `OPENAI_API_KEY`.

### I only want to find JSON, not send it to AI

Run:

```bash
jsonlogic scan . --no-interactive
```

Scanning is local. Files enter the semantic AI pipeline only when you choose to explain/render one.

## 11. Developing with Claude Code or Codex

Claude Code:

```bash
claude
```

Codex:

```bash
codex
```

Both have repository-specific instructions in `CLAUDE.md` and `AGENTS.md`.
