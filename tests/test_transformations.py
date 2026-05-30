import pandas as pd
import pytest

from src.cleaning.transformations import (
    lower_case,
    strip_whitespace,
    remove_non_digits,
    standardize_email,
    handle_missing_values,
    standardize_date,
    clip_outliers,
    remove_duplicates,
)


def test_lower_case():
    s = pd.Series(["Hello", "WORLD", "TeSt"])
    result = lower_case(s)
    assert list(result) == ["hello", "world", "test"]


def test_strip_whitespace():
    s = pd.Series(["  hello  ", "world ", " test"])
    result = strip_whitespace(s)
    assert list(result) == ["hello", "world", "test"]


def test_remove_non_digits():
    s = pd.Series(["+1 (555) 123-4567", "abc123", "555.987.6543"])
    result = remove_non_digits(s)
    assert list(result) == ["15551234567", "123", "5559876543"]


def test_standardize_email():
    s = pd.Series(["  JOHN.DOE@GMAIL.COM ", "Jane.Smith@Yahoo.com"])
    result = standardize_email(s)
    assert list(result) == ["john.doe@gmail.com", "jane.smith@yahoo.com"]


def test_handle_missing_values_fill():
    s = pd.Series([1, None, 3, None])
    result = handle_missing_values(s, strategy="fill", fill_value=0)
    assert list(result) == [1, 0, 3, 0]


def test_handle_missing_values_mean():
    s = pd.Series([10, None, 30, 50])
    result = handle_missing_values(s, strategy="mean")
    assert list(result) == [10, 30.0, 30, 50]


def test_standardize_date_auto():
    s = pd.Series(["2024-01-15", "15/02/2024", None])
    result = standardize_date(s, errors="coerce")
    assert pd.api.types.is_datetime64_any_dtype(result)
    assert pd.isna(result.iloc[2])


def test_clip_outliers_iqr():
    s = pd.Series([10, 12, 11, 100, 13, 9])
    result = clip_outliers(s, method="iqr", factor=1.5)
    # 100 should be clipped down
    assert result.max() < 100
    assert result.min() >= 9


def test_remove_duplicates():
    df = pd.DataFrame({
        "id": [1, 2, 1, 3],
        "name": ["A", "B", "A", "C"]
    })
    result = remove_duplicates(df, subset=["id"])
    assert len(result) == 3
    assert list(result["id"]) == [1, 2, 3]


def test_remove_duplicates_no_subset():
    df = pd.DataFrame({
        "id": [1, 2, 1, 3],
        "name": ["A", "B", "A", "C"]
    })
    result = remove_duplicates(df)
    assert len(result) == 3
