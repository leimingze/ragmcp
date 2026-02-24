"""Tests for VisionLLMFactory."""

import pytest

from ragmcp.factory.vision_llm_factory import VisionLLMFactory
from ragmcp.vision.base import BaseVisionLLM


class TestVisionLLMFactory:
    """Test VisionLLMFactory creates correct Vision LLM instances based on config."""

    def test_azure_vision_config_returns_azure_vision_llm(self):
        """Azure vision config should return an Azure Vision LLM instance."""
        config = {
            "provider": "azure",
            "api_key": "test-key",
            "endpoint": "https://test.openai.azure.com",
        }

        vision_llm = VisionLLMFactory.get_vision_llm(config)

        assert isinstance(vision_llm, BaseVisionLLM)
        assert type(vision_llm).__name__ == "MockAzureOpenAIVision"

    def test_unknown_provider_raises_error(self):
        """Unknown provider should raise ValueError."""
        config = {
            "provider": "unknown_provider",
            "api_key": "test-key",
        }

        with pytest.raises(ValueError, match="Unknown Vision LLM provider"):
            VisionLLMFactory.get_vision_llm(config)

    def test_missing_provider_raises_error(self):
        """Missing provider should raise ValueError."""
        config = {"api_key": "test-key"}

        with pytest.raises(ValueError, match="provider"):
            VisionLLMFactory.get_vision_llm(config)

    def test_vision_llm_accepts_multimodal_messages(self):
        """Factory-created Vision LLM should accept multimodal messages."""
        from ragmcp.vision.base import MultimodalMessage

        config = {
            "provider": "azure",
            "api_key": "test-key",
        }

        vision_llm = VisionLLMFactory.get_vision_llm(config)
        message = MultimodalMessage(
            text="Describe this image",
            images=["image1.png"],
        )

        response = vision_llm.chat([message])

        assert response.content is not None
