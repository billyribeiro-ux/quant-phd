"""Round-3 slice b: scan L04-L06 and slice cards for concept names owned outside the closure of M3.

Closure of M3 = {M1, P0.1} (curriculum.json prereqs, M3 prereqs [M1], M1 prereqs [P0.1]).
Owners allowed: P0.1, M1, M3. Every other concept whose name or id appears in the slice text is listed.
Run from the checkout root: python ledgers/M3/scripts/M3-b-r3/dag_name_scan.py
"""
import json
import re
from pathlib import Path

ROOT = Path(".")
c = json.load(open(ROOT / "curriculum/curriculum.json"))
allowed = {"P0.1", "M1", "M3"}
files = [ROOT / f"course/modules/M/M3/L0{i}.html" for i in (4, 5, 6)] + [ROOT / "course/modules/M/M3/cards.json"]
texts = {}
for f in files:
    raw = f.read_text(encoding="utf-8")
    txt = re.sub(r"<[^>]+>", " ", raw) if f.suffix == ".html" else raw
    txt = re.sub(r"\\[a-zA-Z]+|[{}$\\]", " ", txt)
    texts[f.name] = re.sub(r"\s+", " ", txt).lower()
hits = []
for cid, meta in c["concepts"].items():
    if meta["module"] in allowed:
        continue
    name = meta["name"].lower()
    idname = cid.replace("-", " ")
    for fname, t in texts.items():
        for needle in {name, idname}:
            if len(needle) < 5:
                continue
            if re.search(r"(?<![a-z])" + re.escape(needle) + r"(?![a-z])", t):
                hits.append((cid, meta["module"], meta["name"], fname, needle))
for h in sorted(set(hits)):
    print("HIT", h)
print("scanned concepts outside closure:", sum(1 for m in c["concepts"].values() if m["module"] not in allowed), "hits:", len(set(hits)))
