"""Independent recomputation of the numbers printed on M4 hub and lessons L01-L04 (verifier, round 1).

Run: <checkout>/.venv/bin/python -I ledgers/M4/scripts/M4-a-r1/recompute.py
Uses only fractions and math. Prints each recomputed value next to the value the page states.
"""

import math
from fractions import Fraction as F

ok = []


def check(label, got, want):
    status = "OK" if got == want else "MISMATCH"
    ok.append(status)
    print(f"{status:9s} {label}: recomputed {got} | page {want}")


# L01 Example 3.6 table and quantiles
vals = [-2, -1, 0, 1, 2, 3]
probs = [F(1, 10), F(2, 10), F(3, 10), F(2, 10), F(1, 10), F(1, 10)]
cdf = []
acc = F(0)
for p in probs:
    acc += p
    cdf.append(acc)
check("L01 F values", [str(c) for c in cdf], ["1/10", "3/10", "3/5", "4/5", "9/10", "1"])


def Q(p):
    for v, c in zip(vals, cdf):
        if c >= p:
            return v


check("L01 Q(1/2)", Q(F(1, 2)), 0)
check("L01 Q(3/5)", Q(F(3, 5)), 0)
check("L01 Q(61/100)", Q(F(61, 100)), 1)
check("L01 Q(99/100)", Q(F(99, 100)), 3)
check("L01 Q(9/10)", Q(F(9, 10)), 2)
check("L01 Q(91/100)", Q(F(91, 100)), 3)
check("L01 Q(11/100)", Q(F(11, 100)), -1)
# Prop 3.4 index: ceil(pn) for n=150, p=0.99 and n=200
check("L01 ceil(0.99*150)", math.ceil(F(99, 100) * 150), 149)
check("L01 ceil(0.99*200)", math.ceil(F(99, 100) * 200), 198)
check("L01 ceil(40*0.901)", math.ceil(F(901, 1000) * 40), 37)
check("L01 ceil(40*0.9)", math.ceil(F(9, 10) * 40), 36)

# L01 quiz/problem: left-endpoint quantile at 1/2 for law (0:1/4, 1:1/2, 2:1/4)
check("L01 quiz Q(1/2) of 1/4,1/2,1/4 law", next(v for v, c in zip([0, 1, 2], [F(1, 4), F(3, 4), F(1)]) if c >= F(1, 2)), 1)

# L02 numbers
die_mean = sum(F(k, 6) for k in range(1, 7))
die_m2 = sum(F(k * k, 6) for k in range(1, 7))
check("L02 die E[X]", die_mean, F(7, 2))
check("L02 die E[X^2]", die_m2, F(91, 6))
check("L02 die Var", die_m2 - die_mean**2, F(35, 12))
check("L02 Var(2X)", 4 * (die_m2 - die_mean**2), F(35, 3))
e_l = F(250000, 20)
e_l2 = F(250000**2, 20)
check("L02 loss E[L]", e_l, 12500)
check("L02 loss E[L^2]", e_l2, 3125000000)
check("L02 loss Var", e_l2 - e_l**2, 2968750000)
check("L02 sqrt(Var) to 2dp", f"{math.sqrt(2968750000):.2f}", "54486.24")
check("L02 sqrt(Var(D)) to 4dp, D=L/100", f"{math.sqrt(296875):.4f}", "544.8624")
check("L02 P2 example: Var(D)", F(2968750000, 10000), 296875)
check("L02 M2 loss Var", F(50000**2, 10) - F(5000) ** 2, F(225000000))
check("L02 E[X^2] 91/6 in decimal to 2dp", f"{float(F(91, 6)):.2f}", "15.17")

# L03 skewed law: values 0,1,2,10 with 1/2,1/4,1/8,1/8
law = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
mu = sum(v * p for v, p in law)
check("L03 mu", mu, F(7, 4))


def cm(k):
    return sum(((v - mu) ** k * p for v, p in law), F(0))


m2, m3, m4 = cm(2), cm(3), cm(4)
check("L03 m2", m2, F(163, 16))
check("L03 m3", m3, F(2157, 32))
check("L03 m4", m4, F(149461, 256))
check("L03 squared skewness", m3 * m3 / m2**3, F(18610596, 4330747))
check("L03 kurtosis", m4 / m2**2, F(149461, 26569))
check("L03 skewness to 4dp", f"{math.sqrt(float(m3 * m3 / m2**3)):.4f}", "2.0730")
check("L03 kurtosis to 4dp", f"{float(m4 / m2**2):.4f}", "5.6254")
# Claim on the page: the value-10 term alone (35937/512) exceeds m3 (34512/512), 'so the three negative-side terms reduce it'
terms = [((v - mu) ** 3 * p) for v, p in law]
check("L03 m3 term values (x512)", [str(t * 512) for t in terms], ["-1372", "-54", "1", "35937"])
check("L03 sum of the non-10 terms (x512)", str(sum(terms[:3]) * 512), "-1425")
check("L03 signs of the three non-10 terms", [t > 0 for t in terms[:3]], [False, False, True])

# Bernoulli closed forms and worked values
for p, want_skew_sq, want_kurt in [(F(1, 10), F(64, 9), F(73, 9)), (F(1, 4), None, F(7, 3))]:
    q = 1 - p
    bern = [(0, q), (1, p)]
    bm = sum(v * pr for v, pr in bern)

    def bcm(k, bern=bern, bm=bm):
        return sum(((v - bm) ** k * pr for v, pr in bern), F(0))

    kurt = bcm(4) / bcm(2) ** 2
    check(f"L03 Bernoulli p={p} kurtosis", kurt, want_kurt)
    if want_skew_sq is not None:
        check(f"L03 Bernoulli p={p} squared skewness", bcm(3) ** 2 / bcm(2) ** 3, want_skew_sq)
check("L03 Bernoulli 1/4 skewness 2/sqrt3", (F(1, 2)) / math.sqrt(3 / 16), 2 / math.sqrt(3))

# L03 canon law -2,1,3 with 2/5,1/2,1/10
lw = [(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]
lm = sum(v * p for v, p in lw)
check("L03 canon mean", lm, 0)
check("L03 canon m3", sum(v**3 * p for v, p in lw), 0)
check("L03 canon m2", sum(v**2 * p for v, p in lw), 3)
check("L03 canon m4", sum(v**4 * p for v, p in lw), 15)
check("L03 canon kurtosis", F(15, 9), F(5, 3))

# L04 tables
dep = {(0, 0): F(1, 10), (0, 1): F(3, 10), (1, 0): F(2, 10), (1, 1): F(2, 10), (2, 0): F(1, 10), (2, 1): F(1, 10)}
check("L04 dep sums to 1", sum(dep.values()), 1)
px = {x: sum(p for (a, b), p in dep.items() if a == x) for x in (0, 1, 2)}
py = {y: sum(p for (a, b), p in dep.items() if b == y) for y in (0, 1)}
check("L04 P(Y=0)", py[0], F(2, 5))
check("L04 P(Y=1)", py[1], F(3, 5))
check("L04 E[X]", sum(x * p for x, p in px.items()), F(4, 5))
check("L04 E[X|Y=0]", sum(x * dep[(x, 0)] for x in (0, 1, 2)) / py[0], 1)
check("L04 E[X|Y=1]", sum(x * dep[(x, 1)] for x in (0, 1, 2)) / py[1], F(2, 3))
check("L04 total expectation", py[0] * 1 + py[1] * F(2, 3), F(4, 5))
check("L04 cell (0,0) product", px[0] * py[0], F(4, 25))
check("L04 ratio cell (0,0)", dep[(0, 0)] / (px[0] * py[0]), F(5, 8))
PX = {0: F(1, 5), 1: F(2, 5), 2: F(2, 5)}
PY = {0: F(3, 10), 1: F(7, 10)}
check("L04 product-table cell (0,0)", PX[0] * PY[0], F(3, 50))
# Example 1.9
u = {(x, x * x): F(1, 3) for x in (-1, 0, 1)}
ex = sum(x * p for (x, y), p in u.items())
ey = sum(y * p for (x, y), p in u.items())
exy = sum(x * y * p for (x, y), p in u.items())
check("L04 Ex1.9 Cov", exy - ex * ey, 0)
check("L04 Ex1.9 cell (0,0) vs product", (u[(0, 0)], F(1, 9)), (F(1, 3), F(1, 9)))
# Remark 1.3 style claim: the marginals-only table from canon
check("L04 canon marginals equal, cell differs", (F(1, 2), F(1, 4)), (F(1, 2), F(1, 2) * F(1, 2)))

print()
print(f"{ok.count('OK')} OK, {ok.count('MISMATCH')} MISMATCH")
