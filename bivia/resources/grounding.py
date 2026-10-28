"""Grounding resource -- image and video grounding."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional

from ..types import GroundDecision, VideoGroundDecision

if TYPE_CHECKING:
    from .._http import AsyncHTTPTransport, HTTPTransport


class GroundingResource:
    """Visual grounding -- locate objects in images and video."""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def image(
        self,
        *,
        question: str = "",
        images: Optional[List[Dict[str, Any]]] = None,
        documents: Optional[List[Dict[str, Any]]] = None,
        state: str = "",
        domain: Optional[str] = None,
    ) -> GroundDecision:
        """Locate objects in images via open-vocabulary visual grounding.

        Returns bounding boxes with coordinates normalized to [0, 1000].

        Args:
            question: What to find (e.g. 'the invoice total'). Empty detects broadly.
            images: The image(s) to search (list of dicts with 'url' or 'b64'+'mime').
            documents: Optional documents.
            state: Optional text context.
            domain: Optional domain hint.

        Returns:
            A GroundDecision with detected regions.
        """
        return self._http.post("/ground", {
            "question": question, "images": images, "documents": documents,
            "state": state, "domain": domain,
        }, GroundDecision)

    def video(
        self,
        *,
        video: Dict[str, Any],
        query: str,
        kind: str = "object",
        coarse_step: Optional[float] = None,
        fine_resolution: Optional[float] = None,
        boxes_on_hits: Optional[bool] = None,
        max_probes: Optional[int] = None,
        allow_abstain: Optional[bool] = None,
    ) -> VideoGroundDecision:
        """Locate objects or events in video.

        Args:
            video: Video reference (dict with 'url' or 'b64', optional 'mime', 'max_edge').
            query: What to find in the video.
            kind: 'object' (temporal intervals with boxes) or 'event' (onset timestamps).
            coarse_step: Seconds between coarse scan samples (default 5.0).
            fine_resolution: Seconds between fine scan samples (default 0.5).
            boxes_on_hits: Whether to return per-frame bounding boxes (default True).
            max_probes: Maximum number of frames to probe (default 200).
            allow_abstain: Whether the model may abstain.

        Returns:
            A VideoGroundDecision with detected hits.
        """
        return self._http.post("/ground/video", {
            "video": video, "query": query, "kind": kind,
            "coarse_step": coarse_step, "fine_resolution": fine_resolution,
            "boxes_on_hits": boxes_on_hits, "max_probes": max_probes,
            "allow_abstain": allow_abstain,
        }, VideoGroundDecision)


class AsyncGroundingResource:
    """Async version of GroundingResource."""

    def __init__(self, http: AsyncHTTPTransport) -> None:
        self._http = http

    async def image(self, **kwargs: Any) -> GroundDecision:
        """Open-vocabulary visual grounding."""
        return await self._http.post("/ground", kwargs, GroundDecision)

    async def video(self, **kwargs: Any) -> VideoGroundDecision:
        """Locate objects or events in video."""
        return await self._http.post("/ground/video", kwargs, VideoGroundDecision)
