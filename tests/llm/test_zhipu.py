"""Tests for ZhipuLLM provider."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from ragmcp.llm import LLMClient, Message, Response, ZhipuLLM


class TestZhipuIsLLMClient:
    """Test ZhipuLLM is a valid LLMClient."""

    def test_zhipu_is_llm_client(self):
        """ZhipuLLM should be an instance of LLMClient."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.zhipu_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            client = ZhipuLLM(
                api_key="test-key",
                model="glm-4",
                http_client=mock_http_client,
            )

            assert isinstance(client, LLMClient)


class TestChatCallsZhipuAPI:
    """Test chat() method calls Zhipu API."""

    def test_chat_calls_zhipu_api(self):
        """chat() should send correctly formatted request to Zhipu API."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.zhipu_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            # Mock the response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = ZhipuLLM(
                api_key="test-key",
                model="glm-4",
                http_client=mock_http_client,
            )

            messages = [Message(role="user", content="Hello")]
            response = client.chat(messages)

            # Verify OpenAI client was called with Zhipu base URL
            mock_openai_class.assert_called_once()
            call_kwargs = mock_openai_class.call_args.kwargs
            assert call_kwargs["api_key"] == "test-key"
            assert call_kwargs["base_url"] == "https://open.bigmodel.cn/api/paas/v4/"
            assert call_kwargs["http_client"] == mock_http_client

            # Verify chat.completions.create was called
            assert mock_openai_instance.chat.completions.create.called

            # Verify response
            assert isinstance(response, Response)
            assert response.content == "Test response"

    def test_chat_converts_messages_format(self):
        """chat() should convert Message format to Zhipu format."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.zhipu_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = ZhipuLLM(
                api_key="test-key",
                model="glm-4",
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
            zhipu_messages = call_kwargs["messages"]
            assert len(zhipu_messages) == 2
            assert zhipu_messages[0]["role"] == "system"
            assert zhipu_messages[0]["content"] == "You are helpful."
            assert zhipu_messages[1]["role"] == "user"
            assert zhipu_messages[1]["content"] == "Hello"

    def test_chat_includes_model(self):
        """chat() should include model name in the request."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.zhipu_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = ZhipuLLM(
                api_key="test-key",
                model="glm-4-flash",
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify model is set
            create_call = mock_openai_instance.chat.completions.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["model"] == "glm-4-flash"


class TestZhipuAPIErrorIsPropagated:
    """Test error handling."""

    def test_zhipu_api_error_is_propagated(self):
        """Zhipu API errors should be propagated to the caller."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.zhipu_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            # Mock an API error
            mock_openai_instance.chat.completions.create.side_effect = Exception(
                "API Error: Rate limit exceeded"
            )

            client = ZhipuLLM(
                api_key="test-key",
                model="glm-4",
                http_client=mock_http_client,
            )

            with pytest.raises(Exception, match="API Error: Rate limit exceeded"):
                client.chat([Message(role="user", content="Test")])


class TestZhipuSupportsTemperature:
    """Test temperature parameter support."""

    def test_chat_with_temperature(self):
        """chat() should support temperature parameter."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.zhipu_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Creative response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = ZhipuLLM(
                api_key="test-key",
                model="glm-4",
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

        with patch("ragmcp.llm.zhipu_llm.OpenAIClient") as mock_openai_class:
            mock_openai_instance = MagicMock()
            mock_openai_class.return_value = mock_openai_instance

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_openai_instance.chat.completions.create.return_value = mock_response

            client = ZhipuLLM(
                api_key="test-key",
                model="glm-4",
                temperature=0.5,
                http_client=mock_http_client,
            )

            # Override with different temperature
            client.chat([Message(role="user", content="Test")], temperature=0.9)

            # Verify override temperature was used
            create_call = mock_openai_instance.chat.completions.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["temperature"] == 0.9