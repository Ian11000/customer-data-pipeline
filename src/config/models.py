from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class DataSourceConfig(BaseModel):
    type: Literal["csv", "excel", "parquet", "json", "database"]
    path: str
    delimiter: str = ","
    sheet_name: Optional[str] = None  # For Excel
    encoding: str = "utf-8"


class ReferenceDataConfig(BaseModel):
    name: str
    path: str
    type: Literal["csv", "excel", "parquet"] = "csv"


class CleaningRuleConfig(BaseModel):
    column: str
    transformations: list[str] = Field(default_factory=list)
    parameters: dict = Field(default_factory=dict)


class CleaningConfig(BaseModel):
    enabled: bool = True
    rules: list[CleaningRuleConfig] = Field(default_factory=list)


class EnrichmentSourceConfig(BaseModel):
    name: str
    type: Literal["reference", "api", "database"]
    config: dict = Field(default_factory=dict)


class EnrichmentConfig(BaseModel):
    enabled: bool = False
    sources: list[EnrichmentSourceConfig] = Field(default_factory=list)


class OutputConfig(BaseModel):
    format: Literal["csv", "parquet", "excel", "json"] = "parquet"
    path: str
    partition_by: Optional[list[str]] = None


class PipelineConfig(BaseModel):
    name: str
    version: str = "0.1.0"
    environment: Literal["dev", "test", "prod"] = "dev"


class CustomerPipelineConfig(BaseModel):
    pipeline: PipelineConfig
    data_sources: dict[str, DataSourceConfig]
    reference_data: list[ReferenceDataConfig] = Field(default_factory=list)
    cleaning: CleaningConfig = Field(default_factory=CleaningConfig)
    enrichment: EnrichmentConfig = Field(default_factory=EnrichmentConfig)
    output: OutputConfig

    class Config:
        extra = "forbid"
