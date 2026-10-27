"""Data science resource -- decisions over raw numeric signals."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence

from ..types import CategoricalDecision

if TYPE_CHECKING:
    from .._http import AsyncHTTPTransport, HTTPTransport


class DataResource:
    """Decisions over raw numeric signals."""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def decide(
        self,
        *,
        question: str,
        signals: Optional[List[Dict[str, Any]]] = None,
        state: str = "",
        images: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Sequence[Any]] = None,
        kind: Optional[str] = None,
        domain: Optional[str] = None,
        mode: Optional[str] = None,
        think: Optional[bool] = None,
        allow_abstain: Optional[bool] = None,
    ) -> CategoricalDecision:
        """Make a decision based on raw numeric signals.

        The server profiles the signal data (statistics, distribution, anomalies)
        and folds the analysis into context before deciding.

        Args:
            question: The question to decide.
            signals: Raw numeric signals (list of dicts with 'name', 'data', 'fs', etc.).
            state: Optional text context.
            images: Optional images.
            documents: Optional documents.
            options: Candidate answers. Required for useful choice/set results.
            kind: Decision type -- 'set' (default), 'choice', or 'boolean'.
            domain: Optional domain hint.
            mode: 'fast' (default) or 'deep'.
            think: Whether to allow a reasoning trace.
            allow_abstain: Whether the model may abstain.

        Returns:
            A CategoricalDecision with the result.
        """
        body: Dict[str, Any] = {
            "question": question, "signals": signals, "state": state,
            "images": images, "documents": documents,
            "options": list(options) if options is not None else None,
            "kind": kind, "domain": domain, "mode": mode, "think": think,
            "allow_abstain": allow_abstain,
        }
        return self._http.post("/ds", body, CategoricalDecision)


class AsyncDataResource:
    """Async version of DataResource."""

    def __init__(self, http: AsyncHTTPTransport) -> None:
        self._http = http

    async def decide(self, **kwargs: Any) -> CategoricalDecision:
        """Make a decision based on raw numeric signals."""
        if "options" in kwargs and kwargs["options"] is not None:
            kwargs["options"] = list(kwargs["options"])
        return await self._http.post("/ds", kwargs, CategoricalDecision)
