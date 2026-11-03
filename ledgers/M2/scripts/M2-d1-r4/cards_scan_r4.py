"""Round-4 full scan of course/modules/M/M2/cards.json: unique ids, normalised duplicate fronts, and slice membership. Run with python3 -I."""
import json, re, sys
from collections import Counter
from pathlib import Path
root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
fronts = Counter(norm(c["front"]) for c in cards)
dups = [k for k, v in fronts.items() if v > 1]
print("normalised duplicate fronts:", len(dups))
slice_ids = {c["id"] for c in cards if c["lesson"] in ("L19", "L20", "L21")}
print("L19-L21 cards:", len(slice_ids), sorted(slice_ids)[0], "...", sorted(slice_ids)[-1])
for c in cards:
    if norm(c["front"]) in dups:
        print("duplicate:", c["id"], c["lesson"], "in slice" if c["id"] in slice_ids else "outside slice")
