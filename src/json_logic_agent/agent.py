import json
import os
from pathlib import Path
from typing import Any, TypeVar

from openai import OpenAI
from pydantic import BaseModel

from .models import CritiqueReport, InspectionReport, LogicModel, OutputTarget, PipelineTrace, ReviewReport, TranslationResult
from .n8n import analyze_n8n_workflow, is_n8n_workflow, n8n_context_for_prompt
from .prompts import SYSTEM_PROMPT, build_architect_prompt, build_critic_prompt, build_inspector_prompt, build_render_prompt, build_reviewer_prompt, build_revision_prompt

ModelT = TypeVar("ModelT", bound=BaseModel)
SUPPORTED_TARGETS = {"logic", "python", "javascript", "typescript", "mermaid"}
CODE_TARGETS = {"python", "javascript", "typescript"}
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "anthropic/claude-sonnet-4"


class JsonLogicAgent:
    """V5 JSON + n8n workflow reverse-engineering agent using OpenRouter."""

    def __init__(self, model: str | None = None, client: OpenAI | None = None):
        self.model = model or os.getenv("JSON_LOGIC_MODEL", DEFAULT_MODEL)
        if client is not None:
            self.client = client
        else:
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "OPENROUTER_API_KEY is required for semantic analysis. "
                    "Local commands such as `jsonlogic n8n workflow.json --report-only` do not require a key."
                )
            self.client = OpenAI(
                base_url=OPENROUTER_BASE_URL,
                api_key=api_key,
                default_headers={
                    "X-Title": "JSON Logic Agent",
                },
            )

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

    @staticmethod
    def _n8n_context(data: Any):
        if is_n8n_workflow(data):
            report = analyze_n8n_workflow(data)
            return report, n8n_context_for_prompt(report)
        return None, None

    def _call_text(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("OpenRouter returned an empty response")
        return content.strip()

    def _call_model(self, prompt: str, model_type: type[ModelT]) -> ModelT:
        raw = self._strip_markdown_fence(self._call_text(prompt))
        return model_type.model_validate_json(raw)

    def inspect(self, data: Any, source_name: str = "input.json", n8n_context: str | None = None) -> InspectionReport:
        return self._call_model(build_inspector_prompt(source_name, self._normalize_json(data), n8n_context), InspectionReport)

    def architect(self, data: Any, inspection: InspectionReport, source_name: str = "input.json", n8n_context: str | None = None) -> LogicModel:
        return self._call_model(build_architect_prompt(source_name, self._normalize_json(data), inspection.model_dump_json(indent=2), n8n_context), LogicModel)

    def critique(self, data: Any, inspection: InspectionReport, logic: LogicModel, n8n_context: str | None = None) -> CritiqueReport:
        return self._call_model(build_critic_prompt(self._normalize_json(data), inspection.model_dump_json(indent=2), logic.model_dump_json(indent=2), n8n_context), CritiqueReport)

    def revise(self, data: Any, logic: LogicModel, critique: CritiqueReport, n8n_context: str | None = None) -> LogicModel:
        if critique.verdict == "accept":
            return logic
        return self._call_model(build_revision_prompt(self._normalize_json(data), logic.model_dump_json(indent=2), critique.model_dump_json(indent=2), n8n_context), LogicModel)

    def analyze(self, data: Any, source_name: str = "input.json") -> LogicModel:
        _, context = self._n8n_context(data)
        inspection = self.inspect(data, source_name, context)
        draft = self.architect(data, inspection, source_name, context)
        critique = self.critique(data, inspection, draft, context)
        return self.revise(data, draft, critique, context)

    def render(self, data: Any, logic: LogicModel, target: OutputTarget, n8n_context: str | None = None) -> str:
        if target not in SUPPORTED_TARGETS:
            raise ValueError(f"target must be one of: {', '.join(sorted(SUPPORTED_TARGETS))}")
        rendered = self._call_text(build_render_prompt(target, logic.model_dump_json(indent=2), self._normalize_json(data), n8n_context))
        if target in CODE_TARGETS or target == "mermaid":
            rendered = self._strip_markdown_fence(rendered)
        return rendered

    def review(self, data: Any, logic: LogicModel, target: OutputTarget, rendered_output: str, n8n_context: str | None = None) -> ReviewReport:
        return self._call_model(build_reviewer_prompt(target, self._normalize_json(data), logic.model_dump_json(indent=2), rendered_output, n8n_context), ReviewReport)

    def translate(self, data: Any, target: OutputTarget = "logic", source_name: str = "input.json", include_trace: bool = True) -> TranslationResult:
        n8n_report, context = self._n8n_context(data)
        inspection = self.inspect(data, source_name, context)
        draft_logic = self.architect(data, inspection, source_name, context)
        critique = self.critique(data, inspection, draft_logic, context)
        final_logic = self.revise(data, draft_logic, critique, context)
        rendered = self.render(data, final_logic, target, context)
        review = self.review(data, final_logic, target, rendered, context)

        if review.verdict == "revise" and review.corrected_output:
            rendered = review.corrected_output.strip()
            if target in CODE_TARGETS or target == "mermaid":
                rendered = self._strip_markdown_fence(rendered)

        warnings = list(dict.fromkeys(list(final_logic.assumptions) + inspection.ambiguities + critique.semantic_risks + review.issues))
        trace = PipelineTrace(inspection=inspection, draft_logic=draft_logic, critique=critique, final_logic=final_logic, review=review) if include_trace else None

        return TranslationResult(
            source_name=source_name,
            target=target,
            logic=final_logic,
            rendered_output=rendered,
            warnings=warnings,
            metadata={
                "provider": "openrouter",
                "model": self.model,
                "pipeline": "v5",
                "stages": ["format-detection", "n8n-analysis" if n8n_report else "generic-json", "inspector", "architect", "critic", "generator", "reviewer"],
                "fidelity_score": review.fidelity_score,
                "source_format": "n8n-workflow" if n8n_report else "generic-json",
            },
            trace=trace,
            n8n_report=n8n_report,
        )

    def translate_file(self, path: str | Path, target: OutputTarget = "logic", include_trace: bool = True) -> TranslationResult:
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return self.translate(data, target=target, source_name=file_path.name, include_trace=include_trace)
