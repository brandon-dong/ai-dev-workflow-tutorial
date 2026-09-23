"""Load the ShopSmart sales CSV and calculate the numbers the dashboard shows.

Every calculation takes the sales DataFrame and returns a plain number or a
small DataFrame. Nothing here uses Streamlit, so pytest can test it directly.
"""

from pathlib import Path

import pandas as pd

# The CSV sits in the data/ folder next to this file. Building the path from
# this file's location means loading works whichever folder the app starts in.
DEFAULT_DATA_PATH = Path(__file__).parent / "data" / "sales-data.csv"

REQUIRED_COLUMNS = [
    "date",
    "order_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "total_amount",
]
NUMERIC_COLUMNS = ["quantity", "unit_price", "total_amount"]


def load_sales_data(path=DEFAULT_DATA_PATH):
    """Read the sales CSV, check it, and convert dates and numbers.

    Raises ValueError, naming the problem column, if a column is missing,
    a cell is blank, a date isn't YYYY-MM-DD, or a number isn't numeric.
    """
    df = pd.read_csv(path)

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Sales data is missing columns: {', '.join(missing)}")

    blank = [column for column in REQUIRED_COLUMNS if df[column].isna().any()]
    if blank:
        raise ValueError(f"Sales data has blank values in: {', '.join(blank)}")

    try:
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    except ValueError as error:
        raise ValueError(f"Sales data has a date that isn't YYYY-MM-DD: {error}") from error

    for column in NUMERIC_COLUMNS:
        try:
            df[column] = pd.to_numeric(df[column])
        except ValueError as error:
            raise ValueError(f"Sales data column {column} has a non-numeric value: {error}") from error

    return df


def total_sales(df):
    """Sum of every order amount, in dollars."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Number of distinct orders. An order ID on several rows counts once."""
    return int(df["order_id"].nunique())
