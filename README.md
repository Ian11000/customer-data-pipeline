## customer-data-pipeline

**Advanced Python Data Cleaning & Enrichment Pipeline** focused on Customer data.

### Current Status

- Configuration system (Pydantic + YAML) — **Completed**
- Core cleaning modules — In progress

### Overview
This project is a modular, production-style data pipeline for cleaning and enriching customer-related datasets. It is designed to demonstrate real-world data engineering skills including data quality management, enrichment strategies, and scalable pipeline design.

### Key Features (Planned)
- Config-driven pipeline
- Multiple data source support (CSV, Excel, JSON, Database)
- Comprehensive data cleaning (standardization, deduplication, missing value handling)
- Data enrichment via reference data and external APIs
- Data quality scoring and reporting
- Full audit logging and lineage
- Output to Parquet, CSV, and databases

### Tech Stack
- Python 3.11+
- Pandas / Polars
- Pydantic for configuration
- Logging + structured logs
- Optional: FastAPI for pipeline triggering

### Project Structure
```
customer-data-pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── config/          # Configuration system (Pydantic + YAML)
│   ├── cleaning/
│   ├── enrichment/
│   ├── pipeline/
│   └── utils/
├── config/            # Example YAML configurations
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
├── docs/
└── tests/
```

### Getting Started (Configuration)

```bash
pip install -r requirements.txt

# Load configuration
python -c "from src.config import load_config; print(load_config('config/base.yaml'))"
```

### Roadmap
- Phase 1: Configuration system using Pydantic + YAML → **Done**
- Phase 2: Core cleaning functions
- Phase 3: Enrichment layer
- Phase 4: Full pipeline orchestration + quality reporting

### Domain Focus
**Customer Data** (CRM, marketing, support, sales touchpoints)

---

*Part of a 4-project Data Engineering portfolio.*