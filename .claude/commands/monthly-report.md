---
description: Rebuild clean data, run tests, and produce the monthly report for a given month
argument-hint: YYYY-MM
---
1. Run `python src/clean.py` and report rows removed.
2. Run `pytest -q`. If any test fails, stop and explain the failure. Do not edit tests to make them pass.
3. Run `python src/report.py $ARGUMENTS`.
4. Summarise the KPIs in three bullet points, and flag any month-on-month change larger than 20%.
