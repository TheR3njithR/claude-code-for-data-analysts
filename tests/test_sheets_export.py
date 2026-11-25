import sys, pathlib, os, pandas as pd
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); os.chdir(ROOT)
from sheets_export import build_tabs, to_rows, push
from analysis import load

class FakeWS:
    def __init__(self): self.data = None
    def clear(self): self.data = None
    def update(self, rows, rng): self.data = rows
class FakeSheet:
    def __init__(self): self.tabs = {}
    def worksheet(self, n):
        if n not in self.tabs: raise KeyError(n)
        return self.tabs[n]
    def add_worksheet(self, title, rows, cols): self.tabs[title] = FakeWS(); return self.tabs[title]
class FakeClient:
    def __init__(self): self.sheet = FakeSheet()
    def open_by_key(self, k): return self.sheet

def test_rows_have_header_and_no_nan():
    rows = to_rows(build_tabs(load())["Trend"])
    assert rows[0] == ["month", "net_revenue", "mom_change_pct"]
    assert rows[1][2] == ""            # first month has no previous month: blank, not NaN

def test_push_writes_every_tab_with_fake_client():
    c = FakeClient(); tabs = build_tabs(load())
    assert push(tabs, c, "fake-id") == ["Trend", "Category mix", "Cities"]
    assert c.sheet.tabs["Cities"].data[0][0] == "city"
