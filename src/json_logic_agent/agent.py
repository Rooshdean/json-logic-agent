import json
import os
from pathlib import Path
from typing import Any

from openai import OpenAI

from .models import LogicModel, TranslationResult
from .prompts import SYSTEM_PROMPT, build_analysis_prompt, build_render_prompt


class JsonLogicAgent:
    """Translate JSON into a normalized logic model and optional source code."""

    def __init__(self, model: str | None = None, client: OpenAI | None = None):
        self.model = model or os.getenv("JSON_LOGIC_MODEL", "gpt-5.6")
        self.client = client or OpenAI()

    @staticmethod
    def _normalize_json(data: Any) -> str:
        return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False)

    @staticmethod
    def _strip_markdown_fence(text: str) -> str:
        raw = text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1]
            raw = raw.rsplit("```", 1)[0].strip()
        return raw

    def analyze(self, data: Any, source_name: str = "input.json") -> LogicModel:
        json_text = self._normalize_json(data)
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=build_analysis_prompt(source_name, json_text),
        )
        raw = self._strip_markdown_fence(response.output_text)
        return LogicModel.model_validate_json(raw)

    def render(self, data: Any, logic: LogicModel, target: str) -> str:
        if target not in {"logic", "python", "javascript"}:
            raise ValueError("target must be one of: logic, python, javascript")

        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=build_render_prompt(
                target,
                logic.model_dump_json(indent=2),
                self._normalize_json(data),
            ),
        )
        rendered = response.output_text.strip()
        if target in {"python", "javascript"}:
            rendered = self._strip_markdown_fence(rendered)
        return rendered

    def translate(
        self,
        data: Any,
        target: str = "logic",
        source_name: str = "input.json",
    ) -> TranslationResult:
        logic = self.analyze(data, source_name=source_name)
        rendered = self.render(data, logic, target)
        return TranslationResult(
            source_name=source_name,
            target=target,
            logic=logic,
            rendered_output=rendered,
            warnings=list(logic.assumptions),
            metadata={"model": self.model},
        )

    def translate_file(self, path: str | Path, target: str = "logic") -> TranslationResult:
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return self.translate(data, target=target, source_name=file_path.name)
