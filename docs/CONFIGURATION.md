# Configuration System

## Overview

The pipeline uses a YAML + Pydantic configuration system for type safety and flexibility.

## Key Design Decisions

- **Pydantic v2** for validation and settings management
- YAML as the primary configuration language (human-readable)
- Support for environment variable substitution
- Strict mode (`extra = 'forbid'`) to catch typos early

## How to Use

```python
from src.config import load_config

config = load_config("config/base.yaml")
print(config.pipeline.name)
print(config.cleaning.rules)
```

## Configuration Sections

| Section         | Description                              |
|-----------------|------------------------------------------|
| pipeline        | General pipeline metadata                |
| data_sources    | Input data locations and formats         |
| reference_data  | Lookup/reference datasets                |
| cleaning        | Data cleaning rules                      |
| enrichment      | Future enrichment configuration          |
| output          | Output format and location               |

## Environment Variable Support

You can use `${VAR_NAME}` or `${VAR_NAME:default}` syntax in YAML files.

Example:
```yaml
data_sources:
  customers:
    path: ${RAW_DATA_PATH:data/raw/customers.csv}
```

## Adding New Configuration

1. Add fields to the Pydantic models in `src/config/models.py`
2. Update example YAML files
3. Update this documentation
