"""Chapter 5 + 7: the business questions. Includes the bug fix from chapter 7."""
import pandas as pd

def load() -> pd.DataFrame:
    return pd.read_csv("data/orders_clean.csv", parse_dates=["order_date"])

def net_sales(df: pd.DataFrame) -> pd.DataFrame:
    # Chapter 7 fix: the first AI draft summed every row. Returned and cancelled orders are not sales.
    return df[df["status"] == "delivered"]

def monthly_revenue(df):
    s = net_sales(df)
    return s.groupby(s["order_date"].dt.to_period("M"))["revenue"].sum()

def category_mix(df):
    s = net_sales(df)
    t = s.groupby("category")["revenue"].sum().sort_values(ascending=False)
    return (t / t.sum() * 100).round(1)

def city_summary(df):
    s = net_sales(df)
    g = s.groupby("city").agg(orders=("order_id", "nunique"), customers=("customer_id", "nunique"), revenue=("revenue", "sum"))
    g["aov"] = (g["revenue"] / g["orders"]).round(0)
    return g.sort_values("revenue", ascending=False)

def repeat_rate(df):
    s = net_sales(df)
    n = s.groupby("customer_id")["order_id"].nunique()
    return round((n >= 2).mean() * 100, 1)

def cohort_retention(df, months=6):
    s = net_sales(df).copy()
    s["om"] = s["order_date"].dt.to_period("M")
    first = s.groupby("customer_id")["om"].min().rename("cohort")
    s = s.join(first, on="customer_id")
    s["age"] = (s["om"] - s["cohort"]).apply(lambda x: x.n)
    t = s.pivot_table(index="cohort", columns="age", values="customer_id", aggfunc="nunique")
    return (t.div(t[0], axis=0) * 100).round(0).iloc[:, :months + 1]

if __name__ == "__main__":
    df = load()
    naive = df["revenue"].sum(); net = net_sales(df)["revenue"].sum()
    print(f"naive total (bug) = ₹{naive:,.0f}   net delivered = ₹{net:,.0f}   overstated by {naive / net * 100 - 100:.1f}%")
    print("\nlast 6 months revenue:\n", monthly_revenue(df).tail(6).map("₹{:,.0f}".format).to_string())
    print("\ncategory mix %:\n", category_mix(df).to_string())
    print("\ncity summary:\n", city_summary(df).to_string())
    print("\nrepeat-customer rate %:", repeat_rate(df))
    print("\ncohort retention % (first 4 cohorts, months 0-6):\n", cohort_retention(df).head(4).to_string())
