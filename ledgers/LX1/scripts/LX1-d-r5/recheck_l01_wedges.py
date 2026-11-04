"""Independent re-derivation of the L01 Lab 1 seeded counts (cards c009, c010) with plain floats+Fractions. Stdlib only."""
import math, random
from fractions import Fraction as Fr

def rhu(x):
    return math.floor(x + Fr(1, 2))

def F(growth, t):
    return Fr(400) * (1 + growth) ** t / (Fr(9, 100) - growth)

rng = random.Random(20261103)
gaps3, gaps1 = [], []
for t in range(13):
    w = Fr(rng.randint(-8, 25), 100)
    price = rhu(F(Fr(3, 100), t) * (1 + w))
    gaps3.append(price - rhu(F(Fr(3, 100), t)))
    gaps1.append(price - rhu(F(Fr(1, 100), t)))
print("gap under 3% (13 periods):", gaps3)
print("periods price above fundamental under 3%:", sum(g > 0 for g in gaps3), "of 13")
print("gap under 1%:", gaps1)
print("periods price above alternative fundamental under 1%:", sum(g > 0 for g in gaps1), "of 13")
