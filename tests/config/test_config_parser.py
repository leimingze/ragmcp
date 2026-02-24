"""Tests for ConfigParser."""

import os
import tempfile

import pytest
import yaml

from ragmcp.config import Config, ConfigError, load_config


class TestLoadValidConfig:
    """Test loading valid configuration files."""

    def test_load_valid_config_succeeds(self):
        """Loading a valid config file should return a Config object."""
        # Create a temporary valid config file
        valid_config = {
            "llm": {"provider": "azure", "model": "gpt-4o"},
            "embedding": {"provider": "azure", "model": "text-embedding-3-large"},
            "vector_store": {"backend": "chroma"},
            "retrieval": {"rerank_backend": "none"},
            "evaluation": {"enabled": True},
            "observability": {"logging": {"level": "INFO"}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(valid_config, f)
            temp_path = f.name

        try:
            config = load_config(temp_path)

            assert isinstance(config, Config)
            assert config.llm["provider"] == "azure"
            assert config.llm["model"] == "gpt-4o"
        finally:
            os.unlink(temp_path)

    def test_load_config_from_default_path(self):
        """Loading from default path 'config/settings.yaml' should work."""
        # This assumes config/settings.yaml exists from task 1.7.1
        if os.path.exists("config/settings.yaml"):
            config = load_config("config/settings.yaml")
            assert isinstance(config, Config)


class TestMissingConfigDefaults:
    """Test that missing configuration uses default values."""

    def test_missing_llm_provider_uses_default(self):
        """Missing llm.provider should use a sensible default."""
        minimal_config = {
            "llm": {"model": "gpt-4o"},  # missing provider
            "embedding": {"provider": "azure", "model": "text-embedding-3-large"},
            "vector_store": {"backend": "chroma"},
            "retrieval": {"rerank_backend": "none"},
            "evaluation": {"enabled": True},
            "observability": {"logging": {"level": "INFO"}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(minimal_config, f)
            temp_path = f.name

        try:
            config = load_config(temp_path)
            # Should have a default provider
            assert "provider" in config.llm
        finally:
            os.unlink(temp_path)

    def test_missing_optional_sections_ignored(self):
        """Missing optional sections should not cause errors."""
        minimal_config = {
            "llm": {"provider": "azure", "model": "gpt-4o"},
            "embedding": {"provider": "azure", "model": "text-embedding-3-large"},
            "vector_store": {"backend": "chroma"},
            "retrieval": {"rerank_backend": "none"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(minimal_config, f)
            temp_path = f.name

        try:
            config = load_config(temp_path)
            assert isinstance(config, Config)
        finally:
            os.unlink(temp_path)


class TestInvalidConfigRaisesError:
    """Test that invalid configuration raises ConfigError."""

    def test_missing_required_section_raises_error(self):
        """Missing required section should raise ConfigError."""
        invalid_config = {
            "llm": {"provider": "azure", "model": "gpt-4o"},
            # Missing embedding, vector_store, retrieval
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(invalid_config, f)
            temp_path = f.name

        try:
            with pytest.raises(ConfigError, match="required"):
                load_config(temp_path)
        finally:
            os.unlink(temp_path)

    def test_invalid_yaml_syntax_raises_error(self):
        """Invalid YAML syntax should raise ConfigError."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content:\n  - broken")
            temp_path = f.name

        try:
            with pytest.raises(ConfigError):
                load_config(temp_path)
        finally:
            os.unlink(temp_path)

    def test_nonexistent_file_raises_error(self):
        """Loading a non-existent file should raise ConfigError."""
        with pytest.raises(ConfigError, match="not found"):
            load_config("nonexistent_config.yaml")

    def test_invalid_llm_provider_raises_error(self):
        """Invalid llm.provider should raise ConfigError."""
        invalid_config = {
            "llm": {"provider": "invalid_provider", "model": "gpt-4o"},
            "embedding": {"provider": "azure", "model": "text-embedding-3-large"},
            "vector_store": {"backend": "chroma"},
            "retrieval": {"rerank_backend": "none"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(invalid_config, f)
            temp_path = f.name

        try:
            with pytest.raises(ConfigError, match="provider"):
                load_config(temp_path)
        finally:
            os.unlink(temp_path)


class TestConfigObject:
    """Test Config object properties."""

    def test_config_has_required_sections(self):
        """Config object should expose all required sections."""
        valid_config = {
            "llm": {"provider": "azure", "model": "gpt-4o"},
            "embedding": {"provider": "azure", "model": "text-embedding-3-large"},
            "vector_store": {"backend": "chroma"},
            "retrieval": {"rerank_backend": "none"},
            "evaluation": {"enabled": True},
            "observability": {"logging": {"level": "INFO"}},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(valid_config, f)
            temp_path = f.name

        try:
            config = load_config(temp_path)

            # Check that all required sections are accessible
            assert hasattr(config, "llm")
            assert hasattr(config, "embedding")
            assert hasattr(config, "vector_store")
            assert hasattr(config, "retrieval")
            assert hasattr(config, "evaluation")
            assert hasattr(config, "observability")
        finally:
            os.unlink(temp_path)
