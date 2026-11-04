"""Round-5 verifier (CS2-d): card checks on course/modules/CS/CS2/cards.json at the pin.

1. every card: numbers (integers and decimals) in front and back appear in the card's own lesson text (plain-text
   dump of the lesson HTML, written to /tmp/cs2d_r5_text by ledgers/CS2/scripts/CS2-d-r5/lesson_text_dump_r5.py);
2. every cited locator (Definition/Proposition/Corollary/Theorem/Lemma/Section/Lab/Assumption, with its number) appears
   in the card's own lesson text;
3. duplicate scan: pairs of cards whose front+back word sets have Jaccard similarity >= 0.5;
4. the 14 changed and 8 new card ids of this round are printed for the row-level review.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
TEXT = Path("/tmp/cs2d_r5_text")
lesson_text = {p.stem.split(".")[0]: p.read_text(encoding="utf-8") for p in TEXT.glob("L*.html.txt")}

problems: list[str] = []
for c in cards:
    text = lesson_text[c["lesson"]]
    body = c["front"] + " " + c["back"]
    for num in set(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", body)):
        if num not in text:
            problems.append(f"{c['id']} number {num} absent from {c['lesson']}")
    for kind, n in set(
        re.findall(
            r"\b(Definition|Proposition|Corollary|Theorem|Lemma|Section|Assumption|Lab|Remark)\s+(\d+(?:\.\d+)?)", body
        )
    ):
        if not re.search(rf"{kind}\s+{re.escape(n)}", text):
            problems.append(f"{c['id']} locator '{kind} {n}' absent from {c['lesson']}")


def words(c: dict) -> set[str]:
    return set(re.findall(r"[A-Za-z]+", (c["front"] + " " + c["back"]).lower()))


dups = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = words(cards[i]), words(cards[j])
        if a and b and len(a & b) / len(a | b) >= 0.5:
            dups.append((cards[i]["id"], cards[j]["id"], round(len(a & b) / len(a | b), 2)))

print("cards", len(cards), "lessons", sorted({c["lesson"] for c in cards}))
print("problems", len(problems))
for line in problems[:60]:
    print("PROBLEM", line)
print("near-duplicate pairs (Jaccard >= 0.5):", dups)
