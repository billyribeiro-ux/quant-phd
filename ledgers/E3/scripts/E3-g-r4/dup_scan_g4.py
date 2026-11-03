"""Near-duplicate scan of the E3 cards (stdlib only): token Jaccard on front+back and on back alone.

Usage: python -I dup_scan_g4.py <cards.json>
Lists every pair with Jaccard >= 0.35 on backs, or >= 0.5 on fronts, where at least one card is in L05-L08.
"""
import json
import re
import sys
from itertools import combinations

cards = json.load(open(sys.argv[1], encoding="utf-8"))
STOP = {"the", "a", "of", "and", "is", "to", "for", "in", "on", "at", "under", "with", "by", "as", "if", "that", "it",
        "its", "an", "does", "not", "this", "be", "or", "so", "from", "which", "what", "are", "was", "than"}


def toks(s: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in STOP}


def jac(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


def in_slice(c: dict) -> bool:
    return c["lesson"] in ("L05", "L06", "L07", "L08")


exact_f = [k for k, v in __import__("collections").Counter(c["front"].strip().lower() for c in cards).items() if v > 1]
exact_b = [k for k, v in __import__("collections").Counter(c["back"].strip().lower() for c in cards).items() if v > 1]
print("exact duplicate fronts:", exact_f)
print("exact duplicate backs:", exact_b)
n = 0
for a, b in combinations(cards, 2):
    if not (in_slice(a) or in_slice(b)):
        continue
    fb = jac(toks(a["back"]), toks(b["back"]))
    ff = jac(toks(a["front"]), toks(b["front"]))
    if fb >= 0.35 or ff >= 0.5:
        n += 1
        print(f"{a['id']}({a['lesson']}) ~ {b['id']}({b['lesson']}) back={fb:.2f} front={ff:.2f}")
        print(f"   F1: {a['front']}\n   F2: {b['front']}")
print("pairs listed:", n)
