"""E4 slice a, delta round 1: card structure, duplicates, and card numbers present in the card's lesson.

Run from the checkout root: .venv/bin/python ledgers/E4/scripts/E4-a-r1/cards_check.py
Reads course/modules/E/E4/cards.json and the lesson pages; prints one line per card with its lesson, the
numeric tokens of front and back, and whether each token occurs in the lesson's visible text (tags stripped,
entities unescaped). Tokens are fractions a/b, decimals, and integers of two or more digits.
"""
from __future__ import annotations

import collections
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E4 = ROOT / "course/modules/E/E4"
cards = json.loads((E4 / "cards.json").read_text(encoding="utf-8"))
print("cards", len(cards))
ids = collections.Counter(c["id"] for c in cards)
print("duplicate ids", [k for k, v in ids.items() if v > 1])
fb = collections.Counter((c["front"], c["back"]) for c in cards)
print("duplicate front+back", [k[0][:60] for k, v in fb.items() if v > 1])
fr = collections.Counter(c["front"] for c in cards)
print("duplicate fronts", [k[:60] for k, v in fr.items() if v > 1])
req = {"id", "lesson", "front", "back"}
for c in cards:
    missing = req - set(c)
    if missing:
        print("MISSING FIELDS", c["id"], missing)
    if c.get("grade") not in (None, "T", "C", "A", "B", "D", "X"):
        print("BAD GRADE", c["id"], c.get("grade"))
    if "grade" in c and "basis" not in c:
        print("NO BASIS", c["id"])
pages: dict[str, str] = {}
for lesson in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "L09"):
    raw = (E4 / f"{lesson}.html").read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)))
    text = re.sub(r"\\[td]?frac\{(\d+)\}\{(\d+)\}", r"\1/\2", text)
    text = re.sub(r"\\[td]?frac(\d)(\d+)", r"\1/\2", text)
    pages[lesson] = re.sub(r"\s+", " ", text)
tok = re.compile(r"\b\d+/\d+\b|\b\d+\.\d+(?:e-?\d+)?\b|\b\d{2,}\b")
only = set(sys.argv[1:]) or {"L01", "L02", "L03"}
for c in cards:
    if c["lesson"] not in only:
        continue
    for field in ("front", "back"):
        for t in sorted(set(tok.findall(c[field]))):
            present = t in pages[c["lesson"]]
            if not present:
                print(f"ABSENT {c['id']} {c['lesson']} {field} token {t!r}")
    print("CARD", c["id"], c["lesson"], c.get("grade"), "|", c["front"][:110], "|", c["back"][:200])
