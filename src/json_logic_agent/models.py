from typing import Any, Literal

from pydantic import BaseModel, Field


OutputTarget = Literal["logic", "python", "javascript", "typescript", "mermaid"]


class LogicStep(BaseModel):
    order: int
    title: str
    explanation: str
    condition: str | None = None
    action: str | None = None


class InspectionReport(BaseModel):
    json_kind: str
    structural_summary: str
    notable_keys: list[str] = Field(default_factory=list)
    candidate_inputs: list[str] = Field(default_factory=list)
    candidate_outputs: list[str] = Field(default_factory=list)
    candidate_entities: list[str] = Field(default_factory=list)
    candidate_conditions: list[str] = Field(default_factory=list)
    candidate_actions: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    ambiguities: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class LogicModel(BaseModel):
    summary: str
    json_kind: str = Field(description="Best classification of the JSON structure")
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    conditions: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    steps: list[LogicStep] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


class CritiqueReport(BaseModel):
    verdict: Literal["accept", "revise"] = "accept"
    semantic_risks: list[str] = Field(default_factory=list)
    unsupported_inferences: list[str] = Field(default_factory=list)
    missing_logic: list[str] = Field(default_factory=list)
    ordering_issues: list[str] = Field(default_factory=list)
    recommended_changes: list[str] = Field(default_factory=list)


class ReviewReport(BaseModel):
    verdict: Literal["pass", "revise"] = "pass"
    fidelity_score: int = Field(default=100, ge=0, le=100)
    issues: list[str] = Field(default_factory=list)
    corrected_output: str | None = None


class PipelineTrace(BaseModel):
    inspection: InspectionReport
    draft_logic: LogicModel
    critique: CritiqueReport
    final_logic: LogicModel
    review: ReviewReport | None = None


class TranslationResult(BaseModel):
    source_name: str
    target: OutputTarget
    logic: LogicModel
    rendered_output: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    trace: PipelineTrace | None = None


class ScannedJsonFile(BaseModel):
    path: str
    size_bytes: int
    top_level_type: str
    top_level_keys: list[str] = Field(default_factory=list)
    likely_kind: str
    note: str


class ProjectScanResult(BaseModel):
    root: str
    files: list[ScannedJsonFile] = Field(default_factory=list)
    skipped_invalid_json: list[str] = Field(default_factory=list)
    skipped_large_files: list[str] = Field(default_factory=list)
