"""Models resource -- model discovery and capability introspection."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import Capabilities, ModelList

if TYPE_CHECKING:
    from .._http import AsyncHTTPTransport, HTTPTransport


class ModelsResource:
    """Model discovery and capability introspection."""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def list(self) -> ModelList:
        """List available models.

        Returns:
            A ModelList containing the models available on this deployment.
        """
        return self._http.get("/v1/models", ModelList)

    def capabilities(self) -> Capabilities:
        """Discover available decision types, modalities, and features.

        Returns:
            A Capabilities document describing the deployment's features.
        """
        return self._http.get("/capabilities", Capabilities)


class AsyncModelsResource:
    """Async version of ModelsResource."""

    def __init__(self, http: AsyncHTTPTransport) -> None:
        self._http = http

    async def list(self) -> ModelList:
        """List available models."""
        return await self._http.get("/v1/models", ModelList)

    async def capabilities(self) -> Capabilities:
        """Discover available decision types, modalities, and features."""
        return await self._http.get("/capabilities", Capabilities)
