"""ShopSmart Sales Dashboard.

Run with:  streamlit run app.py

All numbers come from data.py. This file only lays out the page and draws
the charts.
"""

import streamlit as st

from data import load_sales_data

# --- Page setup ------------------------------------------------------------
st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")


@st.cache_data
def get_sales_data():
    """Load the CSV once and reuse it each time the page reruns."""
    return load_sales_data()


# --- Load data -------------------------------------------------------------
# If the file is missing or broken, show a readable message instead of a traceback.
try:
    sales = get_sales_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Could not load the sales data: {error}")
    st.stop()
