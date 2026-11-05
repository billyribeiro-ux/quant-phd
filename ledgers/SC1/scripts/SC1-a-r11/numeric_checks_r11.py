"""Independent recomputation of the SC1 slice-a numbers (round 11).

Covers: L02 E3 (seeded level-1 sup and bound), L03 standard-error gaps (key-results row, c187), L03 closed forms
(E2, E3, the 2.39 z value), the hub placement percentages, the rung-2 count 29 (reflection), 216 and 36 counts,
and the 81-pair count. Every number is recomputed here, not copied from the page.
"""

import math
import random
from fractions import Fraction

# L02 E3: seed 20260101, xi0 first, then the level-1 coefficient (lab draw order)
rng = random.Random(20260101)
xi0 = rng.gauss(0.0, 1.0)
xi11 = rng.gauss(0.0, 1.0)
sup1 = abs(xi11) * 2 ** (-1)
print(f"L02 E3: unrounded level-1 sup {sup1!r}; printed {sup1:.6f}; 2*sup {2 * sup1:.7f} -> {2 * sup1:.6f}")
print(f"L02 E3: doubling the printed 0.116589 gives {2 * 0.116589:.6f}")
bound1 = math.sqrt(4 * math.log(2)) * 2 ** (-1)
print(f"L02 E3: sqrt(4 log 2) = {math.sqrt(4 * math.log(2)):.6f}; bound {bound1:.6f}")

# L03 standard-error gaps: printed se (four decimals, lab output) vs H sqrt(2/N)/20
printed = {
    1: [(1, 0.0718), (2, 0.0538), (4, 0.0373), (8, 0.0249), (16, 0.0174), (32, 0.0131), (64, 0.0092), (128, 0.0063)],
    2: [(1, 0.1601), (2, 0.0934), (4, 0.0772), (8, 0.0475), (16, 0.0364), (32, 0.0256), (64, 0.0190), (128, 0.0125)],
}
gaps = []
for H, rows in printed.items():
    for N, se in rows:
        th = H * math.sqrt(2 / N) / 20
        gaps.append((100 * (se / th - 1), H, N))
big = max(gaps, key=lambda g: abs(g[0]))
print(f"L03 SE gaps: max |gap| {abs(big[0]):.2f}% at H={big[1]}, N={big[2]} (sign {'+' if big[0] > 0 else '-'});"
      f" max absolute over all 16 pairs = {max(abs(g[0]) for g in gaps):.2f}%")
print(f"L03 E3: sqrt(2/128) = {math.sqrt(2 / 128):.6f}; H sqrt(2/N)/20 at H=2 = {2 * math.sqrt(2 / 128) / 20:.6f}")

# L03 E2: H=2, N=8
N = 8
print(f"L03 E2: 2^4 (4*64-1)/(3*512) = {Fraction(16 * (4 * N * N - 1), 3 * N ** 3)} = {16 * (4 * N * N - 1) / (3 * N ** 3)}")
# L03 quiz: H=1, N=2 exact sum
print(f"L03 quiz: H=1,N=2 sum = {Fraction(1 * (4 * 4 - 1), 3 * 8)} = {15 / 24}")

# Hub placement percentages
print(f"hub: 7/9 = {100 * 7 / 9:.1f} percent; 8/9 = {100 * 8 / 9:.1f} percent")

# Rung-2 count: simple random walk, n = 6 steps, level a = 2 (reflection: ends >= a plus ends > a)
def count_max_reaches(n: int, a: int) -> int:
    total = 0
    for mask in range(2**n):
        s = 0
        hit = False
        for i in range(n):
            s += 1 if (mask >> i) & 1 else -1
            if s >= a:
                hit = True
        total += hit
    return total

print(f"rung 2: walks n=6 with max >= 2 by enumeration = {count_max_reaches(6, 2)}")
print(f"hub rung 1 explanation: n=2, a=1 enumeration = {count_max_reaches(2, 1)}")

# L02 E2 and quiz: dyadic count 216 and 36 pairs
pairs = sum(2**n + 1 for n in range(5))
cases = sum((2**n + 1) * (9 - n) for n in range(5))
print(f"L02 dyadic: pairs {pairs}, cases {cases}")

# L01 count: 3 times x 5 depths; 9 x 9 grid pairs
print(f"L01 counts: dyadic cases {3 * 5}, grid pairs {9 * 9}")

# L01 E1: pieces of t=3/4 at depth 4
print(f"L01 E1: piece length {Fraction(3, 4) / 16}, sum {16 * Fraction(3, 4) / 16}")
