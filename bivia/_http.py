"""HTTP transport layer with retries and backoff."""

from __future__ import annotations

import time
import logging
from typing import Any, Dict, Optional, Type, TypeVar

import httpx

from ._errors import (
    APIConnectionError,
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

logger = logging.getLogger("bivia")

T = TypeVar("T")

_STATUS_ERROR_MAP: Dict[int, Type[APIStatusError]] = {
    400: BadRequestError,
    401: AuthenticationError,
    403: PermissionDeniedError,
    404: NotFoundError,
    422: UnprocessableEntityError,
    429: RateLimitError,
}

_RETRYABLE_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}


def _should_retry(status_code: int) -> bool:
    return status_code in _RETRYABLE_STATUS_CODES or status_code >= 500


def _backoff_delay(attempt: int) -> float:
    """Exponential backoff: 0.5s, 1s, 2s, ... capped at 8s."""
    return min(0.5 * (2 ** attempt), 8.0)


def _raise_for_status(response: httpx.Response) -> None:
    if response.status_code < 400:
        return
    try:
        body = response.json()
    except Exception:
        body = response.text
    message = str(body) if isinstance(body, (dict, list)) else (body or f"HTTP {response.status_code}")
    error_cls = _STATUS_ERROR_MAP.get(response.status_code)
    if error_cls is not None:
        raise error_cls(message=str(message), body=body, response=response)
    if response.status_code >= 500:
        raise InternalServerError(
            message=str(message),
            status_code=response.status_code,
            body=body,
            response=response,
        )
    raise APIStatusError(
        message=str(message),
        status_code=response.status_code,
        body=body,
        response=response,
    )


class HTTPTransport:
    """Synchronous HTTP transport with retries and exponential backoff."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 60.0,
        max_retries: int = 2,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = httpx.Client(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=timeout,
        )

    def _request(self, method: str, path: str, *, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        url = f"{self._base_url}{path}"
        last_exc: Optional[Exception] = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(method, url, json=json)

                if _should_retry(response.status_code) and attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.debug(
                        "Retrying %s %s (status %d) in %.1fs",
                        method, path, response.status_code, delay,
                    )
                    time.sleep(delay)
                    continue

                return response

            except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.debug("Connection error on %s %s, retrying in %.1fs", method, path, delay)
                    time.sleep(delay)
                    continue
                raise APIConnectionError(message=f"Connection error: {exc}", cause=exc) from exc

            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.debug("Timeout on %s %s, retrying in %.1fs", method, path, delay)
                    time.sleep(delay)
                    continue
                raise APITimeoutError() from exc

        raise APIConnectionError(message="Max retries exceeded.", cause=last_exc)  # type: ignore[arg-type]

    def post(self, path: str, body: Dict[str, Any], model: Type[T]) -> T:
        """POST JSON and return a parsed Pydantic model."""
        cleaned = {k: v for k, v in body.items() if v is not None}
        response = self._request("POST", path, json=cleaned)
        _raise_for_status(response)
        return model.model_validate(response.json())  # type: ignore[attr-defined]

    def get(self, path: str, model: Type[T]) -> T:
        """GET and return a parsed Pydantic model."""
        response = self._request("GET", path)
        _raise_for_status(response)
        return model.model_validate(response.json())  # type: ignore[attr-defined]

    def close(self) -> None:
        self._client.close()


class AsyncHTTPTransport:
    """Asynchronous HTTP transport with retries and exponential backoff."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float = 60.0,
        max_retries: int = 2,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=timeout,
        )

    async def _request(self, method: str, path: str, *, json: Optional[Dict[str, Any]] = None) -> httpx.Response:
        import asyncio

        url = f"{self._base_url}{path}"
        last_exc: Optional[Exception] = None

        for attempt in range(self._max_retries + 1):
            try:
                response = await self._client.request(method, url, json=json)

                if _should_retry(response.status_code) and attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.debug(
                        "Retrying %s %s (status %d) in %.1fs",
                        method, path, response.status_code, delay,
                    )
                    await asyncio.sleep(delay)
                    continue

                return response

            except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.debug("Connection error on %s %s, retrying in %.1fs", method, path, delay)
                    await asyncio.sleep(delay)
                    continue
                raise APIConnectionError(message=f"Connection error: {exc}", cause=exc) from exc

            except httpx.TimeoutException as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    delay = _backoff_delay(attempt)
                    logger.debug("Timeout on %s %s, retrying in %.1fs", method, path, delay)
                    await asyncio.sleep(delay)
                    continue
                raise APITimeoutError() from exc

        raise APIConnectionError(message="Max retries exceeded.", cause=last_exc)  # type: ignore[arg-type]

    async def post(self, path: str, body: Dict[str, Any], model: Type[T]) -> T:
        """POST JSON and return a parsed Pydantic model."""
        cleaned = {k: v for k, v in body.items() if v is not None}
        response = await self._request("POST", path, json=cleaned)
        _raise_for_status(response)
        return model.model_validate(response.json())  # type: ignore[attr-defined]

    async def get(self, path: str, model: Type[T]) -> T:
        """GET and return a parsed Pydantic model."""
        response = await self._request("GET", path)
        _raise_for_status(response)
        return model.model_validate(response.json())  # type: ignore[attr-defined]

    async def close(self) -> None:
        await self._client.aclose()
