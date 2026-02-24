"""Reranker base abstractions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class RankedChunk:
    """A chunk with its relevance score.

    Attributes:
        chunk: The chunk content (can be string, dict, or custom object).
        score: Relevance score (higher is more relevant).
    """

    chunk: Any
    score: float


class Reranker(ABC):
    """Abstract base class for reranking implementations.

    Provides unified interface for reordering retrieved chunks by relevance
    to the query.
    """

    @abstractmethod
    def rerank(
        self,
        query: str,
        chunks: list[Any],
        top_k: Optional[int] = None,
    ) -> list[RankedChunk]:
        """Rerank chunks by relevance to the query.

        Args:
            query: The search query.
            chunks: List of chunks to rerank (can be strings, dicts, or objects).
            top_k: Maximum number of results to return. None returns all.

        Returns:
            List of RankedChunk objects sorted by relevance (highest first).
        """
        ...
