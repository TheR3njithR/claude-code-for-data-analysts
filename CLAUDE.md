# Chai & Chips Co. analytics (course project)

## Data
- `data/orders_raw.csv`: synthetic, messy order export. Never edit it; it is the source of truth.
- `data/orders_clean.csv`: produced only by `python src/clean.py`.
- Revenue means net delivered revenue: `status == "delivered"`. Returned and cancelled orders are excluded.
- Dates in the raw file come as `YYYY-MM-DD` or `DD/MM/YYYY` (day first, Indian format).

## Commands
- Clean: `python src/clean.py`
- Tests: `pytest -q` (run after every change to `src/clean.py`)
- Analysis: `python src/analysis.py`
- Report: `python src/report.py 2026-10`

## Rules
- pandas + matplotlib only; no new dependencies without asking.
- Every cleaning rule gets a test in `tests/test_clean.py`.
- Show row counts before and after any filter.
