from __future__ import annotations

import pandas as pd
from loguru import logger

from src.config.models import CleaningConfig, CleaningRuleConfig
from src.cleaning.transformations import get_transformation_function


def apply_cleaning_rules(
    df: pd.DataFrame, 
    cleaning_config: CleaningConfig
) -> pd.DataFrame:
    """
    Apply all cleaning rules defined in the configuration.
    
    This is the main entry point for the cleaning module.
    """
    if not cleaning_config.enabled:
        logger.info("Cleaning is disabled in config. Returning original DataFrame.")
        return df

    cleaned_df = df.copy()
    
    for rule in cleaning_config.rules:
        cleaned_df = _apply_single_rule(cleaned_df, rule)
    
    logger.success(f"Applied {len(cleaning_config.rules)} cleaning rule(s)")
    return cleaned_df


def _apply_single_rule(df: pd.DataFrame, rule: CleaningRuleConfig) -> pd.DataFrame:
    """Apply a single cleaning rule to the DataFrame."""
    column = rule.column
    
    if column not in df.columns:
        logger.warning(f"Column '{column}' not found in DataFrame. Skipping rule.")
        return df
    
    series = df[column]
    
    for transformation_name in rule.transformations:
        try:
            func = get_transformation_function(transformation_name)
            
            # Pass parameters if the function supports them
            if transformation_name == "handle_missing_values":
                params = rule.parameters or {}
                series = func(series, **params)
            else:
                series = func(series)
            
            logger.debug(f"Applied '{transformation_name}' on column '{column}'")
            
        except Exception as e:
            logger.error(f"Failed to apply '{transformation_name}' on '{column}': {e}")
            
    df[column] = series
    return df
