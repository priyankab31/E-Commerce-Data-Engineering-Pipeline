
import pandas as pd
import pytest

from src.data_quality import (
    check_required_columns,
    check_duplicates,
    check_missing_values
)


def test_required_columns_pass():
    df = pd.DataFrame({
        "customer_id": ["C001"],
        "email": ["test@example.com"]
    })

    check_required_columns(
        df,
        ["customer_id", "email"],
        "customers"
    )


def test_missing_required_column_fails():
    df = pd.DataFrame({
        "customer_id": ["C001"]
    })

    with pytest.raises(ValueError):
        check_required_columns(
            df,
            ["customer_id", "email"],
            "customers"
        )


def test_duplicate_detection():
    df = pd.DataFrame({
        "customer_id": ["C001", "C001", "C002"]
    })

    assert check_duplicates(
        df,
        "customer_id",
        "customers"
    ) == 1


def test_missing_value_detection():
    df = pd.DataFrame({
        "customer_id": ["C001", None],
        "email": ["test@example.com", None]
    })

    result = check_missing_values(df, "customers")

    assert result["customer_id"] == 1
    assert result["email"] == 1

