"""Tests for EmbeddingFactory."""

import numpy as np
import pytest

from ragmcp.embedding.base import EmbeddingClient
from ragmcp.factory.embedding_factory import EmbeddingFactory


class TestEmbeddingFactory:
    """Test EmbeddingFactory creates correct Embedding instances based on config."""

    def test_openai_config_returns_openai_embedding(self):
        """OpenAI config should return an OpenAI Embedding instance."""
        config = {
            "provider": "openai",
            "api_key": "test-key",
            "model": "text-embedding-3-small",
        }

        embedder = EmbeddingFactory.get_embedding(config)

        assert isinstance(embedder, EmbeddingClient)
        assert type(embedder).__name__ == "MockOpenAIEmbedding"

    def test_unknown_provider_raises_error(self):
        """Unknown provider should raise ValueError."""
        config = {
            "provider": "unknown_provider",
            "api_key": "test-key",
        }

        with pytest.raises(ValueError, match="Unknown Embedding provider"):
            EmbeddingFactory.get_embedding(config)

    def test_missing_provider_raises_error(self):
        """Missing provider should raise ValueError."""
        config = {"api_key": "test-key"}

        with pytest.raises(ValueError, match="provider"):
            EmbeddingFactory.get_embedding(config)

    def test_embedding_produces_vectors(self):
        """Factory-created embedder should produce valid vectors."""
        config = {
            "provider": "openai",
            "api_key": "test-key",
        }

        embedder = EmbeddingFactory.get_embedding(config)
        vectors = embedder.embed(["test text"])

        assert len(vectors) == 1
        assert isinstance(vectors[0], np.ndarray)
