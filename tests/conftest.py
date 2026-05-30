import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    """Sample messy DataFrame for testing cleaning functions."""
    data = {
        "full_name": ["  John Doe ", "jane smith", "  ROBERT JOHNSON  ", "Jane Smith"],
        "email": ["JOHN.DOE@GMAIL.COM", " jane.smith@yahoo.com ", "robert@outlook.com", "jane.smith@yahoo.com"],
        "phone_number": ["+1 (555) 123-4567", "555.987.6543", "(555) 222-3333", "555.987.6543"],
        "age": [25, 150, 32, 28],  # 150 is an outlier
        "signup_date": ["2024-01-15", "15/02/2024", "2024-03-10", "2024-01-15"],
    }
    return pd.DataFrame(data)
