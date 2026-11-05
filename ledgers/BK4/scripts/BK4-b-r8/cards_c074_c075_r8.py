"""Verifier round 8: exact check of the two changed stablecoin cards (BK4-c074, BK4-c075).

Does not read the lab twins. Run as: python -I -W error cards_c074_c075_r8.py
"""

import json
import sys
from fractions import Fraction as F

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    cards = {c["id"]: c for c in json.load(fh)}
c74, c75 = cards["BK4-c074"], cards["BK4-c075"]
print("c074 grade", c74["grade"], "basis", c74["basis"])
print("c075 grade", c75["grade"], "basis", c75["basis"])
bad = 0

# c074: under A1-3 coverage is exactly 1 at each admissible share when rho = 1 (Prop 2.4).
rho = F(1)
for x in [F(0), F(1, 7), F(1, 2), F(9, 10), F(99, 100)]:
    assert x <= rho and x < 1
    if (rho - x) / (1 - x) != 1:
        bad += 1
print("c074 part 1 (rho=1, A1-3 coverage exactly 1 at sampled shares): ok" if bad == 0 else "FAIL part 1")

# c074: with measured ratio rho*(1-h), rho=1, h>0, coverage < 1 at every admissible share of 1-h.
for h in [F(1, 20), F(1, 3), F(99, 100), F(1, 10000)]:
    m = rho * (1 - h)
    for x in [F(0), F(1, 7), F(1, 2), m - F(1, 1000), m]:
        if x < 0 or x >= 1 or x > m:
            continue
        cov = (m - x) / (1 - x)
        if not cov < 1:
            bad += 1
            print("FAIL c074 h", h, "x", x, cov)
print("c074 part 2 (rho=1, h>0: measured coverage below 1 at sampled admissible shares): ok" if bad == 0 else "FAIL part 2")

# c075: at x = 1/2, coverage (rho - 1/2)/(1/2) versus rho/2; and 19/20 gives 9/10 = 9000 bps, not 19/40.
for r in [F(1, 2), F(3, 5), F(19, 20), F(1), F(21, 20)]:
    th = (r - F(1, 2)) / F(1, 2)
    print(f"c075 rho={r} coverage={th} bps={(10000 * th).__floor__()} rho/2={r / 2} equal_to_rho_over_2={th == r / 2}")
th = (F(19, 20) - F(1, 2)) / F(1, 2)
assert th == F(9, 10) and (10000 * th).__floor__() == 9000 and F(19, 20) / 2 == F(19, 40)
print("c075 numbers: 9/10, 9000 bps, 19/40 ok")
print("ALL OK" if bad == 0 else f"FAILURES {bad}")
