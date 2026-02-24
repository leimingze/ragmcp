"""Tests for Transform abstractions."""

import pytest

from ragmcp.pipeline.base import Chunk, Transform


class TestTransformAbstractClass:
    """Test Transform abstract class behavior."""

    def test_cannot_instantiate_abstract_transform(self):
        """Transform is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            Transform()  # type: ignore

    def test_transform_has_transform_method(self):
        """Subclass must implement transform() method."""

        class IncompleteTransform(Transform):
            pass  # Missing transform() implementation

        with pytest.raises(TypeError):
            IncompleteTransform()


class TestTransformMethods:
    """Test Transform method signatures."""

    def test_transform_accepts_chunk(self):
        """transform() should accept a Chunk as input."""

        class MockTransform(Transform):
            def transform(self, chunk):
                return chunk

        transformer = MockTransform()
        chunk = Chunk(text="Original content", metadata={"source": "test.pdf"})

        # Should not raise an error
        result = transformer.transform(chunk)
        assert result is chunk

    def test_transform_returns_enhanced_chunk(self):
        """transform() should return an enhanced Chunk with additional metadata."""

        class ImageCaptionTransform(Transform):
            def transform(self, chunk):
                # Simulate adding image caption to metadata
                new_metadata = dict(chunk.metadata)
                new_metadata["image_caption"] = "A diagram showing the RAG pipeline"
                return Chunk(text=chunk.text, metadata=new_metadata)

        transformer = ImageCaptionTransform()
        chunk = Chunk(text="Content with image", metadata={"source": "doc.pdf"})

        result = transformer.transform(chunk)

        assert result.text == "Content with image"
        assert "image_caption" in result.metadata
        assert result.metadata["image_caption"] == "A diagram showing the RAG pipeline"
        # Original metadata should be preserved
        assert result.metadata["source"] == "doc.pdf"

    def test_transform_can_modify_text(self):
        """transform() can modify the chunk text content."""

        class HTMLCleanerTransform(Transform):
            def transform(self, chunk):
                # Simulate HTML cleaning
                cleaned_text = chunk.text.replace("<tag>", "").replace("</tag>", "")
                return Chunk(text=cleaned_text, metadata=chunk.metadata)

        transformer = HTMLCleanerTransform()
        chunk = Chunk(
            text="<tag>Content</tag> with tags", metadata={"source": "doc.html"}
        )

        result = transformer.transform(chunk)

        assert result.text == "Content with tags"
        assert "<tag>" not in result.text

    def test_transform_preserves_positioning_metadata(self):
        """transform() should preserve positioning information in metadata."""

        class MetadataEnricherTransform(Transform):
            def transform(self, chunk):
                new_metadata = dict(chunk.metadata)
                new_metadata["enriched"] = True
                return Chunk(text=chunk.text, metadata=new_metadata)

        transformer = MetadataEnricherTransform()
        chunk = Chunk(
            text="Sample content",
            metadata={
                "source": "test.pdf",
                "chunk_index": 0,
                "start_offset": 0,
                "end_offset": 100,
            },
        )

        result = transformer.transform(chunk)

        # Positioning metadata should be preserved
        assert result.metadata["chunk_index"] == 0
        assert result.metadata["start_offset"] == 0
        assert result.metadata["end_offset"] == 100
        # New metadata should be added
        assert result.metadata["enriched"] is True
