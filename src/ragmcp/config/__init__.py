"""Configuration management for RAG MCP.

This module provides configuration loading and validation for the RAG MCP system.
Configuration is loaded from YAML files and validated against required sections.
"""

from pathlib import Path
from typing import Any

import yaml


class ConfigError(Exception):
    """Exception raised for configuration errors."""

    pass


class Config:
    """Configuration container for RAG MCP.

    This class holds all configuration sections and provides
    attribute access to each section.
    """

    # Valid LLM providers
    VALID_LLM_PROVIDERS = ["azure", "openai", "ollama", "deepseek", "anthropic"]

    # Valid embedding providers
    VALID_EMBEDDING_PROVIDERS = ["azure", "openai", "ollama"]

    # Valid vector store backends
    VALID_VECTOR_STORE_BACKENDS = ["chroma", "qdrant", "milvus"]

    # Valid rerank backends
    VALID_RERANK_BACKENDS = ["none", "cross_encoder", "llm"]

    # Required top-level sections
    REQUIRED_SECTIONS = ["llm", "embedding", "vector_store", "retrieval"]

    def __init__(self, config_dict: dict[str, Any]):
        """Initialize Config from a dictionary.

        Args:
            config_dict: Dictionary containing configuration values.

        Raises:
            ConfigError: If required sections are missing or values are invalid.
        """
        self._raw = config_dict

        # Validate required sections exist
        missing_sections = [s for s in self.REQUIRED_SECTIONS if s not in config_dict]
        if missing_sections:
            raise ConfigError(
                f"Missing required configuration sections: {missing_sections}"
            )

        # Validate and set each section
        self.llm = self._validate_llm(config_dict.get("llm", {}))
        self.embedding = self._validate_embedding(config_dict.get("embedding", {}))
        self.vector_store = self._validate_vector_store(
            config_dict.get("vector_store", {})
        )
        self.retrieval = self._validate_retrieval(config_dict.get("retrieval", {}))
        self.evaluation = config_dict.get("evaluation", {"enabled": False})
        self.observability = config_dict.get(
            "observability",
            {"logging": {"level": "INFO", "format": "text"}},
        )

    def _validate_llm(self, llm_config: dict[str, Any]) -> dict[str, Any]:
        """Validate LLM configuration.

        Args:
            llm_config: LLM configuration dictionary.

        Returns:
            Validated LLM configuration.

        Raises:
            ConfigError: If provider is invalid.
        """
        if "provider" not in llm_config:
            # Default to 'openai' if not specified
            llm_config = dict(llm_config)  # Make a copy
            llm_config["provider"] = "openai"

        provider = llm_config["provider"]
        if provider not in self.VALID_LLM_PROVIDERS:
            raise ConfigError(
                f"Invalid LLM provider: {provider}. "
                f"Valid options: {self.VALID_LLM_PROVIDERS}"
            )

        return llm_config

    def _validate_embedding(self, embedding_config: dict[str, Any]) -> dict[str, Any]:
        """Validate embedding configuration.

        Args:
            embedding_config: Embedding configuration dictionary.

        Returns:
            Validated embedding configuration.

        Raises:
            ConfigError: If provider is invalid.
        """
        if "provider" not in embedding_config:
            embedding_config = dict(embedding_config)  # Make a copy
            embedding_config["provider"] = "openai"

        provider = embedding_config["provider"]
        if provider not in self.VALID_EMBEDDING_PROVIDERS:
            raise ConfigError(
                f"Invalid embedding provider: {provider}. "
                f"Valid options: {self.VALID_EMBEDDING_PROVIDERS}"
            )

        return embedding_config

    def _validate_vector_store(self, vs_config: dict[str, Any]) -> dict[str, Any]:
        """Validate vector store configuration.

        Args:
            vs_config: Vector store configuration dictionary.

        Returns:
            Validated vector store configuration.

        Raises:
            ConfigError: If backend is invalid.
        """
        if "backend" not in vs_config:
            vs_config = dict(vs_config)  # Make a copy
            vs_config["backend"] = "chroma"

        backend = vs_config["backend"]
        if backend not in self.VALID_VECTOR_STORE_BACKENDS:
            raise ConfigError(
                f"Invalid vector store backend: {backend}. "
                f"Valid options: {self.VALID_VECTOR_STORE_BACKENDS}"
            )

        return vs_config

    def _validate_retrieval(self, retrieval_config: dict[str, Any]) -> dict[str, Any]:
        """Validate retrieval configuration.

        Args:
            retrieval_config: Retrieval configuration dictionary.

        Returns:
            Validated retrieval configuration.

        Raises:
            ConfigError: If rerank_backend is invalid.
        """
        if "rerank_backend" not in retrieval_config:
            retrieval_config = dict(retrieval_config)  # Make a copy
            retrieval_config["rerank_backend"] = "none"

        rerank_backend = retrieval_config["rerank_backend"]
        if rerank_backend not in self.VALID_RERANK_BACKENDS:
            raise ConfigError(
                f"Invalid rerank backend: {rerank_backend}. "
                f"Valid options: {self.VALID_RERANK_BACKENDS}"
            )

        return retrieval_config


def load_config(config_path: str) -> Config:
    """Load configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        A Config object containing the loaded configuration.

    Raises:
        ConfigError: If the file doesn't exist, cannot be parsed,
                     or contains invalid configuration.
    """
    path = Path(config_path)

    # Check if file exists
    if not path.exists():
        raise ConfigError(f"Configuration file not found: {config_path}")

    # Read and parse YAML
    try:
        with open(path) as f:
            config_dict = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigError(f"Failed to parse YAML file: {e}") from e
    except OSError as e:
        raise ConfigError(f"Failed to read configuration file: {e}") from e

    # Validate and create Config object
    if not isinstance(config_dict, dict):
        raise ConfigError(
            f"Configuration file must contain a dictionary, got {type(config_dict)}"
        )

    return Config(config_dict)
