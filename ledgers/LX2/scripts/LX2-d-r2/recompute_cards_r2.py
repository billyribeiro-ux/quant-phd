"""Independent recomputation of the numbers on the LX2 cards (round 2), from the twin printouts and from first principles.

Usage: python3 -I recompute_cards_r2.py <L03 twin output> <L04 twin output>
"""
import re
import sys
from fractions import Fraction
from itertools import product

# --- L04 Part A table, read from the twin printout (rows "t forecast realised error hit") ---
l04 = open(sys.argv[2], encoding="utf-8").read().splitlines()
rows = []
for ln in l04:
    m = re.match(r"^\s*(\d+)\s+(\d+)\s+(\d+)\s+(-?\d+)\s+([01])\s*$", ln)
    if m:
        t, f, r, e, h = map(int, m.groups())
        rows.append((t, f, r, e, h))
assert len(rows) == 24, len(rows)
errs = [f - r for (_, f, r, _, _) in rows]
assert all(errs[i] == rows[i][3] for i in range(24)), "printed error column disagrees with forecast - realised"
hits = [1 if abs(e) <= 2 else 0 for e in errs]
assert hits == [h for (*_, h) in rows], "printed hit column disagrees with |e| <= 2"
print("L04 Part A: n =", len(errs), "hits =", sum(hits), "sum of errors =", sum(errs))
print("  hit rate =", Fraction(sum(hits), 24), "bias =", Fraction(sum(errs), 24))
def disp(x):
    s = -1 if x < 0 else 1
    units = int((abs(x) * 10**4 + Fraction(1, 2)) // 1)  # floor(|x| 10^4 + 1/2)
    return f"{'-' if s < 0 else ''}{units // 10**4}.{units % 10**4:04d}"
print("  displayed: hit", disp(Fraction(sum(hits), 24)), "bias", disp(Fraction(sum(errs), 24)))
print("  first 12 errors sum:", sum(errs[:12]), "last 12 errors sum:", sum(errs[12:]))
print("  first12 hits", sum(hits[:12]), "last12 hits", sum(hits[12:]), "| periods with hits:", [rows[i][0] for i in range(24) if hits[i]])
# Part C hand path
pc = [3, -3, 3, -3]
print("L04 Part C: bias", Fraction(sum(pc), 4), "hit rate", Fraction(sum(1 for e in pc if abs(e) <= 2), 4),
      "MAE", Fraction(sum(abs(e) for e in pc), 4))
# Proposition 4.4 enumeration over (V, U): e = 1 + V - U, V in -4..4, U in -6..6
pairs = [1 + v - u for v, u in product(range(-4, 5), range(-6, 7))]
print("Prop 4.4: pairs", len(pairs), "hits", sum(1 for e in pairs if abs(e) <= 2),
      "P(hit)", Fraction(sum(1 for e in pairs if abs(e) <= 2), len(pairs)), "~", float(Fraction(44, 117)),
      "E[e]", Fraction(sum(pairs), len(pairs)))
print("  disp P(hit) 44/117:", disp(Fraction(44, 117)))
# Theorem 4.3 equality check on a few windows (sanity): all same sign -> equality
# --- L03 ratio table (read from twin printout) ---
l03 = open(sys.argv[1], encoding="utf-8").read().splitlines()
tab = []
for ln in l03:
    m = re.match(r"^(\d)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\S+)\s+(yes|no|undefined)\s*$", ln)
    if m:
        tab.append(m.groups())
ratios = {int(t[0]): Fraction(int(t[3]), int(t[4])) for t in tab}
print("L03 ratios:", {k: str(v) for k, v in ratios.items()})
print("largest ratio:", max(ratios.values()), "flagged at D=2:", [k for k, v in ratios.items() if v > 2])
print("3*97 =", 3 * 97, "6*104 =", 6 * 104, "3/104 < 6/97:", Fraction(3, 104) < Fraction(6, 97))
print("17/50 vs 21/37 cross:", 21 * 50, 17 * 37, "| 5/34 vs 6/29 cross:", 5 * 29, 6 * 34)
print("L03 identity check from printed totals: G-less check: traded 4060 = 2*executions? executions 207 -> shares traded", 4060, "fills total 414 == 2*207:", 414 == 2 * 207)
print("G = R + 2X + Cm + Ct example (lesson M3): 1000-120-600-40 =", 1000 - 120 - 600 - 40)
