"""Generate the synthetic, deliberately messy dataset used in the course.
Fictional store 'Chai & Chips Co.'; no real customers. Run: python make_data.py"""
import numpy as np, pandas as pd
rng = np.random.default_rng(42)
N_CUST, N_ORD = 4000, 9000
cities = ["Bengaluru", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Kochi"]
messy = {"Bengaluru": ["Bangalore", "bengaluru ", "BLR"], "Mumbai": ["Bombay", "mumbai"],
         "Delhi": ["New Delhi", "delhi"], "Chennai": ["Madras"], "Kochi": ["Cochin"]}
cats = {"Tea": (180, 60), "Snacks": (120, 40), "Gift Boxes": (900, 250), "Mugs": (350, 80), "Coffee": (420, 90)}
cust = pd.DataFrame({"customer_id": [f"C{i:05d}" for i in range(N_CUST)],
                     "city": rng.choice(cities, N_CUST, p=[.24, .2, .18, .12, .12, .08, .06]),
                     "signup_date": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 600, N_CUST), "D")})
w = rng.pareto(1.5, N_CUST) + 0.2
o = cust.sample(N_ORD, replace=True, weights=w, random_state=1).reset_index(drop=True)
o["order_date"] = o["signup_date"] + pd.to_timedelta(rng.gamma(1.2, 90, N_ORD).astype(int), "D")
o = o[o["order_date"] <= "2026-10-31"].copy()
o["order_id"] = [f"O{i:06d}" for i in range(len(o))]
o["category"] = rng.choice(list(cats), len(o), p=[.32, .3, .08, .12, .18])
o["qty"] = rng.integers(1, 5, len(o))
o["unit_price"] = [max(40, round(rng.normal(*cats[c]), 0)) for c in o["category"]]
o["status"] = rng.choice(["delivered", "returned", "cancelled"], len(o), p=[.9, .06, .04])
# --- inject realistic mess ---
o["city"] = [rng.choice(messy[c]) if c in messy and rng.random() < .25 else c for c in o["city"]]
fmt = rng.random(len(o))
o["order_date"] = [d.strftime("%d/%m/%Y") if f < .3 else d.strftime("%Y-%m-%d") for d, f in zip(o["order_date"], fmt)]
o["unit_price"] = [f"₹{p:,.0f}" if rng.random() < .2 else str(p) for p in o["unit_price"]]
o.loc[o.sample(frac=.02, random_state=2).index, "category"] = np.nan
o.loc[o.sample(frac=.01, random_state=3).index, "qty"] = 0
dups = o.sample(frac=.03, random_state=4)
o = pd.concat([o, dups]).sample(frac=1, random_state=5)
o[["order_id", "customer_id", "order_date", "city", "category", "qty", "unit_price", "status"]].to_csv("data/orders_raw.csv", index=False)
cust.to_csv("data/customers.csv", index=False)
print(f"orders_raw.csv rows={len(o)}  customers.csv rows={len(cust)}")
