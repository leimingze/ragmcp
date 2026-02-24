"""Tests for OllamaLLM provider."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from ragmcp.llm import LLMClient, Message, OllamaLLM, Response


class TestOllamaIsLLMClient:
    """Test OllamaLLM is a valid LLMClient."""

    def test_ollama_is_llm_client(self):
        """OllamaLLM should be an instance of LLMClient."""
        client = OllamaLLM(model="llama2")

        assert isinstance(client, LLMClient)


class TestOllamaCommunicatesViaHTTP:
    """Test OllamaLLM communicates via HTTP."""

    def test_chat_calls_ollama_api(self):
        """chat() should send correctly formatted request to Ollama API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": "Test response"}}

        with patch("ragmcp.llm.ollama_llm.httpx") as mock_httpx:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_httpx.Client.return_value.__enter__.return_value = mock_client

            client = OllamaLLM(model="llama2", base_url="http://localhost:11434")
            messages = [Message(role="user", content="Hello")]
            response = client.chat(messages)

            # Verify HTTP POST was called
            assert mock_client.post.called

            # Verify request format
            call_args = mock_client.post.call_args
            assert call_args[0][0] == "http://localhost:11434/api/chat"
            request_body = call_args[1]["json"]
            assert request_body["model"] == "llama2"
            assert request_body["messages"] == [{"role": "user", "content": "Hello"}]
            assert request_body["stream"] is False

            # Verify response
            assert isinstance(response, Response)
            assert response.content == "Test response"

    def test_chat_uses_default_base_url(self):
        """chat() should use default base URL if not specified."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": "Response"}}

        with patch("ragmcp.llm.ollama_llm.httpx") as mock_httpx:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_httpx.Client.return_value.__enter__.return_value = mock_client

            client = OllamaLLM(model="llama2")
            client.chat([Message(role="user", content="Test")])

            call_args = mock_client.post.call_args
            assert call_args[0][0] == "http://localhost:11434/api/chat"

    def test_chat_includes_model(self):
        """chat() should include model name in the request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": "Response"}}

        with patch("ragmcp.llm.ollama_llm.httpx") as mock_httpx:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_httpx.Client.return_value.__enter__.return_value = mock_client

            client = OllamaLLM(model="codellama")
            client.chat([Message(role="user", content="Test")])

            call_args = mock_client.post.call_args
            request_body = call_args[1]["json"]
            assert request_body["model"] == "codellama"


class TestChatConvertsMessagesFormat:
    """Test chat() message format conversion."""

    def test_chat_converts_messages_format(self):
        """chat() should convert Message format to Ollama format."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": {"content": "Response"}}

        with patch("ragmcp.llm.ollama_llm.httpx") as mock_httpx:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_httpx.Client.return_value.__enter__.return_value = mock_client

            client = OllamaLLM(model="llama2")

            messages = [
                Message(role="system", content="You are helpful."),
                Message(role="user", content="Hello"),
            ]
            client.chat(messages)

            call_args = mock_client.post.call_args
            request_body = call_args[1]["json"]
            assert len(request_body["messages"]) == 2
            assert request_body["messages"][0]["role"] == "system"
            assert request_body["messages"][0]["content"] == "You are helpful."
            assert request_body["messages"][1]["role"] == "user"
            assert request_body["messages"][1]["content"] == "Hello"


class TestOllamaAPIErrorIsPropagated:
    """Test error handling."""

    def test_ollama_api_error_is_propagated(self):
        """Ollama API errors should be propagated to the caller."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal server error"}

        with patch("ragmcp.llm.ollama_llm.httpx") as mock_httpx:
            mock_client = MagicMock()
            mock_client.post.return_value = mock_response
            mock_httpx.Client.return_value.__enter__.return_value = mock_client

            client = OllamaLLM(model="llama2")

            with pytest.raises(Exception, match="Ollama API error"):
                client.chat([Message(role="user", content="Test")])

    def test_connection_error_is_propagated(self):
        """Connection errors should be propagated."""
        with patch("ragmcp.llm.ollama_llm.httpx") as mock_httpx:
            mock_client = MagicMock()
            mock_client.post.side_effect = Exception("Connection refused")
            mock_httpx.Client.return_value.__enter__.return_value = mock_client

            client = OllamaLLM(model="llama2")

            with pytest.raises(Exception, match="Connection refused"):
                client.chat([Message(role="user", content="Test")])