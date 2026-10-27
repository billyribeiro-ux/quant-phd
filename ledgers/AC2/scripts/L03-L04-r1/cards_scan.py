"""Duplicate and schema scan of course/modules/AC/AC2/cards.json (run: python -I -W error <this file> <checkout>)."""
import difflib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/AC/AC2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("keys seen:", sorted({k for c in cards for k in c}))
bad = [c["id"] for c in cards if not c.get("front") or not c.get("back")]
print("empty front/back:", bad)
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        r1 = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        r2 = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
        if r1 >= 0.75 or r2 >= 0.75 or a["front"] == b["front"]:
            pairs.append((round(r1, 2), round(r2, 2), a["id"], b["id"]))
print("near-duplicate pairs (front>=0.75 or back>=0.75):", len(pairs))
for p in pairs:
    print(p)
l34 = [c for c in cards if c.get("lesson") in ("L03", "L04")]
print("L03/L04 ids:", [c["id"] for c in l34][:3], "...", len(l34))
