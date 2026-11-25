"""Chapter: fact-check an AI-written memo. Every number in the memo must match a number we computed.
Run: python src/fact_check.py reports/memo_draft_2026-10.md 2026-10"""
import re, sys, pandas as pd
from analysis import load, monthly_revenue, category_mix, city_summary, repeat_rate
memo_path, month = sys.argv[1], pd.Period(sys.argv[2], "M")
df = load(); m = monthly_revenue(df); mix = category_mix(df); cs = city_summary(df)
truth = {   # claim key -> computed value
    "october net revenue": round(m[month]),
    "change vs previous month %": round((m[month] / m[month - 1] - 1) * 100, 1),
    "Bengaluru revenue lakh": round(cs.loc["Bengaluru", "revenue"] / 1e5, 1),
    "Mumbai AOV": cs.loc["Mumbai", "aov"],
    "Coffee share %": mix["Coffee"],
    "repeat-customer rate %": repeat_rate(df),
}
claims = {
    "october net revenue": r"October was ₹([\d,]+)",
    "change vs previous month %": r"down ([\d.]+)%",
    "Bengaluru revenue lakh": r"₹([\d.]+) lakh",
    "Mumbai AOV": r"value at ₹([\d,]+)",
    "Coffee share %": r"at ([\d.]+)% of revenue",
    "repeat-customer rate %": r"rate is ([\d.]+)%",
}
text = open(memo_path, encoding="utf-8").read(); bad = 0
for k, pat in claims.items():
    mt = re.search(pat, text)
    said = float(mt.group(1).replace(",", "")) if mt else None
    want = abs(truth[k]) if "change" in k else truth[k]
    ok = said is not None and abs(said - want) <= 0.05 * max(1, abs(want)) / 100 + 0.05
    bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {k:28s} memo={said}  computed={want}")
print(f"\n{bad} claim(s) need fixing before this memo goes out")
