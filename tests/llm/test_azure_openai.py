"""Tests for AzureOpenAILLM provider."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from ragmcp.llm import AzureOpenAILLM, LLMClient, Message, Response


class TestAzureOpenAIIsLLMClient:
    """Test AzureOpenAILLM is a valid LLMClient."""

    def test_azure_openai_is_llm_client(self):
        """AzureOpenAILLM should be an instance of LLMClient."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            # Mock the AzureOpenAI class to return a mock client
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            client = AzureOpenAILLM(
                api_key="test-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="gpt-4",
                http_client=mock_http_client,
            )

            assert isinstance(client, LLMClient)


class TestChatCallsAzureOpenAI:
    """Test chat() method calls Azure OpenAI API."""

    def test_chat_calls_azure_openai_api(self):
        """chat() should send correctly formatted request to Azure API."""

        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            # Setup mock
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            # Mock the response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_azure_instance.chat.completions.create.return_value = mock_response

            client = AzureOpenAILLM(
                api_key="test-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="gpt-4",
                http_client=mock_http_client,
            )

            messages = [Message(role="user", content="Hello")]
            response = client.chat(messages)

            # Verify Azure OpenAI class was called correctly
            mock_azure_class.assert_called_once()
            call_kwargs = mock_azure_class.call_args.kwargs
            assert call_kwargs["api_key"] == "test-key"
            assert call_kwargs["base_url"] == "https://test.openai.azure.com"
            assert call_kwargs["api_version"] == "2024-02-15-preview"
            assert call_kwargs["http_client"] == mock_http_client

            # Verify chat.completions.create was called
            assert mock_azure_instance.chat.completions.create.called

            # Verify response
            assert isinstance(response, Response)
            assert response.content == "Test response"

    def test_chat_converts_messages_format(self):
        """chat() should convert Message format to Azure format."""

        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_azure_instance.chat.completions.create.return_value = mock_response

            client = AzureOpenAILLM(
                api_key="test-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="gpt-4",
                http_client=mock_http_client,
            )

            messages = [
                Message(role="system", content="You are a helpful assistant."),
                Message(role="user", content="Hello"),
            ]
            client.chat(messages)

            # Get the call arguments
            create_call = mock_azure_instance.chat.completions.create
            assert create_call.called

            # Verify messages were converted
            call_kwargs = create_call.call_args.kwargs
            assert "messages" in call_kwargs
            azure_messages = call_kwargs["messages"]
            assert len(azure_messages) == 2
            assert azure_messages[0]["role"] == "system"
            assert azure_messages[0]["content"] == "You are a helpful assistant."
            assert azure_messages[1]["role"] == "user"
            assert azure_messages[1]["content"] == "Hello"

    def test_chat_includes_deployment_name(self):
        """chat() should include deployment name in the request."""

        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_azure_instance.chat.completions.create.return_value = mock_response

            client = AzureOpenAILLM(
                api_key="test-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="my-deployment",
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify model/deployment is set
            create_call = mock_azure_instance.chat.completions.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["model"] == "my-deployment"


class TestAzureUsesAPIKeyAuthentication:
    """Test API key authentication."""

    def test_azure_uses_api_key_authentication(self):
        """AzureOpenAILLM should use API key for authentication."""

        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_azure_instance.chat.completions.create.return_value = mock_response

            client = AzureOpenAILLM(
                api_key="my-secret-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="gpt-4",
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify API key was passed to AzureOpenAI
            call_kwargs = mock_azure_class.call_args.kwargs
            assert call_kwargs["api_key"] == "my-secret-key"


class TestAzureAPIErrorIsPropagated:
    """Test error handling."""

    def test_azure_api_error_is_propagated(self):
        """Azure API errors should be propagated to the caller."""

        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            # Mock an API error
            mock_azure_instance.chat.completions.create.side_effect = Exception(
                "API Error: Rate limit exceeded"
            )

            client = AzureOpenAILLM(
                api_key="test-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="gpt-4",
                http_client=mock_http_client,
            )

            with pytest.raises(Exception, match="API Error: Rate limit exceeded"):
                client.chat([Message(role="user", content="Test")])

    def test_azure_authentication_error_is_propagated(self):
        """Authentication errors should be propagated."""

        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            # Mock authentication error
            mock_azure_instance.chat.completions.create.side_effect = Exception(
                "Invalid API key"
            )

            client = AzureOpenAILLM(
                api_key="invalid-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="gpt-4",
                http_client=mock_http_client,
            )

            with pytest.raises(Exception, match="Invalid API key"):
                client.chat([Message(role="user", content="Test")])


class TestAzureOpenAISupportsTemperature:
    """Test temperature parameter support."""

    def test_chat_with_temperature(self):
        """chat() should support temperature parameter."""

        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Creative response"
            mock_azure_instance.chat.completions.create.return_value = mock_response

            client = AzureOpenAILLM(
                api_key="test-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="gpt-4",
                temperature=0.7,
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify temperature was passed
            create_call = mock_azure_instance.chat.completions.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["temperature"] == 0.7

    def test_chat_temperature_override(self):
        """chat() should allow overriding default temperature."""

        mock_http_client = Mock()

        with patch("ragmcp.llm.azure_openai.AzureOpenAIClient") as mock_azure_class:
            mock_azure_instance = MagicMock()
            mock_azure_class.return_value = mock_azure_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_azure_instance.chat.completions.create.return_value = mock_response

            client = AzureOpenAILLM(
                api_key="test-key",
                api_base="https://test.openai.azure.com",
                api_version="2024-02-15-preview",
                deployment_name="gpt-4",
                temperature=0.5,
                http_client=mock_http_client,
            )

            # Override with different temperature
            client.chat([Message(role="user", content="Test")], temperature=0.9)

            # Verify override temperature was used
            create_call = mock_azure_instance.chat.completions.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["temperature"] == 0.9
