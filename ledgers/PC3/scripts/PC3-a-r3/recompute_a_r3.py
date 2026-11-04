"""Round-3 PC3 slice a: independent recomputation of the prose numbers in index.html, L01-L03 (not the lab code).
Run as: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r3/recompute_a_r3.py
Prints each checked quantity with the value recomputed here.
"""

import itertools
import math
from fractions import Fraction as F

ok = True


def show(label: str, value: object) -> None:
    print(f"{label} = {value}")


def check(label: str, got: object, want: object, tol: float = 0.0) -> None:
    global ok
    if isinstance(got, float) or isinstance(want, float):
        good = abs(float(got) - float(want)) <= tol
    else:
        good = got == want
    ok = ok and good
    print(f"{'OK  ' if good else 'FAIL'} {label}: recomputed {got}, page {want}")


# ---- L01 Example 1.4 and Section 2
lo = 20 * 2 * 300
hi = 60 * 10 * 390
check("L01 product lower", lo, 12000)
check("L01 product upper", hi, 234000)
check("L01 ratio", F(hi, lo), F(39, 2))
w = math.log(19.5)
check("L01 ln 19.5 to 4 dp", round(w, 4), 2.9704)
check("L01 ln19.5 to 10 dp", f"{w:.10f}", "2.9704144656")
mid = math.sqrt(12000 * 234000)
check("L01 geometric midpoint to 2 dp", f"{mid:.2f}", "52990.57")
check("L01 geometric midpoint to 4 dp", f"{mid:.4f}", "52990.5652")
check("L01 ln3 + ln5 + ln1.3 = ln19.5", math.log(3) + math.log(5) + math.log(1.3), w, 1e-12)
check("L01 ln3 width", f"{math.log(3):.4f}", "1.0986")
check("L01 ln5 width", f"{math.log(5):.4f}", "1.6094")
check("L01 ln1.3 width", f"{math.log(1.3):.4f}", "0.2624")
check("L01 half total", f"{w / 2:.4f}", "1.4852")

# Section 2 narrowings
sym = math.log(40 / 20)
qu = math.log(8 / 4)
mi = math.log(360 / 330)
red_sym = math.log(3) - math.log(2)
red_qu = math.log(5) - math.log(2)
red_mi = math.log(1.3) - math.log(12 / 11)
check("L01 reduction symbols 0.4055", f"{red_sym:.4f}", "0.4055")
check("L01 reduction quote 0.9163", f"{red_qu:.4f}", "0.9163")
check("L01 reduction minutes 0.1754", f"{red_mi:.4f}", "0.1754")
check("L01 total after quote narrowing 2.0541", f"{w - red_qu:.4f}", "2.0541")
check("L01 total after minutes narrowing 2.7951", f"{w - red_mi:.4f}", "2.7951")
check("L01 total after symbols narrowing 2.5649", f"{w - red_sym:.4f}", "2.5649")
check("L01 quote share 30.8 percent", f"{100 * red_qu / w:.1f}", "30.8")
check("L01 minutes share 5.9 percent", f"{100 * red_mi / w:.1f}", "5.9")
check("L01 quote share from 4dp (0.3085)", f"{0.9163 / 2.9704:.4f}", "0.3085")
check("L01 minutes share from 4dp (0.0590)", f"{0.1754 / 2.9704:.4f}", "0.0590")

# ---- L01 Section 3, Example 1.7, Remark 1.6
def rem(n: int, x: F) -> F:
    return (1 + x) ** n - 1 - n * x


def bnd(n: int, x: F) -> F:
    return F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x


r = rem(10, F(1, 100))
b = bnd(10, F(1, 100))
check("L01 Ex1.7 remainder 10dp", f"{float(r):.10f}", "0.0046221254")
check("L01 Ex1.7 bound 10dp", f"{float(b):.10f}", "0.0048728552")
check("L01 Ex1.7 (1.01)^10 10dp", f"{float((1 + F(1, 100)) ** 10):.10f}", "1.1046221254")
check("L01 Ex1.7 ratio rem/bound 4dp", f"{float(r / b):.4f}", "0.9485")
check("L01 Ex1.7 bound/rem - 1 3dp", f"{float(b / r - 1):.3f}", "0.054")
check("L01 Ex1.7 bound/rem - 1 as percent 5.4", f"{100 * float(b / r - 1):.1f}", "5.4")
r2 = rem(10, F(1, 20))
b2 = bnd(10, F(1, 20))
check("L01 Ex1.7 x=1/20 exact 4dp", f"{float(1 + F(1, 20)) ** 10:.4f}", "1.6289")
check("L01 Ex1.7 x=1/20 remainder 4dp", f"{float(r2):.4f}", "0.1289")
check("L01 Ex1.7 x=1/20 bound 4dp", f"{float(b2):.4f}", "0.1662")
check("L01 Ex1.7 miss share 7.9 percent", f"{100 * float(r2 / (1 + F(1, 20)) ** 10):.1f}", "7.9")
check("L01 Ex1.7 x=1/20 miss ratio 0.079", f"{float(r2 / (1 + F(1, 20)) ** 10):.3f}", "0.079")
check("L01 x=1/20 first-order 1.5", 1 + 10 * F(1, 20), F(3, 2))
check("L01 M3 remainder 31/1000", rem(3, F(1, 10)), F(31, 1000))
check("L01 M3 bound 33/1000", bnd(3, F(1, 10)), F(33, 1000))
check("L01 Remark 1.6 n=2 bound equals x^2", bnd(2, F(1, 3)), F(1, 9))
check("L01 Remark 1.6 n=2 remainder equals x^2", rem(2, F(1, 3)), F(1, 9))
for n in (5, 10):
    for x in (F(1, 100), F(1, 20)):
        check(f"L01 strict remainder < bound n={n} x={x}", rem(n, x) < bnd(n, x), True)

# Example 1.7 'remainder is below the bound'
check("L01 E3 ln16.5 4dp", f"{math.log(16.5):.4f}", "2.8034")
check("L01 E3 ln19.5-ln16.5 6dp", f"{math.log(19.5) - math.log(16.5):.6f}", "0.167054")
check("L01 E3 new product upper", 60 * 10 * 330, 198000)
check("L01 E3 ratio 16.5", F(198000, 12000), F(33, 2))

# R3 counterexample
check("L01 R3 reduction B 0.9063", f"{math.log(2.5) - math.log(1.01):.4f}", "0.9063")
check("L01 R3 width B ln2.5 0.9163", f"{math.log(2.5):.4f}", "0.9163")
check("L01 R3 width A ln3 1.0986", f"{math.log(3):.4f}", "1.0986")
check("L01 R3 reduction A 0.4055", f"{math.log(3) - math.log(2):.4f}", "0.4055")

# quiz numbers
check("L01 quiz ln4 6dp", f"{math.log(4):.6f}", "1.386294")
check("L01 quiz geometric mean 4dp", f"{math.sqrt(2808000000):.4f}", "52990.5652")

# ---- L01 Lab Part 1 grid: 5 points per factor, 125 products, all inside [12000, 234000]
ranges = [(F(20), F(60)), (F(2), F(10)), (F(300), F(390))]
axes = [[a + (b - a) * F(k, 4) for k in range(5)] for a, b in ranges]
prods = [x * y * z for x, y, z in itertools.product(*axes)]
check("L01 grid count", len(prods), 125)
check("L01 grid all inside", all(F(12000) <= p <= F(234000) for p in prods), True)

# ---- L03 numbers, independent of the lab code
fair = [(100, F(1, 2)), (-100, F(1, 2))]
biased = [(150, F(1, 2)), (-100, F(1, 2))]


def paths(outcomes, n):
    for seq in itertools.product(outcomes, repeat=n):
        w_ = F(1)
        for _, p in seq:
            w_ *= p
        yield [x for x, _ in seq], w_


def first_hit_total(seq, rule):
    h = []
    for x in seq:
        h.append(x)
        if rule(h):
            break
    return sum(h)


rules = {
    "play all": lambda h: False,
    "first win": lambda h: bool(h) and h[-1] > 0,
    "first loss": lambda h: bool(h) and h[-1] < 0,
    "reach 100": lambda h: sum(h) >= 100,
    "200 gain or loss": lambda h: sum(h) >= 200 or sum(h) <= -200,
}
for name, rule in rules.items():
    e_fair = sum(w_ * first_hit_total(s, rule) for s, w_ in paths(fair, 6))
    e_bias = sum(w_ * first_hit_total(s, rule) for s, w_ in paths(biased, 6))
    check(f"L03 fair {name} = 0", e_fair, 0)
    print(f"      biased {name} = {e_bias}")
    if name == "first loss":
        check("L03 biased first loss 1575/32", e_bias, F(1575, 32))
    if name == "reach 100":
        check("L03 biased reach100 575/8", e_bias, F(575, 8))
    if name == "200 gain or loss":
        check("L03 biased 200 625/8", e_bias, F(625, 8))
    if name == "play all":
        check("L03 biased play-all 150", e_bias, 150)
    if name == "first win":
        check("L03 biased first win 1575/32", e_bias, F(1575, 32))

# Example 3.6 reroll game
cont = F(sum(100 * g for g in range(1, 7)), 6) - 100
check("L03 continuation 250", cont, 250)
vals = [max(F(100 * f), cont) for f in range(1, 7)]
check("L03 backward-induction value 1150/3", sum(vals) / 6, F(1150, 3))
check("L03 100/3 gain", sum(vals) / 6 - 350, F(100, 3))
best = max(
    sum((F(100 * f) if bits[f - 1] else cont) for f in range(1, 7)) / 6
    for bits in itertools.product((0, 1), repeat=6)
)
check("L03 best of 64 policies", best, F(1150, 3))
check("L03 stop on every face 350", sum(F(100 * f) for f in range(1, 7)) / 6, 350)
check("L03 sum 2300", sum(vals), 2300)
# R2 fee variant
for c, want in ((100, F(100, 3)), (1, F(149, 2))):
    cc = F(350 - c)
    gain = sum(max(F(100 * f), cc) for f in range(1, 7)) / 6 - 350
    check(f"L03 R2 gain at fee {c}", gain, want)
# Misconception: reroll relative
check("L03 E2 625/8-150", F(625, 8) - 150, F(-575, 8))
check("L03 E2 -71.875", float(F(-575, 8)), -71.875)
check("L03 E3 100/3 two dp", f"{float(F(100, 3)):.2f}", "33.33")
check("L03 1150/3 two dp", f"{float(F(1150, 3)):.2f}", "383.33")

# R1 two-turn look-ahead
tot = []
for a in (100, -100):
    for b in (100, -100):
        w1, w2 = a, a + b
        tot.append(w2 if w2 > w1 else w1)
check("L03 R1 expected total 50", F(sum(tot), 4), 50)

# ---- L02 numbers (Fraction enumeration independent of the lab)
def cond(space, ev, given):
    k = [o for o in space if given(o)]
    return F(sum(1 for o in k if ev(o)), len(k))


flips = list(itertools.product("HT", repeat=2))
check("L02 P(both|at least one)", cond(flips, lambda o: o == ("H", "H"), lambda o: "H" in o), F(1, 3))
check("L02 P(both|first H)", cond(flips, lambda o: o == ("H", "H"), lambda o: o[0] == "H"), F(1, 2))
check("L02 P(one|both)", cond(flips, lambda o: "H" in o, lambda o: o == ("H", "H")), 1)
urn = [(a, b) for a in ("r1", "r2", "r3", "b1", "b2") for b in ("r1", "r2", "r3", "b1", "b2") if a != b]
red = {"r1", "r2", "r3"}
check("L02 urn second red 3/5", F(sum(b in red for _, b in urn), 20), F(3, 5))
check("L02 urn first red 3/5", F(sum(a in red for a, _ in urn), 20), F(3, 5))
check("L02 urn both red 3/10", F(sum(a in red and b in red for a, b in urn), 20), F(3, 10))
check("L02 urn second red | first blue 3/4", cond(urn, lambda o: o[1] in red, lambda o: o[0].startswith("b")), F(3, 4))
# Monty Hall rule A and B, own derivation by listing (car, pick, host)
def monty(rule):
    stay = switch = tot = F(0)
    for car in range(3):
        for pick in range(3):
            others = [d for d in range(3) if d != pick]
            for host in others:
                if rule == "A":
                    goats = [d for d in others if d != car]
                    if host not in goats:
                        continue
                    p = F(1, len(goats))
                else:
                    if host == car:
                        continue
                    p = F(1, 2)
                w_ = F(1, 9) * p
                tot += w_
                sw = [d for d in others if d != host][0]
                stay += w_ * (pick == car)
                switch += w_ * (sw == car)
    return stay / tot, switch / tot


check("L02 Monty rule A stay", monty("A")[0], F(1, 3))
check("L02 Monty rule A switch", monty("A")[1], F(2, 3))
check("L02 Monty rule B stay", monty("B")[0], F(1, 2))
check("L02 Monty rule B switch", monty("B")[1], F(1, 2))
check("L02 E3 difference 1/6", monty("A")[1] - monty("B")[1], F(1, 6))
check("L02 bag P(red)", F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4), F(1, 2))
check("L02 bag posterior", F(1, 2) * F(3, 4) / (F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4)), F(3, 4))
check("L02 M2 bayes 15/29", F(1, 2) * F(3, 10) / (F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10)), F(15, 29))
check("L02 E1 57/64", 1 - F(1, 64) - F(6, 64), F(57, 64))
check("L02 M1 1/6", F(1, 36) / F(6, 36), F(1, 6))
check("L02 M3 2/5", F(4, 6) * F(3, 5), F(2, 5))

# ---- L02 drill items: rebuild each probability from the printed item text (independent of enumerate_probability)
from fractions import Fraction as Fr  # noqa: E402

printed = {
    1: ("the first head on flip 4 of 6", Fr(1, 16)),
    2: ("at least 3 heads in 3", Fr(1, 8)),
    3: ("at least 3 heads in 6", Fr(21, 32)),
    4: ("at least 2 heads in 6", Fr(57, 64)),
    5: ("at least 2 heads in 7", Fr(15, 16)),
    6: ("the first head on flip 2 of 3", Fr(1, 4)),
    7: ("the first head on flip 7 of 7", Fr(1, 128)),
    8: ("the first head on flip 3 of 7", Fr(1, 8)),
    9: ("the first head on flip 3 of 3", Fr(1, 8)),
    10: ("at least 1 head in 5", Fr(31, 32)),
    11: ("at least 5 heads in 5", Fr(1, 32)),
    12: ("the first head on flip 8 of 8", Fr(1, 256)),
}
for num, (text, val) in printed.items():
    if text.startswith("at least"):
        k = int(text.split()[2])
        n = int(text.split()[-1])
        p = Fr(sum(math.comb(n, i) for i in range(k, n + 1)), 2**n)
    else:
        j = int(text.split()[5])
        p = Fr(1, 2**j)
    check(f"L02 drill item {num} ({text})", p, val)

print("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED")
