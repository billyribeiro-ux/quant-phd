"""Round-12 independent recomputation of the numbers in PC3 slice a (index, L01, L02, L03). Run: python3 -I <this>."""

import itertools
import math
from fractions import Fraction as F

print("== L01 Example 1.4 and Proposition 1.3")
lo = 20 * 2 * 300
hi = 60 * 10 * 390
print("bounds", lo, hi, "ratio", F(hi, lo), float(F(hi, lo)))
W = math.log(hi / lo)
w = [math.log(3), math.log(5), math.log(1.3)]
print("ln19.5", f"{W:.10f}", "factor widths", [f"{x:.10f}" for x in w], "sum", f"{sum(w):.10f}")
print("midpoint", f"{math.sqrt(lo*hi):.10f}", "to 2dp", f"{math.sqrt(lo*hi):.2f}", "to 4dp", f"{math.sqrt(lo*hi):.4f}")
print("half of total", W / 2, "ln5 > half?", math.log(5) > W / 2, "ln3", math.log(3), "ln1.3", math.log(1.3))

print("== L01 Part 2 narrowings (exact ln of ratios)")
base = W
for name, nlo, nhi in [("symbols", 20, 40), ("updates", 4, 8), ("minutes", 330, 360)]:
    pass
t1 = math.log((40 * 2 * 300 * 0 + 40) / 20 * 0 + 0) if False else None
tot_sym = math.log(60 * 10 * 390 / (20 * 2 * 300)) - math.log(60 / 20) + math.log(40 / 20)
tot_upd = W - math.log(10 / 2) + math.log(8 / 4)
tot_min = W - math.log(390 / 300) + math.log(360 / 330)
for nm, t in [("symbols", tot_sym), ("updates", tot_upd), ("minutes", tot_min)]:
    print(nm, f"total {t:.10f}", f"reduction {base - t:.10f}", f"share {100*(base-t)/base:.6f}%")
print("E2 four-place quotient 0.9163/2.9704 =", 0.9163 / 2.9704, "percent", 100 * 0.9163 / 2.9704)
print("E2 full quotient 0.9162907319/2.9704144656 =", 0.9162907319 / 2.9704144656)
print("E2 minutes 0.1753528875/2.9704144656 =", 0.1753528875 / 2.9704144656)
print("E2 exact share updates", (math.log(5) - math.log(2)) / W)
print("E3 new width ln16.5", math.log(16.5), "ratio 198000/12000", F(198000, 12000), "change", W - math.log(16.5))
print("Example 1.4 new upper", 60 * 10 * 330)
print("R3 A reduction ln(3/2)", math.log(1.5), "B width ln2.5", math.log(2.5), "B reduction ln(2.5/1.01)", math.log(2.5 / 1.01))

print("== L01 Example 1.7 and 1.5")
x = F(1, 100)
n = 10
exact = (1 + x) ** n
rem = exact - 1 - n * x
bound = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
print("exact", float(exact), f"{float(exact):.10f}", "rem", f"{float(rem):.10f}", "bound", f"{float(bound):.10f}")
print("ratio rem/bound", float(rem / bound), "bound/rem-1", float(bound / rem - 1), "pct", float(100 * (bound / rem - 1)))
x = F(1, 20)
exact = (1 + x) ** n
print("x=1/20 exact", float(exact), "rem", float(exact - 1 - n * x), "bound", float(F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x), "miss pct", float(100 * (exact - 1 - n * x) / exact))
print("(1.01)^10 six places rem", round(float(rem), 6))
print("sqrt(2808000000) 4dp", f"{math.sqrt(2808000000):.4f}")

print("== L01 M1-M3, E1, P1")
print("M1 bounds", 2*5*F(1, 2), 3*7, "ln 4.2", math.log(4.2), math.log(1.5)+math.log(1.4)+math.log(2))
print("M2 ln16", math.log(16), "ln4+ln4", math.log(4) + math.log(4))
print("M3 rem", F(1331, 1000) - 1 - F(3, 10), "bound", F(3, 1) * F(11, 10) * F(1, 100))
print("E1 ratio", F(46221254, 10**10) / F(48728552, 10**10), float(F(46221254, 10**10) / F(48728552, 10**10)))

print("== L02")
# Example 2.6
outs = list(itertools.product("HT", repeat=2))
def cond(ev, gv):
    g = [o for o in outs if gv(o)]
    return F(sum(1 for o in g if ev(o)), len(g))
print("2.6", cond(lambda o: o == ("H", "H"), lambda o: "H" in o), cond(lambda o: o == ("H", "H"), lambda o: o[0] == "H"))
print("2.6 reverse", cond(lambda o: "H" in o, lambda o: o == ("H", "H")))
balls = ["r1", "r2", "r3", "b1", "b2"]
pairs = [(a, b) for a in balls for b in balls if a != b]
red = {"r1", "r2", "r3"}
print("2.7 second red", F(sum(b in red for _, b in pairs), len(pairs)), "first", F(sum(a in red for a, _ in pairs), len(pairs)), "both", F(sum(a in red and b in red for a, b in pairs), len(pairs)))
print("2.7 second red | first blue", F(sum(b in red for a, b in pairs if a.startswith("b")), sum(1 for a, b in pairs if a.startswith("b"))))
print("E1 L02 57/64", F(64 - 1 - 6, 64))
print("M1 L02", F(1, 36) / F(6, 36))
pB = F(1, 2) * F(3, 10) + F(1, 5) * F(7, 10)
print("M2 L02 P(B)", pB, "P(A|B)", F(1, 2) * F(3, 10) / pB)
print("M3 L02 urn", F(4, 6) * F(3, 5), F(12, 30))
print("R3 L02 blue first", F(3, 3))
print("Example 2.9", F(1, 2) * F(3, 4) + F(1, 2) * F(1, 4), (F(1, 2) * F(3, 4)) / (F(1, 2)))
print("Monty B conditional", (F(1, 3)) / (F(2, 3)))

print("== L03")
from functools import lru_cache
HOR = 6
def expect(outcomes, rule):
    def val(h):
        if len(h) == HOR or rule(h):
            return F(sum(h))
        return sum((p * val(h + (x,)) for x, p in outcomes), F(0))
    return val(())
rules = [
    ("play all", lambda h: False),
    ("first win", lambda h: bool(h) and h[-1] > 0),
    ("first loss", lambda h: bool(h) and h[-1] < 0),
    ("total>=100", lambda h: sum(h) >= 100),
    ("total +-200", lambda h: sum(h) >= 200 or sum(h) <= -200),
]
fair = ((100, F(1, 2)), (-100, F(1, 2)))
bias = ((150, F(1, 2)), (-100, F(1, 2)))
for nm, r in rules:
    print("fair", nm, expect(fair, r), "biased", expect(bias, r))
# Brute force over all 2^6 sequences for the biased game too
for nm, r in rules:
    tot = F(0)
    for seq in itertools.product(bias, repeat=HOR):
        wgt = F(1)
        h = ()
        for x, p in seq:
            wgt *= p
        h = ()
        for x, _ in seq:
            h = h + (x,)
            if r(h):
                break
        tot += wgt * sum(h)
    print("brute biased", nm, tot)
print("reroll", (F(sum(100 * g for g in range(1, 7)), 6) - 100), F(sum(max(100 * f, 250) for f in range(1, 7)), 6))
for c in (100, 1):
    print("fee", c, F(sum(max(100 * f, 350 - c) for f in range(1, 7)), 6) - 350)
print("R1 L03 mean", F(200 + 100 + 0 - 100, 4))
print("E2 L03", F(625, 8) - 150, float(F(625, 8) - 150))
print("E3 L03", F(1150, 3) - 350, float(F(1150, 3) - 350))
print("Example 3.3 E[X+Y]", F(sum(x + y for x in range(1, 7) for y in range(1, 7)), 36))
print("M2 L03 p", F(100, 300))
print("R2 check 1150/3", F(2300, 6))
print("ALL DONE")

# Fair game: brute force over all 2^6 sequences (the page's second method) for every rule.
for nm, r in rules:
    tot = F(0)
    for seq in itertools.product(fair, repeat=HOR):
        wgt = F(1)
        for _, p in seq:
            wgt *= p
        h = ()
        for x, _ in seq:
            h = h + (x,)
            if r(h):
                break
        tot += wgt * sum(h)
    print("brute fair", nm, tot)
