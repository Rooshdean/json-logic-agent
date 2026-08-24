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


class N8nNodeSummary(BaseModel):
    name: str
    node_type: str
    category: str
    disabled: bool = False
    credential_types: list[str] = Field(default_factory=list)
    expression_count: int = 0
    has_error_policy: bool = False


class N8nConnectionSummary(BaseModel):
    source: str
    target: str
    output_index: int = 0
    connection_type: str = "main"


class N8nRiskFinding(BaseModel):
    severity: Literal["low", "medium", "high"]
    node: str | None = None
    finding: str


class N8nWorkflowReport(BaseModel):
    is_n8n: bool = True
    workflow_name: str | None = None
    active: bool | None = None
    node_count: int = 0
    connection_count: int = 0
    trigger_nodes: list[str] = Field(default_factory=list)
    decision_nodes: list[str] = Field(default_factory=list)
    code_nodes: list[str] = Field(default_factory=list)
    ai_nodes: list[str] = Field(default_factory=list)
    integrations: list[str] = Field(default_factory=list)
    credential_types: list[str] = Field(default_factory=list)
    nodes: list[N8nNodeSummary] = Field(default_factory=list)
    connections: list[N8nConnectionSummary] = Field(default_factory=list)
    disconnected_nodes: list[str] = Field(default_factory=list)
    terminal_nodes: list[str] = Field(default_factory=list)
    risks: list[N8nRiskFinding] = Field(default_factory=list)


class TranslationResult(BaseModel):
    source_name: str
    target: OutputTarget
    logic: LogicModel
    rendered_output: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    trace: PipelineTrace | None = None
    n8n_report: N8nWorkflowReport | None = None


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
