"""Extract resource -- exact field values from documents."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence

from ..types import ExtractDecision

if TYPE_CHECKING:
    from .._http import AsyncHTTPTransport, HTTPTransport


class ExtractResource:
    """Extract exact field values from document text with character offsets."""

    def __init__(self, http: HTTPTransport) -> None:
        self._http = http

    def extract(
        self,
        *,
        question: str,
        state: str = "",
        documents: Optional[List[Dict[str, Any]]] = None,
    ) -> ExtractDecision:
        """Extract a single field value from the document.

        Args:
            question: The field to extract (e.g. 'termination notice period').
            state: Text content of the document.
            documents: Optional document attachments (PDF, DOCX, etc.).

        Returns:
            An ExtractDecision with the extracted value and character offsets.
        """
        return self._http.post("/extract", {
            "question": question, "state": state, "documents": documents,
        }, ExtractDecision)

    def extract_many(
        self,
        *,
        fields: Sequence[str],
        state: str = "",
        documents: Optional[List[Dict[str, Any]]] = None,
    ) -> ExtractDecision:
        """Extract multiple field values from the document at once.

        Args:
            fields: List of field names to extract.
            state: Text content of the document.
            documents: Optional document attachments.

        Returns:
            An ExtractDecision with a ``values`` dict mapping field names
            to ExtractValue objects.
        """
        return self._http.post("/extract", {
            "fields": list(fields), "state": state, "documents": documents,
        }, ExtractDecision)


class AsyncExtractResource:
    """Async version of ExtractResource."""

    def __init__(self, http: AsyncHTTPTransport) -> None:
        self._http = http

    async def extract(self, **kwargs: Any) -> ExtractDecision:
        """Extract a single field value from the document."""
        return await self._http.post("/extract", kwargs, ExtractDecision)

    async def extract_many(self, **kwargs: Any) -> ExtractDecision:
        """Extract multiple field values from the document at once."""
        if "fields" in kwargs and not isinstance(kwargs["fields"], list):
            kwargs["fields"] = list(kwargs["fields"])
        return await self._http.post("/extract", kwargs, ExtractDecision)
