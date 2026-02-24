"""Tests for LLMFactory."""

import pytest
from ragmcp.factory.llm_factory import LLMFactory
from ragmcp.llm.base import LLMClient


class TestLLMFactory:
    """Test LLMFactory creates correct LLM instances based on config."""

    def test_azure_config_returns_azure_llm(self):
        """Azure config should return an Azure LLM instance."""
        config = {
            "provider": "azure",
            "api_key": "test-key",
            "endpoint": "https://test.openai.azure.com",
        }

        llm = LLMFactory.get_llm(config)

        assert isinstance(llm, LLMClient)
        # Should have some indication it's Azure (via type or metadata)
        assert type(llm).__name__ == "MockAzureOpenAILLM"

    def test_openai_config_returns_openai_llm(self):
        """OpenAI config should return an OpenAI LLM instance."""
        config = {
            "provider": "openai",
            "api_key": "test-key",
            "model": "gpt-4",
        }

        llm = LLMFactory.get_llm(config)

        assert isinstance(llm, LLMClient)
        assert type(llm).__name__ == "MockOpenAILLM"

    def test_unknown_provider_raises_error(self):
        """Unknown provider should raise ValueError."""
        config = {
            "provider": "unknown_provider",
            "api_key": "test-key",
        }

        with pytest.raises(ValueError, match="Unknown LLM provider"):
            LLMFactory.get_llm(config)

    def test_default_provider_when_not_specified(self):
        """When provider is not specified, should use default or raise error."""
        config = {"api_key": "test-key"}

        # Should raise error for missing provider
        with pytest.raises(ValueError, match="provider"):
            LLMFactory.get_llm(config)
