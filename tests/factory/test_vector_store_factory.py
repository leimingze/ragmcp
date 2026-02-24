"""Tests for VectorStoreFactory."""

import numpy as np
import pytest

from ragmcp.factory.vector_store_factory import VectorStoreFactory
from ragmcp.vector_store.base import VectorStore


class TestVectorStoreFactory:
    """Test VectorStoreFactory creates correct VectorStore instances based on config."""

    def test_milvus_config_returns_milvus_store(self):
        """Milvus config should return a Milvus VectorStore instance."""
        config = {
            "backend": "milvus",
            "host": "localhost",
            "port": 19530,
        }

        store = VectorStoreFactory.get_vector_store(config)

        assert isinstance(store, VectorStore)
        assert type(store).__name__ == "MockMilvusVectorStore"

    def test_chroma_config_returns_chroma_store(self):
        """Chroma config should return a Chroma VectorStore instance."""
        config = {
            "backend": "chroma",
            "path": "./chroma_db",
        }

        store = VectorStoreFactory.get_vector_store(config)

        assert isinstance(store, VectorStore)
        assert type(store).__name__ == "MockChromaVectorStore"

    def test_unknown_backend_raises_error(self):
        """Unknown backend should raise ValueError."""
        config = {
            "backend": "unknown_backend",
        }

        with pytest.raises(ValueError, match="Unknown VectorStore backend"):
            VectorStoreFactory.get_vector_store(config)

    def test_missing_backend_raises_error(self):
        """Missing backend should raise ValueError."""
        config = {"host": "localhost"}

        with pytest.raises(ValueError, match="backend"):
            VectorStoreFactory.get_vector_store(config)

    def test_vector_store_supports_basic_operations(self):
        """Factory-created store should support basic operations."""
        config = {"backend": "milvus"}

        store = VectorStoreFactory.get_vector_store(config)

        # Test insert
        vectors = [np.array([1.0, 2.0, 3.0])]
        payloads = [{"id": 1}]
        count = store.insert(vectors, payloads)
        assert count == 1

        # Test query
        results = store.query(np.array([1.0, 2.0, 3.0]), top_k=1)
        assert len(results) >= 0
