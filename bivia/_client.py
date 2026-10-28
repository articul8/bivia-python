"""Bivia client -- the main entry point for the SDK."""

from __future__ import annotations

import os
from typing import Any, Optional

from ._http import AsyncHTTPTransport, HTTPTransport

_DEFAULT_BASE_URL = "https://api.articul8.ai/bivia"
_DEFAULT_TIMEOUT = 60.0
_DEFAULT_MAX_RETRIES = 2


class Bivia:
    """Synchronous client for the Bivia calibrated decision engine.

    Usage::

        from bivia import Bivia

        client = Bivia()  # reads A8_API_KEY from env
        result = client.decisions.boolean(
            question="Is this urgent?",
            state="Customer threatened to cancel.",
        )
        print(result.value, result.probability)

    Args:
        api_key: API key for authentication. Defaults to the ``A8_API_KEY``
            environment variable.
        base_url: Base URL for the API. Defaults to
            ``https://api.articul8.ai/bivia``.
        timeout: Request timeout in seconds. Defaults to 60.
        max_retries: Maximum number of retries on transient errors.
            Defaults to 2. Retries use exponential backoff.
    """

    _http: HTTPTransport

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("A8_API_KEY") or ""
        if not resolved_key:
            raise ValueError(
                "No API key provided. Pass api_key= or set the A8_API_KEY "
                "environment variable."
            )

        self._http = HTTPTransport(
            base_url=base_url or os.environ.get("BIVIA_BASE_URL") or _DEFAULT_BASE_URL,
            api_key=resolved_key,
            timeout=timeout if timeout is not None else _DEFAULT_TIMEOUT,
            max_retries=max_retries if max_retries is not None else _DEFAULT_MAX_RETRIES,
        )

        from .resources.decisions import DecisionsResource
        from .resources.extract import ExtractResource
        from .resources.grounding import GroundingResource
        from .resources.batch import BatchResource
        from .resources.data import DataResource
        from .resources.models import ModelsResource

        self.decisions = DecisionsResource(self._http)
        self.extract = ExtractResource(self._http)
        self.grounding = GroundingResource(self._http)
        self.batch = BatchResource(self._http)
        self.data = DataResource(self._http)
        self.models = ModelsResource(self._http)

    def with_options(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> Bivia:
        """Return a new client with overridden options."""
        return Bivia(
            api_key=api_key or self._http._client.headers.get("authorization", "").removeprefix("Bearer "),
            base_url=base_url or self._http._base_url,
            max_retries=max_retries if max_retries is not None else self._http._max_retries,
            timeout=timeout if timeout is not None else self._http._client.timeout.connect,
        )

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> Bivia:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncBivia:
    """Asynchronous client for the Bivia calibrated decision engine.

    Usage::

        import asyncio
        from bivia import AsyncBivia

        async def main():
            client = AsyncBivia()  # reads A8_API_KEY from env
            result = await client.decisions.boolean(
                question="Is this urgent?",
                state="Customer threatened to cancel.",
            )
            print(result.value, result.probability)

        asyncio.run(main())

    Args:
        api_key: API key for authentication. Defaults to the ``A8_API_KEY``
            environment variable.
        base_url: Base URL for the API. Defaults to
            ``https://api.articul8.ai/bivia``.
        timeout: Request timeout in seconds. Defaults to 60.
        max_retries: Maximum number of retries on transient errors.
            Defaults to 2. Retries use exponential backoff.
    """

    _http: AsyncHTTPTransport

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("A8_API_KEY") or ""
        if not resolved_key:
            raise ValueError(
                "No API key provided. Pass api_key= or set the A8_API_KEY "
                "environment variable."
            )

        self._http = AsyncHTTPTransport(
            base_url=base_url or os.environ.get("BIVIA_BASE_URL") or _DEFAULT_BASE_URL,
            api_key=resolved_key,
            timeout=timeout if timeout is not None else _DEFAULT_TIMEOUT,
            max_retries=max_retries if max_retries is not None else _DEFAULT_MAX_RETRIES,
        )

        from .resources.decisions import AsyncDecisionsResource
        from .resources.extract import AsyncExtractResource
        from .resources.grounding import AsyncGroundingResource
        from .resources.batch import AsyncBatchResource
        from .resources.data import AsyncDataResource
        from .resources.models import AsyncModelsResource

        self.decisions = AsyncDecisionsResource(self._http)
        self.extract = AsyncExtractResource(self._http)
        self.grounding = AsyncGroundingResource(self._http)
        self.batch = AsyncBatchResource(self._http)
        self.data = AsyncDataResource(self._http)
        self.models = AsyncModelsResource(self._http)

    def with_options(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_retries: Optional[int] = None,
        timeout: Optional[float] = None,
    ) -> AsyncBivia:
        """Return a new client with overridden options."""
        return AsyncBivia(
            api_key=api_key or self._http._client.headers.get("authorization", "").removeprefix("Bearer "),
            base_url=base_url or self._http._base_url,
            max_retries=max_retries if max_retries is not None else self._http._max_retries,
            timeout=timeout if timeout is not None else self._http._client.timeout.connect,
        )

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._http.close()

    async def __aenter__(self) -> AsyncBivia:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
