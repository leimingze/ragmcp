"""Embedding client base abstractions."""

from abc import ABC, abstractmethod

import numpy as np


class EmbeddingClient(ABC):
    """Abstract base class for embedding clients.

    Provides batch processing interface and automatic L2 normalization
    of returned vectors.
    """

    @abstractmethod
    def embed(self, texts: list[str]) -> list[np.ndarray]:
        """Generate embeddings for a batch of texts.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors (numpy arrays). Each vector should
            be L2 normalized (unit length).
        """
        ...
