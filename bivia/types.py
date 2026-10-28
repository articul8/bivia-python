from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


class EvidenceSpan(BaseModel):
    start: int
    end: int
    text: str


class Evidence(BaseModel):
    spans: list[EvidenceSpan] = []


class Verification(BaseModel):
    performed: bool
    result: str


class DocumentNote(BaseModel):
    document: str
    status: str
    chars: Optional[int] = None
    tokens: Optional[int] = None
    truncated: Optional[bool] = None
    reason: Optional[str] = None


class _DecisionBase(BaseModel):
    """Shared envelope fields for all decision types."""
    status: str
    abstain_reason: Optional[str] = None
    mode: str
    think_allowed: Optional[bool] = None
    thought: bool = False
    verification: Verification
    evidence: Evidence
    latency_ms: float
    model: str
    input_tokens: Optional[int] = None
    image_tokens: Optional[int] = None
    document_tokens: Optional[int] = None
    billable_tokens: Optional[int] = None
    document_notes: Optional[list[DocumentNote]] = None


class CategoricalDecision(_DecisionBase):
    """Generic categorical decision (decide/choice/boolean)."""
    type: str
    value: Any = None
    probability: Optional[float] = None
    distribution: Optional[dict[str, float]] = None


class BooleanDecision(_DecisionBase):
    """Yes/no decision."""
    type: str = "boolean"
    value: Optional[str] = None
    probability: Optional[float] = None
    distribution: Optional[dict[str, float]] = None


class ChoiceDecision(_DecisionBase):
    """Pick-one decision."""
    type: str = "choice"
    value: Optional[str] = None
    probability: Optional[float] = None
    distribution: Optional[dict[str, float]] = None


class DecideDecision(_DecisionBase):
    """Auto-detected decision type."""
    type: str = "decide"
    value: Any = None
    probability: Optional[float] = None
    distribution: Optional[dict[str, float]] = None


class ScoreDecision(_DecisionBase):
    type: str
    value: Optional[float] = None
    levels: Optional[dict[str, float]] = None


class SetDecision(_DecisionBase):
    type: str
    value: list[Any] = []
    probabilities: Optional[dict[str, float]] = None


class SpanDecision(_DecisionBase):
    type: str
    value: list[EvidenceSpan] = []


class ExtractValue(BaseModel):
    """A single extracted field value."""
    value: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    confidence: Optional[float] = None
    found: bool = False


class ExtractDecision(BaseModel):
    """Response for /extract — exact field values copied from document text."""
    type: str = "extract"
    field: Optional[str] = None
    value: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    confidence: Optional[float] = None
    found: Optional[bool] = None
    grounded: bool = True
    values: Optional[dict[str, ExtractValue]] = None


class GroundRegion(BaseModel):
    label: str
    box: list[float]
    score: Optional[float] = None


def _empty_verification() -> Verification:
    """Picture-finding replies omit the decision envelope. Keep the same fields."""
    return Verification(performed=False, result="")


class GroundDecision(BaseModel):
    type: str
    value: list[GroundRegion] = []
    status: str = ""
    abstain_reason: Optional[str] = None
    mode: str = ""
    thought: bool = False
    grounded: Optional[bool] = None
    verification: Verification = Field(default_factory=_empty_verification)
    evidence: Evidence = Field(default_factory=Evidence)
    latency_ms: float = 0
    model: str = ""
    input_tokens: Optional[int] = None
    image_tokens: Optional[int] = None
    billable_tokens: Optional[int] = None


class VideoGroundHit(BaseModel):
    start: Optional[float] = None
    end: Optional[float] = None
    peak_t: Optional[float] = None
    onset_t: Optional[float] = None
    confidence: float
    boxes: list[GroundRegion] = []

    @field_validator("boxes", mode="before")
    @classmethod
    def empty_boxes(cls, value: object) -> object:
        # The service sends null when a hit has no boxes. Callers still get a list.
        if value is None:
            return []
        return value


class VideoGroundDecision(BaseModel):
    type: str
    kind: str
    duration_s: float
    scanned: Optional[int] = None
    truncated: Optional[bool] = None
    hits: list[VideoGroundHit] = []
    input_tokens: Optional[int] = None
    image_tokens: Optional[int] = None
    billable_tokens: Optional[int] = None


class BatchChoiceAnswer(BaseModel):
    """A choice answer within a batch response."""
    type: str
    choice: Any = None
    confidence: Optional[float] = None
    probabilities: Optional[dict[str, float]] = None
    abstained: bool = False


class BatchBooleanAnswer(BaseModel):
    """A boolean answer within a batch response."""
    type: str
    noul: Optional[float] = None
    probability: Optional[float] = None
    confidence: Optional[float] = None
    abstained: bool = False


class BatchScoreAnswer(BaseModel):
    """A score answer within a batch response."""
    type: str
    score: Optional[float] = None
    confidence: Optional[float] = None
    legend: Optional[dict[str, str]] = None
    probabilities: Optional[dict[str, float]] = None
    distribution: Optional[dict[str, float]] = None
    abstained: bool = False


class BatchSetAnswer(BaseModel):
    """A set (multi-select) answer within a batch response."""
    type: str
    selected: Optional[list[Any]] = None
    probabilities: Optional[dict[str, float]] = None
    abstained: bool = False


class BatchBoxAnswer(BaseModel):
    """A bounding-box answer within a batch response."""
    type: str
    box: Optional[dict[str, float]] = None
    label: Optional[str] = None
    confidence: Optional[float] = None
    abstained: bool = False


class BatchUsage(BaseModel):
    """Token usage for a batch request."""
    questions: int
    input_tokens: int = 0
    output_tokens: Optional[int] = None
    billable_tokens: int = 0


class BatchResponse(BaseModel):
    """Response for the batch (systemone) endpoint."""
    model: str
    answers: dict[str, Any]
    usage: BatchUsage


class ModelInfo(BaseModel):
    name: str
    description: Optional[str] = None
    release_date: Optional[str] = None


class ModelList(BaseModel):
    models: list[ModelInfo]


class Capabilities(BaseModel):
    model: Optional[str] = None
    decision_types: list[str] = []
    modalities: Optional[dict[str, Any]] = None
    evidence: Optional[dict[str, Any]] = None
    abstention: Optional[bool] = None
