"""Verifier round 4 (E5 slice b): duplicate scan of all E5 retrieval cards and listing of the L04-L06 cards.

Usage: python3 -I ledgers/E5/scripts/E5-b-r4/cards_check_r4.py <checkout_root>
"""
import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1]).resolve()
cards = json.loads((root / "course/modules/E/E5/cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
print("lesson counts:", dict(Counter(c["lesson"] for c in cards)))
print("duplicate ids:", [k for k, v in Counter(c["id"] for c in cards).items() if v > 1])
print("duplicate fronts:", [k for k, v in Counter(c["front"] for c in cards).items() if v > 1])
for c in cards:
    if c["lesson"] in ("L04", "L05", "L06"):
        print(json.dumps(c, ensure_ascii=False))
