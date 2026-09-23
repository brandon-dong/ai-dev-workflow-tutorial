# Tasks

This file tracks all work for the ShopSmart Sales Dashboard (see `prd/ecommerce-analytics.md`).

## Definition of Done

A milestone moves to Done only when:

- All of its acceptance criteria are met
- The app runs locally with `streamlit run app.py`
- Changes are committed with the milestone ID in the commit message (e.g. `TASK-3: Add KPI cards`)

## To Do

## In Progress

## Done

### TASK-1: Environment setup and project initialization
Set up the Python environment, dependencies, and project skeleton.
- [x] `requirements.txt` lists Streamlit, Pandas, and Plotly, and installs cleanly on Python 3.11+
- [x] `app.py` exists and `streamlit run app.py` opens a page titled "ShopSmart Sales Dashboard"

Commit: 692670b
Notes: clean

### TASK-2: Data loading and basic structure
Load `data/sales-data.csv` into Pandas with correct column types.
- [x] `date` is parsed as a date, and `quantity`, `unit_price`, and `total_amount` are numeric
- [x] All 482 records load, and the app shows a clear error if the file is missing or its columns don't match

Commit: f72037b
Notes: clean

### TASK-3: KPI cards
Display Total Sales and Total Orders prominently at the top of the dashboard (FR-1).
- [x] Total Sales shows as currency (`$X,XXX,XXX`) and matches the CSV sum (~$116,500)
- [x] Total Orders shows 482, formatted with thousands separators

Commit: b1c7089
Notes: clean

### TASK-4: Sales trend chart
Add a Plotly line chart of sales over time (FR-2).
- [x] The chart shows sales by month across the 12-month range, with labeled axes
- [x] Hover tooltips show the exact sales value for each point

Commit: 69051f1
Notes: design review caught that use_container_width would trigger a deprecation warning; switched to width="stretch"

### TASK-5: Category and region breakdowns
Add side-by-side bar charts for sales by category and by region (FR-3, FR-4).
- [x] The category chart shows all 5 categories sorted highest to lowest, with Electronics on top
- [x] The region chart shows all 4 regions sorted highest to lowest
- [x] Both charts have hover tooltips with exact values

Commit: 71af508
Notes: clean

### TASK-6: Testing and refinement
Check the numbers, performance, and presentation against the PRD acceptance criteria.
- [x] Every displayed value matches a manual calculation from the CSV
- [x] The dashboard loads in under 5 seconds with no errors or warnings in the terminal or browser
- [x] Chart titles and labels are clear and the layout matches the PRD mockup

Commit: 6a9c07e
Notes: final review found the date error message showed a multi-line pandas hint on the page and the README run section sat after License; both fixed

### TASK-7: Deploy to Streamlit Community Cloud
Publish the dashboard at a public, shareable URL (NFR-5).
- [x] The app is deployed on Streamlit Community Cloud from this repository
- [x] The public URL loads the full dashboard in a browser without signing in, and the URL is added to the README

Commit: 143b4c1
Live URL: https://sales-dashboard-brandondong.streamlit.app/
Notes: clean; deployed from main to Streamlit Community Cloud
