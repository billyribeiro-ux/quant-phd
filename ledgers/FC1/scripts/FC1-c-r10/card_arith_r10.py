"""Round-10 (verifier): exact re-derivation of the numbers quoted on FC1 cards (cards.json), printed for the record.

Usage: python -I ledgers/FC1/scripts/FC1-c-r10/card_arith_r10.py
"""

from __future__ import annotations

import datetime
from fractions import Fraction as F

print("c010 total after stage 10, rho=1/10, d=1000:", float(1000 * (1 - F(9, 10) ** 11) / F(1, 10)), "-> 686189 cents? ", round(1000 * (1 - F(9, 10) ** 11) / F(1, 10) * 100))
print("c011 limit phi=1/2:", float(F(1000) / (1 - F(1, 2) * F(9, 10))), "share of 10000:", float(F(1000) / (1 - F(1, 2) * F(9, 10)) / 10000 * 100), "%")
print("c012 multiplier rounded 6.8619 x 1000 =", F("6.8619") * 1000, "; exact 6861.8940391 -> 6861.89")
print("c016 multiplier at stage 10:", float((1 - F(9, 10) ** 11) / F(1, 10)))
print("c092 half redeposit S_10 (kappa=0.45) in cents:", float(1000 * (1 - F(45, 100) ** 11) / F(55, 100)) * 100, "-> 181790 printed")
print("c037 bid/ask/spread/relative:", 5000 - 15, 5000 + 15, (5000 + 15) - (5000 - 15), F(30, 5000), float(F(30, 5000) * 100), "%")
print("c061 cost/avg:", 60 * 1000 + 90 * 1100, F(60 * 1000 + 90 * 1100, 150))
print("c082 consideration:", 216 * 10060)
print("c083 weekdays:", datetime.date(2026, 10, 28).strftime("%A"), datetime.date(2026, 10, 30).strftime("%A"))
print("c084 ratio:", float(F(14282414, 68398886)), "-> 0.209 at 3 dp; five dp", f"{14282414 / 68398886:.5f}")
print("c053/c098 spread capture and mark-to-mid:", 2 * 2000, 4000 - 545)
print("c043 hV:", 2 * 200, "c139:", (-1) * 100 * (10000 - 9990), "c140:", 400 - 1000)
print("c103/104 S_1, S_2 (rho=1/10, d=1000):", 1000 + 900, 1000 + 900 + 810)
print("c093 equity after losses 50/100/150 on equity 100:", [100 - x for x in (50, 100, 150)])
print("c122 threshold: lambda <= E", "holds for E=100, lambda=100:", 100 - 100 >= 0)
print("c066/c067 share conservation example: 60 shares x 2 =", 2 * 60)
print("c112 V = 2Q with Q = shares bought (example 100): V =", 2 * 100)
print("c117 relative spread has no unit: s/m =", F(30, 5000))
print("c138 s = 2h: h=15 -> s =", 2 * 15)
print("c131 volume, Example 2.5 is closed: buys 0, sells 100 in example 2.5 (sign -1 first trade)")
