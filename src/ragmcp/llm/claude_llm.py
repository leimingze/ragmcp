"""Anthropic Claude LLM provider implementation."""

from ragmcp.llm.base import LLMClient, Message, Response

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None  # type: ignore[misc]


class ClaudeLLM(LLMClient):
    """Anthropic Claude LLM provider.

    This client uses Anthropic's API to generate text completions.
    """

    DEFAULT_MODEL = "claude-3-opus-20240229"

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        http_client: object | None = None,
    ):
        """Initialize Claude LLM client.

        Args:
            api_key: Anthropic API key.
            model: Model name (e.g., claude-3-opus-20240229, claude-3-sonnet-20240229).
            temperature: Sampling temperature for generation.
            max_tokens: Maximum tokens to generate.
            http_client: Optional HTTP client for testing.
        """
        if Anthropic is None:
            raise ImportError(
                "anthropic package is required. Install with: pip install anthropic"
            )

        # Build client kwargs
        client_kwargs: dict = {"api_key": api_key}
        if http_client is not None:
            client_kwargs["http_client"] = http_client

        self._client = Anthropic(**client_kwargs)
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    def chat(
        self,
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> Response:
        """Generate chat completion using Claude.

        Args:
            messages: List of chat messages.
            temperature: Override default temperature.
            max_tokens: Override default max_tokens.

        Returns:
            Response containing generated text.

        Raises:
            Exception: If API call fails.
        """
        # Separate system message from other messages
        system_message = None
        claude_messages = []

        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                claude_messages.append({"role": msg.role, "content": msg.content})

        # Build request parameters
        request_params: dict = {
            "model": self._model,
            "messages": claude_messages,
            "temperature": (
                temperature if temperature is not None else self._temperature
            ),
        }

        if system_message:
            request_params["system"] = system_message

        if max_tokens is not None:
            request_params["max_tokens"] = max_tokens
        elif self._max_tokens is not None:
            request_params["max_tokens"] = self._max_tokens

        # Call Claude API
        completion = self._client.messages.create(**request_params)

        # Extract response content
        content = completion.content[0].text if completion.content else ""

        return Response(content=content)

    @property
    def client(self):
        """Expose the underlying client for testing."""
        return self._client
