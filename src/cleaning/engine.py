from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pandas as pd
from loguru import logger

from src.config.models import CleaningConfig, CleaningRuleConfig
from src.cleaning.transformations import get_transformation_function


@dataclass
class CleaningReport:
    """Summary report of cleaning operations."""
    rows_before: int
    rows_after: int
    columns_changed: dict[str, int] = field(default_factory=dict)  # column -> number of values changed
    transformations_applied: list[str] = field(default_factory=list)
    
    @property
    def rows_removed(self) -> int:
        return self.rows_before - self.rows_after
    
    def summary(self) -> str:
        lines = [
            f"Rows before: {self.rows_before}",
            f"Rows after:  {self.rows_after} (removed: {self.rows_removed})",
        ]
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
    
    Returns:
        (cleaned_dataframe, CleaningReport)
    """
    report = CleaningReport(
        rows_before=len(df),
        rows_after=len(df)
    )
    
    if not cleaning_config.enabled:
        logger.info("Cleaning is disabled in config.")
        return df, report

    cleaned_df = df.copy()
    original_values = {}  # Track original values for comparison
    
    for rule in cleaning_config.rules:
        column = rule.column
        if column not in cleaned_df.columns:
            logger.warning(f"Column '{column}' not found. Skipping.")
            continue
        
        # Store original values for change tracking
        original_values[column] = cleaned_df[column].copy()
        
        cleaned_df = _apply_single_rule(cleaned_df, rule)
        
        # Count how many values changed in this column
        if column in original_values:
            changed_mask = original_values[column] != cleaned_df[column]
            changed_count = changed_mask.sum()
            if changed_count > 0:
                report.columns_changed[column] = int(changed_count)
            
        for t in rule.transformations:
            report.transformations_applied.append(f"{column}:{t}")
    
    report.rows_after = len(cleaned_df)
    
    logger.success(f"Cleaning complete. {report.rows_removed} rows removed.")
    return cleaned_df, report


def _apply_single_rule(df: pd.DataFrame, rule: CleaningRuleConfig) -> pd.DataFrame:
    column = rule.column
    
    if column not in df.columns:
        return df
    
    series = df[column]
    
    for transformation_name in rule.transformations:
        try:
            func = get_transformation_function(transformation_name)
            params = rule.parameters or {}
            
            # Handle DataFrame-level operations
            if transformation_name == "remove_duplicates":
                df = func(df, subset=params.get("subset"), **params)
            else:
                series = func(series, **params)
                df[column] = series
                
        except Exception as e:
            logger.error(f"Failed to apply '{transformation_name}' on '{column}': {e}")
    
    return df
