"""Round 4: card integrity for the slice (ids, count, grades, basis) and a near-duplicate scan over all 208 cards."""
import itertools
import json
import re
import sys

cards = json.load(open(sys.argv[1] + "/course/modules/M/M3/cards.json", encoding="utf-8"))
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}) == len(cards))
sl = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("slice", len(sl), {l: sum(c["lesson"] == l for c in sl) for l in ("L04", "L05", "L06")})
for c in sl:
    if c.get("grade") == "C" and not c.get("basis"):
        print("C without basis", c["id"])
print("grade counts (slice)", {g: sum(c.get("grade") == g for c in sl) for g in ("T", "A", "B", "C", "D", "X", None)})


def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))


pairs = []
for a, b in itertools.combinations(cards, 2):
    ta = toks(a["front"] + " " + a["back"])
    tb = toks(b["front"] + " " + b["back"])
    j = len(ta & tb) / max(1, len(ta | tb))
    if j >= 0.5:
        pairs.append((round(j, 2), a["id"], b["id"]))
print("pairs with token Jaccard >= 0.5:", len(pairs))
for p in sorted(pairs, reverse=True):
    print(p)
