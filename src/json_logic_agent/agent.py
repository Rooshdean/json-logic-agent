import json
import os
from pathlib import Path
from typing import Any, TypeVar

from openai import OpenAI
from pydantic import BaseModel

from .models import (
    CritiqueReport,
    InspectionReport,
    LogicModel,
    OutputTarget,
    PipelineTrace,
    ReviewReport,
    TranslationResult,
)
from .prompts import (
    SYSTEM_PROMPT,
    build_architect_prompt,
    build_critic_prompt,
    build_inspector_prompt,
    build_render_prompt,
    build_reviewer_prompt,
    build_revision_prompt,
)

ModelT = TypeVar("ModelT", bound=BaseModel)
SUPPORTED_TARGETS = {"logic", "python", "javascript", "typescript", "mermaid"}
CODE_TARGETS = {"python", "javascript", "typescript"}


class JsonLogicAgent:
    """V3 developer-focused JSON reverse-engineering agent.

    Fidelity pipeline:
        Inspector -> Logic Architect -> Ambiguity Critic -> Generator -> Reviewer
    """

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

    def _call_text(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=prompt,
        )
        return response.output_text.strip()

    def _call_model(self, prompt: str, model_type: type[ModelT]) -> ModelT:
        raw = self._strip_markdown_fence(self._call_text(prompt))
        return model_type.model_validate_json(raw)

    def inspect(self, data: Any, source_name: str = "input.json") -> InspectionReport:
        return self._call_model(
            build_inspector_prompt(source_name, self._normalize_json(data)), InspectionReport
        )

    def architect(self, data: Any, inspection: InspectionReport, source_name: str = "input.json") -> LogicModel:
        return self._call_model(
            build_architect_prompt(
                source_name,
                self._normalize_json(data),
                inspection.model_dump_json(indent=2),
            ),
            LogicModel,
        )

    def critique(self, data: Any, inspection: InspectionReport, logic: LogicModel) -> CritiqueReport:
        return self._call_model(
            build_critic_prompt(
                self._normalize_json(data),
                inspection.model_dump_json(indent=2),
                logic.model_dump_json(indent=2),
            ),
            CritiqueReport,
        )

    def revise(self, data: Any, logic: LogicModel, critique: CritiqueReport) -> LogicModel:
        if critique.verdict == "accept":
            return logic
        return self._call_model(
            build_revision_prompt(
                self._normalize_json(data),
                logic.model_dump_json(indent=2),
                critique.model_dump_json(indent=2),
            ),
            LogicModel,
        )

    def analyze(self, data: Any, source_name: str = "input.json") -> LogicModel:
        inspection = self.inspect(data, source_name=source_name)
        draft = self.architect(data, inspection, source_name=source_name)
        critique = self.critique(data, inspection, draft)
        return self.revise(data, draft, critique)

    def render(self, data: Any, logic: LogicModel, target: OutputTarget) -> str:
        if target not in SUPPORTED_TARGETS:
            raise ValueError(f"target must be one of: {', '.join(sorted(SUPPORTED_TARGETS))}")
        rendered = self._call_text(
            build_render_prompt(target, logic.model_dump_json(indent=2), self._normalize_json(data))
        )
        if target in CODE_TARGETS or target == "mermaid":
            rendered = self._strip_markdown_fence(rendered)
        return rendered

    def review(self, data: Any, logic: LogicModel, target: OutputTarget, rendered_output: str) -> ReviewReport:
        return self._call_model(
            build_reviewer_prompt(
                target,
                self._normalize_json(data),
                logic.model_dump_json(indent=2),
                rendered_output,
            ),
            ReviewReport,
        )

    def translate(
        self,
        data: Any,
        target: OutputTarget = "logic",
        source_name: str = "input.json",
        include_trace: bool = True,
    ) -> TranslationResult:
        inspection = self.inspect(data, source_name=source_name)
        draft_logic = self.architect(data, inspection, source_name=source_name)
        critique = self.critique(data, inspection, draft_logic)
        final_logic = self.revise(data, draft_logic, critique)
        rendered = self.render(data, final_logic, target)
        review = self.review(data, final_logic, target, rendered)

        if review.verdict == "revise" and review.corrected_output:
            rendered = review.corrected_output.strip()
            if target in CODE_TARGETS or target == "mermaid":
                rendered = self._strip_markdown_fence(rendered)

        warnings = list(dict.fromkeys(
            list(final_logic.assumptions)
            + inspection.ambiguities
            + critique.semantic_risks
            + review.issues
        ))

        trace = PipelineTrace(
            inspection=inspection,
            draft_logic=draft_logic,
            critique=critique,
            final_logic=final_logic,
            review=review,
        ) if include_trace else None

        return TranslationResult(
            source_name=source_name,
            target=target,
            logic=final_logic,
            rendered_output=rendered,
            warnings=warnings,
            metadata={
                "model": self.model,
                "pipeline": "v3",
                "stages": ["inspector", "architect", "critic", "generator", "reviewer"],
                "fidelity_score": review.fidelity_score,
            },
            trace=trace,
        )

    def translate_file(
        self,
        path: str | Path,
        target: OutputTarget = "logic",
        include_trace: bool = True,
    ) -> TranslationResult:
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return self.translate(data, target=target, source_name=file_path.name, include_trace=include_trace)
