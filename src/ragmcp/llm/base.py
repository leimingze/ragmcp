"""LLM client base abstractions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Message:
    """A message in a conversation."""

    role: str
    content: str


@dataclass
class Response:
    """A response from an LLM."""

    content: str


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def chat(self, messages: list[Message]) -> Response:
        """Send a chat request and return the response.

        Args:
            messages: List of messages in the conversation.

        Returns:
            Response from the LLM.
        """
        ...
