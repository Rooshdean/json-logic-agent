# JSON Logic Agent V2 Architecture

## Goal

V2 improves translation fidelity by separating discovery, semantic modeling, challenge, generation, and review into explicit stages.

```text
JSON
 ↓
JSON Inspector
 ↓
Logic Architect
 ↓
Ambiguity Critic
 ↓
(optional revision)
 ↓
Code Generator
 ↓
Code Reviewer
 ↓
Final output
```

## Canonical semantic boundary

`LogicModel` remains the central representation. Generated Python, JavaScript, or plain-language logic must be based on the final `LogicModel`, never produced as an unreviewed direct JSON-to-code shortcut.

## Stage 1 — JSON Inspector

Purpose: understand structure before committing to meaning.

Output: `InspectionReport`.

Responsibilities:

- classify the likely JSON type;
- identify notable keys and structural patterns;
- surface candidate inputs, outputs, entities, conditions, actions, and dependencies;
- record ambiguities;
- provide a confidence score.

The Inspector may suggest semantics, but its candidates are not facts.

## Stage 2 — Logic Architect

Purpose: construct the first semantic execution model.

Output: draft `LogicModel`.

Responsibilities:

- summarize the actual behavior supported by the source;
- define inputs, outputs, entities, dependencies, conditions, and actions;
- build ordered `LogicStep` objects;
- record assumptions rather than hiding uncertainty;
- explicitly mark data-only JSON when no operational semantics are present.

## Stage 3 — Ambiguity Critic

Purpose: attack the draft before code is generated.

Output: `CritiqueReport`.

Checks:

- unsupported inference;
- missing branches or defaults;
- wrong execution order;
- semantic risks;
- logic omitted from nested structures;
- assumptions incorrectly presented as facts.

The critic returns either `accept` or `revise`.

When revision is required, the Logic Architect receives the original JSON, draft model, and critique and returns a corrected final `LogicModel`.

## Stage 4 — Code Generator

Purpose: render the final model.

Current targets:

- `logic`
- `python`
- `javascript`

Rules:

- preserve branch and condition semantics;
- do not invent integrations;
- use TODOs/placeholders for unresolved external operations;
- do not auto-execute generated code;
- use the original JSON only as a fidelity reference, not as a bypass around the final model.

## Stage 5 — Code Reviewer

Purpose: detect semantic drift after generation.

Output: `ReviewReport`.

The reviewer compares:

1. original JSON;
2. final `LogicModel`;
3. generated target output.

It returns:

- `pass` or `revise`;
- fidelity score from 0 to 100;
- issues;
- optional complete corrected output.

When `corrected_output` is returned with a `revise` verdict, it replaces the generator output.

## Pipeline trace

Every normal translation can carry a `PipelineTrace` containing:

- inspector report;
- draft logic model;
- critic report;
- final logic model;
- reviewer report.

Use:

```bash
jsonlogic examples/order_workflow.json --to logic --show-trace
```

or:

```bash
jsonlogic examples/order_workflow.json --to python --trace-out trace.json
```

This trace is designed for debugging, evaluation, and future semantic regression tests.

## Backward compatibility

Existing calls remain valid:

```python
agent.translate_file("workflow.json", target="python")
```

and:

```bash
jsonlogic workflow.json --to python
```

The difference is that V2 now performs the multi-stage pipeline internally.

## Extension points

### Provider abstraction

Move model calls behind a provider interface while preserving identical typed stage contracts.

Potential providers:

- OpenAI
- Anthropic
- local/OpenAI-compatible models

### New renderers

Future targets should consume the final `LogicModel`:

- TypeScript
- Mermaid
- pseudocode
- Go
- SQL
- Terraform-oriented explanation

### Batch mode

Recursively process directories and produce one trace/output bundle per JSON file.

### Interactive ambiguity mode

If Inspector confidence is low or Critic identifies material uncertainty, optionally ask the user a targeted question before generation.

### Regression evaluation

Store source JSON plus expected semantic invariants rather than brittle exact prose outputs. Examples:

- expected condition count;
- required action names;
- expected branch relationships;
- prohibited invented dependencies.

## Safety and fidelity principles

1. JSON structure is not automatically executable logic.
2. Candidates are not facts.
3. Assumptions must remain visible.
4. Unknown external actions stay unresolved.
5. Generated code is representation, not permission to execute.
6. Fidelity matters more than stylistic elegance.
7. Every stage must remain independently inspectable.
