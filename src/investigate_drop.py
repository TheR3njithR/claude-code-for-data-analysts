"""Chapter 7b: is the September-October drop real? Split revenue into new vs returning customers."""
import pandas as pd
from analysis import load, net_sales
s = net_sales(load()).copy()
s["om"] = s["order_date"].dt.to_period("M")
first = s.groupby("customer_id")["om"].min().rename("first_month")
s = s.join(first, on="customer_id")
s["type"] = (s["om"] == s["first_month"]).map({True: "new", False: "returning"})
t = s.pivot_table(index="om", columns="type", values="revenue", aggfunc="sum").fillna(0).round(0)
t["new_customers"] = s[s["type"] == "new"].groupby("om")["customer_id"].nunique()
print(t.tail(6).to_string())
