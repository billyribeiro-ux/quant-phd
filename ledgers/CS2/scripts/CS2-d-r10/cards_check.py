"""Mechanical checks on course/modules/CS/CS2/cards.json (verifier round 10)."""

from __future__ import annotations

import difflib
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CS2 = ROOT / "course" / "modules" / "CS" / "CS2"
cards = json.loads((CS2 / "cards.json").read_text(encoding="utf-8"))
print("type", type(cards).__name__, "entries", len(cards))
keysets = Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets", dict(keysets))
ids = [c["id"] for c in cards]
print("unique ids", len(set(ids)), "of", len(ids))
fronts = Counter(c["front"].strip() for c in cards)
print("duplicate fronts", [f for f, k in fronts.items() if k > 1])
grades = Counter(c["grade"] for c in cards)
print("grades", dict(grades))
print("C without basis", [c["id"] for c in cards if c["grade"] == "C" and not c.get("basis", "").strip()])
print("T with basis", [c["id"] for c in cards if c["grade"] == "T" and c.get("basis")])
lessons = Counter(c["lesson"] for c in cards)
print("per lesson", dict(sorted(lessons.items())))
missing = [L for L in sorted(lessons) if not (CS2 / f"{L}.html").exists()]
print("lesson pages missing", missing)
# near-duplicate fronts and backs
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        r = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        if r >= 0.8:
            pairs.append((round(r, 2), a["id"], b["id"]))
print("front pairs >=0.8 similarity", len(pairs))
for p in sorted(pairs, reverse=True)[:12]:
    print("  ", p)
bk = Counter(c["back"].strip() for c in cards)
print("duplicate backs", [(b[:60], k) for b, k in bk.items() if k > 1])
# numbers on the card must appear in its lesson
bad = []
text_cache: dict[str, str] = {}
for c in cards:
    L = c["lesson"]
    if L not in text_cache:
        text_cache[L] = html.unescape(re.sub(r"<[^>]+>", " ", (CS2 / f"{L}.html").read_text(encoding="utf-8")))
    nums = {n.rstrip(",") for n in re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?", c["back"] + " " + c["front"])}
    for n in nums:
        if n.replace(",", "") and n not in text_cache[L]:
            bad.append((c["id"], n))
print("card numbers not found verbatim in their lesson", len(bad), bad[:40])
