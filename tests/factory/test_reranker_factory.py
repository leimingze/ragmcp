"""Tests for RerankerFactory."""

import pytest

from ragmcp.factory.reranker_factory import RerankerFactory
from ragmcp.rerank.base import Reranker


class TestRerankerFactory:
    """Test RerankerFactory creates correct Reranker instances based on config."""

    def test_none_config_returns_noop_reranker(self):
        """None config should return a NoOpReranker that returns original order."""
        config = {"backend": "none"}

        reranker = RerankerFactory.get_reranker(config)

        assert isinstance(reranker, Reranker)
        assert type(reranker).__name__ == "NoOpReranker"

    def test_noop_reranker_preserves_original_order(self):
        """NoOpReranker should return chunks in their original order."""
        config = {"backend": "none"}

        reranker = RerankerFactory.get_reranker(config)

        chunks = ["chunk1", "chunk2", "chunk3"]
        results = reranker.rerank("test query", chunks)

        # NoOpReranker should preserve order
        assert len(results) == 3
        assert [r.chunk for r in results] == ["chunk1", "chunk2", "chunk3"]

    def test_unknown_backend_raises_error(self):
        """Unknown backend should raise ValueError."""
        config = {"backend": "unknown_backend"}

        with pytest.raises(ValueError, match="Unknown Reranker backend"):
            RerankerFactory.get_reranker(config)

    def test_missing_backend_raises_error(self):
        """Missing backend should raise ValueError."""
        config = {}

        with pytest.raises(ValueError, match="backend"):
            RerankerFactory.get_reranker(config)

    def test_noop_reranker_scores_all_equal(self):
        """NoOpReranker should assign equal scores to all chunks."""
        config = {"backend": "none"}

        reranker = RerankerFactory.get_reranker(config)

        chunks = ["first", "second", "third"]
        results = reranker.rerank("test query", chunks)

        # All scores should be equal (indicating no re-ranking)
        scores = [r.score for r in results]
        assert all(s == scores[0] for s in scores)
