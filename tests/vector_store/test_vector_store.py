"""Tests for VectorStore abstractions."""

import numpy as np
import pytest

from ragmcp.vector_store.base import VectorStore


class TestVectorStoreAbstractClass:
    """Test VectorStore abstract class behavior."""

    def test_cannot_instantiate_abstract_vector_store(self):
        """VectorStore is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            VectorStore()  # type: ignore

    def test_vector_store_has_insert_method(self):
        """Subclass must implement insert() method."""

        class IncompleteVectorStore(VectorStore):
            pass  # Missing insert() implementation

        with pytest.raises(TypeError):
            IncompleteVectorStore()

    def test_vector_store_has_query_method(self):
        """Subclass must implement query() method."""

        class IncompleteVectorStore(VectorStore):
            def insert(self, vectors, payloads):
                pass

        with pytest.raises(TypeError):
            IncompleteVectorStore()

    def test_vector_store_has_delete_and_upsert_methods(self):
        """Subclass must implement delete() and upsert() methods."""

        class IncompleteVectorStore(VectorStore):
            def insert(self, vectors, payloads):
                pass

            def query(self, query_vector, top_k):
                pass

        with pytest.raises(TypeError):
            IncompleteVectorStore()


class TestVectorStoreMethods:
    """Test VectorStore method signatures."""

    def test_insert_method_works(self):
        """insert() should store vectors with payloads."""

        class MockVectorStore(VectorStore):
            def __init__(self):
                self.data = []

            def insert(self, vectors, payloads):
                self.data.extend(zip(vectors, payloads))
                return len(vectors)

            def query(self, query_vector, top_k):
                return []

            def delete(self, ids):
                return 0

            def upsert(self, vectors, payloads):
                return 0

        store = MockVectorStore()
        vectors = [np.array([1.0, 2.0]), np.array([3.0, 4.0])]
        payloads = [{"id": 1}, {"id": 2}]

        count = store.insert(vectors, payloads)
        assert count == 2
        assert len(store.data) == 2

    def test_query_method_works(self):
        """query() should return top-k results."""

        class MockVectorStore(VectorStore):
            def insert(self, vectors, payloads):
                pass

            def query(self, query_vector, top_k):
                return [
                    {"vector": np.array([1.0]), "score": 0.9, "payload": {"id": 1}},
                    {"vector": np.array([2.0]), "score": 0.8, "payload": {"id": 2}},
                ][:top_k]

            def delete(self, ids):
                return 0

            def upsert(self, vectors, payloads):
                return 0

        store = MockVectorStore()
        results = store.query(np.array([1.0]), top_k=2)

        assert len(results) == 2
        assert results[0]["score"] == 0.9

    def test_delete_and_upsert_methods_work(self):
        """delete() and upsert() should work correctly."""

        class MockVectorStore(VectorStore):
            def insert(self, vectors, payloads):
                return 0

            def query(self, query_vector, top_k):
                return []

            def delete(self, ids):
                return len(ids)

            def upsert(self, vectors, payloads):
                return len(vectors)

        store = MockVectorStore()

        # Test delete
        deleted = store.delete([1, 2, 3])
        assert deleted == 3

        # Test upsert
        vectors = [np.array([1.0])]
        payloads = [{"id": 1}]
        upserted = store.upsert(vectors, payloads)
        assert upserted == 1
