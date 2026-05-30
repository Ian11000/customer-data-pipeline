from __future__ import annotations

import re
from typing import Any

import pandas as pd
import numpy as np


def lower_case(series: pd.Series, **kwargs) -> pd.Series:
    """Convert text to lowercase."""
    return series.astype(str).str.lower()


def upper_case(series: pd.Series, **kwargs) -> pd.Series:
    """Convert text to uppercase."""
    return series.astype(str).str.upper()


def strip_whitespace(series: pd.Series, **kwargs) -> pd.Series:
    """Remove leading and trailing whitespace."""
    return series.astype(str).str.strip()


def remove_non_digits(series: pd.Series, **kwargs) -> pd.Series:
    """Keep only digits (useful for phone numbers, IDs, etc.)."""
    return series.astype(str).str.replace(r"\D", "", regex=True)


def remove_special_chars(series: pd.Series, **kwargs) -> pd.Series:
    """Remove common special characters, keeping letters, numbers and spaces."""
    return series.astype(str).str.replace(r"[^a-zA-Z0-9\s]", "", regex=True)


def standardize_email(series: pd.Series, **kwargs) -> pd.Series:
    """Basic email standardization (lowercase + strip)."""
    return series.astype(str).str.lower().str.strip()


def standardize_date(
    series: pd.Series, 
    format: str = "auto",
    errors: str = "coerce",
    **kwargs
) -> pd.Series:
    """
    Convert column to datetime.
    
    Args:
        format: 'auto' to let pandas infer, or specific strftime format.
        errors: 'coerce', 'raise', or 'ignore'
    """
    if format == "auto":
        return pd.to_datetime(series, errors=errors)
    else:
        return pd.to_datetime(series, format=format, errors=errors)


def clip_outliers(
    series: pd.Series, 
    method: str = "iqr",
    factor: float = 1.5,
    **kwargs
) -> pd.Series:
    """
    Clip outliers using IQR method.
    
    Args:
        method: Currently only 'iqr' supported
        factor: IQR multiplier (default 1.5)
    """
    if not pd.api.types.is_numeric_dtype(series):
        return series
    
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    
    return series.clip(lower=lower, upper=upper)


def handle_missing_values(
    series: pd.Series, 
    strategy: str = "fill", 
    fill_value: Any = None,
    **kwargs
) -> pd.Series:
    """
    Handle missing values.
    
    Strategies:
        - 'fill': fill with fill_value
        - 'drop': drop rows (note: affects whole DataFrame when used in engine)
        - 'mean', 'median', 'mode'
    """
    if strategy == "drop":
        return series.dropna()
    
    if strategy == "mean" and pd.api.types.is_numeric_dtype(series):
        return series.fillna(series.mean())
    
    if strategy == "median" and pd.api.types.is_numeric_dtype(series):
        return series.fillna(series.median())
    
    if strategy == "mode":
        mode_val = series.mode()
        if not mode_val.empty:
            return series.fillna(mode_val[0])
    
    return series.fillna(fill_value)


def remove_duplicates(df: pd.DataFrame, subset: list[str] | None = None, **kwargs) -> pd.DataFrame:
    """Remove duplicate rows. This is a DataFrame-level operation."""
    return df.drop_duplicates(subset=subset, keep="first")


def get_transformation_function(name: str):
    """Registry of available transformations."""
    registry = {
        "lower_case": lower_case,
        "upper_case": upper_case,
        "strip_whitespace": strip_whitespace,
        "remove_non_digits": remove_non_digits,
        "remove_special_chars": remove_special_chars,
        "standardize_email": standardize_email,
        "standardize_date": standardize_date,
        "clip_outliers": clip_outliers,
        "handle_missing_values": handle_missing_values,
    }
    
    if name not in registry:
        raise ValueError(f"Unknown transformation: '{name}'. Available: {list(registry.keys())}")
    
    return registry[name]
