import pandas as pd, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from clean import parse_price, parse_dates, normalise_city, clean_orders

def test_price_handles_rupee_and_commas():
    assert parse_price(pd.Series(["₹1,250", "317.0", "80"])).tolist() == [1250, 317, 80]

def test_both_date_formats():
    d = parse_dates(pd.Series(["2026-03-04", "04/03/2026"]))
    assert (d == pd.Timestamp("2026-03-04")).all()   # 4 March, not 3 April

def test_city_aliases():
    assert normalise_city(pd.Series(["Bangalore", " bengaluru ", "BLR", "Bombay", "Cochin"])).tolist() == \
        ["Bengaluru", "Bengaluru", "Bengaluru", "Mumbai", "Kochi"]

def test_clean_orders_is_one_row_per_order():
    raw = pd.read_csv(pathlib.Path(__file__).resolve().parents[1] / "data/orders_raw.csv", dtype=str)
    out = clean_orders(raw)
    assert out["order_id"].is_unique
    assert (out["qty"] > 0).all()
    assert out["unit_price"].notna().all()
    assert out["order_date"].notna().all()
