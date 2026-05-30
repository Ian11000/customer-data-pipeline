from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd
from loguru import logger

from src.config.models import CleaningConfig, CleaningRuleConfig
from src.cleaning.transformations import (
    get_transformation_function,
    is_dataframe_level_transformation,
)


@dataclass
class CleaningReport:
    """Summary report of cleaning operations."""
    rows_before: int
    rows_after: int
    columns_changed: dict[str, int] = field(default_factory=dict)
    transformations_applied: list[str] = field(default_factory=list)
    rows_removed_by_dedup: int = 0
    
    @property
    def rows_removed(self) -> int:
        return self.rows_before - self.rows_after
    
    def summary(self) -> str:
        lines = [
            f"Rows before: {self.rows_before}",
            f"Rows after:  {self.rows_after} (removed: {self.rows_removed})",
        ]
        if self.rows_removed_by_dedup > 0:
            lines.append(f"  - of which {self.rows_removed_by_dedup} removed by deduplication")
        
        if self.columns_changed:
            lines.append("\nValues changed per column:")
            for col, count in self.columns_changed.items():
                lines.append(f"  - {col}: {count} values modified")
        
        if self.transformations_applied:
            lines.append(f"\nTransformations applied: {len(self.transformations_applied)}")
        
        return "\n".join(lines)


def apply_cleaning_rules(
    df: pd.DataFrame, 
    cleaning_config: CleaningConfig
) -> tuple[pd.DataFrame, CleaningReport]:
    """
    Apply cleaning rules and return both the cleaned DataFrame and a report.
    """
    report = CleaningReport(
        rows_before=len(df),
        rows_after=len(df)
    )
    
    if not cleaning_config.enabled:
        logger.info("Cleaning is disabled in config.")
        return df, report

    cleaned_df = df.copy()
    original_values = {}
    
    for rule in cleaning_config.rules:
        column = rule.column
        
        for transformation_name in rule.transformations:
            try:
                func = get_transformation_function(transformation_name)
                params = rule.parameters or {}
                
                if is_dataframe_level_transformation(transformation_name):
                    # DataFrame-level operation (e.g. remove_duplicates)
                    before_len = len(cleaned_df)
                    cleaned_df = func(cleaned_df, subset=params.get("subset"), **params)
                    removed = before_len - len(cleaned_df)
                    report.rows_removed_by_dedup += removed
                    report.transformations_applied.append(f"{transformation_name}")
                else:
                    if column not in cleaned_df.columns:
                        logger.warning(f"Column '{column}' not found. Skipping transformation '{transformation_name}'.")
                        continue
                    
                    # Track original for change counting
                    if column not in original_values:
                        original_values[column] = cleaned_df[column].copy()
                    
                    series = cleaned_df[column]
                    series = func(series, **params)
                    cleaned_df[column] = series
                    
                    # Count changes
                    changed_mask = original_values[column] != cleaned_df[column]
                    changed_count = changed_mask.sum()
                    if changed_count > 0:
                        report.columns_changed[column] = report.columns_changed.get(column, 0) + int(changed_count)
                    
                    report.transformations_applied.append(f"{column}:{transformation_name}")
                    
            except Exception as e:
                logger.error(f"Failed to apply '{transformation_name}' on '{column}': {e}")
    
    report.rows_after = len(cleaned_df)
    
    logger.success(f"Cleaning complete. {report.rows_removed} rows removed.")
    return cleaned_df, report
