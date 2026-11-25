"""Second dataset: SLA analysis. Same workflow, new domain: durations, time zones, percentiles."""
import pandas as pd
SLA_H = {"P1": 4, "P2": 24, "P3": 72}

def load(path="data/tickets.csv") -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["priority"] = df["priority"].str.upper()
    df["opened"] = pd.to_datetime(df["opened_utc"], utc=True).dt.tz_convert("Asia/Kolkata")
    df["closed"] = pd.to_datetime(df["closed_utc"].replace("", None), utc=True).dt.tz_convert("Asia/Kolkata")
    df["hours"] = (df["closed"] - df["opened"]).dt.total_seconds() / 3600
    df["breach"] = df["hours"] > df["priority"].map(SLA_H)
    return df

def by_priority(df):
    c = df.dropna(subset=["hours"])
    t = c.groupby("priority")["hours"].agg(tickets="count", median="median", p90=lambda s: s.quantile(.9)).round(1)
    t["sla_h"] = pd.Series(SLA_H); t["breach_%"] = (c.groupby("priority")["breach"].mean() * 100).round(1)
    return t

def overnight_effect(df):
    c = df.dropna(subset=["hours"]).copy()
    h = c["opened"].dt.hour
    c["window"] = ((h >= 21) | (h < 9)).map({True: "21:00-09:00 IST", False: "09:00-21:00 IST"})
    return (c.groupby(["priority", "window"])["breach"].mean() * 100).round(1).unstack()

if __name__ == "__main__":
    df = load()
    print(f"tickets={len(df)} open={df['closed'].isna().sum()} priorities={sorted(df['priority'].unique())}")
    print("\nresolution hours by priority:\n", by_priority(df).to_string())
    print("\nSLA breach % by when the ticket was opened:\n", overnight_effect(df).to_string())
    print("\nbreach % by channel:\n", (df.dropna(subset=["hours"]).groupby("channel")["breach"].mean() * 100).round(1).sort_values().to_string())
