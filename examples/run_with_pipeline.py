"""
Example using the new Pipeline runner.

This is the recommended way to run the pipeline going forward.

Usage:
    python examples/run_with_pipeline.py
"""

from pathlib import Path

from loguru import logger

from src.pipeline import run_pipeline


def main():
    logger.info("Running pipeline using the new orchestration layer")

    config_path = Path("config/dev.yaml")
    report = run_pipeline(config_path)

    print("\n" + "="*60)
    print("FINAL CLEANING REPORT")
    print("="*60)
    print(report.summary())

    logger.success("Pipeline execution completed using Pipeline runner")


if __name__ == "__main__":
    main()
