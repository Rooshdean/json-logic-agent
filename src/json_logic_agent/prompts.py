SYSTEM_PROMPT = """
You are JSON Logic Agent, a senior software architect and code translator.

Your job is NOT to merely restate JSON keys. Infer the operational logic represented by the JSON while clearly separating facts from assumptions.

For every JSON input:
1. Classify what the JSON appears to represent: configuration, workflow, API payload, state machine, rules engine, automation, schema, data record, UI config, infrastructure config, or another appropriate category.
2. Identify inputs, outputs, entities, conditions, actions, dependencies, and execution order.
3. Produce a normalized intermediate logic model.
4. Never invent missing business rules. Record uncertain interpretations under assumptions.
5. If the JSON is data-only and has no executable semantics, say so explicitly.
6. When generating Python or JavaScript, preserve the inferred semantics and add TODO comments where the source does not contain enough information to implement something safely.
7. Do not hide ambiguity. Prefer faithful translation over cleverness.
8. Never automatically execute generated code.
""".strip()


def build_analysis_prompt(source_name: str, json_text: str) -> str:
    return f"""
Analyze the JSON below and return ONLY a JSON object matching this exact shape:
{{
  "summary": "string",
  "json_kind": "string",
  "inputs": ["string"],
  "outputs": ["string"],
  "entities": ["string"],
  "conditions": ["string"],
  "actions": ["string"],
  "dependencies": ["string"],
  "steps": [
    {{
      "order": 1,
      "title": "string",
      "explanation": "string",
      "condition": "string or null",
      "action": "string or null"
    }}
  ],
  "assumptions": ["string"]
}}

Source: {source_name}

JSON:
{json_text}
""".strip()


def build_render_prompt(target: str, logic_json: str, original_json: str) -> str:
    if target == "logic":
        instruction = (
            "Render the logic model as clear normal-language operational logic for a technical "
            "but non-programmer reader. Use concise headings and ordered steps."
        )
    elif target == "python":
        instruction = (
            "Render the logic as clean Python 3.10+ code. Prefer functions, explicit conditions, "
            "and TODO comments for unresolved external operations. Return code only."
        )
    else:
        instruction = (
            "Render the logic as modern JavaScript (ES2022+). Prefer functions, plain objects, "
            "explicit conditions, async functions when external operations are implied, and TODO "
            "comments for unresolved operations. Return code only."
        )

    return f"""
{instruction}

Normalized logic model:
{logic_json}

Original JSON for fidelity checking:
{original_json}
""".strip()
