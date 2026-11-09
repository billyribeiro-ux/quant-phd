"""M2 slice a round 3: duplicate scan of cards.json (VERIFIER_RULES 2.7). Pairs with a slice card and similarity >= 0.6
on front or back, plus exact duplicate fronts across the unit. Run: python -I <this> <checkout-root>."""

from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

cards = json.loads((Path(sys.argv[1]) / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
slice_ids = {c["id"] for c in cards if c["lesson"] in {"L01", "L02", "L03", "L04", "L05", "L06"}}
fronts: dict[str, list[str]] = {}
for c in cards:
    fronts.setdefault(c["front"].strip().lower(), []).append(c["id"])
print("exact duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
ids = [c["id"] for c in cards]
print("duplicate ids:", sorted({i for i in ids if ids.count(i) > 1}))
pairs = 0
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        if a["id"] not in slice_ids and b["id"] not in slice_ids:
            continue
        rf = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        rb = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        if rf >= 0.6 or rb >= 0.6:
            pairs += 1
            print(f"{a['id']} ~ {b['id']} front={rf:.2f} back={rb:.2f} | {a['front'][:70]} || {b['front'][:70]}")
print("pairs listed:", pairs)
