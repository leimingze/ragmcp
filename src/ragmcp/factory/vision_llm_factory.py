"""Vision LLM Factory for creating vision LLM instances based on configuration."""

from ragmcp.llm.base import Response
from ragmcp.vision.base import BaseVisionLLM, MultimodalMessage


# Mock implementations for testing
# Real implementations will be provided in future tasks
class MockAzureOpenAIVision(BaseVisionLLM):
    """Mock Azure OpenAI Vision LLM implementation."""

    def __init__(self, config: dict):
        self.config = config
        self.api_key = config.get("api_key", "")
        self.endpoint = config.get("endpoint", "")

    def chat(self, messages: list[MultimodalMessage]) -> Response:
        image_count = sum(len(msg.images) for msg in messages)
        return Response(content=f"Azure Vision mock response with {image_count} images")


class VisionLLMFactory:
    """Factory for creating Vision LLM instances based on configuration.

    Supported providers:
        - azure: Azure OpenAI Vision (GPT-4o/GPT-4-Vision)

    Usage:
        config = {"provider": "azure", "api_key": "...", "endpoint": "..."}
        vision_llm = VisionLLMFactory.get_vision_llm(config)
    """

    @staticmethod
    def get_vision_llm(config: dict) -> BaseVisionLLM:
        """Create a Vision LLM instance based on the configuration.

        Args:
            config: Configuration dictionary with at least a "provider" key.

        Returns:
            A BaseVisionLLM instance.

        Raises:
            ValueError: If provider is missing or unknown.
        """
        provider = config.get("provider")

        if not provider:
            raise ValueError("Configuration must specify 'provider'")

        if provider == "azure":
            return MockAzureOpenAIVision(config)
        else:
            raise ValueError(f"Unknown Vision LLM provider: {provider}")
