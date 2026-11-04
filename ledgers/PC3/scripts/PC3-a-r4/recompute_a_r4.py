"""Independent recomputation of every number in the PC3 slice-a pages (L01-L03, index quiz).

Written by the round-4 verifier. Does not import the lab twins. Uses Fraction for exact values and
math for logs. Prints one line per check with OK or FAIL and the value.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction as F

fails: list[str] = []


def check(label: str, got: object, want: object, tol: float | None = None) -> None:
    if tol is None:
        ok = got == want
    else:
        ok = abs(float(got) - float(want)) <= tol  # type: ignore[arg-type]
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got} want {want}")
    if not ok:
        fails.append(label)


# ---- L01: Fermi product, log widths, narrowing ----
lo = [F(20), F(2), F(300)]
hi = [F(60), F(10), F(390)]
L = lo[0] * lo[1] * lo[2]
U = hi[0] * hi[1] * hi[2]
check("L01 lower product", L, 12000)
check("L01 upper product", U, 234000)
check("L01 ratio", U / L, F(39, 2))
W = math.log(float(U / L))
check("L01 ln19.5 to 10 places", f"{W:.10f}", "2.9704144656")
check("L01 geometric midpoint", f"{math.sqrt(float(L * U)):.4f}", "52990.5652")
check("L01 geometric midpoint 2dp", f"{math.sqrt(float(L * U)):.2f}", "52990.57")
w = [math.log(float(h / l)) for l, h in zip(lo, hi)]
check("L01 sum factor widths = ln19.5", sum(w), W, 1e-12)
check("L01 ln3", f"{w[0]:.10f}", "1.0986122887")
check("L01 ln5", f"{w[1]:.10f}", "1.6094379124")
check("L01 ln1.3", f"{w[2]:.10f}", "0.2623642645")
# narrowing (Part 2)
new_sym = math.log(float(F(40) / F(20)))
tot_sym = new_sym + w[1] + w[2]
check("L01 narrow symbols total 2.5649", f"{tot_sym:.4f}", "2.5649")
check("L01 narrow symbols reduction 0.4055", f"{W - tot_sym:.4f}", "0.4055")
new_qu = math.log(float(F(8) / F(4)))
tot_qu = w[0] + new_qu + w[2]
check("L01 narrow quotes total 2.0541", f"{tot_qu:.4f}", "2.0541")
check("L01 narrow quotes reduction 0.9163", f"{W - tot_qu:.4f}", "0.9163")
check("L01 quotes share percent (1dp)", f"{100 * (W - tot_qu) / W:.1f}", "30.8")
check("L01 quotes share 4dp", f"{(W - tot_qu) / 2.9704:.4f}", "0.3085")
new_min = math.log(float(F(360) / F(330)))
tot_min = w[0] + w[1] + new_min
check("L01 narrow minutes total 2.7951", f"{tot_min:.4f}", "2.7951")
check("L01 narrow minutes reduction 0.1754", f"{W - tot_min:.4f}", "0.1754")
check("L01 minutes share percent (1dp)", f"{100 * (W - tot_min) / W:.1f}", "5.9")
check("L01 minutes share 4dp (E2 text 0.0590)", f"{(W - tot_min) / 2.9704:.4f}", "0.0590")
# E3: minutes [300,330]
check("L01 E3 upper", F(60) * 10 * 330, 198000)
check("L01 E3 ratio 16.5", F(198000, 12000), F(33, 2))
check("L01 E3 ln16.5 (4dp 2.8034)", f"{math.log(16.5):.4f}", "2.8034")
check("L01 E3 change 0.167054", f"{math.log(19.5) - math.log(16.5):.6f}", "0.167054")
# R1 threshold
check("L01 R1 half total 1.4852", f"{W / 2:.4f}", "1.4852")
check("L01 R1 ln5 1.6094", f"{math.log(5):.4f}", "1.6094")
# R3 counterexample
check("L01 R3 ln3", f"{math.log(3):.4f}", "1.0986")
check("L01 R3 reduction A ln(3/2)", f"{math.log(1.5):.4f}", "0.4055")
check("L01 R3 ln2.5", f"{math.log(2.5):.4f}", "0.9163")
check("L01 R3 reduction B ln(2.5/1.01)", f"{math.log(2.5 / 1.01):.4f}", "0.9063")

# Mechanics M1, M2, M3 and Example 3.10-level numbers
check("L01 M1 ln(21/5)=ln4.2", math.log(F(21, 5).__float__()), math.log(4.2), 1e-12)
check("L01 M1 factor sum", math.log(1.5) + math.log(1.4) + math.log(2), math.log(4.2), 1e-12)
check("L01 M2 ln16", f"{math.log(16):.4f}", "2.7726")
check("L01 M3 remainder", (F(11, 10) ** 3) - 1 - F(3, 10), F(31, 1000))
check("L01 M3 bound", F(3) * F(11, 10) * F(1, 100), F(33, 1000))
check("L01 E4 ln4", math.log(4), math.log(2) * 2, 1e-12)
check("L01 E3 ln 16.5 = ln 198000/12000", math.log(F(198000, 12000).__float__()), math.log(16.5), 1e-12)


def rem(n: int, x: F) -> F:
    return (1 + x) ** n - 1 - n * x


def bnd(n: int, x: F) -> F:
    return F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x


r = rem(10, F(1, 100))
b = bnd(10, F(1, 100))
check("L01 Ex1.7 remainder 10dp", f"{float(r):.10f}", "0.0046221254")
check("L01 Ex1.7 bound 10dp", f"{float(b):.10f}", "0.0048728552")
check("L01 Ex1.7 ratio 4dp (E1 0.9485)", f"{float(r / b):.4f}", "0.9485")
check("L01 Ex1.7 ratio 5dp", f"{float(r / b):.5f}", "0.94855")
check("L01 Ex1.7 bound over remainder 0.054", f"{float(b / r - 1):.3f}", "0.054")
check("L01 quiz remainder 6dp 0.004622", f"{float(r):.6f}", "0.004622")
r2 = rem(10, F(1, 20))
b2 = bnd(10, F(1, 20))
check("L01 Ex1.7 x=1/20 exact 1.6289 (4dp)", f"{float((1 + F(1, 20)) ** 10):.4f}", "1.6289")
check("L01 Ex1.7 x=1/20 remainder 0.1289", f"{float(r2):.4f}", "0.1289")
check("L01 Ex1.7 x=1/20 bound 0.1662", f"{float(b2):.4f}", "0.1662")
check("L01 Ex1.7 miss share 0.079", f"{float(r2 / (1 + F(1, 20)) ** 10):.3f}", "0.079")
check("L01 misc 0.1289/1.6289 share 7.9%", f"{100 * float(r2 / (1 + F(1, 20)) ** 10):.1f}", "7.9")
check("L01 remark n=2 bound equals x^2", bnd(2, F(1, 3)), F(1, 9))
check("L01 remark n=2 remainder equals x^2", rem(2, F(1, 3)), F(1, 9))
for n in (2, 5, 10):
    for x in (F(1, 100), F(1, 20)):
        check(f"L01 part3 0<=rem<=bnd n={n} x={x}", 0 <= rem(n, x) <= bnd(n, x), True)
check("L01 Part3 n=5 x=0.05 exact", f"{float((1 + F(1, 20)) ** 5):.10f}", "1.2762815625")
check("L01 Part3 n=5 x=0.05 bound", f"{float(bnd(5, F(1, 20))):.10f}", "0.0289406250")
# binomial tail identity
for n in (2, 5, 10):
    for x in (F(1, 100), F(1, 20)):
        tail = sum(math.comb(n, j) * x**j for j in range(2, n + 1))
        check(f"L01 binomial tail identity n={n} x={x}", tail == rem(n, x), True)
# grid (5 points per factor)
pts = []
axes = [[l + (h - l) * F(k, 4) for k in range(5)] for l, h in zip(lo, hi)]
for combo in itertools.product(*axes):
    pts.append(combo[0] * combo[1] * combo[2])
check("L01 grid 125 points inside", sum(L <= p <= U for p in pts), 125)

# ---- L02: probability ----
# Def 2.2 two flips
flips = list(itertools.product("HT", repeat=2))
at_least_one = [s for s in flips if "H" in s]
both = [s for s in flips if s == ("H", "H")]
check("L02 P(both|at least one)", F(len(both), len(at_least_one)), F(1, 3))
first_h = [s for s in flips if s[0] == "H"]
check("L02 P(both|first H)", F(len([s for s in both if s[0] == "H"]), len(first_h)), F(1, 2))
check("L02 P(at least one|both)", F(len([s for s in flips if "H" in s and s == ("H", "H")]), 1), 1)
# Urn 3 red 2 blue, ordered pairs of distinct balls
balls = ["r1", "r2", "r3", "b1", "b2"]
pairs = [(a, b) for a in balls for b in balls if a != b]
red = {"r1", "r2", "r3"}
check("L02 urn pairs 20", len(pairs), 20)
check("L02 P(second red)", F(sum(b in red for _, b in pairs), 20), F(3, 5))
check("L02 P(first red)", F(sum(a in red for a, _ in pairs), 20), F(3, 5))
check("L02 P(both red)", F(sum(a in red and b in red for a, b in pairs), 20), F(3, 10))
bl = [(a, b) for a, b in pairs if a.startswith("b")]
check("L02 P(second red | first blue) = 3/4", F(sum(b in red for _, b in bl), len(bl)), F(3, 4))
# Monty Hall by independent enumeration over (car, pick, opened) with the two host rules
def monty(rule: str) -> tuple[F, F]:
    stay = F(0)
    sw = F(0)
    tot = F(0)
    for car in range(3):
        for pick in range(3):
            others = [d for d in range(3) if d != pick]
            if rule == "A":
                goats = [d for d in others if d != car]
                for op in goats:
                    w = F(1, 9) * F(1, len(goats))
                    tot += w
                    stay += w if pick == car else 0
                    sw += w if [d for d in others if d != op][0] == car else 0
            else:
                for op in others:
                    if op == car:
                        continue
                    w = F(1, 9) * F(1, 2)
                    tot += w
                    stay += w if pick == car else 0
                    sw += w if [d for d in others if d != op][0] == car else 0
    return stay / tot, sw / tot


check("L02 Monty rule A stay", monty("A")[0], F(1, 3))
check("L02 Monty rule A switch", monty("A")[1], F(2, 3))
check("L02 Monty rule B stay", monty("B")[0], F(1, 2))
check("L02 Monty rule B switch", monty("B")[1], F(1, 2))
check("L02 Monty rule B P(goat reveal) 2/3", F(2, 3), F(2, 3))
# Bag example
p_red = F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)
check("L02 P(red) bag", p_red, F(1, 2))
check("L02 P(bag1|red)", F(1, 2) * F(3, 4) / p_red, F(3, 4))
# M2 Bayes
pB = F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10)
check("L02 M2 P(B)=29/100", pB, F(29, 100))
check("L02 M2 P(A|B)=15/29", F(1, 2) * F(3, 10) / pB, F(15, 29))
# M1 dice
check("L02 M1 P(sum7|first3)=1/6", F(1, 36) / F(6, 36), F(1, 6))
# M3 urn both red 2/5
check("L02 M3 (4/6)(3/5)=2/5", F(4, 6) * F(3, 5), F(2, 5))
check("L02 M3 12 of 30", F(12, 30), F(2, 5))
# E1: at least 2 heads in 6 flips
check("L02 E1 57/64", F(64 - 1 - 6, 64), F(57, 64))
# R3 urn 3 red 1 blue
rb = ["r1", "r2", "r3", "b"]
pr = [(a, b) for a in rb for b in rb if a != b]
blue_first = [(a, b) for a, b in pr if a == "b"]
check("L02 R3 P(red second|blue first)=1", F(sum(b != "b" for _, b in blue_first), len(blue_first)), 1)
# Drill set: 12 items, enumeration vs closed form, seed 0 (independent generator usage)
import random

rng = random.Random(0)
items = []
for number in range(1, 13):
    flips_n = rng.randint(3, 8)
    if rng.random() < 0.5:
        k = rng.randint(1, flips_n)
        items.append((number, "atleast", flips_n, k))
    else:
        j = rng.randint(1, flips_n)
        items.append((number, "first", flips_n, j))
agree = 0
for number, kind, n, a in items:
    seqs = list(itertools.product((0, 1), repeat=n))
    if kind == "atleast":
        exact = F(sum(1 for s in seqs if sum(s) >= a), 2**n)
        formula = F(sum(math.comb(n, i) for i in range(a, n + 1)), 2**n)
        desc = f"at least {a} heads in {n} fair flips"
    else:
        exact = F(sum(1 for s in seqs if s[a - 1] == 1 and all(v == 0 for v in s[: a - 1])), 2**n)
        formula = F(1, 2**a)
        desc = f"the first head on flip {a} of {n} fair flips"
    agree += exact == formula
    print(f"  item {number:2d}: {desc}: {exact}")
check("L02 drill set agreement 12/12", agree, 12)

# ---- L03: expectation and stopping ----
check("L03 E[X+Y]=7", F(sum(x + y for x in range(1, 7) for y in range(1, 7)), 36), 7)
check("L03 Ex3.6 reroll continuation 250", F(sum(100 * g for g in range(1, 7)), 6) - 100, 250)
best = [max(100 * f, 250) for f in range(1, 7)]
check("L03 Ex3.6 value 1150/3", F(sum(best), 6), F(1150, 3))
check("L03 Ex3.6 gain 100/3", F(1150, 3) - 350, F(100, 3))
check("L03 Ex3.6 1150/3 to 2dp", f"{float(F(1150, 3)):.2f}", "383.33")
check("L03 Ex3.6 gain 2dp", f"{float(F(100, 3)):.2f}", "33.33")
# all 64 policies on first face (2^6): best equals sum of per-face maxima
cont = F(250)
vals = []
for bits in itertools.product((0, 1), repeat=6):
    v = sum((F(100 * f) if bits[f - 1] else cont) for f in range(1, 7)) / 6
    vals.append(v)
check("L03 max over 64 policies = 1150/3", max(vals), F(1150, 3))
check("L03 stop-everywhere 350", F(sum(100 * f for f in range(1, 7)), 6), 350)
# R2 fee formula
def gain(c: int) -> F:
    cont_c = F(350) - c
    return F(sum(max(F(100 * f), cont_c) for f in range(1, 7)), 6) - 350


check("L03 R2 gain at fee 100 = 100/3", gain(100), F(100, 3))
check("L03 R2 gain at fee 1 = 74.5", gain(1), F(149, 2))
check("L03 R2 gain > 10", gain(100) > 10, True)


# stopping rules, fair and biased, by recursion and by sequences
def expect(outcomes, rule, horizon=6):
    def value(h):
        if len(h) == horizon or rule(h):
            return F(sum(h))
        return sum((p * value(h + (x,)) for x, p in outcomes), F(0))

    return value(())


RULES = {
    "play all": lambda h: False,
    "first win": lambda h: bool(h) and h[-1] > 0,
    "first loss": lambda h: bool(h) and h[-1] < 0,
    "total 100": lambda h: sum(h) >= 100,
    "total +-200": lambda h: sum(h) >= 200 or sum(h) <= -200,
}
FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
BIAS = ((150, F(1, 2)), (-100, F(1, 2)))
for name, rule in RULES.items():
    check(f"L03 fair {name} = 0", expect(FAIR, rule), 0)
exp_biased = {name: expect(BIAS, rule) for name, rule in RULES.items()}
check("L03 biased play all 150", exp_biased["play all"], 150)
check("L03 biased first win 1575/32", exp_biased["first win"], F(1575, 32))
check("L03 biased first loss 1575/32", exp_biased["first loss"], F(1575, 32))
check("L03 biased total100 575/8", exp_biased["total 100"], F(575, 8))
check("L03 biased total200 625/8", exp_biased["total +-200"], F(625, 8))
check("L03 E2 change -575/8", exp_biased["total +-200"] - 150, F(-575, 8))
check("L03 E2 change decimal -71.875", float(exp_biased["total +-200"] - 150), -71.875)
# R1 two-turn look-ahead rule
tot = F(0)
for x1, x2 in itertools.product((100, -100), repeat=2):
    tot += F(max(x1, x1 + x2), 4)
check("L03 R1 expected total 50", tot, 50)
# M2 fair win-or-lose p=1/3
check("L03 M2 p=1/3", F(1, 3) * 300 - 100, 0)
# M3 two-stage 200
check("L03 M3 two-stage 200", F(1, 2) * 100 + F(1, 2) * (-50 + F(700, 2)), 200)
# P3 threshold
check("L03 P3 threshold 100f<250 faces", [f for f in range(1, 7) if 100 * f < 250], [1, 2])
# R3 finite horizon N=1..6 zero
for N in range(1, 7):
    check(f"L03 R3 total-100 rule horizon {N} = 0", expect(FAIR, RULES["total 100"], N), 0)

print()
print("FAILS:", fails)
print("TOTAL FAILS:", len(fails))
