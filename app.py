"""ShopSmart Sales Dashboard.

Run with:  streamlit run app.py

All numbers come from data.py. This file only lays out the page and draws
the charts.
"""

import plotly.express as px
import streamlit as st

from data import load_sales_data, sales_by_month, total_orders, total_sales

# One color for every chart keeps the page consistent.
ACCENT_COLOR = "#1f77b4"

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


# --- KPI cards -------------------------------------------------------------
sales_column, orders_column = st.columns(2)
sales_column.metric("Total Sales", f"${total_sales(sales):,.0f}")
orders_column.metric("Total Orders", f"{total_orders(sales):,}")


# --- Sales trend -----------------------------------------------------------
trend_chart = px.line(
    sales_by_month(sales),
    x="month",
    y="sales",
    markers=True,
    title="Sales Trend by Month",
    labels={"month": "Month", "sales": "Sales"},
    color_discrete_sequence=[ACCENT_COLOR],
)
trend_chart.update_xaxes(tickformat="%b %Y", dtick="M1")
trend_chart.update_yaxes(tickprefix="$", tickformat=",.0f")
trend_chart.update_traces(hovertemplate="%{x|%b %Y}<br>$%{y:,.2f}<extra></extra>")
st.plotly_chart(trend_chart, width="stretch")
