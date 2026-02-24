"""Tests for LLM base abstractions."""

import pytest
from ragmcp.llm.base import LLMClient, Message, Response


class TestLLMClientAbstractClass:
    """Test LLMClient abstract class behavior."""

    def test_cannot_instantiate_abstract_llm_client_directly(self):
        """LLMClient is abstract and cannot be instantiated directly."""
        with pytest.raises(TypeError):
            LLMClient()  # type: ignore

    def test_subclass_without_chat_method_raises_error(self):
        """Subclass must implement chat() method."""
        class IncompleteLLMClient(LLMClient):
            pass  # Missing chat() implementation

        with pytest.raises(TypeError):
            IncompleteLLMClient()

    def test_subclass_with_chat_method_can_be_instantiated(self):
        """Subclass with chat() can be instantiated and used."""
        class MockLLMClient(LLMClient):
            def chat(self, messages: list[Message]) -> Response:
                return Response(content="mock response")

        client = MockLLMClient()
        response = client.chat([Message(role="user", content="hello")])

        assert response.content == "mock response"


class TestMessageAndResponseDataclasses:
    """Test Message and Response data structures."""

    def test_message_has_role_and_content(self):
        """Message should have role and content fields."""
        msg = Message(role="user", content="hello")
        assert msg.role == "user"
        assert msg.content == "hello"

    def test_response_has_content(self):
        """Response should have content field."""
        resp = Response(content="answer")
        assert resp.content == "answer"

    def test_message_and_response_dataclass_structure(self):
        """Verify Message and Response dataclass structure."""
        # Message has role and content
        msg = Message(role="user", content="test")
        assert hasattr(msg, "role")
        assert hasattr(msg, "content")

        # Response has content
        resp = Response(content="response")
        assert hasattr(resp, "content")
