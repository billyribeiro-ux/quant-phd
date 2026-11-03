"""Mechanical card checks (round 2, slice e): number presence in the card's own lesson text, near-duplicate
fronts or backs across all 170 cards, lesson-reference names (Definition/Theorem/Proposition/Lemma/Remark/
Example/Problem/Lab) in each card that must exist in the same lesson text.

Usage: python3 -I card_checks_r2.py <cards.json> <lesson-text-dir>
"""
import difflib
import json
import re
import sys
from pathlib import Path

cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
tdir = Path(sys.argv[2])
texts = {p.stem: p.read_text(encoding="utf-8") for p in tdir.glob("L0*.txt")}
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}))

NUM = re.compile(r"(?<![A-Za-z_])(\d+(?:[./]\d+)?)(?![\w])")
missing = []
for c in cards:
    txt = texts[c["lesson"]]
    for tok in set(NUM.findall(c["back"] + " " + c["front"])):
        if tok in ("1", "0", "2"):
            continue
        if tok not in txt:
            missing.append((c["id"], tok))
print("numbers in card text absent from its lesson text (token-level, excluding 0,1,2):", len(missing))
for m in missing:
    print("  ", m)

REF = re.compile(r"\b(Definition|Theorem|Proposition|Lemma|Remark|Example|Problem|Corollary)\s+([0-9]+(?:\.[0-9]+)?[a-z]?)")
badrefs = []
for c in cards:
    txt = texts[c["lesson"]]
    for kind, num in set(REF.findall(c["back"] + " " + c["front"])):
        pat = f"{kind} {num}"
        if pat not in txt and not (kind in ("Problem",) and f"{num} ·" in txt):
            # Problem labels appear as 'M1 ·', 'P1 ·', 'E1 ·', 'R1 ·'
            badrefs.append((c["id"], c["lesson"], pat))
print("references in card text not found verbatim in its lesson:", len(badrefs))
for b in badrefs:
    print("  ", b)

# near-duplicate fronts/backs
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        r1 = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        r2 = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if r1 > 0.75 or r2 > 0.75:
            pairs.append((a["id"], b["id"], round(r1, 2), round(r2, 2)))
print("near-duplicate pairs (front or back ratio > 0.75):", len(pairs))
for p in pairs:
    print("  ", p)

# per-lesson card counts and grade counts
from collections import Counter
print("per lesson", sorted(Counter(c["lesson"] for c in cards).items()))
print("grades", Counter(c["grade"] for c in cards))
print("C cards without basis", [c["id"] for c in cards if c["grade"] == "C" and not str(c.get("basis", "")).strip()])
print("T cards with a basis field", [c["id"] for c in cards if c["grade"] == "T" and c.get("basis")])
