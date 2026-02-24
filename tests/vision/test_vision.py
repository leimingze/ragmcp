"""Tests for Vision LLM abstractions."""

from ragmcp.llm.base import Response
from ragmcp.vision.base import BaseVisionLLM, MultimodalMessage


class TestBaseVisionLLMInheritance:
    """Test BaseVisionLLM inheritance."""

    def test_base_vision_llm_is_llm_client_subclass(self):
        """BaseVisionLLM should be a subclass of LLMClient."""
        from ragmcp.llm.base import LLMClient

        assert issubclass(BaseVisionLLM, LLMClient)


class TestMultimodalMessageStructure:
    """Test MultimodalMessage data structure."""

    def test_multimodal_message_structure(self):
        """MultimodalMessage should contain text and images fields."""
        msg = MultimodalMessage(text="hello", images=[])
        assert hasattr(msg, "text")
        assert hasattr(msg, "images")
        assert msg.text == "hello"
        assert msg.images == []

    def test_images_is_list(self):
        """images should be a list type."""
        msg = MultimodalMessage(text="test", images=["img1.png", "img2.png"])
        assert isinstance(msg.images, list)
        assert len(msg.images) == 2


class TestVisionLLMAcceptsMultimodalMessage:
    """Test BaseVisionLLM accepts multimodal input."""

    def test_chat_accepts_multimodal_message(self):
        """chat() should accept messages with images."""

        class MockVisionLLM(BaseVisionLLM):
            def chat(self, messages: list[MultimodalMessage]) -> Response:
                return Response(content=f"Processed {len(messages)} messages")

        client = MockVisionLLM()

        # Text-only message
        response1 = client.chat([MultimodalMessage(text="hello", images=[])])
        assert response1.content == "Processed 1 messages"

        # Message with images
        response2 = client.chat(
            [MultimodalMessage(text="what's this?", images=["image1.png"])]
        )
        assert response2.content == "Processed 1 messages"

        # Mixed content
        response3 = client.chat(
            [
                MultimodalMessage(text="describe", images=["img1.png", "img2.png"]),
                MultimodalMessage(text="and this", images=[]),
            ]
        )
        assert response3.content == "Processed 2 messages"
