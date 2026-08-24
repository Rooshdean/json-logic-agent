# Getting Started with JSON Logic Agent

This guide assumes you are a developer who can read Python or JavaScript, but JSON files can be difficult to understand when they become large, nested, or configuration-heavy.

JSON Logic Agent answers one simple question:

> **What does this JSON actually mean?**

It can show the answer as:

- normal English logic
- Python
- JavaScript
- TypeScript
- a Mermaid flow diagram

## 1. Install

You need:

- Python 3.10 or newer
- Git
- an OpenAI API key

Clone the project:

```bash
git clone https://github.com/Rooshdean/json-logic-agent.git
cd json-logic-agent
```

Run setup:

```bash
chmod +x scripts/*.sh
./scripts/setup.sh
source .venv/bin/activate
```

## 2. Add your API key

Create a `.env` file in the project root if setup has not already created one.

```bash
cp .env.example .env
```

Open `.env` and set:

```text
OPENAI_API_KEY=your-api-key-here
```

Do not commit your real API key to GitHub.

## 3. Test the installation

Run:

```bash
jsonlogic --help
```

Then try the included example:

```bash
jsonlogic explain examples/order_workflow.json
```

If everything is configured correctly, you should receive a normal-language explanation plus a fidelity score.

## 4. Use it on your own JSON

Imagine your project contains:

```text
my-project/
├── package.json
├── config.json
├── permissions.json
└── workflows/
    └── approval.json
```

First discover the JSON files:

```bash
jsonlogic scan my-project
```

Then choose the file you care about.

### Explain it normally

```bash
jsonlogic explain my-project/workflows/approval.json
```

### Think in JavaScript instead

```bash
jsonlogic explain my-project/workflows/approval.json --to javascript
```

### Think in Python instead

```bash
jsonlogic explain my-project/workflows/approval.json --to python
```

### Use TypeScript

```bash
jsonlogic explain my-project/workflows/approval.json --to typescript
```

### Draw the logic

```bash
jsonlogic explain my-project/workflows/approval.json --to mermaid
```

## 5. Save the output

```bash
jsonlogic explain approval.json --to python --out approval.py
```

Or:

```bash
jsonlogic explain approval.json --to mermaid --out approval.mmd
```

The generated code is for understanding the semantics. JSON Logic Agent does not automatically execute it.

## 6. What does the fidelity score mean?

The tool does not translate JSON directly into code.

It first builds an internal semantic model, challenges that interpretation, generates the requested output, and reviews the result against the original JSON.

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

A higher fidelity score means the reviewer believes the generated representation closely preserves the meaning supported by the original JSON.

It is still AI-generated output. Treat it as an explanation and development aid, especially for important production logic.

## 7. See what the agent inferred

For difficult JSON, use:

```bash
jsonlogic explain approval.json --to python --show-trace
```

This exposes the inspector report, draft logic, critique, final logic model, and reviewer report.

You can save that information:

```bash
jsonlogic explain approval.json --to python --trace-out trace.json
```

This is useful when you want to understand why the agent interpreted something in a particular way.

## 8. Common commands

| What you want | Command |
| --- | --- |
| Find JSON files | `jsonlogic scan .` |
| Explain JSON normally | `jsonlogic explain file.json` |
| Show as Python | `jsonlogic explain file.json --to python` |
| Show as JavaScript | `jsonlogic explain file.json --to javascript` |
| Show as TypeScript | `jsonlogic explain file.json --to typescript` |
| Draw the flow | `jsonlogic explain file.json --to mermaid` |
| Save output | `jsonlogic explain file.json --to python --out output.py` |
| Inspect agent reasoning artifacts | `jsonlogic explain file.json --show-trace` |
| Save the trace | `jsonlogic explain file.json --trace-out trace.json` |

## 9. What kinds of JSON can I use?

Examples include:

- workflow definitions
- automation rules
- application configuration
- permissions and access policies
- schemas
- API structures
- state-machine definitions
- infrastructure configuration
- ordinary JSON data

Not every JSON file contains executable logic. If the file is simply data, the agent should tell you that rather than inventing a workflow.

## 10. Using Claude Code or Codex to develop this project

For Claude Code:

```bash
claude
```

Then ask:

```text
Read CLAUDE.md, AGENTS.md and README.md. Run the tests and explain the JSON Logic Agent architecture before making changes.
```

For Codex:

```bash
codex
```

Then ask:

```text
Read AGENTS.md and README.md. Run the tests and explain the JSON Logic Agent architecture before making changes.
```

## Troubleshooting

### `jsonlogic: command not found`

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

If necessary, run setup again:

```bash
./scripts/setup.sh
```

### OpenAI/API authentication error

Check that `.env` contains a valid `OPENAI_API_KEY`.

### The agent is uncertain about the JSON

Use `--show-trace` and inspect the assumptions, ambiguities, and reviewer issues. The tool is intentionally designed to expose uncertainty instead of silently inventing missing behavior.

### The project contains thousands of JSON files

Use `jsonlogic scan .` first. The scanner ignores common generated/vendor folders and does not automatically send every discovered file to the model.
