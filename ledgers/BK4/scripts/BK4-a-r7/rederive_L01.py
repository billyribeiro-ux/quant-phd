"""Independent re-derivation of the L01 lab numbers and of the L01 worked examples (BK4 slice a, round 7).

Written by the verifier from the printed day only (Part A of the page output), plus an independent
re-implementation of the seeded generator for the cross-check. Uses fractions.Fraction for every ratio.
"""
import random
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP

# Part A of the printed output (sending order, cents): (sender, receiver, cents), banks 0=A 1=B 2=C
printed = [
    (1, 2, 101800), (1, 0, 324400), (1, 2, 318300), (1, 2, 278600), (1, 2, 218000), (2, 0, 149400),
    (0, 2, 269700), (1, 0, 173600), (0, 2, 91800), (0, 1, 398400), (1, 2, 25300), (1, 0, 492300),
]

# Independent generator: same seed and same draw order as the lab's stated method (Random(seed), sample 2 banks, randint dollars)
rng = random.Random(20260)
gen = []
for _ in range(12):
    s, r = rng.sample(range(3), 2)
    d = rng.randint(100, 5000)
    gen.append((s, r, 100 * d))
print("generator reproduces printed day:", gen == printed)

def net(day, b):
    return sum(c for s, r, c in day if r == b) - sum(c for s, r, c in day if s == b)

def need(day, b):
    bal, low = 0, 0
    for s, r, c in day:
        if s == b:
            bal -= c
        elif r == b:
            bal += c
        low = min(low, bal)
    return -low

def running(day, b):
    bal, out = 0, [0]
    for s, r, c in day:
        if s == b:
            bal -= c
        elif r == b:
            bal += c
        out.append(bal)
    return out

day = printed
gross = sum(c for _, _, c in day)
nets = [net(day, b) for b in range(3)]
debits = [max(0, -x) for x in nets]
needs = [need(day, b) for b in range(3)]
print("gross", gross, "nets", nets, "debits", debits, "needs", needs)
print("sum nets zero:", sum(nets) == 0)
print("need >= debit each:", all(n >= d for n, d in zip(needs, debits)))
print("moved (sum debits):", sum(debits), "funded banks:", sum(1 for d in debits if d > 0),
      "need>debit banks:", sum(1 for n, d in zip(needs, debits) if n > d))
ratio = Fraction(sum(debits), gross)
q = (ratio * 10000).__floor__()  # not used for display
dec = (Decimal(sum(debits)) / Decimal(gross))
print("ratio exact", float(ratio), "decimal", dec)
print("ratio 4dp half-up:", Decimal(sum(debits)/gross).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
print("ratio as percent 2dp half-up:", (Decimal(sum(debits))*100/Decimal(gross)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
print("Bank A running sums:", running(day, 0))
print("Bank B running sums:", running(day, 1))
print("Bank C running sums:", running(day, 2))
# Remark: net positions do not depend on order; the need does. Check on the printed day: sending order irrelevant to net
print("Bank B need == debit:", needs[1] == debits[1], "Bank A need-debit:", needs[0] - debits[0], "Bank C:", needs[2]-debits[2])
print("Bank B running minimum is final position:", min(running(day, 1)) == net(day, 1))
# Settlement lag: trade day t settles t+1
print([t + 1 for t in range(3)])

# Worked Example 2.6 (dollars), payments: A pays B 100; B pays C 80; C pays A 50
A, B, C = 0, 1, 2
ex = [(A, B, 100), (B, C, 80), (C, A, 50)]
print("Ex2.6 needs", [need(ex, b) for b in range(3)], "nets", [net(ex, b) for b in range(3)],
      "debits", [max(0, -net(ex, b)) for b in range(3)], "gross", sum(c for *_, c in ex))
print("Ex2.6 running A", running(ex, A), "B", running(ex, B), "C", running(ex, C))
# Remark 2.7: payment 3 first
ex2 = [ex[2], ex[0], ex[1]]
print("Remark2.7 running A", running(ex2, A), "need A", need(ex2, A), "debit A", max(0, -net(ex2, A)))
# M1: receives 300 then pays 500 (opening 0)
m1 = [(1, 0, 300), (0, 1, 500)]
print("M1 need", need(m1, 0), "debit", max(0, -net(m1, 0)), "running", running(m1, 0))
# M2: doubled example
m2 = [(A, B, 200), (B, C, 160), (C, A, 100)]
print("M2 need A", need(m2, A), "debit A", max(0, -net(m2, A)))
# M3: receive 40, pay 70, receive 10
m3 = [(1, 0, 40), (0, 1, 70), (1, 0, 10)]
print("M3 running A", running(m3, 0), "need", need(m3, 0), "debit", max(0, -net(m3, 0)))
# R3: cycle of 100
r3 = [(0, 1, 100), (1, 2, 100), (2, 0, 100)]
print("R3 running A", running(r3, 0), "need", need(r3, 0), "nets", [net(r3, b) for b in range(3)])
