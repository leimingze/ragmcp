"""Vision LLM base abstractions."""

from abc import abstractmethod
from dataclasses import dataclass

from ragmcp.llm.base import LLMClient, Response


@dataclass
class MultimodalMessage:
    """A multimodal message containing text and images."""

    text: str
    images: list[str]


class BaseVisionLLM(LLMClient):
    """Abstract base class for Vision LLM clients.

    Extends LLMClient to support multimodal input with both text and images.
    """

    @abstractmethod
    def chat(self, messages: list[MultimodalMessage]) -> Response:
        """Send a chat request with multimodal input and return the response.

        Args:
            messages: List of multimodal messages, each containing text and optional images.

        Returns:
            Response from the Vision LLM.
        """
        ...
