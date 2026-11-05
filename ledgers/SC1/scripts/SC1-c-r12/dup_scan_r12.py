"""Near-duplicate scan of SC1 cards.json fronts (token Jaccard), all pairs; prints pairs at or above a threshold.

Usage: python -I dup_scan_r12.py <cards.json> [threshold]
"""
import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
def toks(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))
sets = [(c["id"], c["lesson"], toks(c["front"] + " " + c["back"])) for c in cards]
exact = {}
for c in cards:
    exact.setdefault(c["front"].strip(), []).append(c["id"])
print("cards:", len(cards), " exact duplicate fronts:", [v for v in exact.values() if len(v) > 1])
pairs = []
for i in range(len(sets)):
    for j in range(i + 1, len(sets)):
        a, b = sets[i][2], sets[j][2]
        jac = len(a & b) / len(a | b) if a | b else 0.0
        if jac >= thr:
            pairs.append((round(jac, 3), sets[i][0], sets[i][1], sets[j][0], sets[j][1]))
for p in sorted(pairs, reverse=True):
    print("NEAR", p)
print("pairs >= threshold:", len(pairs))
