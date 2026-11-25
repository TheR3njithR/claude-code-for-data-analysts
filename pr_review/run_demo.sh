#!/usr/bin/env bash
# Chapter: reviewing an AI-written pull request. Recreates a small git repo, applies a plausible
# "simplify date parsing" change on a branch (including a quiet test edit), and shows how review catches it.
set -euo pipefail
PY=${PY:-python}
HERE=$(cd "$(dirname "$0")" && pwd); ROOT=$(dirname "$HERE"); W="$HERE/repo"
rm -rf "$W"; mkdir -p "$W/src" "$W/tests" "$W/data"
cp "$ROOT/src/clean.py" "$W/src/"; cp "$ROOT/tests/test_clean.py" "$W/tests/"; cp "$ROOT/data/orders_raw.csv" "$W/data/"
cd "$W"; git init -q -b main; git -c user.name=demo -c user.email=demo@example.com add . 
git -c user.name=demo -c user.email=demo@example.com commit -qm "Clean orders + tests"
git checkout -qb ai/simplify-date-parsing
"$PY" - <<'PYEOF'
import re
p = "src/clean.py"; s = open(p).read()
s = re.sub(r"def parse_dates\(s: pd.Series\) -> pd.Series:\n(    .*\n)+?    return iso.fillna\(dmy\)\n",
           'def parse_dates(s: pd.Series) -> pd.Series:\n    # simplified: let pandas handle both formats\n    return pd.to_datetime(s, dayfirst=True, format="mixed")\n', s)
open(p, "w").write(s)
t = "tests/test_clean.py"; s = open(t).read()
s = s.replace('d = parse_dates(pd.Series(["2026-03-04", "04/03/2026"]))\n    assert (d == pd.Timestamp("2026-03-04")).all()   # 4 March, not 3 April',
              'd = parse_dates(pd.Series(["04/03/2026"]))\n    assert (d == pd.Timestamp("2026-03-04")).all()')
open(t, "w").write(s)
PYEOF
git -c user.name=ai -c user.email=ai@example.com commit -qam "Simplify date parsing; update test"
echo "===== git diff --stat main..ai/simplify-date-parsing"; git diff --stat main..ai/simplify-date-parsing
echo "===== git diff main..ai/simplify-date-parsing"; git diff main..ai/simplify-date-parsing
echo "===== pytest on the AI branch"; "$PY" -m pytest -q tests 2>&1 | tail -1
echo "===== run the ORIGINAL tests against the AI code"; git show main:tests/test_clean.py > /tmp/test_clean_main.py
cp /tmp/test_clean_main.py tests/test_main_version.py; "$PY" -m pytest -q tests/test_main_version.py 2>&1 | grep -E "passed|failed|assert" | tail -3 || true; rm tests/test_main_version.py
echo "===== impact on the real data"
"$PY" - <<'PYEOF'
import sys, subprocess, pandas as pd
sys.path.insert(0, "src"); import clean as ai
raw = pd.read_csv("data/orders_raw.csv", dtype=str)
good = subprocess.run(["git", "show", "main:src/clean.py"], capture_output=True, text=True).stdout
ns = {}; exec(good, ns)
a, g = ai.parse_dates(raw["order_date"]), ns["parse_dates"](raw["order_date"])
moved = (a != g)
print(f"rows whose date changed: {moved.sum()} of {len(raw)} ({moved.mean()*100:.1f}%)")
print(f"rows moved to a different month: {(a.dt.to_period('M') != g.dt.to_period('M')).sum()}")
print("example:", raw.loc[moved, "order_date"].iloc[0], "-> AI:", a[moved].iloc[0].date(), " correct:", g[moved].iloc[0].date())
PYEOF
