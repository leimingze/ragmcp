"""Ollama LLM provider implementation."""

import httpx

from ragmcp.llm.base import LLMClient, Message, Response


class OllamaLLM(LLMClient):
    """Ollama LLM provider.

    This client uses Ollama's local HTTP API to generate text completions.
    """

    DEFAULT_BASE_URL = "http://localhost:11434"

    def __init__(
        self,
        model: str,
        base_url: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ):
        """Initialize Ollama LLM client.

        Args:
            model: Model name (e.g., llama2, codellama, mistral).
            base_url: Ollama API base URL (default: http://localhost:11434).
            temperature: Sampling temperature for generation.
            max_tokens: Maximum tokens to generate.
        """
        self._model = model
        self._base_url = base_url or self.DEFAULT_BASE_URL
        self._temperature = temperature
        self._max_tokens = max_tokens

    def chat(
        self,
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> Response:
        """Generate chat completion using Ollama.

        Args:
            messages: List of chat messages.
            temperature: Override default temperature.
            max_tokens: Override default max_tokens.

        Returns:
            Response containing generated text.

        Raises:
            Exception: If API call fails.
        """
        # Convert Message format to Ollama format
        ollama_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        # Build request body
        request_body: dict = {
            "model": self._model,
            "messages": ollama_messages,
            "stream": False,
            "options": {
                "temperature": (
                    temperature if temperature is not None else self._temperature
                ),
            },
        }

        if max_tokens is not None:
            request_body["options"]["num_predict"] = max_tokens
        elif self._max_tokens is not None:
            request_body["options"]["num_predict"] = self._max_tokens

        # Make HTTP request to Ollama API
        with httpx.Client() as client:
            response = client.post(
                f"{self._base_url}/api/chat",
                json=request_body,
            )

            if response.status_code != 200:
                error_msg = response.json().get("error", "Unknown error")
                raise Exception(f"Ollama API error: {error_msg}")

            result = response.json()

        # Extract response content
        content = result.get("message", {}).get("content", "")

        return Response(content=content)
