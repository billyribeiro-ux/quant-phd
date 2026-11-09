"""Verifier round 5: whole-deck duplicate scan of course/modules/E/E1/cards.json (exact and near-duplicates)."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
print("cards", len(cards))


def norm(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))


fronts = {}
for c in cards:
    key = " ".join(sorted(norm(c["front"])))
    fronts.setdefault(key, []).append(c["id"])
print("exact-duplicate fronts (token-sorted):", [v for v in fronts.values() if len(v) > 1])
backs = {}
for c in cards:
    backs.setdefault(c["back"], []).append(c["id"])
print("exact-duplicate backs:", [v for v in backs.values() if len(v) > 1])
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        sa, sb = norm(a["front"] + " " + a["back"]), norm(b["front"] + " " + b["back"])
        j = len(sa & sb) / len(sa | sb)
        if j >= 0.45:
            pairs.append((round(j, 3), a["id"], b["id"]))
print("near-duplicate pairs (Jaccard >= 0.45 on front+back tokens):")
for p in sorted(pairs, reverse=True):
    print(" ", p)
for c in cards:
    if c["id"] in ("E1-c088", "E1-c159", "E1-c160"):
        print(c["id"], c["lesson"], "|", c["front"], "|", c["back"])
