"""FC2 slice a, round 1: brute-force sanity checks of L01 Prop 3.5, L01 R1, L01 R3 and L02 R1 on exact fractions."""
from fractions import Fraction as Fr
from itertools import product

BOX = [Fr(k, 4) for k in range(-40, 41)]  # holdings in quarter units, -10 to 10


def arb(h, prices, pay):
    cost = sum(h[j] * prices[j] for j in range(len(prices)))
    out = [sum(h[j] * pay[s][j] for j in range(len(prices))) for s in range(len(pay))]
    if cost > 0 or any(x < 0 for x in out):
        return False
    return cost < 0 or any(x > 0 for x in out)


def has_arb(prices, pay, bond_nonneg=False):
    for h in product(BOX, BOX):
        if bond_nonneg and h[0] < 0:
            continue
        if arb(h, prices, pay):
            return True
    return False


# Prop 3.5 (bond 9/10, payoffs bond (1,1), stock (3,1)): arbitrage exists iff q <= 9/10 or q >= 27/10
pay2 = [[Fr(1), Fr(3)], [Fr(1), Fr(1)]]
bad = []
for q in [Fr(k, 20) for k in range(1, 80)]:
    expected = not (Fr(9, 10) < q < Fr(27, 10))
    got = has_arb([Fr(9, 10), q], pay2)
    if expected != got:
        bad.append(q)
print("Prop 3.5 grid mismatches (q in k/20, 1/20..79/20):", bad)

# L01 R3 (no short bond): arbitrage exists iff q <= 0 or q >= 27/10 (grid of q)
bad = []
for q in [Fr(k, 20) for k in range(1, 80)]:
    expected = not (Fr(0) < q < Fr(27, 10))
    got = has_arb([Fr(9, 10), q], pay2, bond_nonneg=True)
    if expected != got:
        bad.append(q)
print("R3 grid mismatches:", bad)

# L01 R1 (three states u, m, d; stock pays 3, 2, 1; bond 1 in all)
pay3 = [[Fr(1), Fr(3)], [Fr(1), Fr(2)], [Fr(1), Fr(1)]]
bad = []
for q in [Fr(k, 20) for k in range(1, 80)]:
    expected = not (Fr(9, 10) < q < Fr(27, 10))
    got = has_arb([Fr(9, 10), q], pay3)
    if expected != got:
        bad.append(q)
print("R1 grid mismatches:", bad)

# L02 R1: lending rate rl, borrowing rate rb: forward price band; grid check with float-free exp proxy skipped (algebra only)
print("done")
