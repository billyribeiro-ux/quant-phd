"""Mechanical scan of LX2 cards.json against the lesson pages (run as: python3 -I cards_mech.py <checkout>).

Checks: schema; unique ids and fronts; per-lesson counts; grade counts; Dodd/MiFID mentions; cite keys in the
registry; every number token (fractions and integers of 2+ digits) in a card's front or back occurs in its lesson.
"""

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
lx = root / "course/modules/LX/LX2"
cards = json.loads((lx / "cards.json").read_text(encoding="utf-8"))
refs = {e["key"] for e in json.loads((root / "references/references.json").read_text(encoding="utf-8"))["entries"]}
lesson_text = {}
for L in ("L01", "L02", "L03", "L04"):
    raw = (lx / f"{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    lesson_text[L] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
ALLOWED = {"id", "lesson", "front", "back", "cite", "grade", "basis"}
problems = []
ids = Counter(c["id"] for c in cards)
print("cards:", len(cards), "unique ids:", len(ids))
for k, v in ids.items():
    if v > 1:
        problems.append(f"duplicate id {k}")
fronts = Counter(c["front"].strip().lower() for c in cards)
backs = Counter(c["back"].strip().lower() for c in cards)
for f, v in fronts.items():
    if v > 1:
        problems.append(f"duplicate front: {f[:60]}")
for b, v in backs.items():
    if v > 1:
        problems.append(f"duplicate back: {b[:60]}")
print("per lesson:", dict(Counter(c["lesson"] for c in cards)))
print("grades:", dict(Counter(c.get("grade", "none") for c in cards)))
for c in cards:
    extra = set(c) - ALLOWED
    if extra:
        problems.append(f"{c['id']} extra fields {extra}")
    if not c.get("front") or not c.get("back") or c.get("lesson") not in lesson_text:
        problems.append(f"{c['id']} missing field or lesson")
    for k in c.get("cite", []):
        if k not in refs:
            problems.append(f"{c['id']} cite {k} not in registry")
    blob = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    if re.search(r"dodd|mifid", blob, flags=re.I):
        problems.append(f"{c['id']} mentions Dodd-Frank or MiFID II")
    # number tokens must occur in the card's own lesson
    lt = lesson_text[c["lesson"]].replace("−", "-")
    for tok in set(re.findall(r"\b\d+/\d+\b|\b\d{2,}\b", c["front"] + " " + c["back"])):
        if (
            tok not in lt
            and tok not in lesson_text["L01"] + lesson_text["L02"] + lesson_text["L03"] + lesson_text["L04"]
        ):
            problems.append(f"{c['id']} number {tok} not found in any lesson text")
        elif tok not in lt:
            problems.append(f"{c['id']} number {tok} found only outside its lesson {c['lesson']}")
print("problems:", len(problems))
for p in problems:
    print(" -", p)
