"""Decisions resource -- boolean, choice, decide, score, set, span."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence

from ..types import CategoricalDecision, ScoreDecision, SetDecision, SpanDecision

if TYPE_CHECKING:
    from .._http import AsyncHTTPTransport, HTTPTransport


class DecisionsResource:
    """Access to the six decision endpoints: boolean, choice, create (decide), score, multi_select (set), span."""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def boolean(
        self,
        *,
        question: str,
        state: str = "",
        images: Optional[List[Dict[str, Any]]] = None,
        audio: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        domain: Optional[str] = None,
        mode: Optional[str] = None,
        think: Optional[bool] = None,
        allow_abstain: Optional[bool] = None,
    ) -> CategoricalDecision:
        """Yes/no decision with calibrated probability.

        Args:
            question: The question to decide.
            state: Text context for the decision.
            images: Optional images (list of dicts with 'url' or 'b64'+'mime').
            audio: Optional audio clips (list of dicts with 'url' or 'b64'+'mime').
            documents: Optional documents (list of dicts with 'url' or 'b64').
            domain: Optional domain hint (e.g. 'finance').
            mode: 'fast' (default) or 'deep'.
            think: Whether to allow a reasoning trace before deciding.
            allow_abstain: Whether the model may abstain if not confident.

        Returns:
            A CategoricalDecision with type='boolean'.
        """
        return self._http.post("/boolean", {
            "question": question, "state": state, "images": images, "audio": audio,
            "documents": documents, "domain": domain, "mode": mode, "think": think,
            "allow_abstain": allow_abstain,
        }, CategoricalDecision)

    def choice(
        self,
        *,
        question: str,
        choices: Sequence[Any],
        state: str = "",
        images: Optional[List[Dict[str, Any]]] = None,
        audio: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        domain: Optional[str] = None,
        mode: Optional[str] = None,
        think: Optional[bool] = None,
        allow_abstain: Optional[bool] = None,
    ) -> CategoricalDecision:
        """Pick one from a list of choices.

        Args:
            question: The question to decide.
            choices: The options to choose from (2-26 items).
            state: Text context for the decision.
            images: Optional images.
            audio: Optional audio clips.
            documents: Optional documents.
            domain: Optional domain hint.
            mode: 'fast' (default) or 'deep'.
            think: Whether to allow a reasoning trace.
            allow_abstain: Whether the model may abstain.

        Returns:
            A CategoricalDecision with type='choice'.
        """
        return self._http.post("/choice", {
            "question": question, "choices": list(choices), "state": state,
            "images": images, "audio": audio, "documents": documents,
            "domain": domain, "mode": mode, "think": think,
            "allow_abstain": allow_abstain,
        }, CategoricalDecision)

    def create(
        self,
        *,
        question: str,
        state: str = "",
        outcomes: Optional[Sequence[Any]] = None,
        images: Optional[List[Dict[str, Any]]] = None,
        audio: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        domain: Optional[str] = None,
        mode: Optional[str] = None,
        think: Optional[bool] = None,
        allow_abstain: Optional[bool] = None,
    ) -> CategoricalDecision:
        """Auto-detect the best decision type from the question.

        Args:
            question: The question to decide.
            state: Text context for the decision.
            outcomes: Candidate outcomes (2-26 items). When omitted, the model
                infers options from the question text.
            images: Optional images.
            audio: Optional audio clips.
            documents: Optional documents.
            domain: Optional domain hint.
            mode: 'fast' (default) or 'deep'.
            think: Whether to allow a reasoning trace.
            allow_abstain: Whether the model may abstain.

        Returns:
            A CategoricalDecision with the auto-detected type.
        """
        body: Dict[str, Any] = {
            "question": question, "state": state, "images": images, "audio": audio,
            "documents": documents, "domain": domain, "mode": mode, "think": think,
            "allow_abstain": allow_abstain,
        }
        if outcomes is not None:
            body["outcomes"] = list(outcomes)
        return self._http.post("/decide", body, CategoricalDecision)

    def score(
        self,
        *,
        question: str,
        state: str = "",
        range: Optional[List[float]] = None,
        buckets: Optional[int] = None,
        images: Optional[List[Dict[str, Any]]] = None,
        audio: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        domain: Optional[str] = None,
        mode: Optional[str] = None,
        think: Optional[bool] = None,
        allow_abstain: Optional[bool] = None,
    ) -> ScoreDecision:
        """Numeric score on a scale.

        Args:
            question: The question to decide.
            state: Text context for the decision.
            range: Inclusive [low, high] of the numeric scale (default [0, 1]).
            buckets: Number of evenly spaced levels (default 11, minimum 2).
            images: Optional images.
            audio: Optional audio clips.
            documents: Optional documents.
            domain: Optional domain hint.
            mode: 'fast' (default) or 'deep'.
            think: Whether to allow a reasoning trace.
            allow_abstain: Whether the model may abstain.

        Returns:
            A ScoreDecision with the expected value and per-level probabilities.
        """
        return self._http.post("/score", {
            "question": question, "state": state, "range": range, "buckets": buckets,
            "images": images, "audio": audio, "documents": documents,
            "domain": domain, "mode": mode, "think": think,
            "allow_abstain": allow_abstain,
        }, ScoreDecision)

    def multi_select(
        self,
        *,
        question: str,
        options: Sequence[Any],
        state: str = "",
        images: Optional[List[Dict[str, Any]]] = None,
        audio: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        domain: Optional[str] = None,
        mode: Optional[str] = None,
        think: Optional[bool] = None,
        allow_abstain: Optional[bool] = None,
    ) -> SetDecision:
        """Multi-select from a list (zero or more may be selected).

        Args:
            question: The question to decide.
            options: The options to select from.
            state: Text context for the decision.
            images: Optional images.
            audio: Optional audio clips.
            documents: Optional documents.
            domain: Optional domain hint.
            mode: 'fast' (default) or 'deep'.
            think: Whether to allow a reasoning trace.
            allow_abstain: Whether the model may abstain.

        Returns:
            A SetDecision with selected options and per-option probabilities.
        """
        return self._http.post("/set", {
            "question": question, "options": list(options), "state": state,
            "images": images, "audio": audio, "documents": documents,
            "domain": domain, "mode": mode, "think": think,
            "allow_abstain": allow_abstain,
        }, SetDecision)

    def span(
        self,
        *,
        question: str,
        state: str = "",
        images: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        domain: Optional[str] = None,
    ) -> SpanDecision:
        """Locate text spans in the input.

        Note: /span always runs in fast mode. Sending mode='deep' or think=True
        is rejected (422).

        Args:
            question: What to locate in the text.
            state: The text to search for spans in.
            images: Optional images.
            documents: Optional documents.
            domain: Optional domain hint.

        Returns:
            A SpanDecision with character offset ranges into the state text.
        """
        return self._http.post("/span", {
            "question": question, "state": state, "images": images,
            "documents": documents, "domain": domain,
        }, SpanDecision)


class AsyncDecisionsResource:
    """Async version of DecisionsResource."""

    def __init__(self, http: AsyncHTTPTransport) -> None:
        self._http = http

    async def boolean(self, **kwargs: Any) -> CategoricalDecision:
        """Yes/no decision with calibrated probability."""
        return await self._http.post("/boolean", kwargs, CategoricalDecision)

    async def choice(self, **kwargs: Any) -> CategoricalDecision:
        """Pick one from a list of choices."""
        if "choices" in kwargs and not isinstance(kwargs["choices"], list):
            kwargs["choices"] = list(kwargs["choices"])
        return await self._http.post("/choice", kwargs, CategoricalDecision)

    async def create(self, **kwargs: Any) -> CategoricalDecision:
        """Auto-detect decision type from the question."""
        if "outcomes" in kwargs and kwargs["outcomes"] is not None:
            kwargs["outcomes"] = list(kwargs["outcomes"])
        return await self._http.post("/decide", kwargs, CategoricalDecision)

    async def score(self, **kwargs: Any) -> ScoreDecision:
        """Numeric score on a scale."""
        return await self._http.post("/score", kwargs, ScoreDecision)

    async def multi_select(self, **kwargs: Any) -> SetDecision:
        """Multi-select from a list."""
        if "options" in kwargs and not isinstance(kwargs["options"], list):
            kwargs["options"] = list(kwargs["options"])
        return await self._http.post("/set", kwargs, SetDecision)

    async def span(self, **kwargs: Any) -> SpanDecision:
        """Locate text spans in the input."""
        return await self._http.post("/span", kwargs, SpanDecision)
