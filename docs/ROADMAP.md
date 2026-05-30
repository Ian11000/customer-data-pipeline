# Roadmap - customer-data-pipeline

## Phase 1: Foundation
- [x] Configuration system using Pydantic + YAML
- [x] Basic cleaning transformation functions
- [x] Cleaning engine with change tracking + summary reports
- [x] Support for DataFrame-level operations (e.g. remove_duplicates)
- [x] Unit tests for cleaning transformations
- [x] Core pipeline runner / orchestration layer
- [ ] Add CLI entry point (e.g. `python -m src.pipeline`)
- [ ] Improve logging and observability

## Phase 2: Enrichment
- Reference data joins
- External API enrichment
- Fuzzy matching for customer records

## Phase 3: Pipeline & Quality
- End-to-end pipeline orchestration
- Data quality scoring framework
- Detailed audit reports

## Phase 4: Production Readiness
- Docker support
- Scheduling
- Monitoring and alerting
