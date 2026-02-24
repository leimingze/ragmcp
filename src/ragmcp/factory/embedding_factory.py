"""Embedding Factory for creating embedding instances based on configuration."""

import numpy as np

from ragmcp.embedding.base import EmbeddingClient


# Mock implementations for testing
# Real implementations will be provided in future tasks
class MockOpenAIEmbedding(EmbeddingClient):
    """Mock OpenAI Embedding implementation."""

    def __init__(self, config: dict):
        self.config = config
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "text-embedding-3-small")

    def embed(self, texts: list[str]) -> list[np.ndarray]:
        # Return mock normalized vectors (deterministic for testing)
        vectors = []
        for text in texts:
            # Create a deterministic vector based on text content
            dim = 1536  # OpenAI embedding dimension
            # Use hash of text to generate deterministic values
            np.random.seed(hash(text) % (2**31))
            vec = np.random.randn(dim)
            # L2 normalize
            vec = vec / np.linalg.norm(vec)
            vectors.append(vec)
        return vectors


class EmbeddingFactory:
    """Factory for creating Embedding instances based on configuration.

    Supported providers:
        - openai: OpenAI Embedding API

    Usage:
        config = {"provider": "openai", "api_key": "...", "model": "..."}
        embedder = EmbeddingFactory.get_embedding(config)
    """

    @staticmethod
    def get_embedding(config: dict) -> EmbeddingClient:
        """Create an Embedding instance based on the configuration.

        Args:
            config: Configuration dictionary with at least a "provider" key.

        Returns:
            An EmbeddingClient instance.

        Raises:
            ValueError: If provider is missing or unknown.
        """
        provider = config.get("provider")

        if not provider:
            raise ValueError("Configuration must specify 'provider'")

        if provider == "openai":
            return MockOpenAIEmbedding(config)
        else:
            raise ValueError(f"Unknown Embedding provider: {provider}")
