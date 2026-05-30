# Roadmap - customer-data-pipeline

## Phase 1: Foundation
- [x] Configuration system using Pydantic + YAML
- [x] Basic cleaning transformation functions
- [x] Cleaning engine with change tracking + summary reports
- [ ] Core pipeline runner (orchestration)
- [ ] Unit tests for cleaning functions
- [ ] Support for DataFrame-level operations in config

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
