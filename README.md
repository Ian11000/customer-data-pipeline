## customer-data-pipeline

**Advanced Python Data Cleaning & Enrichment Pipeline** focused on Customer data.

### Current Status

- Configuration system (Pydantic + YAML) — **Completed**
- Core cleaning transformations + reporting — **Completed**
- **Core Pipeline Runner / Orchestration** — **Completed**

### Overview
This project demonstrates a modular, production-style data pipeline for cleaning and enriching customer-related datasets.

### Key Features (Implemented so far)
- YAML + Pydantic configuration system
- Configurable cleaning rules with rich transformations
- Change tracking and detailed cleaning reports
- Support for both column-level and DataFrame-level operations (e.g. deduplication)
- Clean orchestration layer (`Pipeline` class)

### Tech Stack
- Python 3.11+
- Pandas / Polars
- Pydantic v2
- Loguru

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run using the new Pipeline runner (recommended)
python examples/run_with_pipeline.py

# Or run the older direct example
python examples/run_cleaning_example.py
```

### Project Structure
```
customer-data-pipeline/
├── src/
│   ├── config/          # Configuration system
│   ├── cleaning/        # Cleaning transformations + engine
│   ├── pipeline/        # Main orchestration layer
│   └── utils/
├── config/              # YAML configuration files
├── data/
├── examples/
├── tests/
└── docs/
```

### Running the Pipeline

The recommended way is using the orchestration layer:

```bash
python examples/run_with_pipeline.py
```

### Roadmap
See [docs/ROADMAP.md](docs/ROADMAP.md) for detailed next steps.

### Domain Focus
**Customer Data** (CRM, marketing, support, sales touchpoints)

---

*Part of a 4-project Data Engineering portfolio.*
