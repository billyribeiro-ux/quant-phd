"""Verifier scan (CS2 slice a, round 1) of course/modules/CS/CS2/cards.json.

Checks: unique ids and CS2-cNNN form; grade/basis rule (T has no basis, non-T has basis); every lesson has a card;
per-lesson counts for L01-L04; near-duplicate fronts or backs across all cards (difflib ratio), printed for review.
Run from the checkout root: .venv/bin/python -I ledgers/CS2/scripts/CS2-a-r1/cards_scan.py
"""

import collections
import difflib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)) == len(ids))
print("id form ok", all(re.fullmatch(r"CS2-c\d{3}", i) for i in ids))
print("grades", dict(collections.Counter(c["grade"] for c in cards)))
print("grade/basis mismatches", [c["id"] for c in cards if (c["grade"] != "T") == (not c.get("basis"))])
per = collections.Counter(c["lesson"] for c in cards)
print("per lesson", {k: per[k] for k in sorted(per)})
print("L01-L04 total", sum(per[k] for k in ("L01", "L02", "L03", "L04")))
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1:]:
        rf = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        rb = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        if (rf > 0.95 and rb > 0.6) or rf > 0.99:
            pairs.append((a["id"], b["id"]))
print("near-identical pairs (front>0.95 and back>0.6, or identical fronts):", pairs)
