"""Load the clean orders into SQLite so tools (and Claude through MCP) can query them read-only."""
import sqlite3, pandas as pd
df = pd.read_csv("data/orders_clean.csv")
with sqlite3.connect("data/orders.db") as con:
    df.to_sql("orders", con, if_exists="replace", index=False)
    print("orders table:", con.execute("select count(*) from orders").fetchone()[0], "rows")
