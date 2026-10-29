"""Round-3 card checks for CF8 (slice c): duplicate scan, id/lesson/grade fields, theorem and remark labels cited on each card
that do not appear in its lesson, and every number on a card back that appears in no lesson text (small integers excluded).

Usage: .venv/bin/python ledgers/CF8/scripts/CF8-c-r3/cards_r3_check.py
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
UNIT = ROOT / "course" / "modules" / "CF" / "CF8"
cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))

plain: dict[str, str] = {}
for lesson in ("L01", "L02", "L03", "L04", "L05"):
    raw = (UNIT / f"{lesson}.html").read_text(encoding="utf-8")
    plain[lesson] = html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("{,}", ",")

print("cards:", len(cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
print("lessons:", Counter(c["lesson"] for c in cards))
print("grades:", Counter(c.get("grade") for c in cards))

labels = re.compile(r"\b(Theorem|Proposition|Corollary|Definition|Remark|Example|Lemma|Problem|Assumption|Convention|Misconception|Section|Lab)\s+(\d+(?:\.\d+)?|\d+\.\d+\([a-z]\))")
bad_labels = []
for c in cards:
    src = plain[c["lesson"]]
    for m in labels.finditer(c["back"] + " " + c["front"]):
        kind, num = m.group(1), m.group(2)
        pat = f"{kind} {num}"
        if pat not in src and pat not in src.replace(" ", " "):
            bad_labels.append((c["id"], c["lesson"], pat))
print("cited labels not in cited lesson:", bad_labels)

missing = []
for c in cards:
    src = plain[c["lesson"]]
    for number in re.findall(r"\d[\d,]*(?:\.\d+)?", c["back"] + " " + c["front"]):
        bare = number.replace(",", "").rstrip(".")
        if bare in {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12", "13", "14", "20", "30", "45", "50", "60", "90", "100", "365"}:
            continue
        if number.rstrip(".") not in src and bare not in src:
            missing.append((c["id"], c["lesson"], number))
print("numbers in card text found in no cited lesson:", missing)
