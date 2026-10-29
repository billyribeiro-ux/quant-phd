"""Duplicate scan of M2 retrieval cards (verifier round 1, slice M2-b).

Flags exact duplicate fronts or backs, and pairs of fronts whose token Jaccard similarity is >= 0.6.
Run: .venv/bin/python -I ledgers/M2/scripts/M2-b-r1/card_dupes.py
"""

from __future__ import annotations

import json
import re
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))


def toks(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))


exact_front: dict[str, list[str]] = {}
exact_back: dict[str, list[str]] = {}
for c in cards:
    exact_front.setdefault(c["front"].strip().lower(), []).append(c["id"])
    exact_back.setdefault(c["back"].strip().lower(), []).append(c["id"])
print("cards:", len(cards))
print("exact duplicate fronts:", [v for v in exact_front.values() if len(v) > 1])
print("exact duplicate backs:", [v for v in exact_back.values() if len(v) > 1])
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = toks(cards[i]["front"]), toks(cards[j]["front"])
        if not a or not b:
            continue
        jac = len(a & b) / len(a | b)
        if jac >= 0.6:
            pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"], cards[i]["front"], cards[j]["front"]))
print("front pairs with Jaccard >= 0.6:", len(pairs))
for p in sorted(pairs, reverse=True)[:40]:
    print(p)
