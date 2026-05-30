# Examples

This folder contains runnable examples for the customer data pipeline.

## Available Examples

### 1. Basic Cleaning Example

**File:** `run_cleaning_example.py`

**What it does:**
- Loads the development configuration
- Reads messy sample customer data
- Applies cleaning rules defined in the YAML config
- Shows before/after comparison
- Saves output as Parquet

**How to run:**

```bash
# From the root of the project
python examples/run_cleaning_example.py
```

**Expected Output:**
You will see the raw data, the cleaned data, and confirmation that the file was saved.

## Sample Data

The file `data/raw/sample_customers.csv` contains intentionally messy customer data with:
- Extra whitespace
- Mixed case text
- Phone numbers in different formats
- Missing values
- Duplicate records

This makes it perfect for testing the cleaning transformations.
