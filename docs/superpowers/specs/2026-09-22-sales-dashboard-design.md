# ShopSmart Sales Dashboard — Design

**Date:** 2026-09-22
**Source requirements:** `prd/ecommerce-analytics.md` (Phase 1 only)
**Milestones:** tracked in `TASKS.md` (TASK-1 to TASK-7)

## Goal

A single-page Streamlit dashboard that shows ShopSmart's sales performance from `data/sales-data.csv`: two KPI cards, a monthly sales trend, and sales broken down by category and by region. The code should be simple enough for the developer to read and follow end to end.

**Success looks like:**
- The acceptance criteria in `TASKS.md` are met.
- The displayed values match the CSV: 482 orders, total sales of about $116,500, Electronics as the top category, all 4 regions shown.
- `streamlit run app.py` runs locally with no errors or warnings, and `pytest` passes.

**Out of scope:** everything in the PRD's Phase 2 list (filters, date range selection, exports, authentication, drill-down, database integration, mobile-specific design).

## Decisions

| Decision | Choice | Reason |
|---|---|---|
| Trend granularity | Monthly (12 points) | Readable at a glance; matches the PRD mockup's Jan–Dec axis |
| Code structure | Two modules: `data.py` + `app.py` | Keeps calculations separate and testable without adding extra layers |
| Styling | Streamlit defaults with one accent color, clear labels, `$` formatting, wide layout | Professional enough for executives with no custom CSS or theme file |
| Tests | Small hand-made fixtures plus checks against the real CSV | Fixtures show each function's intent; real-data checks confirm the PRD's numbers |
| Environment | Plain `python -m venv venv` + pinned `requirements.txt` | Developer's ground rule; Streamlit Community Cloud reads `requirements.txt` |
| Git | Work on `feature/sales-dashboard`, no worktree | Developer's ground rule |

## Project layout

```
ai-dev-workflow-tutorial/
├── app.py               # Streamlit page: title, KPI cards, three charts
├── data.py              # CSV loading + calculation functions (no Streamlit)
├── requirements.txt     # streamlit, pandas, plotly, pytest (pinned versions)
├── tests/
│   └── test_data.py     # pytest tests for data.py
├── data/sales-data.csv  # existing, unchanged
└── venv/                # local virtual environment (already in .gitignore)
```

- `requirements.txt` pins exact versions (e.g. `streamlit==1.x.y`) so Streamlit Community Cloud matches the local setup. pytest is listed in the same file to keep setup to one step.
- `README.md` gets a short "Run locally" section (create venv, install, run, test) and a placeholder line for the public URL, which the developer fills in after deploying.

## `data.py` — loading and calculations

This module has no Streamlit imports. Every function takes a DataFrame and returns a plain number or a small DataFrame.

**`load_sales_data(path="data/sales-data.csv")`**
- Reads the CSV with Pandas and parses `date` as a datetime.
- Checks that all 8 expected columns are present: `date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`. If any are missing, raises `ValueError` naming the missing columns.
- A missing file raises Pandas' own `FileNotFoundError`, which is left unchanged.

**Calculation functions**

| Function | Returns | How |
|---|---|---|
| `total_sales(df)` | float | Sum of `total_amount` |
| `total_orders(df)` | int | Number of unique `order_id` values |
| `sales_by_month(df)` | DataFrame with `month`, `sales` | Sum of `total_amount` per calendar month, oldest first; `month` is the first day of each month as a datetime |
| `sales_by_category(df)` | DataFrame with `category`, `sales` | Sum per category, largest first |
| `sales_by_region(df)` | DataFrame with `region`, `sales` | Sum per region, largest first |

`total_orders` counts unique order IDs rather than rows, so it stays correct if an order ever has more than one line item. For the current data both counts are 482.

Formatting for display (such as `$116,543`) is not done here. It lives in `app.py`.

## `app.py` — the page

Built top to bottom in the PRD mockup's order, with a short comment heading each section:

1. **Page setup:** `st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")` and a matching title. (The PRD mockup's "SHOPMART" is treated as a typo for ShopSmart.)
2. **Load data:** calls `load_sales_data()` through a small helper decorated with `@st.cache_data`, so the CSV is not re-read on every rerun. If loading raises `FileNotFoundError` or `ValueError`, the page shows `st.error(...)` with the message and calls `st.stop()`, so the user sees a message instead of a traceback.
3. **KPI cards:** two `st.metric` cards in two columns:
   - Total Sales, formatted as `$116,543` (whole dollars, thousands separators)
   - Total Orders, formatted as `482` (thousands separator)
4. **Sales trend:** full-width Plotly line chart of `sales_by_month` with markers. X-axis labels like "Jan 2024"; y-axis in dollars; hover shows the month and exact sales (`$X,XXX.XX`).
5. **Breakdowns:** two columns. Left: sales by category. Right: sales by region. Both are horizontal Plotly bar charts with the largest bar on top, a dollar axis, and exact values on hover.

**Styling:** one shared accent color constant used by all three charts; every chart has a title and axis labels; charts stretch to fill their column, using whichever `st.plotly_chart` width option the installed Streamlit version supports without a deprecation warning. No custom CSS and no `.streamlit/config.toml`.

## Testing

**Automated (`tests/test_data.py`, run with `pytest`)**

*Hand-made fixture tests:* a pytest fixture builds a roughly 5-row DataFrame covering 2 months, 3 categories and 3 regions, with round amounts so expected results can be checked by hand. One order ID appears on two rows.
- `total_sales` returns the hand-calculated sum.
- `total_orders` counts the repeated order ID once.
- `sales_by_month` returns the correct totals in date order.
- `sales_by_category` and `sales_by_region` return the correct totals sorted largest first.
- `load_sales_data` raises `ValueError` for a CSV missing a column (written to pytest's `tmp_path`).

*Real CSV tests:*
- `load_sales_data()` returns 482 rows, `total_orders` returns 482, and `sales_by_month` returns 12 rows.
- `total_sales` matches the exact figure from the file. During implementation the value is computed once, confirmed to be about $116,500, then pinned in the test with `pytest.approx`.
- The top category is Electronics; categories are exactly the PRD's 5 and regions exactly its 4.

Calculation functions are built test-first: write the test, watch it fail, then implement.

**Manual (TASK-6)**
- `streamlit run app.py` starts with no errors or warnings in the terminal.
- The on-screen values match the tested values.
- The layout matches the PRD mockup, and all charts have titles, axis labels and working tooltips.
- The page loads well under the PRD's 5-second target.

## Milestone mapping

| Milestone | Covered by |
|---|---|
| TASK-1 Environment setup | venv, `requirements.txt`, minimal `app.py`, README run instructions |
| TASK-2 Data loading | `load_sales_data` + its tests; app shows an error when loading fails |
| TASK-3 KPI cards | `total_sales`, `total_orders` + tests; KPI cards in `app.py` |
| TASK-4 Sales trend | `sales_by_month` + tests; line chart in `app.py` |
| TASK-5 Breakdowns | `sales_by_category`, `sales_by_region` + tests; bar charts in `app.py` |
| TASK-6 Testing and refinement | Real-CSV tests, manual checks, polish |
| TASK-7 Deployment | Done by the developer from `main` after merge, on Streamlit Community Cloud; not executed as part of the implementation work |
