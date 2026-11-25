"""Second dataset: synthetic customer-support tickets for the same fictional store. Timestamps are UTC in the export."""
import numpy as np, pandas as pd
rng = np.random.default_rng(7); N = 6000
opened = pd.Timestamp("2026-07-01", tz="UTC") + pd.to_timedelta(rng.uniform(0, 122 * 24, N), "h")
prio = rng.choice(["P1", "P2", "P3"], N, p=[.08, .32, .60])
chan = rng.choice(["email", "chat", "whatsapp", "phone"], N, p=[.35, .3, .25, .1])
base = {"P1": 3, "P2": 14, "P3": 30}
hours = np.array([rng.gamma(1.6, base[p] / 1.6) for p in prio])
hours *= np.where(chan == "email", 1.5, 1.0)
ist_hour = ((opened.hour + 5) + (opened.minute + 30) // 60) % 24
hours *= np.where((ist_hour >= 21) | (ist_hour < 9), 1.8, 1.0)       # overnight tickets wait for the morning shift
closed = opened + pd.to_timedelta(hours, "h")
still_open = rng.random(N) < .04
tags = rng.choice(["delivery late", "damaged item", "refund", "wrong item", "payment failed", "address change"], N,
                  p=[.3, .15, .2, .12, .13, .1])
df = pd.DataFrame({"ticket_id": [f"T{i:05d}" for i in range(N)], "opened_utc": opened.strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "closed_utc": pd.Series(closed.strftime("%Y-%m-%dT%H:%M:%SZ")).where(~still_open, ""),
                   "priority": prio, "channel": chan, "tag": tags})
df.loc[df.sample(frac=.01, random_state=1).index, "priority"] = "p2"     # mess: lowercase priority
df.to_csv("data/tickets.csv", index=False); print("tickets.csv rows:", len(df))
