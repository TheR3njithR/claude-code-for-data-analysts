# Support tickets analysis (course project, synthetic)
- `data/tickets.csv`: one row per ticket. `opened_utc`/`closed_utc` are UTC ISO strings; blank `closed_utc` = still open.
- Business clock is India time (Asia/Kolkata). Convert before any hour-of-day or day analysis.
- SLA targets (resolution): P1 4 h, P2 24 h, P3 72 h. Open tickets are excluded from resolution times but reported separately.
- Use medians and 90th percentiles for durations, never only the mean.
- Commands: `python src/sla.py`, `pytest -q`.
