"""PC3 slice a, round 8: independent recomputation of every number in the hub, L01, L02 and L03 prose and keys."""
import itertools
import math
import random
from fractions import Fraction as F

fails: list[str] = []
n_checks = 0


def chk(label: str, got: object, want: object, tol: float | None = None) -> None:
    global n_checks
    n_checks += 1
    if tol is None:
        ok = got == want
    else:
        ok = abs(float(got) - float(want)) <= tol  # type: ignore[arg-type]
    if not ok:
        fails.append(label)
    print(("PASS " if ok else "FAIL ") + f"{label}: got {got} want {want}")


def dec(x: float, places: int) -> str:
    return f"{x:.{places}f}"


# ---- hub placement ----
chk("hub die expected face 21/6", F(21, 6), F(7, 2))
chk("hub expected face 3.5", 3.5, float(F(21, 6)), 1e-6)
chk("hub two coins both heads", 0.25, 0.5 * 0.5, 1e-6)
chk("hub ln(e^2) = 2", 2, round(math.log(math.exp(2)), 9), 1e-9)
chk("hub derivative x^3 at 1", 3, 3 * 1**2)
chk("hub PV 100/1.1 to 6dp", "90.909091", dec(100 / 1.1, 6))
chk("hub skill rung 1 cash flow", -10005, -10005)
chk("hub skill rung 2 mark", 10040, 1 * 10040)
chk("hub placement 8 of 10 = 80%", 8 / 10, 0.8)
chk("hub placement 7 of 10 = 70%", 7 / 10, 0.7)
chk("hub 36/50 = 72%", 36 / 50, 0.72)
chk("hub 14/50 = 28%", 14 / 50, 0.28)
chk("hub hours lines sum 1+1+3+2+2+4+1", 1 + 1 + 3 + 2 + 2 + 4 + 1, 14)
chk("hub 6 lessons x 6 h", 6 * 6, 36)

# ---- L01 Example 1.4 and Lab Part 1 ----
lo = F(20) * 2 * 300
hi = F(60) * 10 * 390
chk("L01 product lower", lo, 12000)
chk("L01 product upper", hi, 234000)
chk("L01 ratio 19.5", float(hi / lo), 19.5, 1e-12)
w = math.log(19.5)
chk("L01 ln 19.5 to 10dp", dec(w, 10), "2.9704144656")
chk("L01 ln3+ln5+ln1.3 = ln19.5", math.log(3) + math.log(5) + math.log(1.3), w, 1e-12)
chk("L01 ln3", dec(math.log(3), 4), "1.0986")
chk("L01 ln5", dec(math.log(5), 4), "1.6094")
chk("L01 ln1.3", dec(math.log(1.3), 4), "0.2624")
chk("L01 geometric midpoint 52990.57 (2dp)", dec(math.sqrt(12000 * 234000), 2), "52990.57")
chk("L01 geometric midpoint 52990.5652 (4dp, quiz)", dec(math.sqrt(2808000000), 4), "52990.5652")
chk("L01 midpoint unrounded 52990.5651979671", math.sqrt(2808000000), 52990.5651979671, 1e-9)

# Part 2 narrowings
base = w
sym = math.log(40 / 20) ; qu = math.log(8 / 4); mi = math.log(360 / 330)
red_sym = math.log(3) - math.log(2)
red_qu = math.log(5) - math.log(2)
red_mi = math.log(1.3) - mi
chk("L01 symbols reduction 0.4055", dec(red_sym, 4), "0.4055")
chk("L01 quote reduction 0.9163", dec(red_qu, 4), "0.9163")
chk("L01 quote reduction full 0.9162907319", red_qu, 0.9162907319, 1e-10)
chk("L01 minutes reduction 0.1754", dec(red_mi, 4), "0.1754")
chk("L01 minutes reduction full 0.1753528875", red_mi, 0.1753528875, 1e-10)
chk("L01 totals 2.5649, 2.0541, 2.7951", [dec(base - red_sym, 4), dec(base - red_qu, 4), dec(base - red_mi, 4)], ["2.5649", "2.0541", "2.7951"])
chk("L01 quote share 30.8 percent", round(100 * red_qu / base, 1), 30.8)
chk("L01 minutes share 5.9 percent", round(100 * red_mi / base, 1), 5.9)
chk("L01 E2 four-place quotient 0.3085", dec(0.9163 / 2.9704, 4), "0.3085")
chk("L01 E2 full quotient 0.308472", dec(red_qu / base, 6), "0.308472")
chk("L01 E2 minutes quotient 0.059033", dec(red_mi / base, 6), "0.059033")
chk("L01 E2 four-place quotient percent 30.85", dec(100 * 0.9163 / 2.9704, 2), "30.85")
chk("L01 symbols reduction is the smaller of quote", red_sym < red_qu, True)
chk("L01 largest width is quote (ln5)", max(math.log(3), math.log(5), math.log(1.3)), math.log(5), 0)
chk("L01 misconception: minutes 0.1754 is 5.9 percent", dec(100 * red_mi / base, 1), "5.9")

# E3 changed range
w_e3 = math.log(F(60 * 10 * 330, 12000))
chk("L01 E3 ratio 16.5", float(F(60 * 10 * 330, 12000)), 16.5, 0)
chk("L01 E3 ln16.5 = 2.8034", dec(w_e3, 4), "2.8034")
chk("L01 E3 change 0.167054", dec(math.log(19.5) - math.log(16.5), 6), "0.167054")

# R1 half, R3 counterexample
chk("L01 R1 half of total 1.4852", dec(w / 2, 4), "1.4852")
chk("L01 R3 reduction A 0.4055", dec(math.log(3 / 2), 4), "0.4055")
chk("L01 R3 reduction B 0.9063", dec(math.log(2.5 / 1.01), 4), "0.9063")
chk("L01 R3 widths A ln3 = 1.0986 > B ln2.5 = 0.9163", (dec(math.log(3), 4), dec(math.log(2.5), 4)), ("1.0986", "0.9163"))

# M1 M2 M3 mechanics
chk("L01 M1 lower 5", 2 * 5 * F(1, 2), 5)
chk("L01 M1 upper 21", 3 * 7 * 1, 21)
chk("L01 M1 ln(21/5) = ln 4.2", math.log(F(21, 5)), math.log(4.2), 1e-12)
chk("L01 M1 factor widths sum", math.log(1.5) + math.log(1.4) + math.log(2), math.log(4.2), 1e-12)
chk("L01 M2 product [2,32]", (1 * 2, 4 * 8), (2, 32))
chk("L01 M2 ln16 4dp 2.7726", dec(math.log(16), 4), "2.7726")
chk("L01 M3 remainder 31/1000", (F(11, 10)) ** 3 - 1 - F(3, 10), F(31, 1000))
chk("L01 M3 bound 33/1000", F(3 * 2, 2) * F(11, 10) * F(1, 100), F(33, 1000))
chk("L01 M3 inequality", F(31, 1000) <= F(33, 1000), True)

# E1, E4
r1 = 0.0046221254 / 0.0048728552
chk("L01 E1 ratio 0.94854 (5dp) and 0.9485 (4dp)", (dec(r1, 5), dec(r1, 4)), ("0.94854", "0.9485"))
chk("L01 E4 ln2+ln2 = ln4", math.log(2) + math.log(2), math.log(4), 1e-12)

# Example 1.7 and Part 3 (all six pairs)
def rem(n: int, x: F) -> F:
    return (1 + x) ** n - 1 - n * x
def bound(n: int, x: F) -> F:
    return F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
def tail(n: int, x: F) -> F:
    return sum((math.comb(n, j) * x ** j for j in range(2, n + 1)), F(0))
pairs_want = {
    (2, F(1, 100)): ("0.0001000000", "0.0001000000"),
    (2, F(1, 20)): ("0.0025000000", "0.0025000000"),
    (5, F(1, 100)): ("0.0010100501", "0.0010303010"),
    (5, F(1, 20)): ("0.0262815625", "0.0289406250"),
    (10, F(1, 100)): ("0.0046221254", "0.0048728552"),
    (10, F(1, 20)): ("0.1288946268", "0.1662137374"),
}
for (n, x), (wr, wb) in pairs_want.items():
    r, b = rem(n, x), bound(n, x)
    chk(f"L01 Part3 n={n} x={x} remainder", dec(float(r), 10), wr)
    chk(f"L01 Part3 n={n} x={x} bound", dec(float(b), 10), wb)
    chk(f"L01 Part3 n={n} x={x} 0<=rem<=bound and tail identity", (0 <= r <= b, r == tail(n, x)), (True, True))
chk("L01 Example 1.7 (1.01)^10 to 10dp", dec(float((F(101, 100)) ** 10), 10), "1.1046221254")
chk("L01 Example 1.7 ratio 0.9485 (4dp)", dec(float(rem(10, F(1, 100)) / bound(10, F(1, 100))), 4), "0.9485")
chk("L01 Example 1.7 bound/remainder - 1 = 0.054", dec(float(bound(10, F(1, 100)) / rem(10, F(1, 100)) - 1), 3), "0.054")
chk("L01 Example 1.7 x=1/20 exact 1.6289 (4dp)", dec(float((F(21, 20)) ** 10), 4), "1.6289")
chk("L01 Example 1.7 x=1/20 remainder 0.1289", dec(float(rem(10, F(1, 20))), 4), "0.1289")
chk("L01 Example 1.7 x=1/20 bound 0.1662", dec(float(bound(10, F(1, 20))), 4), "0.1662")
chk("L01 Example 1.7 miss share 0.079", dec(float(rem(10, F(1, 20)) / (F(21, 20)) ** 10), 3), "0.079")
chk("L01 Remark n=2 bound equals remainder x^2", (rem(2, F(3, 7)), bound(2, F(3, 7))), (F(9, 49), F(9, 49)))

# Part 1 grid: 125 points all inside
ax = [[F(lo_) + (F(hi_) - F(lo_)) * F(k, 4) for k in range(5)] for lo_, hi_ in [(20, 60), (2, 10), (300, 390)]]
prods = [a * b * c for a, b, c in itertools.product(*ax)]
chk("L01 grid 125 inside", (sum(12000 <= p <= 234000 for p in prods), len(prods)), (125, 125))

# ---- L02 ----
# two flips and Monty Hall brute force
flips = list(itertools.product("HT", repeat=2))
def cond(ev, given, space):
    k = [o for o in space if given(o)]
    return F(len([o for o in k if ev(o)]), len(k))
chk("L02 P(both|at least one) 1/3", cond(lambda o: o == ("H", "H"), lambda o: "H" in o, flips), F(1, 3))
chk("L02 P(both|first H) 1/2", cond(lambda o: o == ("H", "H"), lambda o: o[0] == "H", flips), F(1, 2))
chk("L02 P(at least one|both) 1", cond(lambda o: "H" in o, lambda o: o == ("H", "H"), flips), F(1))
# urn
balls = ["r1", "r2", "r3", "b1", "b2"]
pr = [(a, b) for a in balls for b in balls if a != b]
red = {"r1", "r2", "r3"}
chk("L02 urn 20 pairs", len(pr), 20)
chk("L02 P(second red) 3/5", F(sum(b in red for _, b in pr), 20), F(3, 5))
chk("L02 P(first red) 3/5", F(sum(a in red for a, _ in pr), 20), F(3, 5))
chk("L02 P(both red) 3/10", F(sum(a in red and b in red for a, b in pr), 20), F(3, 10))
chk("L02 P(second red|first blue) 3/4", cond(lambda o: o[1] in red, lambda o: o[0].startswith("b"), pr), F(3, 4))
chk("L02 M1 dice", cond(lambda o: sum(o) == 7, lambda o: o[0] == 3, list(itertools.product(range(1, 7), repeat=2))), F(1, 6))
chk("L02 M2 P(B) 29/100, P(A|B) 15/29", (F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10), F(1, 2) * F(3, 10) / (F(29, 100))), (F(29, 100), F(15, 29)))
chk("L02 M3 (4/6)(3/5) = 2/5", F(4, 6) * F(3, 5), F(2, 5))
chk("L02 E1 57/64 by complement", 1 - F(1, 64) - F(6, 64), F(57, 64))
chk("L02 E3 difference 1/6", F(2, 3) - F(1, 2), F(1, 6))
chk("L02 R3 P(second red | first blue) with 3 red 1 blue", F(3, 3), 1)

# Monty Hall: brute force over (car, pick, host) with uniform host rules
def monty(rule: str) -> tuple[F, F]:
    stay = switch = total = F(0)
    for car, pick in itertools.product(range(3), repeat=2):
        others = [d for d in range(3) if d != pick]
        for opened in others:
            if rule == "A":
                goats = [d for d in others if d != car]
                if opened not in goats:
                    continue
                p = F(1, len(goats))
            else:
                if opened == car:
                    continue
                p = F(1, 2)
            wgt = F(1, 3) * F(1, 3) * p
            total += wgt
            sw = next(d for d in others if d != opened)
            stay += wgt * (pick == car)
            switch += wgt * (sw == car)
    return stay / total, switch / total
chk("L02 Monty rule A (stay, switch)", monty("A"), (F(1, 3), F(2, 3)))
chk("L02 Monty rule B (stay, switch)", monty("B"), (F(1, 2), F(1, 2)))
chk("L02 Monty 9 (car,pick) pairs", len(list(itertools.product(range(3), repeat=2))), 9)

# Bag example
chk("L02 bag P(red) 1/2", F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4), F(1, 2))
chk("L02 bag P(bag1|red) 3/4", F(1, 2) * F(3, 4) / F(1, 2), F(3, 4))
chk("L02 Q bag 0.75", 0.75, float(F(3, 4)), 1e-9)

# Drill set: independent re-generation with the same call order, exact probabilities
rng = random.Random(0)
items = []
for number in range(1, 13):
    flips_n = rng.randint(3, 8)
    if rng.random() < 0.5:
        k = rng.randint(1, flips_n)
        items.append(("atleast", flips_n, k))
    else:
        j = rng.randint(1, flips_n)
        items.append(("first", flips_n, j))
def exact(kind: str, nflips: int, arg: int) -> F:
    if kind == "atleast":
        return F(sum(math.comb(nflips, i) for i in range(arg, nflips + 1)), 2 ** nflips)
    return F(1, 2 ** arg)
want_items = [F(1, 16), F(1, 8), F(21, 32), F(57, 64), F(15, 16), F(1, 4), F(1, 128), F(1, 8), F(1, 8), F(31, 32), F(1, 32), F(1, 256)]
chk("L02 Part 1 twelve drill probabilities (independent regeneration)", [exact(*it) for it in items], want_items)
chk("L02 Q 1/3 6dp 0.333333", dec(1 / 3, 6), "0.333333")
chk("L02 Q 3/10 6dp", dec(0.3, 6), "0.300000")

# ---- L03 ----
die = list(range(1, 7))
chk("L03 E[face] 7/2", F(sum(die), 6), F(7, 2))
chk("L03 two dice E[X+Y] 7", F(sum(x + y for x in die for y in die), 36), 7)
chk("L03 100*E face 350", 100 * F(7, 2), 350)
cont = F(sum(100 * g for g in die), 6) - 100
chk("L03 continuation 250", cont, 250)
best = [max(F(100 * f), cont) for f in die]
chk("L03 backward induction 1150/3", sum(best) / 6, F(1150, 3))
chk("L03 P3 threshold 100f < 250 only f=1,2", [f for f in die if 100 * f < 250], [1, 2])
chk("L03 gain 100/3", F(1150, 3) - 350, F(100, 3))
chk("L03 383.33 two places", dec(float(F(1150, 3)), 2), "383.33")
chk("L03 33.33 two places", dec(float(F(100, 3)), 2), "33.33")
chk("L03 383.333333 6dp", dec(float(F(1150, 3)), 6), "383.333333")
best64 = max(sum((F(100 * f) if bits[f - 1] else cont) for f in die) / 6 for bits in itertools.product((0, 1), repeat=6))
chk("L03 best of 64 policies = 1150/3", best64, F(1150, 3))
chk("L03 stop every face 350", sum(F(100 * f) for f in die) / 6, 350)

# fair/biased stopping rules: independent recursion with memo
def expect(outcomes, rule, horizon=6):
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def val(h):
        if len(h) == horizon or rule(h):
            return F(sum(h))
        return sum(p * val(h + (x,)) for x, p in outcomes)

    return val(())
rules = {
    "play": lambda h: False,
    "first win": lambda h: bool(h) and h[-1] > 0,
    "first loss": lambda h: bool(h) and h[-1] < 0,
    "reach 100": lambda h: sum(h) >= 100,
    "200 gain or loss": lambda h: sum(h) >= 200 or sum(h) <= -200,
}
FAIR = ((100, F(1, 2)), (-100, F(1, 2)))
BIAS = ((150, F(1, 2)), (-100, F(1, 2)))
fair_vals = {k: expect(FAIR, r) for k, r in rules.items()}
chk("L03 fair five rules all zero", all(v == 0 for v in fair_vals.values()), True)
bias_vals = {k: expect(BIAS, r) for k, r in rules.items()}
chk("L03 biased play-all 150", bias_vals["play"], 150)
chk("L03 biased first win 1575/32", bias_vals["first win"], F(1575, 32))
chk("L03 biased first loss 1575/32", bias_vals["first loss"], F(1575, 32))
chk("L03 biased reach 100 575/8", bias_vals["reach 100"], F(575, 8))
chk("L03 biased 200 625/8", bias_vals["200 gain or loss"], F(625, 8))
chk("L03 E2 change 625/8-150 = -575/8", F(625, 8) - 150, F(-575, 8))
chk("L03 E2 -71.875", float(F(-575, 8)), -71.875, 0)
chk("L03 biased per turn 25", F(1, 2) * 150 + F(1, 2) * (-100), 25)

# R1: two-turn look-ahead rule
tot = []
for a, b in itertools.product((100, -100), repeat=2):
    w1, w2 = a, a + b
    tot.append(max(w1, w2))
chk("L03 R1 paths totals 200,100,0,-100 mean 50", (sorted(tot, reverse=True), F(sum(tot), 4)), ([200, 100, 0, -100], F(50)))

# R2 fee gain formula
gain = lambda c: F(sum(max(100 * f, 350 - c) for f in die), 6) - 350
chk("L03 R2 gain at fee 100 = 100/3", gain(100), F(100, 3))
chk("L03 R2 gain at fee 1 = 74.5", gain(1), F(149, 2))

# problem set
chk("L03 M1 net 300", 100 * F(7, 2) - 50, 300)
chk("L03 M2 p = 1/3", F(1, 3), F(1, 3))
chk("L03 M2 quiz 0.333333", dec(1 / 3, 6), "0.333333")
chk("L03 M3 200", F(1, 2) * 100 + F(1, 2) * (-50 + 100 * F(7, 2)), 200)
chk("L03 P3 9 uses", 100 * 2 < 250 and 100 * 3 >= 250, True)
chk("L03 quiz 100/3 = 33.33", dec(100 / 3, 2), "33.33")

print(f"\n{n_checks} checks, {len(fails)} FAIL: {fails}")
