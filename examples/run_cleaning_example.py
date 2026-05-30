"""
Working Example: Customer Data Cleaning Pipeline

This script demonstrates how to use the configuration system + cleaning engine
with real (sample) data.

Run it from the project root:
    python examples/run_cleaning_example.py
"""

from pathlib import Path

import pandas as pd
from loguru import logger

from src.config import load_config
from src.cleaning import apply_cleaning_rules


def main():
    logger.info("Starting Customer Data Cleaning Example")

    # 1. Load configuration
    config_path = Path("config/dev.yaml")
    logger.info(f"Loading configuration from {config_path}")
    config = load_config(config_path)

    # 2. Load sample (messy) data
    input_path = Path("data/raw/sample_customers.csv")
    logger.info(f"Loading sample data from {input_path}")
    df = pd.read_csv(input_path)

    print("\n" + "="*60)
    print("RAW DATA (Before Cleaning)")
    print("="*60)
    print(df.to_string())
    print(f"\nShape: {df.shape}")

    # 3. Apply cleaning rules from config
    logger.info("Applying cleaning rules from configuration...")
    cleaned_df = apply_cleaning_rules(df, config.cleaning)

    print("\n" + "="*60)
    print("CLEANED DATA (After Cleaning)")
    print("="*60)
    print(cleaned_df.to_string())
    print(f"\nShape: {cleaned_df.shape}")

    # 4. Save output
    output_path = Path("data/processed/sample_customers_cleaned.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_parquet(output_path, index=False)
    logger.success(f"Cleaned data saved to {output_path}")

    logger.info("Example completed successfully!")


if __name__ == "__main__":
    main()
