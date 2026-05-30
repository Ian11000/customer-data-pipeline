## customer-data-pipeline

**Advanced Python Data Cleaning & Enrichment Pipeline** focused on Customer data.

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
│   ├── config/
│   ├── cleaning/
│   ├── enrichment/
│   ├── pipeline/
│   └── utils/
├── data/
│   ├── raw/
│   ├── processed/
│   └── reference/
├── docs/
├── tests/
└── notebooks/
```

### Roadmap
- Phase 1: Core cleaning modules + configuration system
- Phase 2: Enrichment layer + reference data handling
- Phase 3: Full pipeline orchestration + quality reporting
- Phase 4: Docker support + scheduling

### Domain Focus
**Customer Data** (CRM, marketing, support, sales touchpoints)

---

*Part of a 4-project Data Engineering portfolio.*