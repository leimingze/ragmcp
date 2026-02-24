"""Tests for Splitter abstractions."""

import pytest

from ragmcp.pipeline.base import Chunk, Document, Splitter


class TestChunk:
    """Test Chunk data structure has required fields."""

    def test_chunk_has_text_field(self):
        """Chunk should have a text field."""
        chunk = Chunk(text="Sample content", metadata={"source": "test.pdf"})
        assert chunk.text == "Sample content"

    def test_chunk_metadata_supports_positioning_fields(self):
        """Chunk metadata should support source, chunk_index, start_offset, end_offset."""
        chunk = Chunk(
            text="Sample content",
            metadata={
                "source": "test.pdf",
                "chunk_index": 0,
                "start_offset": 0,
                "end_offset": 100,
            },
        )

        assert chunk.metadata["source"] == "test.pdf"
        assert chunk.metadata["chunk_index"] == 0
        assert chunk.metadata["start_offset"] == 0
        assert chunk.metadata["end_offset"] == 100


class TestSplitterAbstractClass:
    """Test Splitter abstract class behavior."""

    def test_cannot_instantiate_abstract_splitter(self):
        """Splitter is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Splitter()  # type: ignore

    def test_splitter_has_split_method(self):
        """Subclass must implement split() method."""

        class IncompleteSplitter(Splitter):
            pass  # Missing split() implementation

        with pytest.raises(TypeError):
            IncompleteSplitter()


class TestSplitterMethods:
    """Test Splitter method signatures."""

    def test_split_returns_list_of_chunks(self):
        """split() should return a list of Chunk instances."""

        class MockSplitter(Splitter):
            def split(self, document):
                return [
                    Chunk(
                        text="First part",
                        metadata={
                            "source": document.metadata.get("source", ""),
                            "chunk_index": 0,
                            "start_offset": 0,
                            "end_offset": 50,
                        },
                    ),
                    Chunk(
                        text="Second part",
                        metadata={
                            "source": document.metadata.get("source", ""),
                            "chunk_index": 1,
                            "start_offset": 50,
                            "end_offset": 100,
                        },
                    ),
                ]

        splitter = MockSplitter()
        doc = Document(text="Full document content", metadata={"source": "test.pdf"})

        chunks = splitter.split(doc)

        assert len(chunks) == 2
        assert isinstance(chunks[0], Chunk)
        assert chunks[0].text == "First part"
        assert chunks[0].metadata["chunk_index"] == 0
        assert chunks[1].metadata["chunk_index"] == 1

    def test_split_accepts_document(self):
        """split() should accept a Document as input."""

        class MockSplitter(Splitter):
            def split(self, document):
                return [
                    Chunk(
                        text=document.text[:50],
                        metadata={
                            "source": document.metadata.get("source", ""),
                            "chunk_index": 0,
                            "start_offset": 0,
                            "end_offset": 50,
                        },
                    )
                ]

        splitter = MockSplitter()
        doc = Document(
            text="This is a longer document that needs to be split into chunks.",
            metadata={"source": "doc.pdf"},
        )

        chunks = splitter.split(doc)

        assert len(chunks) == 1
        assert chunks[0].metadata["source"] == "doc.pdf"
