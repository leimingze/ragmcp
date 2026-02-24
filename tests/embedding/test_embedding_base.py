"""Tests for Embedding base abstractions."""

import numpy as np
import pytest
from ragmcp.embedding.base import EmbeddingClient


class TestEmbeddingClientAbstractClass:
    """Test EmbeddingClient abstract class behavior."""

    def test_cannot_instantiate_abstract_embedding_client(self):
        """EmbeddingClient is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            EmbeddingClient()  # type: ignore

    def test_subclass_without_embed_raises_error(self):
        """Subclass must implement embed() method."""
        class IncompleteEmbeddingClient(EmbeddingClient):
            pass  # Missing embed() implementation

        with pytest.raises(TypeError):
            IncompleteEmbeddingClient()

    def test_embed_accepts_batch_and_returns_vectors(self):
        """embed() accepts batch texts and returns vector list."""
        class MockEmbeddingClient(EmbeddingClient):
            def embed(self, texts: list[str]) -> list[np.ndarray]:
                # Return fixed vectors for testing
                return [np.array([0.1, 0.2, 0.3]) for _ in texts]

        client = MockEmbeddingClient()
        vectors = client.embed(["text1", "text2"])

        assert len(vectors) == 2
        assert all(isinstance(v, np.ndarray) for v in vectors)
        assert vectors[0].shape == (3,)

    def test_vectors_are_l2_normalized(self):
        """Returned vectors should be L2 normalized."""
        class MockEmbeddingClient(EmbeddingClient):
            def embed(self, texts: list[str]) -> list[np.ndarray]:
                # Return normalized vectors
                vectors = []
                for _ in texts:
                    v = np.array([0.6, 0.8, 0.0])
                    v = v / np.linalg.norm(v)  # L2 normalize
                    vectors.append(v)
                return vectors

        client = MockEmbeddingClient()
        vectors = client.embed(["test"])

        # L2 norm should be approximately 1.0
        assert np.abs(np.linalg.norm(vectors[0]) - 1.0) < 1e-6
