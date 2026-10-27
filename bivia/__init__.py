"""Bivia Python SDK -- calibrated decisions with confidence."""

from ._client import AsyncBivia, Bivia
from ._errors import (
    APIConnectionError,
    APIError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitError,
    UnprocessableEntityError,
)
from .types import (
    BatchBoxAnswer,
    BatchBooleanAnswer,
    BatchChoiceAnswer,
    BatchResponse,
    BatchScoreAnswer,
    BatchSetAnswer,
    BatchUsage,
    Capabilities,
    CategoricalDecision,
    DocumentNote,
    Evidence,
    EvidenceSpan,
    GroundDecision,
    GroundRegion,
    ModelInfo,
    ModelList,
    ScoreDecision,
    SetDecision,
    SpanDecision,
    Verification,
    VideoGroundDecision,
    VideoGroundHit,
)

__version__ = "1.0.0"

__all__ = [
    # Clients
    "Bivia",
    "AsyncBivia",
    # Errors
    "APIError",
    "APIStatusError",
    "APIConnectionError",
    "APITimeoutError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
    # Response types
    "CategoricalDecision",
    "ScoreDecision",
    "SetDecision",
    "SpanDecision",
    "GroundDecision",
    "GroundRegion",
    "VideoGroundDecision",
    "VideoGroundHit",
    "BatchResponse",
    "BatchChoiceAnswer",
    "BatchBooleanAnswer",
    "BatchScoreAnswer",
    "BatchSetAnswer",
    "BatchBoxAnswer",
    "BatchUsage",
    "ModelList",
    "ModelInfo",
    "Capabilities",
    # Supporting types
    "Evidence",
    "EvidenceSpan",
    "Verification",
    "DocumentNote",
]
