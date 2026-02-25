"""Tests for ClaudeLLM provider."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from ragmcp.llm import ClaudeLLM, LLMClient, Message, Response


class TestClaudeIsLLMClient:
    """Test ClaudeLLM is a valid LLMClient."""

    def test_claude_is_llm_client(self):
        """ClaudeLLM should be an instance of LLMClient."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-opus-20240229",
                http_client=mock_http_client,
            )

            assert isinstance(client, LLMClient)


class TestChatCallsClaudeAPI:
    """Test chat() method calls Claude API."""

    def test_chat_calls_claude_api(self):
        """chat() should send correctly formatted request to Claude API."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            # Mock the response
            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = "Test response"
            mock_anthropic_instance.messages.create.return_value = mock_response

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-opus-20240229",
                http_client=mock_http_client,
            )

            messages = [Message(role="user", content="Hello")]
            response = client.chat(messages)

            # Verify Anthropic client was called
            mock_anthropic_class.assert_called_once()
            call_kwargs = mock_anthropic_class.call_args.kwargs
            assert call_kwargs["api_key"] == "test-key"
            assert call_kwargs["http_client"] == mock_http_client

            # Verify messages.create was called
            assert mock_anthropic_instance.messages.create.called

            # Verify response
            assert isinstance(response, Response)
            assert response.content == "Test response"

    def test_chat_converts_messages_format(self):
        """chat() should convert Message format to Claude format."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = "Response"
            mock_anthropic_instance.messages.create.return_value = mock_response

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-opus-20240229",
                http_client=mock_http_client,
            )

            messages = [
                Message(role="user", content="Hello"),
            ]
            client.chat(messages)

            # Get the call arguments
            create_call = mock_anthropic_instance.messages.create
            assert create_call.called

            # Verify messages were converted
            call_kwargs = create_call.call_args.kwargs
            assert "messages" in call_kwargs
            claude_messages = call_kwargs["messages"]
            assert len(claude_messages) == 1
            assert claude_messages[0]["role"] == "user"
            assert claude_messages[0]["content"] == "Hello"

    def test_chat_includes_model(self):
        """chat() should include model name in the request."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = "Response"
            mock_anthropic_instance.messages.create.return_value = mock_response

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-sonnet-20240229",
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify model is set
            create_call = mock_anthropic_instance.messages.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["model"] == "claude-3-sonnet-20240229"

    def test_chat_adds_system_message(self):
        """chat() should add system message if provided."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = "Response"
            mock_anthropic_instance.messages.create.return_value = mock_response

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-opus-20240229",
                http_client=mock_http_client,
            )

            messages = [
                Message(role="system", content="You are helpful."),
                Message(role="user", content="Hello"),
            ]
            client.chat(messages)

            # Verify system message is passed separately
            create_call = mock_anthropic_instance.messages.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["system"] == "You are helpful."
            # System message should not be in messages list
            claude_messages = call_kwargs["messages"]
            assert len(claude_messages) == 1
            assert claude_messages[0]["role"] == "user"


class TestClaudeAPIErrorIsPropagated:
    """Test error handling."""

    def test_claude_api_error_is_propagated(self):
        """Claude API errors should be propagated to the caller."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            # Mock an API error
            mock_anthropic_instance.messages.create.side_effect = Exception(
                "API Error: Rate limit exceeded"
            )

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-opus-20240229",
                http_client=mock_http_client,
            )

            with pytest.raises(Exception, match="API Error: Rate limit exceeded"):
                client.chat([Message(role="user", content="Test")])


class TestClaudeSupportsTemperature:
    """Test temperature parameter support."""

    def test_chat_with_temperature(self):
        """chat() should support temperature parameter."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = "Creative response"
            mock_anthropic_instance.messages.create.return_value = mock_response

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-opus-20240229",
                temperature=0.7,
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify temperature was passed
            create_call = mock_anthropic_instance.messages.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["temperature"] == 0.7

    def test_chat_temperature_override(self):
        """chat() should allow overriding default temperature."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = "Response"
            mock_anthropic_instance.messages.create.return_value = mock_response

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-opus-20240229",
                temperature=0.5,
                http_client=mock_http_client,
            )

            # Override with different temperature
            client.chat([Message(role="user", content="Test")], temperature=0.9)

            # Verify override temperature was used
            create_call = mock_anthropic_instance.messages.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["temperature"] == 0.9

    def test_chat_with_max_tokens(self):
        """chat() should support max_tokens parameter."""
        mock_http_client = Mock()

        with patch("ragmcp.llm.claude_llm.Anthropic") as mock_anthropic_class:
            mock_anthropic_instance = MagicMock()
            mock_anthropic_class.return_value = mock_anthropic_instance

            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = "Response"
            mock_anthropic_instance.messages.create.return_value = mock_response

            client = ClaudeLLM(
                api_key="test-key",
                model="claude-3-opus-20240229",
                max_tokens=1000,
                http_client=mock_http_client,
            )

            client.chat([Message(role="user", content="Test")])

            # Verify max_tokens was passed
            create_call = mock_anthropic_instance.messages.create
            call_kwargs = create_call.call_args.kwargs
            assert call_kwargs["max_tokens"] == 1000