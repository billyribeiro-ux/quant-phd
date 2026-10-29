"""L04 Theorem 2.4 omits Theorem 2.1's no-interest hypothesis. Counterexample: interest paid in cash on the
opening drawn balance of each week (not circular), 1 percent per week, same seed-7 flows and Lab 1 inputs.
Checks whether a DSO slip still lowers liquidity by the same amount in every week."""
import math
from fractions import Fraction
import random

def inputs(seed):
    rng = random.Random(seed)
    rec, dis = [], []
    for w in range(1, 14):
        slump = -350_000 if 5 <= w <= 8 else 0
        rec.append(1_000_000 + rng.randint(-150_000, 150_000) + slump)
        dis.append(1_020_000 + rng.randint(-120_000, 120_000))
    return rec, dis

def run(rec, dis, K, rate_bp=0):
    cash, B = 1_200_000, 0
    liq = []
    for r, d in zip(rec, dis):
        interest = (B * rate_bp) // 10_000 if rate_bp else 0  # on opening drawn balance, floor to cents
        P = cash + r - d - interest
        Dr = Rp = 0
        if P < 1_000_000:
            Dr = min(1_000_000 - P, K - B)
        elif P > 1_000_000 and B > 0:
            Rp = min(P - 1_000_000, B)
        C = P + Dr - Rp
        B = B + Dr - Rp
        liq.append(C + (K - B))
        cash = C
    return liq

rec, dis = inputs(7)
slip = math.floor(Fraction(5 * 1_234_567, 7) + Fraction(1, 2))
rec2 = list(rec)
rec2[0] -= slip
for rate in (0, 100):  # basis points per week
    base = run(rec, dis, 1_200_000, rate)
    alt = run(rec2, dis, 1_200_000, rate)
    drops = [b - a for b, a in zip(base, alt)]
    print("rate_bp", rate, "drops by week", drops, "uniform", len(set(drops)) == 1)
