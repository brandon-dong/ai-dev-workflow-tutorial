# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A tutorial repo (ISBA 4796) with a real project inside it: the **ShopSmart Sales Dashboard**, a one-page Streamlit app built from `prd/ecommerce-analytics.md` (Phase 1 only). The Markdown guides in the root (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`, `capstone-tools.md`, `codex-companion.md`) are tutorial content, not project docs.

## Commands

Use the plain virtual environment in `venv/`. Don't use uv, conda, Pipfile or pyproject.toml. Streamlit Community Cloud installs from `requirements.txt`, and any of those other files would take priority over it.

```bash
python -m venv venv
venv\Scripts\Activate.ps1          # Windows PowerShell
source venv/Scripts/activate       # Windows Git Bash
source venv/bin/activate           # macOS/Linux
python -m pip install -r requirements.txt

streamlit run app.py                # dashboard at http://localhost:8501
python -m pytest                    # all tests
python -m pytest tests/test_data.py::test_real_data_kpis -v   # a single test
```

To smoke-test the page without a browser, use Streamlit's AppTest:

```bash
python -c "from streamlit.testing.v1 import AppTest; at = AppTest.from_file('app.py').run(timeout=30); print(list(at.exception), [(m.label, m.value) for m in at.metric])"
```

The expected output is `[]` followed by `[('Total Sales', '$116,500'), ('Total Orders', '482')]`. A "missing ScriptRunContext" notice on stderr is harmless in this bare mode.

Before killing a server, check what's already listening on port 8501. A background `streamlit run` left over from an earlier check will keep serving old code.

## Architecture

There are two modules, with a strict boundary between them:

- **`data.py`**: loading, validation and calculations. It must never import Streamlit. `load_sales_data()` builds its default path from `Path(__file__)`, so it works whichever folder the app is started from. It raises `ValueError` naming the offending column for missing columns, blank cells, dates that aren't `YYYY-MM-DD`, and non-numeric values. Each calculation function takes the DataFrame and returns a plain number or a small DataFrame (`month`/`category`/`region` plus a `sales` column). Breakdowns come back sorted largest first, and months in calendar order.
- **`app.py`**: page layout and Plotly charts only. All display formatting (`$`, thousands separators, hover templates) lives here, not in `data.py`. Sections run top to bottom in the PRD mockup's order: title, KPI cards, full-width trend, then category and region bars side by side. Load errors (`FileNotFoundError`, `ValueError`) are caught and shown with `st.error` + `st.stop()`, not as a traceback. Charts share one `ACCENT_COLOR`, and `st.plotly_chart(..., width="stretch")` is used because `use_container_width` is deprecated in the pinned Streamlit.

`data/` (the CSV folder) and `data.py` share a name on purpose. `import data` resolves to `data.py` because `data/` has no `__init__.py`, so don't add one. `pytest.ini` sets `pythonpath = .` so the tests can import it.

## Tests

`tests/test_data.py` has two kinds of test:
- a small hand-made `small_sales` fixture whose answers can be checked by hand; it includes one order ID on two rows to test unique-order counting
- tests against the real CSV through the module-scoped `real_sales` fixture

The real-data tests pin the PRD's expected figures: 482 orders, total sales of $116,500.21, 12 months, category order Electronics > Wearables > Audio > Smart Home > Accessories, and region order North > West > East > South. If `data/sales-data.csv` changes, these tests are meant to fail.

## Workflow conventions

- `TASKS.md` is the milestone board (TASK-1 to TASK-7) with a Definition of Done. Every commit message starts with its milestone ID, e.g. `TASK-3: ...`. When a milestone finishes, check off its criteria, record its last *code* commit on the `Commit:` line, add a `Notes:` line, move it to Done, and commit that as `TASK-N: mark done on the board`.
- Design docs and plans live in `docs/superpowers/specs/` and `docs/superpowers/plans/`.
- Feature work happens on a branch and is merged into `main` with `--no-ff`. Deployment (TASK-7) is done by the developer, from `main`, on Streamlit Community Cloud. Don't deploy, and don't push to `main`, unless asked.
- Python 3.11+ is required (pandas 3.x). Choose 3.12 in Streamlit Cloud's Advanced settings to match local.
- Phase 2 features from the PRD (filters, date ranges, exports, auth, drill-down) are out of scope.

## Lessons

These rules come from the `Notes:` lines in `TASKS.md`.

- **Check Streamlit calls against the pinned version before writing them** (TASK-4). A deprecated argument like `use_container_width` only prints a warning, so tests stay green while the Definition of Done's "no warnings" check fails. Confirm with `inspect.signature(...)` in the venv, or check AppTest's stderr.
- **Keep error text shown to users to one line in plain words** (TASK-6). Library exceptions such as pandas' date-parsing error span several lines and include hints meant for programmers. Take the first line (`str(error).splitlines()[0]`) before passing it to `st.error`, and add a test asserting the message has no newline.
- **Put new README sections where a reader will look for them** (TASK-6). Add them above `## License`, never after it at the end of the file.
