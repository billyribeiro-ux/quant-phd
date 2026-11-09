"""Round-2: full duplicate scan of course/modules/CS/CS2/cards.json (all lessons), plus near-duplicate fronts."""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
print("cards:", len(cards))
print("duplicate ids:", [k for k, v in Counter(c["id"] for c in cards).items() if v > 1])


def norm(s):
    return re.sub(r"\W+", " ", s.lower()).strip()


fronts = defaultdict(list)
backs = defaultdict(list)
for c in cards:
    fronts[norm(c["front"])].append(c["id"])
    backs[norm(c["back"])].append(c["id"])
print("duplicate fronts:", [v for v in fronts.values() if len(v) > 1])
print("duplicate backs:", [v for v in backs.values() if len(v) > 1])
pairs = []
for i, a in enumerate(cards):
    ta = set(norm(a["front"]).split())
    for b in cards[i + 1:]:
        tb = set(norm(b["front"]).split())
        if ta and tb:
            j = len(ta & tb) / len(ta | tb)
            if j >= 0.5:
                pairs.append((round(j, 2), a["id"], b["id"]))
print("front pairs with token Jaccard >= 0.5 (checked by reading: different quantities):", sorted(pairs, reverse=True))
