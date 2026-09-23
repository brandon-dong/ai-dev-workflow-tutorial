# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan part by part. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a one-page Streamlit dashboard showing ShopSmart's total sales, total orders, monthly sales trend, and sales by category and region from `data/sales-data.csv`.

**Architecture:** Two modules. `data.py` loads and validates the CSV and holds one small, pure calculation function per number or table the page shows. It never imports Streamlit, and pytest tests it. `app.py` lays out the page top to bottom and draws the Plotly charts from what `data.py` returns.

**Tech Stack:** Python 3.12, Streamlit, Pandas, Plotly Express, pytest. Plain `venv/` with a pinned `requirements.txt`.

**Spec:** `docs/superpowers/specs/2026-09-22-sales-dashboard-design.md`

### How this plan is numbered

- The plan is split into **Parts 1–7**. Parts are this plan's own numbering.
- Each Part is labeled with the `TASKS.md` milestone it delivers, e.g. **Part 3 → Milestone TASK-3**. Every commit message starts with that milestone ID.
- Part 7 (**TASK-7, deployment**) is **the developer's to execute**. The implementation work stops at the end of Part 6 and hands off.
- Updating the `TASKS.md` board (moving milestones between sections, ticking criteria, filling in `Commit:` lines) and pushing to GitHub are also the developer's. The plan doesn't edit `TASKS.md` or push.

## Global Constraints

- Work on the existing branch `feature/sales-dashboard`. Do not create a git worktree or a new branch.
- Virtual environment: plain `python -m venv venv` in the project root. No uv, conda, Pipfile or pyproject.toml.
- Dependencies are listed and pinned in `requirements.txt` only: `streamlit==1.64.0`, `pandas==3.0.6`, `plotly==7.1.0`, `pytest==9.1.1`.
- Python 3.11+ (the local machine has 3.12).
- `data.py` must not import Streamlit. Formatting for display (`$`, thousands separators) lives in `app.py`, not `data.py`.
- Page title and heading: `ShopSmart Sales Dashboard`.
- Trend chart is monthly (12 points for the current data).
- Styling: Streamlit defaults, one shared accent color, a title and axis labels on every chart, `$` on money axes and tooltips, wide layout. No custom CSS, no `.streamlit/config.toml`.
- Phase 2 features (filters, date ranges, exports, auth, drill-down) are out of scope.
- Every commit message starts with the milestone ID, e.g. `TASK-3: ...`.
- Code stays simple: short functions, a docstring on each function, a comment heading each section of `app.py`.

## Review Focus

These are inputs the spec implies but doesn't spell out. Each one gets a test in the Part that owns the code.

1. **App started from a different folder** (or by Streamlit Cloud's runner): the CSV still loads, because its path is resolved relative to `data.py`, not the current folder. Test: `test_load_works_from_another_folder` (Part 2).
2. **A money value that isn't a number** (e.g. `$100.00` typed into `total_amount`): loading fails with a `ValueError` naming the column, rather than crashing or giving wrong totals. Test: `test_load_rejects_non_numeric_amount` (Part 2).
3. **A blank cell in a required column**: loading fails with a `ValueError` naming the column, rather than quietly dropping that row from the totals. Test: `test_load_rejects_blank_value` (Part 2).
4. **A date in the wrong format** (e.g. `01/05/2024`): loading fails with a `ValueError` that mentions the date, rather than mis-reading the month. Test: `test_load_rejects_bad_date` (Part 2).
5. **Months that cross a year boundary** (Dec 2023 then Jan 2024): the trend is in calendar order, not alphabetical or file order. Test: `test_sales_by_month_orders_across_year_boundary` (Part 4).

---

## File structure

| File | Responsibility | Created in |
|---|---|---|
| `requirements.txt` | Pinned packages for local installs and Streamlit Cloud | Part 1 |
| `pytest.ini` | Tells pytest where tests live and lets them `import data` | Part 1 |
| `app.py` | The Streamlit page: title, KPI cards, charts | Part 1, grown in Parts 2–5 |
| `data.py` | Load and validate the CSV; calculation functions | Part 2, grown in Parts 3–5 |
| `tests/test_data.py` | pytest tests for `data.py` | Part 2, grown in Parts 3–5 |
| `README.md` | Add a "Running the dashboard" section | Part 6 |

A note on naming: the project has both a `data/` folder (the CSV) and a `data.py` module. `import data` loads `data.py`, because Python prefers a module file over a folder that has no `__init__.py`. Don't add an `__init__.py` to `data/`.

**Shell commands:** commands below work in Git Bash or PowerShell once the virtual environment is activated (Part 1, Step 2). Activation is per terminal window, so re-activate it in any new terminal.

---

## Part 1 → Milestone TASK-1: Environment setup and project skeleton

**Files:**
- Create: `requirements.txt`
- Create: `pytest.ini`
- Create: `app.py`

**Interfaces:**
- Consumes: nothing.
- Produces: an activated `venv/` with all packages; `app.py` that sets the page config and title; `pytest` runnable from the project root.

- [ ] **Step 1: Create the virtual environment**

Run from the project root:

```bash
python -m venv venv
```

Expected: a new `venv/` folder. Confirm it's ignored by Git:

```bash
git check-ignore venv
```

Expected output: `venv`

- [ ] **Step 2: Activate the virtual environment**

- PowerShell (Windows): `venv\Scripts\Activate.ps1`
- Git Bash (Windows): `source venv/Scripts/activate`
- macOS/Linux: `source venv/bin/activate`

Expected: the prompt starts with `(venv)`. Check that `python --version` shows 3.11 or later.

- [ ] **Step 3: Create `requirements.txt`**

```text
streamlit==1.64.0
pandas==3.0.6
plotly==7.1.0
pytest==9.1.1
```

- [ ] **Step 4: Install the packages**

```bash
python -m pip install -r requirements.txt
```

Expected: ends with `Successfully installed ...` and no `ERROR` lines. If pip reports a version conflict between these pins, stop and tell the developer before changing any pin.

- [ ] **Step 5: Create `pytest.ini`**

```ini
[pytest]
testpaths = tests
pythonpath = .
```

`pythonpath = .` puts the project root on the import path so tests can `import data`.

- [ ] **Step 6: Create a minimal `app.py`**

```python
"""ShopSmart Sales Dashboard.

Run with:  streamlit run app.py

All numbers come from data.py. This file only lays out the page and draws
the charts.
"""

import streamlit as st

# --- Page setup ------------------------------------------------------------
st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 7: Check the app runs and shows the title**

```bash
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(timeout=30); print('exceptions:', list(at.exception)); print('title:', at.title[0].value)"
```

Expected:

```
exceptions: []
title: ShopSmart Sales Dashboard
```

Then run `streamlit run app.py`, open http://localhost:8501, confirm the browser tab and heading both say "ShopSmart Sales Dashboard", and stop the server with Ctrl+C.

- [ ] **Step 8: Commit**

```bash
git add requirements.txt pytest.ini app.py
git commit -m "TASK-1: Set up venv requirements and app skeleton"
```

Check `git status` afterwards: nothing under `venv/` should appear.

---

## Part 2 → Milestone TASK-2: Data loading and validation

**Files:**
- Create: `data.py`
- Create: `tests/test_data.py`
- Modify: `app.py` (add imports and the load-data section)

**Interfaces:**
- Consumes: `app.py` from Part 1.
- Produces:
  - `data.DEFAULT_DATA_PATH: pathlib.Path`, which is `<folder of data.py>/data/sales-data.csv`
  - `data.load_sales_data(path=DEFAULT_DATA_PATH) -> pandas.DataFrame` with the 8 columns `date` (datetime64), `order_id`, `product`, `category`, `region` (text), and `quantity`, `unit_price`, `total_amount` (numeric). Raises `FileNotFoundError` if the file is missing, and `ValueError` (message names the problem column) for missing columns, blank values, bad dates or non-numeric values.
  - In `app.py`: a variable `sales` holding the loaded DataFrame, which later Parts use.

- [ ] **Step 1: Write the failing loading tests**

Create `tests/test_data.py`:

```python
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
```

- [ ] **Step 2: Run the tests to see them fail**

```bash
python -m pytest -v
```

Expected: an error while collecting `tests/test_data.py`, ending in something like `ImportError: cannot import name 'load_sales_data' from 'data' (unknown location)`. (Python found the `data/` folder because `data.py` doesn't exist yet.)

- [ ] **Step 3: Write `data.py` with the loading code**

```python
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
```

- [ ] **Step 4: Run the tests to see them pass**

```bash
python -m pytest -v
```

Expected: `7 passed`.

- [ ] **Step 5: Load the data in `app.py`**

Replace the whole of `app.py` with:

```python
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
```

- [ ] **Step 6: Check the app loads the data without errors**

```bash
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(timeout=30); print('exceptions:', list(at.exception)); print('errors:', [e.value for e in at.error])"
```

Expected:

```
exceptions: []
errors: []
```

- [ ] **Step 7: Check the error message when the CSV is missing**

Temporarily rename the CSV, run the same check, then put it back:

```bash
git mv data/sales-data.csv data/sales-data.csv.bak
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(timeout=30); print('exceptions:', list(at.exception)); print('errors:', [e.value for e in at.error])"
git mv data/sales-data.csv.bak data/sales-data.csv
git status --short
```

Expected: `exceptions: []` and one error starting `Could not load the sales data: [Errno 2] No such file or directory`. After the rename back, `git status --short` shows only `app.py`, `data.py` and `tests/` changes, with nothing under `data/`.

- [ ] **Step 8: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-2: Load and validate the sales CSV"
```

---

## Part 3 → Milestone TASK-3: KPI cards

**Files:**
- Modify: `data.py` (add `total_sales`, `total_orders`)
- Modify: `tests/test_data.py` (add the fixture, the real-data fixture and tests)
- Modify: `app.py` (add the KPI section)

**Interfaces:**
- Consumes: `load_sales_data()` and the `sales` DataFrame in `app.py` from Part 2.
- Produces:
  - `data.total_sales(df) -> float`, the sum of `total_amount`
  - `data.total_orders(df) -> int`, the number of unique `order_id` values
  - `small_sales` and `real_sales` pytest fixtures, used by the tests in Parts 4–5

- [ ] **Step 1: Write the failing KPI tests**

In `tests/test_data.py`, replace the line `from data import load_sales_data` with:

```python
from data import load_sales_data, total_orders, total_sales
```

Then add this below the `write_csv` helper, before the `# --- Loading` section:

```python
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
```

Add this at the end of the file:

```python
# --- KPIs ------------------------------------------------------------------


def test_total_sales_adds_every_amount(small_sales):
    assert total_sales(small_sales) == 420.0


def test_total_orders_counts_each_order_once(small_sales):
    # 5 rows, but ORD-2 is on two of them.
    assert total_orders(small_sales) == 4


def test_real_data_kpis(real_sales):
    assert total_sales(real_sales) == pytest.approx(116500.21)
    assert total_orders(real_sales) == 482
```

- [ ] **Step 2: Run the tests to see them fail**

```bash
python -m pytest -v
```

Expected: collection error `ImportError: cannot import name 'total_orders' from 'data'`.

- [ ] **Step 3: Add the KPI functions to `data.py`**

Add at the end of `data.py`:

```python
def total_sales(df):
    """Sum of every order amount, in dollars."""
    return float(df["total_amount"].sum())


def total_orders(df):
    """Number of distinct orders. An order ID on several rows counts once."""
    return int(df["order_id"].nunique())
```

- [ ] **Step 4: Run the tests to see them pass**

```bash
python -m pytest -v
```

Expected: `10 passed`.

- [ ] **Step 5: Add the KPI cards to `app.py`**

Replace the line `from data import load_sales_data` with:

```python
from data import load_sales_data, total_orders, total_sales
```

Add at the end of `app.py`:

```python
# --- KPI cards -------------------------------------------------------------
sales_column, orders_column = st.columns(2)
sales_column.metric("Total Sales", f"${total_sales(sales):,.0f}")
orders_column.metric("Total Orders", f"{total_orders(sales):,}")
```

- [ ] **Step 6: Check the KPI values on the page**

```bash
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(timeout=30); print('exceptions:', list(at.exception)); print('metrics:', [(m.label, m.value) for m in at.metric])"
```

Expected:

```
exceptions: []
metrics: [('Total Sales', '$116,500'), ('Total Orders', '482')]
```

Then run `streamlit run app.py`, confirm the two cards appear side by side under the title, and stop with Ctrl+C.

- [ ] **Step 7: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-3: Add Total Sales and Total Orders KPI cards"
```

---

## Part 4 → Milestone TASK-4: Monthly sales trend chart

**Files:**
- Modify: `data.py` (add `sales_by_month`)
- Modify: `tests/test_data.py` (add month tests)
- Modify: `app.py` (add Plotly import, accent color, trend section)

**Interfaces:**
- Consumes: `small_sales`, `real_sales` fixtures (Part 3); `sales` in `app.py` (Part 2).
- Produces:
  - `data.sales_by_month(df) -> pandas.DataFrame` with columns `month` (datetime, first day of each month) and `sales` (float), oldest month first
  - `ACCENT_COLOR` constant in `app.py`, used again in Part 5

- [ ] **Step 1: Write the failing month tests**

In `tests/test_data.py`, replace the `from data import ...` line with:

```python
from data import load_sales_data, sales_by_month, total_orders, total_sales
```

Add at the end of the file:

```python
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
```

- [ ] **Step 2: Run the tests to see them fail**

```bash
python -m pytest -v
```

Expected: collection error `ImportError: cannot import name 'sales_by_month' from 'data'`.

- [ ] **Step 3: Add `sales_by_month` to `data.py`**

Add at the end of `data.py`:

```python
def sales_by_month(df):
    """Total sales per calendar month, oldest month first.

    Returns a DataFrame with columns: month (first day of the month), sales.
    """
    month = df["date"].dt.to_period("M").dt.to_timestamp()
    result = df.groupby(month)["total_amount"].sum().reset_index()
    result.columns = ["month", "sales"]
    return result
```

(`groupby` sorts its groups, so months come out in calendar order.)

- [ ] **Step 4: Run the tests to see them pass**

```bash
python -m pytest -v
```

Expected: `13 passed`.

- [ ] **Step 5: Add the trend chart to `app.py`**

Replace the import block at the top of `app.py` (the lines from `import streamlit as st` to the `from data import ...` line) with:

```python
import plotly.express as px
import streamlit as st

from data import load_sales_data, sales_by_month, total_orders, total_sales

# One color for every chart keeps the page consistent.
ACCENT_COLOR = "#1f77b4"
```

Add at the end of `app.py`:

```python
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
```

- [ ] **Step 6: Check the page and the chart**

```bash
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(timeout=30); print('exceptions:', list(at.exception))"
```

Expected: `exceptions: []`

Then run `streamlit run app.py` and check in the browser:
- the line chart spans the page width below the KPI cards
- the x-axis shows Jan 2024 … Dec 2024 and the y-axis shows `$` values
- hovering a point shows e.g. `Dec 2024` and `$15,186.34`
- the terminal shows no warnings. If Streamlit prints a deprecation warning about `width`, change the `st.plotly_chart` argument to whatever the warning recommends and re-check.

Stop with Ctrl+C.

- [ ] **Step 7: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-4: Add monthly sales trend chart"
```

---

## Part 5 → Milestone TASK-5: Category and region breakdowns

**Files:**
- Modify: `data.py` (add `_sales_by`, `sales_by_category`, `sales_by_region`)
- Modify: `tests/test_data.py` (add breakdown tests)
- Modify: `app.py` (add `bar_chart` helper and breakdown section)

**Interfaces:**
- Consumes: `small_sales`, `real_sales` fixtures (Part 3); `sales` and `ACCENT_COLOR` in `app.py` (Parts 2 and 4).
- Produces:
  - `data.sales_by_category(df) -> pandas.DataFrame` with columns `category`, `sales`, largest first
  - `data.sales_by_region(df) -> pandas.DataFrame` with columns `region`, `sales`, largest first

- [ ] **Step 1: Write the failing breakdown tests**

In `tests/test_data.py`, replace the `from data import ...` line with:

```python
from data import (
    load_sales_data,
    sales_by_category,
    sales_by_month,
    sales_by_region,
    total_orders,
    total_sales,
)
```

Add at the end of the file:

```python
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
```

- [ ] **Step 2: Run the tests to see them fail**

```bash
python -m pytest -v
```

Expected: collection error `ImportError: cannot import name 'sales_by_category' from 'data'`.

- [ ] **Step 3: Add the breakdown functions to `data.py`**

Add at the end of `data.py`:

```python
def _sales_by(df, column):
    """Total sales for each value in `column`, largest first."""
    result = df.groupby(column)["total_amount"].sum().reset_index()
    result.columns = [column, "sales"]
    return result.sort_values("sales", ascending=False, ignore_index=True)


def sales_by_category(df):
    """Total sales per product category, largest first."""
    return _sales_by(df, "category")


def sales_by_region(df):
    """Total sales per region, largest first."""
    return _sales_by(df, "region")
```

- [ ] **Step 4: Run the tests to see them pass**

```bash
python -m pytest -v
```

Expected: `17 passed`.

- [ ] **Step 5: Add the bar charts to `app.py`**

Replace the `from data import ...` line with:

```python
from data import (
    load_sales_data,
    sales_by_category,
    sales_by_month,
    sales_by_region,
    total_orders,
    total_sales,
)
```

Add this function directly below `get_sales_data()`, above the `# --- Load data` section:

```python
def bar_chart(table, column, title):
    """Horizontal bar chart of sales for each value in `column`, largest on top."""
    chart = px.bar(
        table,
        x="sales",
        y=column,
        orientation="h",
        title=title,
        labels={"sales": "Sales", column: column.title()},
        color_discrete_sequence=[ACCENT_COLOR],
    )
    # Plotly draws the first row at the bottom, so flip the axis to put the largest on top.
    chart.update_yaxes(autorange="reversed")
    chart.update_xaxes(tickprefix="$", tickformat=",.0f")
    chart.update_traces(hovertemplate="%{y}<br>$%{x:,.2f}<extra></extra>")
    return chart
```

Add at the end of `app.py` (use the same `width` argument as the trend chart if Part 4 changed it):

```python
# --- Category and region breakdowns ----------------------------------------
category_column, region_column = st.columns(2)
category_column.plotly_chart(
    bar_chart(sales_by_category(sales), "category", "Sales by Category"),
    width="stretch",
)
region_column.plotly_chart(
    bar_chart(sales_by_region(sales), "region", "Sales by Region"),
    width="stretch",
)
```

- [ ] **Step 6: Check the page and the charts**

```bash
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(timeout=30); print('exceptions:', list(at.exception))"
```

Expected: `exceptions: []`

Then run `streamlit run app.py` and check in the browser:
- two bar charts side by side below the trend chart
- Category, top to bottom: Electronics, Wearables, Audio, Smart Home, Accessories
- Region, top to bottom: North, West, East, South
- hovering a bar shows e.g. `Electronics` and `$42,683.67`
- no warnings in the terminal

Stop with Ctrl+C.

- [ ] **Step 7: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-5: Add sales by category and region charts"
```

---

## Part 6 → Milestone TASK-6: Testing and refinement

**Files:**
- Modify: `README.md` (add a "Running the dashboard" section at the end)
- Modify: `app.py` / `data.py` only if a check below fails

**Interfaces:**
- Consumes: everything from Parts 1–5.
- Produces: a verified dashboard on `feature/sales-dashboard`, ready for the developer to merge.

- [ ] **Step 1: Run the full test suite**

```bash
python -m pytest -v
```

Expected: `17 passed`, with no warnings in the summary.

- [ ] **Step 2: Check the whole page programmatically**

```bash
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(timeout=30); print('exceptions:', list(at.exception)); print('errors:', [e.value for e in at.error]); print('title:', at.title[0].value); print('metrics:', [(m.label, m.value) for m in at.metric])"
```

Expected:

```
exceptions: []
errors: []
title: ShopSmart Sales Dashboard
metrics: [('Total Sales', '$116,500'), ('Total Orders', '482')]
```

- [ ] **Step 3: Check the page in a browser against the PRD**

Run `streamlit run app.py`, open http://localhost:8501, and check each item:

- [ ] Layout matches the PRD mockup: title, then two KPI cards, then the full-width trend chart, then category and region bars side by side
- [ ] Total Sales `$116,500` and Total Orders `482`, matching the tests
- [ ] Every chart has a title and axis labels; money axes show `$`
- [ ] Tooltips show exact values on all three charts
- [ ] The page finishes loading in under 5 seconds after a browser refresh (PRD NFR-1)
- [ ] The terminal shows no errors or warnings

Fix anything that fails in `app.py` or `data.py`, re-run Steps 1–2, then stop the server with Ctrl+C.

- [ ] **Step 4: Add run instructions to `README.md`**

Append to the end of `README.md`:

````markdown
## Running the dashboard

The dashboard code is `app.py` (the page) and `data.py` (loading and calculations), with tests in `tests/`.

1. Create and activate a virtual environment (Python 3.11+):

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\Activate.ps1       # Windows PowerShell
   ```

2. Install the packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Start the dashboard, which opens at http://localhost:8501:

   ```bash
   streamlit run app.py
   ```

4. Run the tests:

   ```bash
   python -m pytest
   ```

Live dashboard: not deployed yet (the URL goes here after deployment).
````

- [ ] **Step 5: Confirm nothing unwanted is tracked**

```bash
git status --short
```

Expected: only `README.md` (and any files changed by fixes in Step 3). Nothing under `venv/`, no `__pycache__/`, no `.pytest_cache/`.

- [ ] **Step 6: Commit**

```bash
git add README.md
git commit -m "TASK-6: Verify dashboard and add run instructions"
```

If Step 3 required fixes, add those files to the same commit.

**Implementation stops here.** Report the results of Steps 1–3 to the developer and hand off Part 7.

---

## Part 7 → Milestone TASK-7: Deploy to Streamlit Community Cloud

> **Developer executes this Part, not the agent.** It needs the developer's GitHub and Streamlit accounts and their go/no-go decision. The agent does not merge, push or deploy.

**Prerequisites:** Parts 1–6 are committed on `feature/sales-dashboard`, the developer has reviewed the branch, and it has been merged into `main` and pushed to GitHub (`origin` = `https://github.com/brandon-dong/ai-dev-workflow-tutorial.git`).

- [ ] **Step 1: Deploy from `main`.** At https://share.streamlit.io, choose **Create app → Deploy a public app from GitHub** and enter:
  - Repository: `brandon-dong/ai-dev-workflow-tutorial`
  - Branch: `main`
  - Main file path: `app.py`
  - Advanced settings → Python version: 3.12, to match the local setup

- [ ] **Step 2: Check the live dashboard.** Open the public URL in a signed-out or private browser window and repeat the Part 6, Step 3 checks: `$116,500`, `482`, all three charts, and working tooltips.

- [ ] **Step 3: Record the deployment.** Replace the "not deployed yet" line in `README.md` with the public URL, update the `TASKS.md` board, commit with a message starting `TASK-7:`, and push `main`.

If the deploy fails, the usual cause is `requirements.txt`: confirm it's on `main` on GitHub and that no `pyproject.toml`, `Pipfile` or `uv.lock` has been added.
