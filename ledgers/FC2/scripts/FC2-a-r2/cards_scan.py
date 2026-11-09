"""FC2-a round 2: full scan of the L01-L03 cards in course/modules/FC/FC2/cards.json.

Reports: ids and duplicate ids; duplicate fronts or backs; token-Jaccard >= 0.5 pairs over all 167 cards; numeric tokens
on each L01-L03 card that do not occur in that card's lesson HTML (after unescape); graded cards without basis or cite;
T cards whose front names no hypothesis token (A1-A8, A3 etc.) as a hypothesis check aid.
Run: python3 -I ledgers/FC2/scripts/FC2-a-r2/cards_scan.py
"""

from __future__ import annotations

import html
import itertools
import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
MOD = os.path.join(ROOT, "course", "modules", "FC", "FC2")
cards = json.load(open(os.path.join(MOD, "cards.json"), encoding="utf-8"))
print("cards:", len(cards))
ids = [c["id"] for c in cards]
print("distinct ids:", len(set(ids)), "duplicate ids:", sorted({i for i in ids if ids.count(i) > 1}))
print("duplicate fronts:", sorted({c["front"] for c in cards if sum(d["front"] == c["front"] for d in cards) > 1}))
print("duplicate backs:", sorted({c["back"] for c in cards if sum(d["back"] == c["back"] for d in cards) > 1}))

tok = lambda s: set(re.findall(r"[a-z0-9]+", s.lower()))  # noqa: E731
pairs = []
for a, b in itertools.combinations(cards, 2):
    ta, tb = tok(a["front"] + " " + a["back"]), tok(b["front"] + " " + b["back"])
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.5:
        pairs.append((round(j, 2), a["id"], b["id"]))
print("token Jaccard >= 0.5 pairs:", sorted(pairs, reverse=True))

lesson_text = {}
for lesson in ("L01", "L02", "L03"):
    raw = open(os.path.join(MOD, lesson + ".html"), encoding="utf-8").read()
    lesson_text[lesson] = html.unescape(raw)

for c in cards:
    if c["lesson"] not in lesson_text:
        continue
    text = c["front"] + " " + c["back"]
    nums = re.findall(r"\d+(?:[.,]\d+)*", text)
    missing = [n for n in nums if n not in lesson_text[c["lesson"]] and n.replace(",", "") not in lesson_text[c["lesson"]]]
    if missing:
        print("number not in lesson:", c["id"], missing)
    if c.get("grade") in ("T", "A", "B", "C") and not (c.get("basis") or c.get("cite")):
        print("graded card without basis or cite:", c["id"], c.get("grade"))
    if c.get("grade") == "C" and c.get("basis") and "Lab" not in c["basis"] and "Problem" not in c["basis"]:
        print("C card basis without lab or problem:", c["id"], c["basis"])
    if c.get("grade") == "T" and re.search(r"\b(Assume|Under|under)\b", c["front"]) is None and re.search(r"\bA\d", c["back"]):
        print("T card cites an assumption in back but front has no hypothesis:", c["id"])

print("hypothesis-carrying fronts (contains 'A1', 'A3', 'A8', 'Under'):")
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03") and c.get("grade") == "T":
        has = bool(re.search(r"Under|A[1-8]|Assume|Example 3.4|bond at|market", c["front"]))
        print(f"  {c['id']} hyp_in_front={has} front={c['front'][:90]}")
