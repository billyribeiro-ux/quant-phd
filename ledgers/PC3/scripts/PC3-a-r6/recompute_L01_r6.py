"""Round-6 recomputation of every number on PC3 L01.html (independent of the lab twin), exact fractions where possible.

Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r6/recompute_L01_r6.py  (from the checkout root)
"""

import math
from fractions import Fraction as F

fails = 0
checks = 0


def check(label: str, got: object, want: object) -> None:
    global fails, checks
    checks += 1
    ok = got == want
    if not ok:
        fails += 1
    print(f"{'PASS' if ok else 'FAIL'} {label}: got {got} want {want}")


def close(label: str, got: float, want: float, places: int) -> None:
    global fails, checks
    checks += 1
    ok = round(got, places) == want or abs(got - want) < 0.5 * 10 ** (-places) + 1e-15
    if not ok:
        fails += 1
    print(f"{'PASS' if ok else 'FAIL'} {label}: got {got!r} round{places}={round(got, places)} want {want}")


# Example 1.4
lo = F(20) * 2 * 300
hi = F(60) * 10 * 390
check("product lower", lo, 12000)
check("product upper", hi, 234000)
check("ratio", hi / lo, F(39, 2))
W = math.log(19.5)
close("ln 19.5", W, 2.9704144656, 10)
close("factor width ln3", math.log(3), 1.0986122887, 10)
close("factor width ln5", math.log(5), 1.6094379124, 10)
close("factor width ln1.3", math.log(1.3), 0.2623642645, 10)
check("sum of factor widths equals ln19.5 (float, 1e-12)", abs(math.log(3) + math.log(5) + math.log(1.3) - W) < 1e-12, True)
close("geometric midpoint", math.sqrt(12000 * 234000), 52990.5651979671, 10)
close("geometric midpoint 2dp", math.sqrt(12000 * 234000), 52990.57, 2)
close("geometric midpoint 4dp", math.sqrt(12000 * 234000), 52990.5652, 4)

# Part 2 narrowings
base = W
r_sym = math.log(3) - math.log(2)
r_qu = math.log(5) - math.log(2)
r_min = math.log(1.3) - math.log(360 / 330)
close("reduction symbols", r_sym, 0.4054651081, 10)
close("reduction quote updates", r_qu, 0.9162907319, 10)
close("reduction minutes", r_min, 0.1753528875, 10)
close("total after quote updates", base - r_qu, 2.0541237337, 10)
close("total after minutes", base - r_min, 2.7950615781, 10)
close("total after symbols", base - r_sym, 2.5649493575, 10)
close("share quote updates (full precision) 1dp", 100 * r_qu / base, 30.8, 1)
close("share quote updates (full precision) raw", r_qu / base, 0.308472, 6)
close("share minutes (full precision) 1dp", 100 * r_min / base, 5.9, 1)
close("share minutes raw", r_min / base, 0.059033, 6)
check("four-place division 0.9163/2.9704 rounds to 0.3085", round(0.9163 / 2.9704, 4), 0.3085)
close("four-place share percent", 100 * 0.9163 / 2.9704, 30.85, 2)
check("percent 30.85 in the solution is consistent with rounding half up to 30.9 (round-half-up)", math.floor(30.85 * 10 + 0.5) / 10, 30.9)

# Example 1.7 (n=10, x=1/100) and (x=1/20)
x = F(1, 100)
n = 10
exact = (1 + x) ** n
rem = exact - 1 - n * x
bnd = F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
close("(1.01)^10 exact decimal 1.10462212541", float(exact), 1.10462212541, 11)
close("remainder 1 dp10", float(rem), 0.0046221254, 10)
close("bound 10dp", float(bnd), 0.0048728552, 10)
ratio = float(rem) / float(bnd)
print("ratio remainder/bound (full) =", repr(ratio))
close("ratio to four places (0.9485 claimed)", ratio, 0.9485, 4)
exceed = float(bnd) / float(rem) - 1
close("bound exceeds remainder by 0.054", exceed, 0.054, 3)
close("bound exceeds remainder, percent 5.4", 100 * exceed, 5.4, 1)
# Ratio from the printed (rounded) values, as the solution computes it
print("ratio from printed values:", 0.0046221254 / 0.0048728552)

x2 = F(1, 20)
rem2 = (1 + x2) ** 10 - 1 - 10 * x2
bnd2 = F(45) * (1 + x2) ** 8 * x2 * x2
close("(1.05)^10 to 4dp = 1.6289", float((1 + x2) ** 10), 1.6289, 4)
close("remainder at 1/20 to 4dp = 0.1289", float(rem2), 0.1289, 4)
close("bound at 1/20 to 4dp = 0.1662", float(bnd2), 0.1662, 4)
close("miss share of exact value 7.9 percent", 100 * float(rem2) / float((1 + x2) ** 10), 7.9, 1)
close("miss over exact 0.079", float(rem2) / float((1 + x2) ** 10), 0.079, 3)

# Lab Part 3 values at all six (n, x) pairs: remainder below bound
for nn in (2, 5, 10):
    for xx in (F(1, 100), F(1, 20)):
        r = (1 + xx) ** nn - 1 - nn * xx
        b = F(nn * (nn - 1), 2) * (1 + xx) ** (nn - 2) * xx * xx
        check(f"Part3 n={nn} x={float(xx)} remainder <= bound", 0 <= r <= b, True)

# E3: minutes range [300,330]
check("E3 upper", F(60) * 10 * 330, 198000)
close("E3 ln(16.5)", math.log(16.5), 2.8034, 4)
close("E3 difference ln19.5 - ln16.5", math.log(19.5) - math.log(16.5), 0.167054, 6)

# M1..M3, E4, R3 numbers
close("M2 ln16", math.log(16), 2.7726, 4)
check("M3 remainder", F(1331, 1000) - 1 - F(3, 10), F(31, 1000))
check("M3 bound", F(3 * 2, 2) * F(11, 10) * F(1, 100), F(33, 1000))
close("R1 half of total", W / 2, 1.4852, 4)
close("R1 ln5", math.log(5), 1.6094, 4)
close("R1 ln3", math.log(3), 1.0986, 4)
close("R1 ln1.3", math.log(1.3), 0.2624, 4)
close("R3 reduction A", math.log(3 / 2), 0.4055, 4)
close("R3 width B", math.log(2.5), 0.9163, 4)
close("R3 reduction B", math.log(2.5 / 1.01), 0.9063, 4)
check("R3 claim: width A > width B", math.log(3) > math.log(2.5), True)
check("R3 claim: reduction B > reduction A", math.log(2.5 / 1.01) > math.log(3 / 2), True)
close("M2 factor widths", math.log(4) + math.log(4), math.log(16), 12)
close("M1 ln4.2 sum", math.log(1.5) + math.log(1.4) + math.log(2), math.log(4.2), 12)
check("E1 ratio truncated to five places is 0.94854", math.floor(ratio * 1e5) / 1e5, 0.94854)

# Quiz numbers
close("quiz ln(8/2) 6dp", math.log(4), 1.386294, 6)
close("quiz remainder 6dp", float(rem), 0.004622, 6)
close("quiz geometric 4dp", math.sqrt(2808000000), 52990.5652, 4)

print(f"SUMMARY checks={checks} fails={fails}")
