"""Error types for the Bivia SDK."""

from __future__ import annotations

from typing import Any, Optional


class APIError(Exception):
    """Base class for all Bivia API errors."""

    message: str
    status_code: Optional[int]
    body: Any

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(message={self.message!r}, status_code={self.status_code!r})"
        )


class APIStatusError(APIError):
    """Raised when the API returns a non-success status code (4xx or 5xx)."""

    response: Any

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        body: Any = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=status_code, body=body)
        self.response = response


class APIConnectionError(APIError):
    """Raised when the SDK cannot reach the API server."""

    def __init__(
        self,
        *,
        message: str = "Connection error.",
        cause: Optional[Exception] = None,
    ) -> None:
        super().__init__(message, status_code=None, body=None)
        self.__cause__ = cause


class APITimeoutError(APIConnectionError):
    """Raised when a request times out."""

    def __init__(self) -> None:
        super().__init__(message="Request timed out.")


class BadRequestError(APIStatusError):
    """400 Bad Request."""

    def __init__(
        self, message: str = "Bad request.", *, body: Any = None, response: Any = None
    ) -> None:
        super().__init__(message, status_code=400, body=body, response=response)


class AuthenticationError(APIStatusError):
    """401 Unauthorized."""

    def __init__(
        self,
        message: str = "Authentication failed.",
        *,
        body: Any = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=401, body=body, response=response)


class PermissionDeniedError(APIStatusError):
    """403 Forbidden."""

    def __init__(
        self,
        message: str = "Permission denied.",
        *,
        body: Any = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=403, body=body, response=response)


class NotFoundError(APIStatusError):
    """404 Not Found."""

    def __init__(
        self,
        message: str = "Resource not found.",
        *,
        body: Any = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=404, body=body, response=response)


class UnprocessableEntityError(APIStatusError):
    """422 Unprocessable Entity."""

    def __init__(
        self,
        message: str = "Unprocessable entity.",
        *,
        body: Any = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=422, body=body, response=response)


class RateLimitError(APIStatusError):
    """429 Too Many Requests."""

    def __init__(
        self,
        message: str = "Rate limit exceeded.",
        *,
        body: Any = None,
        response: Any = None,
    ) -> None:
        super().__init__(message, status_code=429, body=body, response=response)


class InternalServerError(APIStatusError):
    """500+ Server Error."""

    def __init__(
        self,
        message: str = "Internal server error.",
        *,
        status_code: int = 500,
        body: Any = None,
        response: Any = None,
    ) -> None:
        super().__init__(
            message, status_code=status_code, body=body, response=response
        )
