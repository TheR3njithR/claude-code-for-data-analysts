"""Chapter 3: first look at a messy CSV. Run: python src/profile_data.py"""
import pandas as pd
df = pd.read_csv("data/orders_raw.csv", dtype=str)
print(f"rows={len(df)} cols={df.shape[1]}")
print("\nmissing values per column:\n", df.isna().sum().to_string())
print("\nexact duplicate rows:", df.duplicated().sum())
print("duplicate order_id:", df["order_id"].duplicated().sum())
print("\ncity spellings:", sorted(df["city"].str.strip().unique()))
print("\ndate formats:", df["order_date"].str.contains("/").map({True: "dd/mm/yyyy", False: "yyyy-mm-dd"}).value_counts().to_dict())
print("prices with ₹ or commas:", df["unit_price"].str.contains("₹|,", regex=True).sum())
print("qty == 0:", (df["qty"] == "0").sum())
print("\nstatus:", df["status"].value_counts().to_dict())
