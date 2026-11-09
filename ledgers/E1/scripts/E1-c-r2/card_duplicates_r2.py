"""Verifier E1-c round 2: Jaccard similarity of card fronts+backs, L07-L09 cards against all E1 cards."""
import json
import re
import sys
from pathlib import Path

cards = json.loads(Path(sys.argv[1], "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))


def toks(c):
    return set(re.findall(r"[a-z0-9]+", (c["front"] + " " + c["back"]).lower()))


pairs = []
mine = [c for c in cards if c["lesson"] in ("L07", "L08", "L09")]
for a in mine:
    for b in cards:
        if a["id"] >= b["id"] and b["lesson"] in ("L07", "L08", "L09"):
            continue
        if a["id"] == b["id"]:
            continue
        ta, tb = toks(a), toks(b)
        j = len(ta & tb) / len(ta | tb)
        if j > 0.45:
            pairs.append((round(j, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
for p in sorted(pairs, reverse=True):
    print(p)
print("pairs above 0.45:", len(pairs))
