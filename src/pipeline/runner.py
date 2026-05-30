from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
from loguru import logger

from src.config import load_config, CustomerPipelineConfig
from src.cleaning import apply_cleaning_rules, CleaningReport


class Pipeline:
    """
    Main orchestration class for the customer data pipeline.
    
    This class coordinates:
    - Loading configuration
    - Loading data
    - Cleaning (current)
    - Enrichment (future)
    - Saving output
    """

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config: Optional[CustomerPipelineConfig] = None
        self.df: Optional[pd.DataFrame] = None
        self.report: Optional[CleaningReport] = None

        logger.info(f"Initializing pipeline with config: {self.config_path}")

    def run(self) -> CleaningReport:
        """
        Execute the full pipeline.
        
        Returns:
            CleaningReport with details of what was done.
        """
        logger.info("Starting pipeline run")
        
        self._load_config()
        self._load_data()
        self._clean()
        self._save_output()
        
        logger.success("Pipeline run completed successfully")
        return self.report

    def _load_config(self) -> None:
        self.config = load_config(self.config_path)
        logger.debug(f"Loaded configuration for pipeline: {self.config.pipeline.name}")

    def _load_data(self) -> None:
        if self.config is None:
            raise RuntimeError("Config not loaded")

        # For now we support only the first data source (customers)
        # This will be expanded when we support multiple sources
        source_key = list(self.config.data_sources.keys())[0]
        source_config = self.config.data_sources[source_key]

        logger.info(f"Loading data from {source_config.path} (type={source_config.type})")

        if source_config.type == "csv":
            self.df = pd.read_csv(
                source_config.path,
                delimiter=source_config.delimiter,
                encoding=source_config.encoding,
            )
        else:
            raise NotImplementedError(f"Data source type '{source_config.type}' not supported yet")

        logger.info(f"Loaded {len(self.df)} rows")

    def _clean(self) -> None:
        if self.df is None or self.config is None:
            raise RuntimeError("Data or config not loaded")

        logger.info("Running cleaning step...")
        self.df, self.report = apply_cleaning_rules(self.df, self.config.cleaning)

    def _save_output(self) -> None:
        if self.df is None or self.config is None or self.report is None:
            raise RuntimeError("Pipeline state incomplete")

        output_config = self.config.output
        output_path = Path(output_config.path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Saving output to {output_path} (format={output_config.format})")

        if output_config.format == "parquet":
            self.df.to_parquet(output_path, index=False)
        elif output_config.format == "csv":
            self.df.to_csv(output_path, index=False)
        else:
            raise NotImplementedError(f"Output format '{output_config.format}' not supported yet")

        logger.success(f"Output saved successfully ({len(self.df)} rows)")


def run_pipeline(config_path: str | Path) -> CleaningReport:
    """
    Convenience function to run the pipeline with a single call.
    
    Args:
        config_path: Path to the YAML configuration file
    
    Returns:
        CleaningReport
    """
    pipeline = Pipeline(config_path)
    return pipeline.run()
