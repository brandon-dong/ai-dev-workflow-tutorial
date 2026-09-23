"""Tests for data.py.

Two kinds of test:
- small hand-made data, where you can check the answer by hand
- the real CSV, to confirm the numbers the PRD expects
"""

import pandas as pd
import pytest

from data import load_sales_data

HEADER = "date,order_id,product,category,region,quantity,unit_price,total_amount"
GOOD_ROW = "2024-01-05,ORD-1,Laptop,Electronics,North,1,100.00,100.00"


def write_csv(tmp_path, *lines):
    """Write the given lines to a CSV file in a temporary folder and return its path."""
    path = tmp_path / "sales.csv"
    path.write_text("\n".join(lines) + "\n")
    return path


# --- Loading ---------------------------------------------------------------


def test_load_converts_dates_and_numbers(tmp_path):
    df = load_sales_data(write_csv(tmp_path, HEADER, GOOD_ROW))

    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df.loc[0, "date"] == pd.Timestamp("2024-01-05")
    assert df.loc[0, "total_amount"] == 100.0
    assert df.loc[0, "quantity"] == 1


def test_load_rejects_missing_column(tmp_path):
    header_without_region = "date,order_id,product,category,quantity,unit_price,total_amount"
    row_without_region = "2024-01-05,ORD-1,Laptop,Electronics,1,100.00,100.00"
    path = write_csv(tmp_path, header_without_region, row_without_region)

    with pytest.raises(ValueError, match="region"):
        load_sales_data(path)


def test_load_rejects_blank_value(tmp_path):
    row_with_blank_amount = "2024-01-05,ORD-1,Laptop,Electronics,North,1,100.00,"
    path = write_csv(tmp_path, HEADER, row_with_blank_amount)

    with pytest.raises(ValueError, match="total_amount"):
        load_sales_data(path)


def test_load_rejects_bad_date(tmp_path):
    row_with_us_date = "01/05/2024,ORD-1,Laptop,Electronics,North,1,100.00,100.00"
    path = write_csv(tmp_path, HEADER, row_with_us_date)

    with pytest.raises(ValueError, match="date"):
        load_sales_data(path)


def test_load_rejects_non_numeric_amount(tmp_path):
    row_with_dollar_sign = "2024-01-05,ORD-1,Laptop,Electronics,North,1,100.00,$100.00"
    path = write_csv(tmp_path, HEADER, row_with_dollar_sign)

    with pytest.raises(ValueError, match="total_amount"):
        load_sales_data(path)


def test_load_works_from_another_folder(tmp_path, monkeypatch):
    # Streamlit may be started from any folder; the default path must not depend on it.
    monkeypatch.chdir(tmp_path)

    assert len(load_sales_data()) == 482


def test_real_data_has_all_482_records():
    assert len(load_sales_data()) == 482
