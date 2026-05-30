from __future__ import annotations

import os
from pathlib import Path

from loguru import logger
from pydantic import ValidationError
import yaml

from src.config.models import CustomerPipelineConfig


def load_config(config_path: str | Path) -> CustomerPipelineConfig:
    """
    Load and validate pipeline configuration from a YAML file.
    Supports environment variable overrides for sensitive values.
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)

    # Basic environment variable substitution (simple ${VAR} support)
    raw_config = _substitute_env_vars(raw_config)

    try:
        config = CustomerPipelineConfig(**raw_config)
        logger.info(f"Configuration loaded successfully from {config_path}")
        return config
    except ValidationError as e:
        logger.error(f"Invalid configuration in {config_path}:\n{e}")
        raise


def _substitute_env_vars(config: dict) -> dict:
    """Recursively substitute ${ENV_VAR} placeholders with environment values."""
    if isinstance(config, dict):
        return {k: _substitute_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [_substitute_env_vars(item) for item in config]
    elif isinstance(config, str) and config.startswith("$") and "{" in config:
        # Simple ${VAR} or ${VAR:default} support
        import re
        def replacer(match):
            var_expr = match.group(1)
            if ":" in var_expr:
                var_name, default = var_expr.split(":", 1)
                return os.getenv(var_name, default)
            return os.getenv(var_expr, "")
        return re.sub(r"\$\{([^}]+)\}", replacer, config)
    return config
