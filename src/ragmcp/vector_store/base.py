"""VectorStore base abstractions."""

from abc import ABC, abstractmethod

import numpy as np


class VectorStore(ABC):
    """Abstract base class for vector storage implementations.

    Provides unified interface for vector operations including insert,
    query, delete, and upsert.
    """

    @abstractmethod
    def insert(self, vectors: list[np.ndarray], payloads: list[dict]) -> int:
        """Insert vectors with their associated payloads.

        Args:
            vectors: List of embedding vectors to store.
            payloads: List of payload dictionaries associated with each vector.

        Returns:
            Number of vectors inserted.
        """
        ...

    @abstractmethod
    def query(
        self, query_vector: np.ndarray, top_k: int
    ) -> list[dict]:
        """Query the vector store for similar vectors.

        Args:
            query_vector: The query vector to search for.
            top_k: Maximum number of results to return.

        Returns:
            List of results, each containing vector, score, and payload.
        """
        ...

    @abstractmethod
    def delete(self, ids: list) -> int:
        """Delete vectors by their IDs.

        Args:
            ids: List of vector IDs to delete.

        Returns:
            Number of vectors deleted.
        """
        ...

    @abstractmethod
    def upsert(self, vectors: list[np.ndarray], payloads: list[dict]) -> int:
        """Update existing vectors or insert new ones (insert-or-update).

        Args:
            vectors: List of embedding vectors to upsert.
            payloads: List of payload dictionaries associated with each vector.

        Returns:
            Number of vectors upserted.
        """
        ...
