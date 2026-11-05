"""Independent re-derivation of the L02 lab numbers and the L02 worked numbers (BK4 slice a, round 7).

The generator is re-implemented here (Random(2026); sample 2 distinct members; randint(500, 20000) dollars).
Every ratio uses fractions.Fraction; the basis-point floor is integer division. Printed values are compared exactly.
"""
import random
from fractions import Fraction
from math import floor

rng = random.Random(2026)
trades = []
for seq in range(1, 7):
    payer, receiver = rng.sample(range(4), 2)
    dollars = rng.randint(500, 20000)
    trades.append((payer, receiver, 100 * dollars))
for t in trades:
    print("trade", t)

printed_trades = [(0, 1, 1696600), (0, 3, 1873700), (3, 2, 1845000), (3, 2, 1495300), (1, 0, 314500), (0, 1, 371200)]
print("generator reproduces printed trades:", trades == printed_trades)

G = sum(a for _, _, a in trades)
rec = [sum(a for p, r, a in trades if r == m) for m in range(4)]
pay = [sum(a for p, r, a in trades if p == m) for m in range(4)]
n = [rec[m] - pay[m] for m in range(4)]
A = sum(max(0, x) for x in n)
Apay = sum(max(0, -x) for x in n)
red = G - A
bps = (10000 * red) // G
print("Part B receivables", rec, "payables", pay, "gross", G, "sum rec == G", sum(rec) == G)
print("Part C nets", n, "sum zero", sum(n) == 0)
print("Part D paid after netting", A, "paid by payers", Apay, "A<=G", A <= G, "reduction", red, "bps floor", bps)
print("printed check: nets", [-3627000, 1753300, 3340300, -1466600] == n, "A", 5093600 == A, "red", 2502700 == red, "bps", 3294 == bps)
print("exact bps value", Fraction(10000 * red, G), float(Fraction(10000 * red, G)))
print("E1: A + red == G:", A + red == G)
print("E2 largest creditor member", max(range(4), key=lambda m: n[m]) + 1, "largest debtor member", min(range(4), key=lambda m: n[m]) + 1,
      "positive nets", sorted(x for x in n if x > 0), sum(x for x in n if x > 0))
print("E3 both receive and pay (Part B):", [m + 1 for m in range(4) if rec[m] > 0 and pay[m] > 0], "member with receive only:", [m + 1 for m in range(4) if rec[m] > 0 and pay[m] == 0])
print("Part B member 1 rec/pay", rec[0], pay[0], "member 2", rec[1], pay[1], "member 3", rec[2], pay[2], "member 4", rec[3], pay[3])
print("Q: 5093600 cents in dollars", Fraction(5093600, 100))
print("Quiz: 100 cents/dollar, 2502700 cents in dollars", Fraction(2502700, 100))

# Worked Example 2.4 (dollars): 1 owes 2 100; 2 owes 3 80; 3 owes 1 50
ex = [(0, 1, 100), (1, 2, 80), (2, 0, 50)]
def nets(ts):
    return [sum(a for p, r, a in ts if r == m) - sum(a for p, r, a in ts if p == m) for m in range(3)]
en = nets(ex)
eG = sum(a for *_, a in ex)
eA = sum(max(0, x) for x in en)
print("Ex2.4 nets", en, "G", eG, "A", eA, "bps", (10000 * (eG - eA)) // eG, Fraction(10000 * (eG - eA), eG), float(Fraction(10000*180, 230)))
# M1: chain 1->2 50, 2->3 70, 3->4 20, 4->1 40
m1 = [(0, 1, 50), (1, 2, 70), (2, 3, 20), (3, 0, 40)]
mn = nets(m1 + []) if False else [sum(a for p, r, a in m1 if r == m) - sum(a for p, r, a in m1 if p == m) for m in range(4)]
mG = sum(a for *_, a in m1); mA = sum(max(0, x) for x in mn)
print("M1 nets", mn, "sum", sum(mn), "A", mA, "G", mG, "red", mG - mA, "bps", (10000*(mG-mA))//mG, Fraction(10000*130,180), float(Fraction(10000*130,180)))
# M2: doubled Example 2.4
d = [(p, r, 2 * a) for p, r, a in ex]
dG = sum(a for *_, a in d); dA = sum(max(0, x) for x in nets(d))
print("M2 G", dG, "A", dA, "red", dG - dA, "bps", (10000 * (dG - dA)) // dG)
# M3: 1 owes 2 100 and 1 owes 3 100 (members 1..3 => indices 0,1,2)
m3 = [(0, 1, 100), (0, 2, 100)]
m3n = [sum(a for p, r, a in m3 if r == m) - sum(a for p, r, a in m3 if p == m) for m in range(3)]
m3G = sum(a for *_, a in m3); m3A = sum(max(0, x) for x in m3n)
print("M3 nets", m3n, "sum", sum(m3n), "G", m3G, "A", m3A, "red", m3G - m3A)
# P3 cycle of k=4, a=7
k, a = 4, 7
cyc = [(i, (i + 1) % k, a) for i in range(k)]
cn = [sum(x for p, r, x in cyc if r == m) - sum(x for p, r, x in cyc if p == m) for m in range(k)]
cG = sum(x for *_, x in cyc); cA = sum(max(0, x) for x in cn)
print("P3 k=4 nets", cn, "A", cA, "bps", (10000*(cG-cA))//cG)
# Misconception: Example 2.4 netted 50 vs gross 230
print("Example 2.4 misconception: A", eA, "G", eG)
# R2 example: X = {1 owes 2: 100}; Y = X + {3 owes 4: 50} + {4 owes 3: 50}
X = [(0, 1, 100)]
Y = X + [(2, 3, 50), (3, 2, 50)]
for name, ts in (("X", X), ("Y", Y)):
    nn = [sum(a for p, r, a in ts if r == m) - sum(a for p, r, a in ts if p == m) for m in range(4)]
    print("R2", name, "nets", nn, "A", sum(max(0, x) for x in nn), "G", sum(a for *_, a in ts))
