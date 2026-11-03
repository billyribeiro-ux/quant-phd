"""Round-2 slice-a card scan: duplicate ids, fronts and backs over all cards, and per-lesson counts for L01-L04."""

import collections
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards))
print("duplicate ids", [k for k, v in collections.Counter(ids).items() if v > 1])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
print("duplicate backs", [k[:60] for k, v in backs.items() if v > 1])
for lesson in ("L01", "L02", "L03", "L04"):
    sel = [c["id"] for c in cards if c["lesson"] == lesson]
    print(lesson, len(sel), " ".join(sel))
for cid in ("M4-c084", "M4-c219", "M4-c220"):
    c = next(x for x in cards if x["id"] == cid)
    print(cid, "|", c["front"], "|", c["back"][:120])
