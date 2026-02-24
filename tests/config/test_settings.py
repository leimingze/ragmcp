"""Tests for settings.yaml configuration file."""

import yaml


class TestSettingsYaml:
    """Test settings.yaml configuration file structure and validity."""

    def test_settings_yaml_is_valid_yaml(self):
        """config/settings.yaml should be valid YAML that can be parsed."""
        config_path = "config/settings.yaml"

        # Read and parse the YAML file
        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Should return a dictionary
        assert isinstance(config, dict)

    def test_config_has_required_sections(self):
        """Configuration should contain all required sections."""
        config_path = "config/settings.yaml"

        with open(config_path) as f:
            config = yaml.safe_load(f)

        # Check for required top-level sections
        required_sections = [
            "llm",
            "embedding",
            "vector_store",
            "retrieval",
            "evaluation",
            "observability",
        ]

        for section in required_sections:
            assert section in config, f"Missing required section: {section}"

    def test_llm_section_has_required_fields(self):
        """LLM section should have provider and model fields."""
        config_path = "config/settings.yaml"

        with open(config_path) as f:
            config = yaml.safe_load(f)

        llm_config = config["llm"]
        assert "provider" in llm_config
        assert "model" in llm_config

        # Provider should be a known value
        valid_providers = ["azure", "openai", "ollama", "deepseek", "anthropic"]
        assert llm_config["provider"] in valid_providers

    def test_vector_store_section_has_backend(self):
        """vector_store section should specify backend."""
        config_path = "config/settings.yaml"

        with open(config_path) as f:
            config = yaml.safe_load(f)

        vs_config = config["vector_store"]
        assert "backend" in vs_config

        # Backend should be a known value
        valid_backends = ["chroma", "qdrant", "milvus"]
        assert vs_config["backend"] in valid_backends

    def test_retrieval_section_has_rerank_config(self):
        """retrieval section should configure reranking."""
        config_path = "config/settings.yaml"

        with open(config_path) as f:
            config = yaml.safe_load(f)

        retrieval = config["retrieval"]
        assert "rerank_backend" in retrieval

        # Rerank backend should be a known value
        valid_rerank = ["none", "cross_encoder", "llm"]
        assert retrieval["rerank_backend"] in valid_rerank
