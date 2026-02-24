"""Tests for Loader abstractions."""

import pytest
from ragmcp.pipeline.base import Document, Loader


class TestDocument:
    """Test Document data structure."""

    def test_document_has_text_and_metadata(self):
        """Document should contain text and metadata fields."""
        doc = Document(text="Sample content", metadata={"source": "test.pdf"})

        assert doc.text == "Sample content"
        assert doc.metadata == {"source": "test.pdf"}

    def test_document_with_empty_metadata(self):
        """Document should work with empty metadata."""
        doc = Document(text="Content only", metadata={})

        assert doc.text == "Content only"
        assert doc.metadata == {}

    def test_document_with_complex_metadata(self):
        """Document should support complex metadata structures."""
        metadata = {
            "source": "doc.pdf",
            "page": 5,
            "title": "Chapter 1",
            "images": ["img1.png", "img2.png"],
        }
        doc = Document(text="Content", metadata=metadata)

        assert doc.metadata["page"] == 5
        assert len(doc.metadata["images"]) == 2


class TestLoaderAbstractClass:
    """Test Loader abstract class behavior."""

    def test_cannot_instantiate_abstract_loader(self):
        """Loader is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Loader()  # type: ignore

    def test_loader_has_load_method(self):
        """Subclass must implement load() method."""
        class IncompleteLoader(Loader):
            pass  # Missing load() implementation

        with pytest.raises(TypeError):
            IncompleteLoader()


class TestLoaderMethods:
    """Test Loader method signatures."""

    def test_load_returns_document(self):
        """load() should return a Document instance."""
        class MockLoader(Loader):
            def load(self, file_path):
                return Document(
                    text=f"Content from {file_path}",
                    metadata={"source": file_path},
                )

        loader = MockLoader()
        doc = loader.load("test.pdf")

        assert isinstance(doc, Document)
        assert doc.text == "Content from test.pdf"
        assert doc.metadata["source"] == "test.pdf"

    def test_load_accepts_file_path(self):
        """load() should accept a file path string."""
        class MockLoader(Loader):
            def load(self, file_path):
                return Document(
                    text="Content",
                    metadata={"loaded_from": file_path},
                )

        loader = MockLoader()
        doc = loader.load("/path/to/document.pdf")

        assert doc.metadata["loaded_from"] == "/path/to/document.pdf"
