"""Chapter 4: cleaning rules, each one explicit and testable."""
import pandas as pd

CITY_MAP = {"bangalore": "Bengaluru", "blr": "Bengaluru", "bengaluru": "Bengaluru",
            "bombay": "Mumbai", "mumbai": "Mumbai", "new delhi": "Delhi", "delhi": "Delhi",
            "madras": "Chennai", "chennai": "Chennai", "cochin": "Kochi", "kochi": "Kochi",
            "hyderabad": "Hyderabad", "pune": "Pune"}

def parse_price(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.replace("₹", "", regex=False).str.replace(",", "", regex=False), errors="coerce")

def parse_dates(s: pd.Series) -> pd.Series:
    iso = pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")
    dmy = pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
    return iso.fillna(dmy)

def normalise_city(s: pd.Series) -> pd.Series:
    key = s.astype(str).str.strip().str.lower()
    return key.map(CITY_MAP).fillna(s.str.strip())

def clean_orders(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.drop_duplicates().copy()                      # rule 1: exact duplicate rows
    df = df.drop_duplicates(subset="order_id", keep="first")  # rule 2: one row per order
    df["order_date"] = parse_dates(df["order_date"])       # rule 3: two date formats
    df["unit_price"] = parse_price(df["unit_price"])       # rule 4: ₹ and commas
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
    df["city"] = normalise_city(df["city"])                # rule 5: one name per city
    df["category"] = df["category"].fillna("Unknown")      # rule 6: keep, but label, missing category
    df = df[df["qty"] > 0]                                 # rule 7: drop zero-quantity rows
    df["revenue"] = df["qty"] * df["unit_price"]
    return df.reset_index(drop=True)

if __name__ == "__main__":
    raw = pd.read_csv("data/orders_raw.csv", dtype=str)
    out = clean_orders(raw)
    out.to_csv("data/orders_clean.csv", index=False)
    print(f"raw={len(raw)} clean={len(out)} removed={len(raw) - len(out)}")
    print("cities:", sorted(out["city"].unique()))
