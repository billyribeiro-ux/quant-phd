"""Round 5 delta check of the prose numbers changed since round 4 (CS2 slice a, pages L01-L04).

Usage: python3 -I ledgers/CS2/scripts/CS2-a-r5/r5_delta_numbers.py <dir with twin outputs>
Reads the twin outputs written by `python3 -I -W error tests/labs/CS2/lab-CS2-L0n-1.py`
(files twin_L0n.out) and recomputes every changed prose number from the printed integers.
Nothing is read from the pages.
"""

import pathlib
import re
import sys
from fractions import Fraction

out_dir = pathlib.Path(sys.argv[1])

# ---- L03: parse the heap / sorted-list rows
rows = {}
for line in (out_dir / "twin_L03.out").read_text().splitlines():
    m = re.match(
        r"N=\s*(\d+) operations=\s*(\d+) heap comparisons=\s*(\d+) heap moves=\s*(\d+) "
        r"sorted-list comparisons=\s*(\d+) sorted-list moves=\s*(\d+)",
        line,
    )
    if m:
        n, ops, hc, hm, lc, lm = map(int, m.groups())
        rows[n] = dict(ops=ops, hc=hc, hm=hm, lc=lc, lm=lm)
print("L03 sizes:", sorted(rows))
print("L03 N=16 list total", rows[16]["lc"] + rows[16]["lm"], "heap total", rows[16]["hc"] + rows[16]["hm"])
print("L03 N=128 list total", rows[128]["lc"] + rows[128]["lm"], "heap total", rows[128]["hc"] + rows[128]["hm"])
print("L03 N=256 list total", rows[256]["lc"] + rows[256]["lm"], "heap total", rows[256]["hc"] + rows[256]["hm"])
first_total = next(n for n in sorted(rows) if rows[n]["hc"] + rows[n]["hm"] < rows[n]["lc"] + rows[n]["lm"])
first_moves = next(n for n in sorted(rows) if rows[n]["hm"] < rows[n]["lm"])
print("L03 first size heap total smaller:", first_total, " first size heap moves smaller:", first_moves)
print("L03 4096 heap cmp / ops =", Fraction(rows[4096]["hc"], rows[4096]["ops"]), "=", float(Fraction(rows[4096]["hc"], rows[4096]["ops"])))
print("L03 4096 list cmp / insertions (2N) =", Fraction(rows[4096]["lc"], 2 * 4096), "=", float(Fraction(rows[4096]["lc"], 2 * 4096)))
print("L03 2N(N+1) at 4096 =", 2 * 4096 * 4097, " list moves / bound =", float(Fraction(rows[4096]["lm"], 2 * 4096 * 4097)))
print("L03 6N floor(log2 N) at 4096 =", 6 * 4096 * 12, " margin =", 6 * 4096 * 12 - rows[4096]["hc"])
ks = sorted(rows)
list_ratios = {b: rows[b]["lm"] / rows[a]["lm"] for a, b in zip(ks, ks[1:])}
heap_move_ratios = {b: rows[b]["hm"] / rows[a]["hm"] for a, b in zip(ks, ks[1:])}
heap_cmp_ratios = {b: rows[b]["hc"] / rows[a]["hc"] for a, b in zip(ks, ks[1:])}
rng = [n for n in ks if n >= 128]  # rows N = 64 to 4096 are the ratio rows from 64 on
sel = [n for n in ks if n >= 64]
print("L03 list-move ratios N=64..4096: min %.4f (N=%d), max %.4f (N=%d)" % (
    min(list_ratios[n] for n in sel), min(sel, key=lambda n: list_ratios[n]),
    max(list_ratios[n] for n in sel), max(sel, key=lambda n: list_ratios[n])))
print("L03 heap-move ratios N=64..4096: min %.4f (N=%d), max %.4f (N=%d)" % (
    min(heap_move_ratios[n] for n in sel), min(sel, key=lambda n: heap_move_ratios[n]),
    max(heap_move_ratios[n] for n in sel), max(sel, key=lambda n: heap_move_ratios[n])))
print("L03 heap-cmp ratios N=64..4096: min %.4f, max %.4f" % (
    min(heap_cmp_ratios[n] for n in sel), max(heap_cmp_ratios[n] for n in sel)))
print("L03 heap-cmp ratios N=512..4096: min %.4f, max %.4f" % (
    min(heap_cmp_ratios[n] for n in ks if n >= 512), max(heap_cmp_ratios[n] for n in ks if n >= 512)))
print("L03 N=128 list moves 4514 vs heap 4933; N=256 list 17663 vs heap 10623; N=64 list 1002 vs 2209")
print("L03 4514/1002 =", round(4514 / 1002, 4), " 21095/10623 =", round(21095 / 10623, 4))

# ---- L02: parse averages and recompute totals from the printed four-decimal values
s = (out_dir / "twin_L02.out").read_text()
succ = re.findall(r"n=\s*(\d+) successful average probes=([\d.]+)", s)
unsucc = re.findall(r"unsuccessful average probes=([\d.]+)", s)
print("L02 successful rows", succ)
for n, v in succ:
    n = int(n)
    lo, hi = Fraction(v) - Fraction(5, 100000), Fraction(v) + Fraction(5, 100000)
    cands = [t for t in range(0, 100000) if lo <= Fraction(t, n) < hi]
    print("L02 n=%d printed %s -> integer totals in printed interval: %s" % (n, v, cands))
for v, n_abs in zip(unsucc, [500] * 5):
    lo, hi = Fraction(v) - Fraction(5, 100000), Fraction(v) + Fraction(5, 100000)
    cands = [t for t in range(0, 100000) if lo <= Fraction(t, n_abs) < hi]
    print("L02 unsuccessful printed %s -> totals over 500 in interval: %s" % (v, cands))
print("L02 257/128 =", Fraction(257, 128), "193/64 =", Fraction(193, 64), "772/256 =", Fraction(772, 256),
      "increase =", Fraction(193, 64) - Fraction(257, 128))
print("L02 successful gaps:", [str(Fraction(t, n) - (1 + Fraction(n - 1, 128))) for t, n in [(16, 16), (37, 32), (97, 64), (257, 128), (772, 256)]])
print("L02 unsuccessful gaps:", [str(Fraction(t, 500) - a) for t, a in [(134, Fraction(1, 4)), (270, Fraction(1, 2)), (548, 1), (1016, 2), (2014, 4)]])

# ---- L04: Part A and Part B values quoted in prose
print("L04 262431/8886 =", round(262431 / 8886, 5), " 5120/8770 =", round(5120 / 8770, 6), " 8886*29 =", 8886 * 29)
print("L04 (1000/2)log2 500 =", round(500 * __import__('math').log2(500), 4))
