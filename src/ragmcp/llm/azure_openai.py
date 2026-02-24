"""Azure OpenAI LLM provider implementation."""


from ragmcp.llm.base import LLMClient, Message, Response

try:
    from openai import AzureOpenAI as AzureOpenAIClient
except ImportError:
    AzureOpenAIClient = None  # type: ignore[assignment, misc]


class AzureOpenAILLM(LLMClient):
    """Azure OpenAI LLM provider.

    This client uses Azure OpenAI service to generate text completions.
    """

    def __init__(
        self,
        api_key: str,
        api_base: str,
        api_version: str,
        deployment_name: str,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        http_client: object | None = None,
    ):
        """Initialize Azure OpenAI LLM client.

        Args:
            api_key: Azure OpenAI API key.
            api_base: Azure OpenAI endpoint URL (e.g., https://your-resource.openai.azure.com).
            api_version: Azure OpenAI API version.
            deployment_name: Name of the deployed model in Azure.
            temperature: Sampling temperature for generation.
            max_tokens: Maximum tokens to generate.
            http_client: Optional HTTP client for testing.
        """
        if AzureOpenAIClient is None:
            raise ImportError(
                "openai package is required. Install with: pip install openai"
            )

        # Build client kwargs
        client_kwargs: dict = {
            "api_key": api_key,
            "base_url": api_base,
            "api_version": api_version,
        }
        if http_client is not None:
            client_kwargs["http_client"] = http_client

        self._client = AzureOpenAIClient(**client_kwargs)
        self._deployment_name = deployment_name
        self._temperature = temperature
        self._max_tokens = max_tokens

    def chat(
        self,
        messages: list[Message],
        temperature: float | None = None,
        max_tokens: int | None = None,
        stop: list[str] | None = None,
        stream: bool = False,
    ) -> Response:
        """Generate chat completion using Azure OpenAI.

        Args:
            messages: List of chat messages.
            temperature: Override default temperature.
            max_tokens: Override default max_tokens.
            stop: Stop sequences.
            stream: Whether to stream responses (not yet supported).

        Returns:
            Response containing generated text.

        Raises:
            Exception: If API call fails.
        """
        # Convert Message format to Azure format
        azure_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        # Build request parameters
        request_params: dict = {
            "model": self._deployment_name,
            "messages": azure_messages,
            "temperature": (
                temperature if temperature is not None else self._temperature
            ),
        }

        if max_tokens is not None:
            request_params["max_tokens"] = max_tokens
        elif self._max_tokens is not None:
            request_params["max_tokens"] = self._max_tokens

        if stop is not None:
            request_params["stop"] = stop

        # Call Azure OpenAI API
        completion = self._client.chat.completions.create(**request_params)

        # Extract response content
        content = completion.choices[0].message.content

        return Response(content=content or "")

    @property
    def client(self):
        """Expose the underlying Azure OpenAI client for testing."""
        return self._client
