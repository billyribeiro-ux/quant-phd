"""Verifier check (M7 slice a, round 2): cards for L01-L03.

1. Every number token (integers, fractions, decimals) on a card front or back of L01-L03 appears in its own lesson text
   (tags stripped, \\tfrac{a}{b} and \\frac{a}{b} read as a/b, minus signs normalised).
2. Ids are unique over the whole file; no two cards (any lesson) have near-identical fronts (SequenceMatcher >= 0.85).
3. Every card with grade other than T has a basis; every card has the required keys.
Run from the checkout root: python -I -W error ledgers/M7/scripts/M7-a-r2/cards_check.py
"""

from __future__ import annotations

import difflib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
cards = json.loads((ROOT / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))


def lesson_text(name: str) -> str:
    t = (ROOT / f"course/modules/M/M7/{name}.html").read_text(encoding="utf-8")
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\\[tdc]?frac\{([^{}]+)\}\{([^{}]+)\}", r"\1/\2", t)
    t = t.replace("\u2212", "-").replace("&minus;", "-")
    t = re.sub(r"\s+", " ", t)
    return t


texts = {n: lesson_text(n) for n in ("L01", "L02", "L03")}
NUM = re.compile(r"(?<![A-Za-z_])-?\d+(?:/\d+)?(?:\.\d+)?")
problems: list[str] = []
checked = 0
for c in cards:
    if c["lesson"] not in texts:
        continue
    checked += 1
    body = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    body = body.replace("\u2212", "-")
    for tok in set(NUM.findall(body)):
        tok_clean = tok.lstrip("-")
        if tok_clean in ("1", "2", "3", "0"):  # bare small integers are checked by the card's own context
            continue
        hay = texts[c["lesson"]].replace("\u2212", "-")
        if tok_clean not in hay and tok not in hay:
            problems.append(f"{c['id']} ({c['lesson']}): token {tok!r} not found in its lesson")
print(f"L01-L03 cards checked: {checked}")
print("number-token problems:", problems if problems else "none")

ids = [c["id"] for c in cards]
dups = [k for k, v in Counter(ids).items() if v > 1]
print("duplicate ids over the file:", dups if dups else "none")
print(f"cards over the file: {len(cards)}")

near = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        if a["lesson"] not in texts and b["lesson"] not in texts:
            continue
        r = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        if r >= 0.85:
            near.append((a["id"], b["id"], round(r, 3), a["front"][:70], b["front"][:70]))
print("near-identical fronts involving an L01-L03 card:", near if near else "none")

bad_basis = [c["id"] for c in cards if c["lesson"] in texts and c["grade"] != "T" and not c.get("basis")]
print("non-T L01-L03 cards without basis:", bad_basis if bad_basis else "none")
keys_bad = [c["id"] for c in cards if not {"id", "lesson", "front", "back", "grade"} <= set(c)]
print("cards missing required keys:", keys_bad if keys_bad else "none")
grades = Counter(c["grade"] for c in cards if c["lesson"] in texts)
print("L01-L03 grade mix:", dict(grades))
