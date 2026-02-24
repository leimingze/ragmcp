"""LLM Factory for creating LLM instances based on configuration."""

from ragmcp.llm.base import LLMClient, Message, Response


# Mock implementations for testing
# Real implementations will be provided in future tasks
class MockAzureOpenAILLM(LLMClient):
    """Mock Azure OpenAI LLM implementation."""

    def __init__(self, config: dict):
        self.config = config
        self.api_key = config.get("api_key", "")
        self.endpoint = config.get("endpoint", "")

    def chat(self, messages: list[Message]) -> Response:
        return Response(content=f"Azure mock response to {len(messages)} messages")


class MockOpenAILLM(LLMClient):
    """Mock OpenAI LLM implementation."""

    def __init__(self, config: dict):
        self.config = config
        self.api_key = config.get("api_key", "")
        self.model = config.get("model", "gpt-4")

    def chat(self, messages: list[Message]) -> Response:
        return Response(content=f"OpenAI mock response using {self.model}")


class LLMFactory:
    """Factory for creating LLM instances based on configuration.

    Supported providers:
        - azure: Azure OpenAI Service
        - openai: OpenAI API

    Usage:
        config = {"provider": "azure", "api_key": "...", "endpoint": "..."}
        llm = LLMFactory.get_llm(config)
    """

    @staticmethod
    def get_llm(config: dict) -> LLMClient:
        """Create an LLM instance based on the configuration.

        Args:
            config: Configuration dictionary with at least a "provider" key.

        Returns:
            An LLMClient instance.

        Raises:
            ValueError: If provider is missing or unknown.
        """
        provider = config.get("provider")

        if not provider:
            raise ValueError("Configuration must specify 'provider'")

        if provider == "azure":
            return MockAzureOpenAILLM(config)
        elif provider == "openai":
            return MockOpenAILLM(config)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
