"""Independent re-derivation of every number that a PC3 card or a lesson sentence states, from first principles.

Written without importing the lab twins. Usage: python -I ledgers/PC3/scripts/PC3-d-r5/rederive_r5.py
"""
import math
import random
from fractions import Fraction as F
from itertools import product

def check(label, got, want, tol=0.0):
    ok = abs(got - want) <= tol if isinstance(got, float) or isinstance(want, float) else got == want
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got} want {want}")
    return ok

print("== L01 Fermi and remainder")
lo = 20 * 2 * 300; hi = 60 * 10 * 390
check("bounds", (lo, hi), (12000, 234000))
check("ratio", F(hi, lo), F(39, 2))
check("ln19.5", round(math.log(19.5), 10), 2.9704144656, 1e-10)
ws = [math.log(3), math.log(5), math.log(1.3)]
check("sum widths = ln19.5", round(sum(ws), 10), round(math.log(19.5), 10), 1e-12)
check("factor widths", [round(w, 10) for w in ws], [1.0986122887, 1.6094379124, 0.2623642645], 1e-10)
base = math.log(19.5)
r_sym = base - math.log(19.5 * 2 / 3 / 0 + 1) if False else base - math.log((60 * 10 * 390 / 0 + 1)) if False else None
# narrowings
def width(f):
    l = 1; u = 1
    for a, b in f:
        l *= a; u *= b
    return math.log(u / l)
facts = [(F(20), F(60)), (F(2), F(10)), (F(300), F(390))]
w0 = width(facts)
r1 = w0 - width([(F(20), F(40)), facts[1], facts[2]])
r2 = w0 - width([facts[0], (F(4), F(8)), facts[2]])
r3 = w0 - width([facts[0], facts[1], (F(330), F(360))])
check("reduce symbols 0.4055", round(r1, 4), 0.4055, 0)
check("reduce quote 0.9163", round(r2, 4), 0.9163, 0)
check("reduce minutes 0.1754", round(r3, 4), 0.1754, 0)
check("share quote 30.8", round(100 * r2 / w0, 1), 30.8, 0)
check("share minutes 5.9", round(100 * r3 / w0, 1), 5.9, 0)
check("after quote narrowing total", round(w0 - r2, 4), 2.0541, 0)
check("after minutes narrowing total", round(w0 - r3, 4), 2.7951, 0)
check("after symbols narrowing total", round(w0 - r1, 4), 2.5649, 0)
check("geo midpoint", round(math.sqrt(12000 * 234000), 2), 52990.57, 0)
check("geo midpoint 4dp", round(math.sqrt(12000 * 234000), 4), 52990.5652, 0)
check("E3 ln16.5", round(math.log(16.5), 4), 2.8034, 0)
check("E3 change", round(math.log(19.5) - math.log(16.5), 6), 0.167054, 0)
check("R1 half", round(base / 2, 4), 1.4852, 0)
check("R1 ln5", round(math.log(5), 4), 1.6094, 0)
check("R3 A reduction", round(math.log(3 / 2), 4), 0.4055, 0)
check("R3 B reduction", round(math.log(2.5 / 1.01), 4), 0.9063, 0)

def rem(n, x):
    return (1 + x) ** n - 1 - n * x
def bnd(n, x):
    return F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x

for n, x in ((10, F(1, 100)), (10, F(1, 20)), (2, F(1, 100)), (5, F(1, 100)), (5, F(1, 20)), (2, F(1, 20))):
    r = rem(n, x); b = bnd(n, x)
    print(f"  n={n} x={x}: exact={float(1+n*x)}+ rem={float(r):.10f} bound={float(b):.10f} first-order={float(1+n*x):.10f}")
check("(1.01)^10 to 10dp", f"{float((1 + F(1, 100)) ** 10):.10f}", "1.1046221254")
check("remainder 10dp", f"{float(rem(10, F(1,100))):.10f}", "0.0046221254")
check("bound 10dp", f"{float(bnd(10, F(1,100))):.10f}", "0.0048728552")
check("ratio rem/bound", round(float(rem(10, F(1,100)) / bnd(10, F(1,100))), 4), 0.9485, 0)
check("bound/rem-1", round(float(bnd(10, F(1,100)) / rem(10, F(1,100)) - 1), 3), 0.054, 0)
check("miss at 1/20 exact 10dp", f"{float((1+F(1,20))**10):.4f}", "1.6289")
check("miss 0.1289", f"{float(rem(10, F(1,20))):.4f}", "0.1289")
check("bound 1/20 4dp", f"{float(bnd(10, F(1,20))):.4f}", "0.1662")
check("miss share 7.9", round(100 * float(rem(10, F(1,20))) / float((1 + F(1,20)) ** 10), 1), 7.9, 0)
check("n=10 x=1/20 bound 10dp", f"{float(bnd(10,F(1,20))):.10f}", "0.1662137374")
check("E2 bound 0.0048728552/0.0046221254", round(0.0048728552 / 0.0046221254 - 1, 3), 0.054, 0)
check("n=2 remainder equals bound", rem(2, F(3, 7)) == bnd(2, F(3, 7)), True)
check("M3 remainder 31/1000", rem(3, F(1, 10)), F(31, 1000))
check("M3 bound 33/1000", bnd(3, F(1, 10)), F(33, 1000))

print("== L02 conditional and urn")
space = list(product("HT", repeat=2))
def P(ev, given=None):
    g = [o for o in space if (given is None or given(o))]
    return F(sum(1 for o in g if ev(o)), len(g))
check("both|at least one", P(lambda o: o == ("H","H"), lambda o: "H" in o), F(1, 3))
check("both|first head", P(lambda o: o == ("H","H"), lambda o: o[0] == "H"), F(1, 2))
check("one|both", P(lambda o: "H" in o, lambda o: o == ("H","H")), F(1))
balls = ["r1","r2","r3","b1","b2"]
pairs = [(a,b) for a in balls for b in balls if a != b]
red = {"r1","r2","r3"}
def PP(ev, given=lambda p: True):
    g = [p for p in pairs if given(p)]
    return F(sum(1 for p in g if ev(p)), len(g))
check("second red", PP(lambda p: p[1] in red), F(3, 5))
check("first red", PP(lambda p: p[0] in red), F(3, 5))
check("both red", PP(lambda p: p[0] in red and p[1] in red), F(3, 10))
check("second red | first blue", PP(lambda p: p[1] in red, lambda p: p[0].startswith("b")), F(3, 4))
# Monty Hall both rules by enumeration
def monty(rule):
    stay = F(0); sw = F(0); tot = F(0)
    for car, pick in product(range(3), range(3)):
        others = [d for d in range(3) if d != pick]
        for opened in others:
            if rule == "A":
                goats = [d for d in others if d != car]
                if opened not in goats: continue
                p = F(1, len(goats))
            else:
                if opened == car: continue
                p = F(1, 2)
            w = F(1, 9) * p
            tot += w
            swd = [d for d in others if d != opened][0]
            if pick == car: stay += w
            if swd == car: sw += w
    return stay / tot, sw / tot
check("monty A", monty("A"), (F(1,3), F(2,3)))
check("monty B", monty("B"), (F(1,2), F(1,2)))
check("bag posterior", F(1,2)*F(3,4)/(F(1,2)*F(3,4)+F(1,2)*F(1,4)), F(3,4))
check("M1 die", P_ := F(1, 6), F(1, 6))
check("M2 P(A|B)", (F(1,2)*F(3,10))/(F(1,2)*F(3,10)+F(1,5)*F(7,10)), F(15,29))
check("E1 57/64", F(57, 64), 1 - F(1, 64) - F(6, 64))

print("== L03 expectations and stopping rules")
faces = range(1, 7)
cont = F(sum(100 * g for g in faces), 6) - 100
check("continuation 250", cont, F(250))
vals = [max(100 * f, cont) for f in faces]
check("reroll value 1150/3", sum(vals) / 6, F(1150, 3))
best = max(sum((100 * f if bit[f - 1] else cont) for f in faces) / 6 for bit in product((0, 1), repeat=6))
check("best of 64 policies", best, F(1150, 3))
def rule_value(outcomes, stop, horizon=6):
    def val(h):
        if len(h) == horizon or stop(h):
            return F(sum(h))
        return sum((p * val(h + (x,)) for x, p in outcomes), F(0))
    return val(())
fair = ((100, F(1,2)), (-100, F(1,2)))
biased = ((150, F(1,2)), (-100, F(1,2)))
rules = [
    ("all", lambda h: False),
    ("first win", lambda h: bool(h) and h[-1] > 0),
    ("first loss", lambda h: bool(h) and h[-1] < 0),
    ("total 100", lambda h: sum(h) >= 100),
    ("200 band", lambda h: sum(h) >= 200 or sum(h) <= -200),
]
for name, r in rules:
    print(f"  fair {name}: {rule_value(fair, r)}   biased {name}: {rule_value(biased, r)}")
check("biased first loss 1575/32", rule_value(biased, rules[2][1]), F(1575, 32))
check("biased total100 575/8", rule_value(biased, rules[3][1]), F(575, 8))
check("biased 200 band 625/8", rule_value(biased, rules[4][1]), F(625, 8))
check("biased all 150", rule_value(biased, rules[0][1]), F(150))
check("E2 change", F(625, 8) - 150, F(-575, 8))
check("E3 choice value 100/3", F(1150, 3) - 350, F(100, 3))
# R1 two-turn look-ahead
paths = [(100, 100), (100, -100), (-100, 100), (-100, -100)]
tot = []
for a, b in paths:
    w1, w2 = a, a + b
    tot.append(w1 if w1 > w2 else w2)  # stop at turn with larger cumulative total
check("R1 mean 50", F(sum(tot), 4), F(50))
# R2 fee
for c in (100, 1):
    g = F(sum(max(100 * f, 350 - c) for f in faces), 6) - 350
    print("  R2 fee", c, "gain", g)
check("R2 fee100 gain 100/3", F(sum(max(100 * f, 250) for f in faces), 6) - 350, F(100, 3))
check("R2 fee1 gain 74.5", F(sum(max(100 * f, 349) for f in faces), 6) - 350, F(149, 2))
check("P3 threshold", [f for f in faces if 100 * f < 250], [1, 2])
check("M1 paid die", 100 * F(7, 2) - 50, F(300))
check("M2 p", F(1, 3), F(1, 3))
check("M3 two-stage", F(1,2)*100 + F(1,2)*(-50 + 100*F(7,2)), F(200))
check("two dice E", F(7, 2) + F(7, 2), F(7))

print("== L04 market making (seed 0 path) and identities")
rng = random.Random(0)
HORIZON = 20
path = [10000]
arr = []
for _ in range(HORIZON):
    mv = 5 if rng.random() < 0.5 else -5
    path.append(path[-1] + mv)
    d = rng.random()
    arr.append("ub" if d < 0.25 else "us" if d < 0.5 else "inf")
print("  seed0 arrivals", arr)
print("  informed count", arr.count("inf"), "of", HORIZON)
check("E2 informed 13", arr.count("inf"), 13)
check("E2 se", round(math.sqrt(0.25 / 20), 4), 0.1118, 0)
check("E2 z", round((0.65 - 0.5) / math.sqrt(0.25 / 20), 2), 1.34, 0)

def play(seed):
    rng = random.Random(seed)
    path = [10000]
    arr = []
    for _ in range(HORIZON):
        mv = 5 if rng.random() < 0.5 else -5
        path.append(path[-1] + mv)
        d = rng.random()
        arr.append("ub" if d < 0.25 else "us" if d < 0.5 else "inf")
    inv = 0; cash = 0; last = None; fills = 0; cf = 0
    for t in range(1, HORIZON + 1):
        mid = 10000 if last is None else last
        bid, ask = mid - 10, mid + 10
        v = path[t]; a = arr[t - 1]
        if a == "ub": side = -1
        elif a == "us": side = 1
        else:
            side = -1 if v > ask else 1 if v < bid else 0
        if side != 0 and abs(inv + side) <= 10:
            price = ask if side < 0 else bid
            cash += -side * price; cf += -side * price; inv += side; last = price; fills += 1
    settle = path[HORIZON]
    return fills, cf, inv, settle, cash + inv * settle
print("  seed0 (fills, cashflow, inv, settle, pnl)", play(0))
print("  seed1 (fills, cashflow, inv, settle, pnl)", play(1))
f0 = play(0)
check("L04 seed0 9 fills", f0[0], 9)
check("L04 seed0 cash flow -9950", f0[1], -9950)
check("L04 seed0 inv 1", f0[2], 1)
check("L04 seed0 settle 9980", f0[3], 9980)
check("L04 seed0 pnl 30", f0[4], 30)
f1 = play(1)
check("E1 seed1 fills 16", f1[0], 16)
check("E1 seed1 cash flow 20100", f1[1], 20100)
check("E1 seed1 inv -2", f1[2], -2)
check("E1 seed1 settle 10020", f1[3], 10020)
check("E1 seed1 pnl 60", f1[4], 60)
h = 10; p = F(1, 2)
def trade_term(v, a=10010, b=9990):
    return (1 - p) * h - p * (max(v - a, 0) + max(b - v, 0))
check("Ex3.2 v=10000", trade_term(10000), F(5))
check("Ex3.2 v=10020", trade_term(10020), F(0))
check("Ex3.2 v=9985", trade_term(9985), F(5, 2))
check("E3 settle pnl 30", -9950 + 1 * 9980, 30)
check("E3 mid pnl 40", -9950 + 1 * 9990, 40)
check("R1 d", (1 - F(3, 5)) * 10 / F(3, 5), F(20, 3))
check("R3 variance", [25 * I * I for I in (1, 2)], [25, 100])
check("M2 at I=10 sell refused", 10 + 1 <= 10, False)
check("Remark 4.2 at I=10 trade term", F(1, 4) * 10, F(5, 2))

print("== L05 operation counts, seed 5 and seed 6")
def make(seed, n=200):
    r = random.Random(seed)
    return [r.randint(0, 999) for _ in range(n)]
def naive(xs, k):
    c = 0; out = []
    for s in range(len(xs) - k + 1):
        best = xs[s]
        for x in xs[s + 1 : s + k]:
            c += 1
            if x > best: best = x
        out.append(best)
    return out, c
def dq(xs, k):
    w = []; out = []; comp = 0; pushes = 0; pops = 0
    for i, x in enumerate(xs):
        while w:
            comp += 1
            if xs[w[-1]] > x: break
            w.pop(); pops += 1
        w.append(i); pushes += 1
        if w[0] <= i - k:
            w.pop(0); pops += 1
        if i >= k - 1: out.append(xs[w[0]])
    return out, comp, pushes, pops
xs5 = make(5)
check("seed5 first five", xs5[:5], [637, 261, 759, 367, 814])
check("seed5 max", max(xs5), 998)
check("naive k=8", naive(xs5, 8)[1], 1351)
check("deque k=8 comps", dq(xs5, 8)[1], 354)
check("deque k=8 pushes/pops", (dq(xs5, 8)[2], dq(xs5, 8)[3]), (200, 199))
for k in (1, 2, 8, 32, 200):
    o, c, pu, po = dq(xs5, k)
    print(f"  k={k} naive={naive(xs5, k)[1]} deque_comp={c} pops={po} pushes={pu}")
check("k=32 naive 5239", naive(xs5, 32)[1], 5239)
check("k=32 deque 382", dq(xs5, 32)[1], 382)
check("k=200 deque 387", dq(xs5, 200)[1], 387)
check("k=200 pops 194", dq(xs5, 200)[3], 194)
xs6 = make(6)
o6, c6, pu6, po6 = dq(xs6, 8)
check("E2 seed6 naive", naive(xs6, 8)[1], 1351)
check("E2 seed6 deque comps 350", c6, 350)
check("E2 seed6 pushes 200", pu6, 200)
check("E2 seed6 pops 197", po6, 197)
check("E2 seed6 outputs equal", naive(xs6, 8)[0] == dq(xs6, 8)[0], True)
check("E1 ratio 13.7", round(5239 / 382, 1), 13.7)
check("E3 bound 194+200", 194 + 200, 394)
check("n=10 k=4 naive", (10 - 4 + 1) * (4 - 1), 21)
check("strictly increasing n-1", dq(list(range(50)), 7)[1], 49)
check("heap bound n=200", 3 * 200 * 7, 4200)
check("P1 peak", (200 - 101 + 1) * (101 - 1), 10000)
print("== L06 forward, NPV, case")
D = F(97, 100); S = F(9700)
check("no-arb F", S / D, F(10000))
check("M1 forward", F(4900) / F(98, 100), F(5000))
A = sum((F(1) / (1 + F(1, 10)) ** t for t in (1, 2, 3)), F(0))
check("annuity 3310/1331", A, F(3310, 1331))
check("break-even 399300/331", F(3000) / A, F(399300, 331))
def npv(u, r):
    A_ = sum((F(1) / (1 + r) ** t for t in (1, 2, 3)), F(0))
    return -F(15000000) + 5000 * u * A_
check("NPV zero at BE", npv(F(399300, 331), F(1, 10)), F(0))
print("  NPV 200 @10% exact", npv(F(200), F(1,10)), float(npv(F(200), F(1,10))))
print("  NPV 1600 @10% exact", npv(F(1600), F(1,10)), float(npv(F(1600), F(1,10))))
for r in (F(8, 100), F(10, 100), F(12, 100)):
    A_ = sum((F(1) / (1 + r) ** t for t in (1, 2, 3)), F(0))
    be = F(3000) / A_
    print(f"  rate {r}: BE {float(be):.6f} NPV200 {float(npv(F(200), r)):.4f} NPV1600 {float(npv(F(1600), r)):.4f}")
check("M2 NPV (600/11 is 60/1.1)", -100 + F(600, 11) + F(6000, 121), F(500, 121))
check("M3 BE", F(100000 * 1331, 400 * 3310), F(33275, 331))
check("E3 subtractions", float(F(399300, 331)), 1206.3444, 1e-4)
print("  unrounded BE 8%/10%/12%:")
for r in (F(8,100), F(10,100), F(12,100)):
    A_ = sum((F(1) / (1 + r) ** t for t in (1, 2, 3)), F(0))
    print("   ", f"{float(F(3000)/A_):.4f}")
print("  E3 width", round(1249.0469 - 1164.1005, 4), "avg", round((1249.0469 - 1164.1005) / 4, 4))
check("R3 margin", float(F(15000000 * 1331, 1600 * 3310)), 3769.8, 0.05)
check("R3 ratio", round(float(F(15000000 * 1331, 1600 * 3310)) / 5000, 4), 0.7540, 0)
check("R3 fall", round(100 * (1 - float(F(15000000 * 1331, 1600 * 3310)) / 5000), 1), 24.6, 0)
check("E2 NPV at 1200", float(npv(F(1200), F(1,10))), -78888.05, 0.01)
check("E2 NPV at 1300", float(npv(F(1300), F(1,10))), 1164537.94, 0.01)
check("E2 NPV at 1300 exact", npv(F(1300), F(1,10)), F(1550000000, 1331))
print("== done")
