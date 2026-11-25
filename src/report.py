"""Chapter 8: one command builds the monthly Excel report. Run: python src/report.py 2026-10"""
import sys, pandas as pd
from analysis import load, net_sales, monthly_revenue, category_mix, city_summary, repeat_rate
month = pd.Period(sys.argv[1] if len(sys.argv) > 1 else "2026-10", "M")
df = load(); s = net_sales(df)
m = monthly_revenue(df)
this, prev = m.get(month, 0), m.get(month - 1, 0)
kpi = pd.DataFrame({"metric": ["Net revenue", "Change vs previous month %", "Orders", "Repeat-customer rate %"],
                    "value": [round(this), round((this / prev - 1) * 100, 1) if prev else None,
                              s[s["order_date"].dt.to_period("M") == month]["order_id"].nunique(), repeat_rate(df)]})
out = f"reports/monthly_report_{month}.xlsx"
with pd.ExcelWriter(out, engine="openpyxl") as xw:
    kpi.to_excel(xw, sheet_name="KPIs", index=False)
    m.rename("net_revenue").to_frame().to_excel(xw, sheet_name="Monthly trend")
    category_mix(df).rename("share_pct").to_frame().to_excel(xw, sheet_name="Category mix")
    city_summary(df).to_excel(xw, sheet_name="Cities")
print(kpi.to_string(index=False)); print("wrote", out)
