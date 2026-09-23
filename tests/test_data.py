"""Tests for data.py.

Two kinds of test:
- small hand-made data, where you can check the answer by hand
- the real CSV, to confirm the numbers the PRD expects
"""

import pandas as pd
import pytest

from data import (
    load_sales_data,
    sales_by_category,
    sales_by_month,
    sales_by_region,
    total_orders,
    total_sales,
)

HEADER = "date,order_id,product,category,region,quantity,unit_price,total_amount"
GOOD_ROW = "2024-01-05,ORD-1,Laptop,Electronics,North,1,100.00,100.00"


def write_csv(tmp_path, *lines):
    """Write the given lines to a CSV file in a temporary folder and return its path."""
    path = tmp_path / "sales.csv"
    path.write_text("\n".join(lines) + "\n")
    return path


@pytest.fixture
def small_sales():
    """Five hand-made rows covering 2 months, 3 categories and 3 regions.

    ORD-2 appears on two rows, like one order containing two products.
    Hand-worked answers:
      total sales   = 100 + 50 + 50 + 200 + 20 = 420
      total orders  = 4 (ORD-1, ORD-2, ORD-3, ORD-4)
      by month      = Jan 200, Feb 220
      by category   = Electronics 300, Audio 70, Accessories 50
      by region     = East 200, North 120, South 100
    """
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2024-01-05", "2024-01-20", "2024-01-20", "2024-02-10", "2024-02-15"]
            ),
            "order_id": ["ORD-1", "ORD-2", "ORD-2", "ORD-3", "ORD-4"],
            "product": ["Laptop", "Earbuds", "Phone Case", "Laptop", "Speaker"],
            "category": ["Electronics", "Audio", "Accessories", "Electronics", "Audio"],
            "region": ["North", "South", "South", "East", "North"],
            "quantity": [1, 2, 1, 1, 1],
            "unit_price": [100.0, 25.0, 50.0, 200.0, 20.0],
            "total_amount": [100.0, 50.0, 50.0, 200.0, 20.0],
        }
    )


@pytest.fixture(scope="module")
def real_sales():
    """The real CSV, loaded once for all the tests that use it."""
    return load_sales_data()


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


# --- KPIs ------------------------------------------------------------------


def test_total_sales_adds_every_amount(small_sales):
    assert total_sales(small_sales) == 420.0


def test_total_orders_counts_each_order_once(small_sales):
    # 5 rows, but ORD-2 is on two of them.
    assert total_orders(small_sales) == 4


def test_real_data_kpis(real_sales):
    assert total_sales(real_sales) == pytest.approx(116500.21)
    assert total_orders(real_sales) == 482


# --- Sales by month --------------------------------------------------------


def test_sales_by_month_totals_each_month(small_sales):
    result = sales_by_month(small_sales)

    assert list(result.columns) == ["month", "sales"]
    assert list(result["month"]) == [pd.Timestamp("2024-01-01"), pd.Timestamp("2024-02-01")]
    assert list(result["sales"]) == [200.0, 220.0]


def test_sales_by_month_orders_across_year_boundary():
    # January 2024 is listed first in the data, but December 2023 comes first in time.
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-10", "2023-12-20"]),
            "total_amount": [10.0, 30.0],
        }
    )

    result = sales_by_month(df)

    assert list(result["month"]) == [pd.Timestamp("2023-12-01"), pd.Timestamp("2024-01-01")]
    assert list(result["sales"]) == [30.0, 10.0]


def test_real_data_has_12_months(real_sales):
    result = sales_by_month(real_sales)

    assert len(result) == 12
    assert result["month"].iloc[0] == pd.Timestamp("2024-01-01")
    assert result["sales"].iloc[0] == pytest.approx(7175.17)
    assert result["month"].iloc[-1] == pd.Timestamp("2024-12-01")
    assert result["sales"].iloc[-1] == pytest.approx(15186.34)


# --- Sales by category and region ------------------------------------------


def test_sales_by_category_is_sorted_largest_first(small_sales):
    result = sales_by_category(small_sales)

    assert list(result.columns) == ["category", "sales"]
    assert list(result["category"]) == ["Electronics", "Audio", "Accessories"]
    assert list(result["sales"]) == [300.0, 70.0, 50.0]


def test_sales_by_region_is_sorted_largest_first(small_sales):
    result = sales_by_region(small_sales)

    assert list(result.columns) == ["region", "sales"]
    assert list(result["region"]) == ["East", "North", "South"]
    assert list(result["sales"]) == [200.0, 120.0, 100.0]


def test_real_data_categories(real_sales):
    result = sales_by_category(real_sales)

    assert list(result["category"]) == [
        "Electronics",
        "Wearables",
        "Audio",
        "Smart Home",
        "Accessories",
    ]
    assert result["sales"].iloc[0] == pytest.approx(42683.67)


def test_real_data_regions(real_sales):
    result = sales_by_region(real_sales)

    assert list(result["region"]) == ["North", "West", "East", "South"]
    assert result["sales"].iloc[0] == pytest.approx(38857.24)
