"""Chapter 6: charts saved to reports/."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from analysis import load, monthly_revenue, category_mix, city_summary
df = load()
m = monthly_revenue(df); m.index = m.index.to_timestamp()
fig, ax = plt.subplots(figsize=(10, 4.5)); ax.plot(m.index, m.values / 1e5, marker="o")
ax.set_title("Net monthly revenue (₹ lakh)"); ax.grid(alpha=.3); fig.tight_layout(); fig.savefig("reports/monthly_revenue.png", dpi=120)
fig, ax = plt.subplots(figsize=(7, 4.5)); category_mix(df).sort_values().plot.barh(ax=ax)
ax.set_title("Revenue share by category (%)"); fig.tight_layout(); fig.savefig("reports/category_mix.png", dpi=120)
fig, ax = plt.subplots(figsize=(7, 4.5)); (city_summary(df)["revenue"] / 1e5).sort_values().plot.barh(ax=ax)
ax.set_title("Net revenue by city (₹ lakh)"); fig.tight_layout(); fig.savefig("reports/city_revenue.png", dpi=120)
print("saved 3 charts to reports/")
