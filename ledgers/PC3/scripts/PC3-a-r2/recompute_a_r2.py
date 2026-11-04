"""Independent recomputation for PC3 slice a (hub, L01-L03). Uses only fractions and math, written apart from the lab twins.

Run as: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r2/recompute_a_r2.py
"""
import math
from fractions import Fraction as F
from itertools import product

print("== L01 Example 1.4 and Section 2")
lo = F(20) * 2 * 300
hi = F(60) * 10 * 390
print("bounds", lo, hi, "ratio", hi / lo)
w = math.log(19.5)
print("ln 19.5 = %.10f" % w, "ln3+ln5+ln1.3 = %.10f" % (math.log(3) + math.log(5) + math.log(1.3)))
print("geometric mean = %.10f" % math.sqrt(lo * hi))
red1 = w - math.log(13 / 5 * 0 + 2) * 0  # placeholder to keep the name used below
s_sym = w - math.log(40 / 20 * 0 + 2) * 0
sym_total = math.log(2) + math.log(5) + math.log(1.3)
qu_total = math.log(3) + math.log(2) + math.log(1.3)
min_total = math.log(3) + math.log(5) + math.log(360 / 330)
for name, t in [("symbols", sym_total), ("quotes", qu_total), ("minutes", min_total)]:
    print(name, "total %.10f reduction %.10f share %.6f%%" % (t, w - t, 100 * (w - t) / w))
print("E3 new width ln(16.5) = %.10f ; ln19.5-ln16.5 = %.10f" % (math.log(16.5), math.log(19.5) - math.log(16.5)))
print("E2 shares: quotes %.6f, minutes %.6f" % ((w - qu_total) / w, (w - min_total) / w))

print("== L01 Part 3 and Example 1.7")
def rem(n, x):
    return (1 + x) ** n - 1 - n * x
def bnd(n, x):
    return F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
for n in (2, 5, 10):
    for x in (F(1, 100), F(1, 20)):
        r = rem(n, x)
        b = bnd(n, x)
        print(n, x, "exact %.10f rem %.10f bound %.10f" % ((1 + x) ** n, r, b), "rem<=bound", 0 <= r <= b, "strict", r < b)
r10 = rem(10, F(1, 100))
b10 = bnd(10, F(1, 100))
print("E1 ratio rem/bound = %.8f" % (float(r10) / float(b10)))
print("Example 1.7 bound/rem - 1 = %.6f" % (float(b10) / float(r10) - 1))
r20 = rem(10, F(1, 20))
print("x=1/20: exact %.10f miss %.10f miss/exact %.6f bound %.10f" % ((1 + F(1, 20)) ** 10, float(r20), float(r20) / float((1 + F(1, 20)) ** 10), float(bnd(10, F(1, 20)))))
print("M3 remainder 31/1000 ? ", rem(3, F(1, 10)) == F(31, 1000), "bound 33/1000 ?", bnd(3, F(1, 10)) == F(33, 1000))
print("ln 4 = %.10f ; ln 16 = %.10f" % (math.log(4), math.log(16)))
print("ln(21/5)=%.10f sum=%.10f" % (math.log(F(21, 5)), math.log(1.5) + math.log(1.4) + math.log(2)))
print("E4 ln2+ln2 - ln4 = %.3e" % (2 * math.log(2) - math.log(4)))

print("== L01 R1 and R3")
A = math.log(3)
B = math.log(2.5)
print("R1 total %.4f half %.4f ln5 %.4f ln3 %.4f ln1.3 %.4f" % (w, w / 2, math.log(5), math.log(3), math.log(1.3)))
print("R3 reductions: A narrow [1,3]->[1,2] = %.4f ; B narrow [1,2.5]->[1,1.01] = %.4f ; widths A %.4f B %.4f" % (math.log(3 / 2), math.log(2.5 / 1.01), A, B))

print("== L02 drill set (independent enumeration)")
import random
rng = random.Random(0)
items = []
for number in range(1, 13):
    flips = rng.randint(3, 8)
    if rng.random() < 0.5:
        k = rng.randint(1, flips)
        items.append(("atleast", flips, k))
    else:
        j = rng.randint(1, flips)
        items.append(("first", flips, j))
for kind, n, a in items:
    cnt = 0
    for seq in product((0, 1), repeat=n):
        if kind == "atleast":
            cnt += sum(seq) >= a
        else:
            cnt += seq[a - 1] == 1 and all(s == 0 for s in seq[: a - 1])
    print(kind, n, a, F(cnt, 2 ** n))

print("== L02 Monty Hall, independent: host opens a door not picked, not car")
def monty(rule):
    tot = F(0); stay = F(0); sw = F(0)
    for car in range(3):
        for pick in range(3):
            if rule == "A":
                # host opens a goat door other than pick, uniform among goat doors available
                opts = [d for d in range(3) if d != pick and d != car]
                for opened in opts:
                    p = F(1, 3) * F(1, 3) * F(1, len(opts))
                    tot += p
                    other = [d for d in range(3) if d not in (pick, opened)][0]
                    stay += p * (pick == car)
                    sw += p * (other == car)
                if pick == car:
                    # host chooses among the two goats
                    pass
            else:
                for opened in [d for d in range(3) if d != pick]:
                    if opened == car:
                        continue
                    p = F(1, 3) * F(1, 3) * F(1, 2)
                    tot += p
                    other = [d for d in range(3) if d not in (pick, opened)][0]
                    stay += p * (pick == car)
                    sw += p * (other == car)
    return stay / tot, sw / tot
print("rule A (stay, switch) given sequential rule:", monty("A"))
print("rule B:", monty("B"))

print("== L02 bag, urn, quiz")
print("P(bag1|red)", (F(1, 2) * F(3, 4)) / (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)))
print("urn second red", F(12, 20), "first red", F(12, 20), "both red", F(6, 20), "second red | first blue", F(3, 4))
print("M2 posterior", F(15, 100) / F(29, 100), "P(B)", F(29, 100))
print("E1 P(>=2 heads in 6)", 1 - F(1, 64) - F(6, 64))
print("Mech-1 L02 P(sum 7 | first 3)", (F(1, 36)) / (F(6, 36)))
print("urn both red M3 L02", F(4, 6) * F(3, 5), F(12, 30))

print("== L03 reroll game")
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
print("continuation", cont)
vals = [max(100 * f, cont) for f in range(1, 7)]
print("backward value", F(sum(vals), 6), "stop all", F(sum(100 * f for f in range(1, 7)), 6))
best = max(F(sum((100 * f if bits[f - 1] else cont) for f in range(1, 7)), 6) for bits in product((0, 1), repeat=6))
print("best of 64 policies", best)
print("choice value", F(sum(vals), 6) - 350, float(F(sum(vals), 6) - 350))
print("E2 change 625/8 - 150 =", F(625, 8) - 150, float(F(625, 8) - 150))
print("R2 fee c=1 and c=100 gains:")
for c in (100, 1):
    cc = 350 - c
    print("  c", c, float(F(sum(max(100 * f, cc) for f in range(1, 7)), 6) - 350))

print("== L03 stopping rules, independent")
def value(outcomes, rule, horizon=6):
    def v(h):
        if len(h) == horizon or rule(h):
            return F(sum(h))
        return sum((p * v(h + (x,)) for x, p in outcomes), F(0))
    return v(())
RULES = [
    lambda h: False,
    lambda h: bool(h) and h[-1] > 0,
    lambda h: bool(h) and h[-1] < 0,
    lambda h: sum(h) >= 100,
    lambda h: sum(h) >= 200 or sum(h) <= -200,
]
fair = ((100, F(1, 2)), (-100, F(1, 2)))
biased = ((150, F(1, 2)), (-100, F(1, 2)))
print("fair:", [str(value(fair, r)) for r in RULES])
print("biased:", [str(value(biased, r)) for r in RULES])
# R1 two-turn look-ahead rule
paths = [(100, 100), (100, -100), (-100, 100), (-100, -100)]
tot = []
for a, b in paths:
    w1, w2 = a, a + b
    tot.append(max(w1, w2))
print("R1 path totals", tot, "mean", F(sum(tot), 4))
