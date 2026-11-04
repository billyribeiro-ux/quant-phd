"""Round-3 BK4-a counterexamples to two page sentences (run from the repo root with python3 -I).

1. L01.html:115 'The order of payments changes the peak need': Example 2.6's payments in the order (2, 1, 3) leave Need_A unchanged.
2. L03.html:421 'The sized margin does not depend on how large these two losses are': lowering the two largest seeded losses
   to 0 changes the 9900-bps sized margin from 2961 to 2938 (seed 2026 draw of Lab 1, Part B; the draw is re-made here).
"""

import math
import random
from fractions import Fraction

# 1. Example 2.6: (payer index, receiver index, amount in dollars); A=0, B=1, C=2
ex = [(0, 1, 100), (1, 2, 80), (2, 0, 50)]


def need(seq, bank):
    bal = low = 0
    for s, r, a in seq:
        bal += -a if s == bank else (a if r == bank else 0)
        low = min(low, bal)
    return -low


print("1. Example 2.6 Need_A, order (1,2,3):", need(ex, 0), "| order (2,1,3):", need([ex[1], ex[0], ex[2]], 0))
print("   order (1,2,3) Need_B:", need(ex, 1), "| order (3,2,1) Need_B:", need([ex[2], ex[1], ex[0]], 1))

# 2. Lab 1, Part B draws: same order as the lab (inputs first, then 200 losses)
rng = random.Random(2026)
for _ in (1, 2, 3, 4):
    rng.randint(1000, 5000)
for _ in (1, 2, 3, 4):
    rng.randint(100, 900)
rng.randint(500, 2000)
losses = [rng.randint(0, 3000) for _ in range(200)]


def sized(ls, t):
    k = math.ceil(Fraction(t * len(ls), 10000))
    return sorted(ls)[k - 1]


base = sized(losses, 9900)
top2 = sorted(range(200), key=lambda i: losses[i])[-2:]
alt = list(losses)
for i in top2:
    alt[i] = 0
print("2. 9900-bps sized margin, as drawn:", base, "| top-two losses", sorted(losses)[-2:], "| after zeroing them:", sized(alt, 9900))
