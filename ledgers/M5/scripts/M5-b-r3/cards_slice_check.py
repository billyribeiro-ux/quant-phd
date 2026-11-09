"""Slice card inventory and duplicate scan for M5-b (L05-L07). Prints counts per lesson, the slice card ids,
and every slice card against all 236 cards with a difflib ratio above 0.7 on the fronts."""
import difflib
import json
from collections import Counter
from pathlib import Path

cards = json.loads(Path("course/modules/M/M5/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "duplicate ids", sorted({i for i in ids if ids.count(i) > 1}))
print("cards by lesson", dict(sorted(Counter(c["lesson"] for c in cards).items())))
slice_cards = [c for c in cards if c["lesson"] in ("L05", "L06", "L07")]
print("slice cards", len(slice_cards), dict(sorted(Counter(c["lesson"] for c in slice_cards).items())))
print("slice ids", " ".join(c["id"] for c in slice_cards))
print("graded slice cards without basis:", [c["id"] for c in slice_cards if c.get("grade") and not c.get("basis")])
print("ungraded slice cards with basis:", [c["id"] for c in slice_cards if not c.get("grade") and c.get("basis")])
hits = []
for a in slice_cards:
    for b in cards:
        if a["id"] == b["id"]:
            continue
        r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        if r > 0.7:
            hits.append((round(r, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
hits.sort(reverse=True)
print("pairs above 0.7:", len(hits))
for h in hits:
    print(h)
