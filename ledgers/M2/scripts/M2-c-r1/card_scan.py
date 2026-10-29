"""Verifier script (M2 slice c, round 1): full duplicate scan of cards.json and card-count check for L13-L18."""

import collections
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(" ".join(c["front"].lower().split()) for c in cards)
backs = collections.Counter(" ".join(c["back"].lower().split()) for c in cards)
print("cards total:", len(cards))
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
for n in range(13, 19):
    print(f"L{n:02d} cards:", sum(1 for c in cards if c["lesson"] == f"L{n:02d}"))
