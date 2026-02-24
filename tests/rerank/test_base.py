"""Tests for Reranker abstractions."""

import pytest
from ragmcp.rerank.base import Reranker, RankedChunk


class TestRerankerAbstractClass:
    """Test Reranker abstract class behavior."""

    def test_cannot_instantiate_abstract_reranker(self):
        """Reranker is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Reranker()  # type: ignore

    def test_reranker_has_rerank_method(self):
        """Subclass must implement rerank() method."""
        class IncompleteReranker(Reranker):
            pass  # Missing rerank() implementation

        with pytest.raises(TypeError):
            IncompleteReranker()


class TestRerankerMethods:
    """Test Reranker method signatures."""

    def test_rerank_method_works(self):
        """rerank() should return ranked chunks with scores."""
        class MockReranker(Reranker):
            def rerank(self, query, chunks, top_k=None):
                # Simple mock: return chunks with descending scores
                return [
                    RankedChunk(chunk=chunks[0], score=0.95),
                    RankedChunk(chunk=chunks[1], score=0.87),
                ][:top_k]

        reranker = MockReranker()
        chunks = ["relevant content", "less relevant content"]

        results = reranker.rerank("test query", chunks, top_k=2)

        assert len(results) == 2
        assert results[0].score == 0.95
        assert results[0].chunk == "relevant content"


class TestRankedChunk:
    """Test RankedChunk data structure."""

    def test_ranked_chunk_structure(self):
        """RankedChunk should contain chunk and score fields."""
        chunk = RankedChunk(chunk="test content", score=0.9)

        assert chunk.chunk == "test content"
        assert chunk.score == 0.9

    def test_ranked_chunk_with_dict(self):
        """RankedChunk should work with dict chunks (metadata)."""
        chunk_dict = {"text": "content", "source": "doc.pdf"}
        ranked = RankedChunk(chunk=chunk_dict, score=0.85)

        assert ranked.chunk == chunk_dict
        assert ranked.chunk["source"] == "doc.pdf"
        assert ranked.score == 0.85
