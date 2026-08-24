from typing import Any, Literal

from pydantic import BaseModel, Field


class LogicStep(BaseModel):
    order: int
    title: str
    explanation: str
    condition: str | None = None
    action: str | None = None


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


class TranslationResult(BaseModel):
    source_name: str
    target: Literal["logic", "python", "javascript"]
    logic: LogicModel
    rendered_output: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
