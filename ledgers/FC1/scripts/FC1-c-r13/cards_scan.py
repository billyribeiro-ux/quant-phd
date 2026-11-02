"""Round-12 scan of course/modules/FC/FC1/cards.json: count, keys, unique ids and fronts, duplicate backs, grades,
basis presence, and notation-sensitive tokens. Run from the checkout root with the repo venv interpreter."""

import collections
import json
import re
import sys
from pathlib import Path

path = Path("course/modules/FC/FC1/cards.json")
raw = path.read_text(encoding="utf-8")
cards = json.loads(raw)
print("cards:", len(cards))
keys = collections.Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets:", dict(keys))
ids = collections.Counter(c["id"] for c in cards)
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
backs = collections.Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [k for k, v in backs.items() if v > 1])
print("grades:", dict(collections.Counter(c.get("grade", "(none)") for c in cards)))
bad_basis = [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")]
print("C without basis:", bad_basis)
print("lessons:", dict(collections.Counter(c["lesson"] for c in cards)))
seq = [c["id"] for c in cards]
print("ids in order:", seq == sorted(seq), seq[0], seq[-1])
for pat in [r"\bQ\b", r"V_b", r"\\?\(", r"\bcard\b", r"\bthe lab\b"]:
    hits = [c["id"] for c in cards if re.search(pat, c["front"] + " " + c["back"])]
    print("pattern", pat, "->", len(hits), hits[:12])
