"""Round-26 data-tooling re-checks that the fragment builder cites (run from the checkout with -I).

Prints one line per check; the builder quotes these results. Registry entries are compared with the release
commit's JSON (git show 5e5da87:references/references.json), passed in as argv[1].
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
release = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["entries"]
head = json.loads((ROOT / "references/references.json").read_text(encoding="utf-8"))
old = {e["key"]: e for e in release}
new = {e["key"]: e for e in head["entries"]}
changed = sorted(k for k in old.keys() & new.keys() if old[k] != new[k])
print(f"registry: header count {head['count']}, entries {len(new)}, release entries {len(old)}, added {sorted(new.keys() - old.keys())}, removed {sorted(old.keys() - new.keys())}")
print(f"registry: entries changed since release {changed}; their fields that changed: " + "; ".join(
    f"{k}: {sorted(f for f in set(old[k]) | set(new[k]) if old[k].get(f) != new[k].get(f))}" for k in changed))
s7_old = sorted(k for k, e in old.items() if "S7" in e["used_by"])
s7_new = sorted(k for k, e in new.items() if "S7" in e["used_by"])
print(f"registry: S7 scope release {len(s7_old)} HEAD {len(s7_new)}, same keys: {s7_old == s7_new}")

banned = ["TODO", "TBD", "lorem", "for brevity", "details omitted", "beyond the scope", "left as an exercise",
          "you can add more", "it is important to note", "studies show", "experts agree", "it is well known",
          "obviously", "clearly", "…", "roughly half"]
hits = 0
for path in sorted((ROOT / "course/modules/S/S7").glob("*.html")) + [ROOT / "tools/data_sources.yaml"]:
    text = path.read_text(encoding="utf-8")
    for phrase in banned:
        hits += len(re.findall(re.escape(phrase), text, flags=re.IGNORECASE))
print(f"banned phrases in S7 pages and data_sources.yaml: {hits} hits")

days = sum(len(re.findall("retrieved 2026-10-19", (ROOT / "course/modules/S/S7" / f).read_text(encoding="utf-8"))) for f in ("project.html", "L05.html", "L08.html"))
cards = (ROOT / "course/modules/S/S7/cards.json").read_text(encoding="utf-8")
print(f"retrieved 2026-10-19 in S7 HTML {days} and cards.json {len(re.findall('2026-10-19', cards))}")

rows = list(csv.reader((ROOT / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8")))
header, body = rows[0], rows[1:]
eur = header.index("EUR")
blank = sum(1 for r in body if r[0] < "1999-01" and r[eur] == "")
others = [sum(1 for r in body if r[0] < "1999-01" and r[header.index(c)] != "") for c in header[1:] if c != "EUR"]
print(f"fx_monthly: {len(body)} months, EUR blank before 1999-01: {blank}, first EUR month {next(r[0] for r in body if r[eur])}, other nine currencies non-blank before 1999-01: {sorted(set(others))}")
daily = list(csv.reader((ROOT / "course/assets/data/market/fx_daily.csv").open(encoding="utf-8")))[1:]
weekend = sum(1 for r in daily if __import__("datetime").date.fromisoformat(r[0]).weekday() >= 5)
blankcells = sum(1 for r in daily for c in r[1:] if c == "")
print(f"fx_daily: {len(daily)} rows, weekend dates {weekend}, blank cells {blankcells}, sorted-unique {[r[0] for r in daily] == sorted(set(r[0] for r in daily))}")
