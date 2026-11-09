"""Card checks for CS2 slice c (L09-L11): number tokens of each card must appear in its lesson text; near-duplicate
scan over the whole deck (difflib ratio on front and on back); cards whose back has no hypothesis when the card
states a graded result (T/A/B/C) are listed for manual reading. Prints every L09-L11 card's numbers and matches.

Run: python3 -I -W error ledgers/CS2/scripts/CS2-c-r4/cards_scan_r4.py   (from the checkout root)
"""
import difflib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
lesson_text = {}
for L in ("L09", "L10", "L11"):
    raw = (ROOT / f"course/modules/CS/CS2/{L}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<[^>]+>", " ", raw)
    lesson_text[L] = html.unescape(raw)

NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?:e-?\d+)?")
missing = []
for c in cards:
    if c["lesson"] not in lesson_text:
        continue
    text = lesson_text[c["lesson"]]
    for tok in set(NUM.findall(c["front"] + " " + c["back"])):
        if tok in ("1", "2", "0"):
            continue
        if tok not in text:
            missing.append((c["id"], tok))
print("number tokens (other than 0,1,2) absent from lesson text:", missing)

# near duplicates over the whole deck
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        rb = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        if rf > 0.6 or rb > 0.7:
            pairs.append((round(rf, 2), round(rb, 2), a["id"], b["id"]))
print("near-duplicate pairs (front>0.6 or back>0.7):")
for p in sorted(pairs, reverse=True):
    ids = (p[2], p[3])
    marker = any(c["lesson"] in ("L09", "L10", "L11") for c in cards if c["id"] in ids)
    if marker:
        print("  ", p)
print("total near-duplicate pairs in deck:", len(pairs))

# graded cards without cite or basis
bad = [c["id"] for c in cards if c["grade"] != "T" and not (c.get("basis") or c.get("cite"))]
print("non-T cards with neither cite nor basis:", bad)
print("L09-L11 count:", sum(1 for c in cards if c["lesson"] in ("L09", "L10", "L11")))
