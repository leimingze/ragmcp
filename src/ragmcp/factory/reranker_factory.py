"""Reranker Factory for creating reranker instances based on configuration."""

from typing import Any

from ragmcp.rerank.base import RankedChunk, Reranker


class NoOpReranker(Reranker):
    """No-op reranker that preserves original chunk order.

    Used when reranking is disabled or not needed.
    """

    def rerank(
        self,
        query: str,
        chunks: list[Any],
        top_k: int | None = None,
    ) -> list[RankedChunk]:
        """Return chunks in their original order without re-ranking.

        Args:
            query: The search query (unused, kept for interface consistency).
            chunks: List of chunks to return in original order.
            top_k: Maximum number to return. None returns all.

        Returns:
            List of RankedChunk with equal scores (1.0) in original order.
        """
        ranked_chunks = [RankedChunk(chunk=chunk, score=1.0) for chunk in chunks]
        if top_k is not None:
            ranked_chunks = ranked_chunks[:top_k]
        return ranked_chunks


class RerankerFactory:
    """Factory for creating Reranker instances based on configuration.

    Supported backends:
        - none: No-op reranker (preserves original order)
        - cross_encoder: Cross-encoder reranker (future)
        - llm: LLM-based reranker (future)

    Usage:
        config = {"backend": "none"}
        reranker = RerankerFactory.get_reranker(config)
    """

    @staticmethod
    def get_reranker(config: dict) -> Reranker:
        """Create a Reranker instance based on the configuration.

        Args:
            config: Configuration dictionary with at least a "backend" key.

        Returns:
            A Reranker instance.

        Raises:
            ValueError: If backend is missing or unknown.
        """
        backend = config.get("backend")

        if not backend:
            raise ValueError("Configuration must specify 'backend'")

        if backend == "none":
            return NoOpReranker()
        else:
            raise ValueError(f"Unknown Reranker backend: {backend}. Supported: none")
