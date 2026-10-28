"""Batch resource -- multiple typed questions in one request."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import BatchResponse

if TYPE_CHECKING:
    from .._http import AsyncHTTPTransport, HTTPTransport


class BatchResource:
    """Send multiple typed questions against the same context in a single request."""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def create(
        self,
        *,
        questions: Dict[str, Any],
        state: str = "",
        images: Optional[List[Dict[str, Any]]] = None,
        audio: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        signals: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> BatchResponse:
        """Send multiple named, independently-typed questions in one request.

        Each question is a dict with 'type' (boolean/choice/score/set/box),
        'instructions' (the question text), and type-specific fields like
        'criteria', 'options', 'levels', or 'buckets'.

        Args:
            questions: Map of question name to typed question definition.
            state: Shared text context for all questions.
            images: Optional shared images.
            audio: Optional shared audio clips.
            documents: Optional shared documents.
            signals: Optional raw numeric signals.
            model: Accepted for compatibility (response model is always dec-1).
            mode: 'fast' (default) or 'deep'.

        Returns:
            A BatchResponse with named answers keyed by question name.
        """
        return self._http.post("/v1/systemone", {
            "questions": questions, "state": state, "images": images, "audio": audio,
            "documents": documents, "signals": signals, "model": model, "mode": mode,
        }, BatchResponse)


class AsyncBatchResource:
    """Async version of BatchResource."""

    def __init__(self, http: AsyncHTTPTransport) -> None:
        self._http = http

    async def create(self, **kwargs: Any) -> BatchResponse:
        """Send multiple named, independently-typed questions in one request."""
        return await self._http.post("/v1/systemone", kwargs, BatchResponse)
