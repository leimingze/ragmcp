"""VectorStore Factory for creating vector store instances based on configuration."""

import numpy as np

from ragmcp.vector_store.base import VectorStore


# Mock implementations for testing
# Real implementations will be provided in future tasks
class MockMilvusVectorStore(VectorStore):
    """Mock Milvus VectorStore implementation."""

    def __init__(self, config: dict):
        self.config = config
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 19530)
        self._data = []

    def insert(self, vectors: list[np.ndarray], payloads: list[dict]) -> int:
        self._data.extend(zip(vectors, payloads))
        return len(vectors)

    def query(self, query_vector: np.ndarray, top_k: int) -> list[dict]:
        return [
            {"vector": v, "score": 0.9, "payload": p} for v, p in self._data[:top_k]
        ]

    def delete(self, ids: list) -> int:
        return len(ids)

    def upsert(self, vectors: list[np.ndarray], payloads: list[dict]) -> int:
        return len(vectors)


class MockChromaVectorStore(VectorStore):
    """Mock Chroma VectorStore implementation."""

    def __init__(self, config: dict):
        self.config = config
        self.path = config.get("path", "./chroma_db")
        self._data = []

    def insert(self, vectors: list[np.ndarray], payloads: list[dict]) -> int:
        self._data.extend(zip(vectors, payloads))
        return len(vectors)

    def query(self, query_vector: np.ndarray, top_k: int) -> list[dict]:
        return [
            {"vector": v, "score": 0.85, "payload": p} for v, p in self._data[:top_k]
        ]

    def delete(self, ids: list) -> int:
        return len(ids)

    def upsert(self, vectors: list[np.ndarray], payloads: list[dict]) -> int:
        return len(vectors)


class VectorStoreFactory:
    """Factory for creating VectorStore instances based on configuration.

    Supported backends:
        - milvus: Milvus vector database
        - chroma: Chroma vector database

    Usage:
        config = {"backend": "milvus", "host": "...", "port": ...}
        store = VectorStoreFactory.get_vector_store(config)
    """

    @staticmethod
    def get_vector_store(config: dict) -> VectorStore:
        """Create a VectorStore instance based on the configuration.

        Args:
            config: Configuration dictionary with at least a "backend" key.

        Returns:
            A VectorStore instance.

        Raises:
            ValueError: If backend is missing or unknown.
        """
        backend = config.get("backend")

        if not backend:
            raise ValueError("Configuration must specify 'backend'")

        if backend == "milvus":
            return MockMilvusVectorStore(config)
        elif backend == "chroma":
            return MockChromaVectorStore(config)
        else:
            raise ValueError(f"Unknown VectorStore backend: {backend}")
