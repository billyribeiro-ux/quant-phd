"""Round-3 slice b: full duplicate scan of cards.json (all 208 cards) and card-id/lesson inventory.

Two cards are flagged when their normalised front+back token sets have Jaccard >= 0.45, or when their fronts
are identical after normalisation, or when a back is a substring of another card's back. Run from the checkout root.
"""
import itertools
import json
import re
from collections import Counter

cards = json.load(open("course/modules/M/M3/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "distinct ids:", len(set(ids)))
dup_ids = [i for i, n in Counter(ids).items() if n > 1]
print("duplicate ids:", dup_ids)
print("lesson counts:", dict(sorted(Counter(c["lesson"] for c in cards).items())))
print("ids c101,c102,c176,c177:", [(c["id"], c["lesson"], c["front"][:90]) for c in cards if c["id"] in ("M3-c101", "M3-c102", "M3-c176", "M3-c177")])
slice_ids = {c["id"] for c in cards if c["lesson"] in ("L04", "L05", "L06")}
print("slice card count (L04-L06):", len(slice_ids))


def norm(s: str) -> str:
    s = re.sub(r"\\[a-zA-Z]+", " ", s.lower())
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


def toks(c: dict) -> set:
    return set(norm(c["front"] + " " + c["back"]).split())


flags = []
for a, b in itertools.combinations(cards, 2):
    ta, tb = toks(a), toks(b)
    jac = len(ta & tb) / max(1, len(ta | tb))
    same_front = norm(a["front"]) == norm(b["front"])
    if jac >= 0.45 or same_front:
        flags.append((round(jac, 3), same_front, a["id"], a["lesson"], b["id"], b["lesson"]))
flags.sort(reverse=True)
print("flagged pairs (jaccard>=0.45 or same front):", len(flags))
for f in flags:
    involves_slice = (f[2] in slice_ids) or (f[4] in slice_ids)
    print("PAIR", f, "SLICE" if involves_slice else "")
