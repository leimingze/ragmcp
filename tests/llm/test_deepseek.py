"""Tests for DeepSeekLLM provider."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from ragmcp.llm import DeepSeekLLM, LLMClient, Message, Response


class TestDeepSeekIsLLMClient:
    """Test DeepSeekLLM is a valid LLMClient."""

    def test_deepseek_is_llm_client(self):
        """DeepSeekLLM should be an instance of LLMClient."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.deepseek_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            client = DeepSeekLLM(
                api_key="test-key",
                model="deepseek-chat",
                http_client=mock_http_client,
            )

            assert isinstance(client, LLMClient)


class TestChatCallsDeepSeekAPI:
    """Test chat() method calls DeepSeek API."""

    def test_chat_calls_deepseek_api(self):
        """chat() should send correctly formatted request to DeepSeek API."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.deepseek_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            # Mock the response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = DeepSeekLLM(
                api_key="test-key",
                model="deepseek-chat",
                http_client=mock_http_client,
            )

            messages = [Message(role="user", content="Hello")]
            response = client.chat(messages)

            # Verify OpenAI client was called with DeepSeek base URL
            mock_openai_class.assert_called_once()
            call_kwargs = mock_openai_class.call_args.kwargs
            assert call_kwargs["api_key"] == "test-key"
            assert call_kwargs["base_url"] == "https://api.deepseek.com"
            assert call_kwargs["http_client"] == mock_http_client

            # Verify chat.completions.create was called
            assert mock_openai_instance.chat.completions.create.called

            # Verify response
            assert isinstance(response, Response)
            assert response.content == "Test response"

    def test_chat_converts_messages_format(self):
        """chat() should convert Message format to DeepSeek format."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.deepseek_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = DeepSeekLLM(
                api_key="test-key",
                model="deepseek-chat",
                http_client=mock_http_client,
            )

            messages = [
                Message(role="system", content="You are helpful."),
                Message(role="user", content="Hello"),
            ]
            client.chat(messages)

            # Get the call arguments
            create_call = mock_openai_instance.chat.completions.create
            assert create_call.called

            # Verify messages were converted
            call_kwargs = create_call.call_args.kwargs
            assert "messages" in call_kwargs
            deepseek_messages = call_kwargs["messages"]
            assert len(deepseek_messages) == 2
            assert deepseek_messages[0]["role"] == "system"
            assert deepseek_messages[0]["content"] == "You are helpful."
            assert deepseek_messages[1]["role"] == "user"
            assert deepseek_messages[1]["content"] == "Hello"

    def test_chat_includes_model(self):
        """chat() should include model name in the request."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.deepseek_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = DeepSeekLLM(
                api_key="test-key",
                model="deepseek-coder",
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify model is set
            create_call = mock_openai_instance.chat.completions.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["model"] == "deepseek-coder"


class TestDeepSeekAPIErrorIsPropagated:
    """Test error handling."""

    def test_deepseek_api_error_is_propagated(self):
        """DeepSeek API errors should be propagated to the caller."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.deepseek_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            # Mock an API error
            mock_openai_instance.chat.completions.create.side_effect = Exception(
                "API Error: Rate limit exceeded"
            )

            client = DeepSeekLLM(
                api_key="test-key",
                model="deepseek-chat",
                http_client=mock_http_client,
            )

            with pytest.raises(Exception, match="API Error: Rate limit exceeded"):
                client.chat([Message(role="user", content="Test")])


class TestDeepSeekSupportsTemperature:
    """Test temperature parameter support."""

    def test_chat_with_temperature(self):
        """chat() should support temperature parameter."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.deepseek_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Creative response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = DeepSeekLLM(
                api_key="test-key",
                model="deepseek-chat",
                temperature=0.7,
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify temperature was passed
            create_call = mock_openai_instance.chat.completions.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["temperature"] == 0.7

    def test_chat_temperature_override(self):
        """chat() should allow overriding default temperature."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.deepseek_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = DeepSeekLLM(
                api_key="test-key",
                model="deepseek-chat",
                temperature=0.5,
                http_client=mock_http_client,
            )

            # Override with different temperature
            client.chat([Message(role="user", content="Test")], temperature=0.9)

            # Verify override temperature was used
            create_call = mock_openai_instance.chat.completions.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["temperature"] == 0.9