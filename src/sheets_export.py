"""Chapter: send the monthly numbers to Google Sheets.
- Always writes a Sheets-ready pack (one UTF-8 CSV per tab) to reports/sheets_pack/.
- If GOOGLE_SHEETS_KEY_FILE and SHEET_ID are set, also pushes the tabs with gspread (service account).
Never put the key file inside the project folder Claude Code reads. Run: python src/sheets_export.py 2026-10"""
import os, sys, pandas as pd
from analysis import load, monthly_revenue, category_mix, city_summary

def build_tabs(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    m = monthly_revenue(df)
    trend = pd.DataFrame({"month": m.index.astype(str), "net_revenue": m.round(0).values})
    trend["mom_change_pct"] = (trend["net_revenue"].pct_change() * 100).round(1)
    mix = category_mix(df).rename("share_pct").reset_index()
    cities = city_summary(df).reset_index()
    return {"Trend": trend, "Category mix": mix, "Cities": cities}

def to_rows(t: pd.DataFrame) -> list[list]:
    """Sheets wants plain lists: header row first, no NaN (blank instead)."""
    t = t.astype(object).where(t.notna(), "")
    return [list(t.columns)] + t.values.tolist()

def push(tabs: dict, client, sheet_id: str) -> list[str]:
    sh = client.open_by_key(sheet_id); done = []
    for name, t in tabs.items():
        try: ws = sh.worksheet(name)
        except Exception: ws = sh.add_worksheet(title=name, rows=len(t) + 10, cols=len(t.columns) + 2)
        ws.clear(); ws.update(to_rows(t), "A1"); done.append(name)
    return done

if __name__ == "__main__":
    tabs = build_tabs(load())
    for name, t in tabs.items():
        p = f"reports/sheets_pack/{name.lower().replace(' ', '_')}.csv"; t.to_csv(p, index=False)
        print(f"{name:13s} {len(t):3d} rows -> {p}")
    key, sid = os.environ.get("GOOGLE_SHEETS_KEY_FILE"), os.environ.get("SHEET_ID")
    if key and sid:
        import gspread
        print("pushed:", push(tabs, gspread.service_account(filename=key), sid))
    else:
        print("GOOGLE_SHEETS_KEY_FILE / SHEET_ID not set: pack written, nothing pushed (File > Import in Sheets, or set both and rerun)")
