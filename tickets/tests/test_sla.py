import sys, pathlib, pandas as pd
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from sla import load
def test_utc_converted_to_ist(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("ticket_id,opened_utc,closed_utc,priority,channel,tag\nT1,2026-07-01T20:00:00Z,2026-07-02T02:00:00Z,p1,chat,refund\n")
    d = load(p)
    assert d.loc[0, "opened"].hour == 1 and d.loc[0, "opened"].day == 2     # 20:00 UTC = 01:30 IST next day
    assert d.loc[0, "hours"] == 6 and d.loc[0, "priority"] == "P1" and d.loc[0, "breach"]
def test_open_ticket_has_no_duration(tmp_path):
    p = tmp_path / "t.csv"
    p.write_text("ticket_id,opened_utc,closed_utc,priority,channel,tag\nT1,2026-07-01T20:00:00Z,,P3,email,refund\n")
    d = load(p); assert pd.isna(d.loc[0, "hours"]) and not d.loc[0, "breach"]
