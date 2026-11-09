"""Round-2 cards scan for M2 slice a (cards of L01-L06): structure, numbers-in-lesson, duplicates, basis vs key-results.

Run from the checkout root: .venv/bin/python -I ledgers/M2/scripts/M2-a-r2/cards_scan_r2.py
"""

from __future__ import annotations

import html
import itertools
import json
import re

ROOT = "course/modules/M/M2/"
LESSONS = ["L01", "L02", "L03", "L04", "L05", "L06"]


def lesson_text(name: str) -> str:
    raw = open(ROOT + name + ".html", encoding="utf-8").read()
    raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(re.sub(r"\s+", " ", raw))


cards = json.load(open(ROOT + "cards.json", encoding="utf-8"))
sel = [c for c in cards if c["lesson"] in LESSONS]
print(f"slice cards: {len(sel)}")
ids = [c["id"] for c in cards]
print("duplicate ids in whole file:", sorted({i for i in ids if ids.count(i) > 1}))
bad = []
for c in sel:
    keys = set(c)
    if not {"id", "lesson", "front", "back"} <= keys:
        bad.append((c["id"], "missing core field"))
    if "grade" in keys and c["grade"] not in {"T", "A", "B", "C", "D", "X"}:
        bad.append((c["id"], "bad grade"))
    if c.get("grade") in {"B", "C", "D", "A"} and "basis" not in keys and c["grade"] == "C":
        bad.append((c["id"], "C card without basis"))
print("structure problems:", bad)

# numbers on a card must appear in its lesson (decimal or >=3-digit integers, and fractions a/b)
for name in LESSONS:
    txt = lesson_text(name)
    for c in [x for x in sel if x["lesson"] == name]:
        blob = c["front"] + " " + c["back"] + " " + c.get("basis", "")
        toks = set(re.findall(r"\d+\.\d+(?:e-?\d+)?|\d{3,}(?:/\d+)?|\d+/\d{2,}|\d+e-\d+", blob))
        missing = []
        for t in toks:
            cand = [t, t.replace(".0", "")]
            if not any(x in txt for x in cand):
                missing.append(t)
        if missing:
            print(f"  {c['id']} {name}: numbers not found verbatim in lesson text: {sorted(missing)}")

# near-duplicate scan (token Jaccard on front+back), reported when >= 0.45
def toks(c: dict) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower())) - {
        "the", "a", "of", "is", "and", "to", "in", "for", "at", "it", "that", "does", "not", "by", "with", "this", "on", "as"}


print("near-duplicate pairs (Jaccard >= 0.45) within slice:")
for x, y in itertools.combinations(sel, 2):
    tx, ty = toks(x), toks(y)
    j = len(tx & ty) / max(1, len(tx | ty))
    if j >= 0.45:
        print(f"  {x['id']} vs {y['id']} J={j:.2f} | {x['front'][:70]} || {y['front'][:70]}")

# basis strings of graded cards vs key-results rows (reported for review; substance compared by reading)
for name in LESSONS:
    raw = open(ROOT + name + ".html", encoding="utf-8").read()
    rows = re.findall(r"<tr><td>(.*?)</td><td><span class=\"grade\" data-grade=\"(\w)\"></span></td><td>(.*?)</td></tr>", raw, flags=re.S)
    rows2 = re.findall(r"<tr><td>(.*?)</td><td><span class=\"grade\" data-grade=\"(\w)\">\w</span></td><td>(.*?)</td></tr>", raw, flags=re.S)
    rows = rows2 or rows
    for c in [x for x in sel if x["lesson"] == name and "basis" in x]:
        print(f"  {c['id']} grade {c['grade']} basis: {c['basis']!r}")
    for r in rows:
        if r[1] == "C":
            print(f"  {name} key-row C source: {html.unescape(r[2])[:150]!r}")
