"""Round-5 independent recomputation of the numbers in L01 prose, worked solutions, key results and quiz.

Run: .venv/bin/python -I ledgers/PC3/scripts/PC3-a-r5/recompute_L01_r5.py
Each CHECK compares the recomputed value, rounded to the page's places, with the string the page prints.
"""

from fractions import Fraction as F
import math

FAILS: list[str] = []
N = 0


def rounds_to(label: str, value: float, places: int, page: str) -> None:
    global N
    N += 1
    got = f"{value:.{places}f}"
    ok = got == page
    print(("OK   " if ok else "FAIL ") + f"{label}: computed {got}, page {page}")
    if not ok:
        FAILS.append(label)


def near(label: str, value: float, page: float, tol: float) -> None:
    global N
    N += 1
    ok = abs(value - page) <= tol
    print(("OK   " if ok else "FAIL ") + f"{label}: computed {value!r}, page {page!r}, tol {tol}")
    if not ok:
        FAILS.append(label)


def truth(label: str, value: bool, page: bool) -> None:
    global N
    N += 1
    ok = value == page
    print(("OK   " if ok else "FAIL ") + f"{label}: computed {value}, page {page}")
    if not ok:
        FAILS.append(label)


# ---- Example 1.4 (exact) ----
lo = F(20) * 2 * 300
hi = F(60) * 10 * 390
assert (lo, hi) == (12000, 234000)
ratio = hi / lo
assert ratio == F(39, 2)
rounds_to("ratio of ends 19.5", float(ratio), 1, "19.5")
W = math.log(float(ratio))
rounds_to("ln 19.5 ten places", W, 10, "2.9704144656")
rounds_to("ln 3 (symbols width)", math.log(3), 10, "1.0986122887")
rounds_to("ln 5 (quote-updates width)", math.log(5), 10, "1.6094379124")
rounds_to("ln 1.3 (minutes width)", math.log(1.3), 10, "0.2623642645")
truth("widths sum to ln19.5 (exact factorisation 3*5*1.3=19.5)", 3 * 5 * F(13, 10) == ratio, True)
gm = math.sqrt(float(lo * hi))
rounds_to("geometric midpoint ten places", gm, 10, "52990.5651979671")
rounds_to("geometric midpoint two places (Example 1.4)", gm, 2, "52990.57")
rounds_to("geometric midpoint four places (quiz Q9)", gm, 4, "52990.5652")
rounds_to("sqrt(2808000000) four places", math.sqrt(2808000000), 4, "52990.5652")
rounds_to("ln 16.5 four places (E3)", math.log(16.5), 4, "2.8034")
near("E3 change ln19.5 - ln16.5", W - math.log(16.5), 0.167054, 5e-7)
truth("E3 new upper bound 60*10*330 = 198000", 60 * 10 * 330 == 198000, True)
truth("E3 new ratio 198000/12000 = 16.5", F(198000, 12000) == F(33, 2), True)

# ---- Section 2 narrowings (each total = ln of ratio of new product interval) ----
t_sym = math.log(float(F(40) / 20 * F(10, 2) * F(390, 300)))
t_qu = math.log(float(F(60) / 20 * F(8, 4) * F(390, 300)))
t_min = math.log(float(F(60) / 20 * F(10, 2) * F(360, 330)))
red_sym, red_qu, red_min = W - t_sym, W - t_qu, W - t_min
rounds_to("total after symbols narrowed", t_sym, 10, "2.5649493575")
rounds_to("total after quote updates narrowed", t_qu, 10, "2.0541237337")
rounds_to("total after minutes narrowed", t_min, 10, "2.7950615781")
rounds_to("reduction symbols", red_sym, 10, "0.4054651081")
rounds_to("reduction quote updates", red_qu, 10, "0.9162907319")
rounds_to("reduction minutes", red_min, 10, "0.1753528875")
rounds_to("prose total symbols 2.5649", t_sym, 4, "2.5649")
rounds_to("prose total quote updates 2.0541", t_qu, 4, "2.0541")
rounds_to("prose total minutes 2.7951", t_min, 4, "2.7951")
rounds_to("prose reduction symbols 0.4055", red_sym, 4, "0.4055")
rounds_to("prose reduction quote updates 0.9163", red_qu, 4, "0.9163")
rounds_to("prose reduction minutes 0.1754", red_min, 4, "0.1754")
rounds_to("share quote updates percent one place", 100 * red_qu / W, 1, "30.8")
rounds_to("share minutes percent one place", 100 * red_min / W, 1, "5.9")
rounds_to("E2 share quote updates from printed 0.9163/2.9704, four places", 0.9163 / 2.9704, 4, "0.3085")
rounds_to("E2 share minutes from printed 0.1754/2.9704, four places", 0.1754 / 2.9704, 4, "0.0590")
truth("largest reduction is quote updates", red_qu == max(red_sym, red_qu, red_min), True)
truth("quote updates has largest width ln5", math.log(5) == max(math.log(3), math.log(5), math.log(1.3)), True)

# ---- Research R1 (criterion threshold) ----
rounds_to("R1 half the total width", W / 2, 4, "1.4852")
rounds_to("R1 ln 5 width", math.log(5), 4, "1.6094")
truth("R1 ln5 exceeds half the total", math.log(5) > W / 2, True)
truth("R1 ln3 does not exceed half", math.log(3) > W / 2, False)
truth("R1 ln1.3 does not exceed half", math.log(1.3) > W / 2, False)
rounds_to("R1 ln 1.3 width four places", math.log(1.3), 4, "0.2624")
rounds_to("R1 ln 3 width four places", math.log(3), 4, "1.0986")

# ---- Research R3 (counterexample) ----
rounds_to("R3 A width ln3", math.log(3), 4, "1.0986")
rounds_to("R3 A reduction ln(3/2)", math.log(3 / 2), 4, "0.4055")
rounds_to("R3 B width ln2.5", math.log(2.5), 4, "0.9163")
rounds_to("R3 B reduction ln(2.5/1.01)", math.log(2.5 / 1.01), 4, "0.9063")
truth("R3 A width > B width", math.log(3) > math.log(2.5), True)
truth("R3 B reduction > A reduction", math.log(2.5 / 1.01) > math.log(3 / 2), True)

# ---- Theorem 1.5, Remark 1.6, Example 1.7 (exact fractions) ----
def rem(n: int, x: F) -> F:
    return (1 + x) ** n - 1 - n * x


def bnd(n: int, x: F) -> F:
    return F(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x


for n in (2, 5, 10):
    for x in (F(1, 100), F(1, 20)):
        r, b = rem(n, x), bnd(n, x)
        truth(f"Theorem 1.5 holds n={n} x={x}", 0 <= r <= b, True)
        tail = sum(math.comb(n, j) * x**j for j in range(2, n + 1))
        truth(f"binomial-tail identity exact n={n} x={x}", tail == r, True)
        print(f"  PART3 n={n} x={float(x):.2f} first={float(1 + n * x):.10f} exact={float((1 + x) ** n):.10f} "
              f"rem={float(r):.10f} bound={float(b):.10f}")
x = F(1, 100)
rounds_to("ex1.7 exact (1.01)^10", float((1 + x) ** 10), 10, "1.1046221254")
rounds_to("ex1.7 remainder", float(rem(10, x)), 10, "0.0046221254")
rounds_to("ex1.7 bound", float(bnd(10, x)), 10, "0.0048728552")
rounds_to("ex1.7 ratio remainder/bound four places", float(rem(10, x) / bnd(10, x)), 4, "0.9485")
rounds_to("E1 ratio five places", float(rem(10, x) / bnd(10, x)), 5, "0.94855")
rounds_to("ex1.7 bound/remainder minus 1, three places", float(bnd(10, x) / rem(10, x) - 1), 3, "0.054")
rounds_to("ex1.7 percent of remainder one place", 100 * float(bnd(10, x) / rem(10, x) - 1), 1, "5.4")
x = F(1, 20)
rounds_to("ex1.7 (1.05)^10 four places", float((1 + x) ** 10), 4, "1.6289")
rounds_to("ex1.7 remainder at 1/20 four places", float(rem(10, x)), 4, "0.1289")
rounds_to("ex1.7 bound at 1/20 four places", float(bnd(10, x)), 4, "0.1662")
rounds_to("ex1.7 miss share three places", float(rem(10, x)) / float((1 + x) ** 10), 3, "0.079")
rounds_to("ex1.7 miss share percent one place", 100 * float(rem(10, x)) / float((1 + x) ** 10), 1, "7.9")
rounds_to("ex1.7 first-order estimate 1.5", float(1 + 10 * x), 1, "1.5")

# ---- Problem set ----
truth("M1 lower 2*5*1/2 = 5", F(2) * 5 * F(1, 2) == 5, True)
truth("M1 upper 3*7*1 = 21", F(3) * 7 == 21, True)
rounds_to("M1 ln(21/5) = ln 4.2 four places", math.log(21 / 5), 4, "1.4351")
near("M1 widths sum to ln 4.2", math.log(1.5) + math.log(1.4) + math.log(2), math.log(4.2), 1e-12)
rounds_to("M2 ln 16 four places", math.log(16), 4, "2.7726")
truth("M2 widths ln4 + ln4 = ln16", abs(2 * math.log(4) - math.log(16)) < 1e-12, True)
truth("M3 remainder 31/1000", F(11, 10) ** 3 - 1 - F(3, 10) == F(31, 1000), True)
truth("M3 bound 33/1000", F(3 * 2, 2) * F(11, 10) * F(1, 100) == F(33, 1000), True)
near("E4 ln2+ln2 = ln4", 2 * math.log(2), math.log(4), 1e-12)
truth("Q2 ln4 to six places 1.386294", f"{math.log(4):.6f}" == "1.386294", True)
truth("Q6 remainder to six places 0.004622", f"{float(rem(10, F(1, 100))):.6f}" == "0.004622", True)
truth("Q7 n=2 remainder equals bound equals x^2 (x=1/3)", rem(2, F(1, 3)) == bnd(2, F(1, 3)) == F(1, 9), True)
truth("Q1 lower bound 2*5", 2 * 5 == 10, True)
truth("Q4 upper bound 60*10*390", 60 * 10 * 390 == 234000, True)
near("Q9 geometric mean tolerance check", math.sqrt(2808000000), 52990.5652, 1e-4)

print(f"SUMMARY checks={N} fails={len(FAILS)} {FAILS}")
