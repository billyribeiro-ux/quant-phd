"""(a) Trade-count versus share-count claim (L03 misconception 2): two 100-share trades, equal sizes.
(b) Brute-force of Proposition 3.2 over whole-cent asks c..c+40 for two dealers (c=100, Q=1000)."""
from fractions import Fraction as F

c, Q = 100, 1000
h = 2
trades = [100, 100]
print("(a) spread term hV =", h * sum(trades), "; trade-count version h*n =", h * len(trades), "; differ with equal sizes:", h * sum(trades) != h * len(trades))

def profit2(a, rival):  # twice the profit
    if a < rival:
        return 2 * (a - c) * Q
    if a == rival:
        return (a - c) * Q
    return 0

asks = list(range(c, c + 41))
eq = []
for a1 in asks:
    for a2 in asks:
        ok1 = all(profit2(d, a2) <= profit2(a1, a2) for d in asks)
        ok2 = all(profit2(d, a1) <= profit2(a2, a1) for d in asks)
        if ok1 and ok2:
            eq.append((a1 - c, a2 - c))
print("(b) equilibria in grid c..c+40 as offsets:", eq)
