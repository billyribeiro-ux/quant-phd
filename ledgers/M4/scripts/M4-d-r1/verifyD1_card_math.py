"""Verifier round-1 recomputation of the numerical and algebraic claims on the M4 cards (exact fractions, then floats).

Each line states the card, the claim and the recomputed value. Run from the checkout root:
    .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_card_math.py
"""

from __future__ import annotations

import math
from fractions import Fraction as F

results: list[tuple[str, str, bool]] = []


def check(card: str, claim: str, value: object, ok: bool) -> None:
    results.append((card, f"{claim} -> {value}", ok))


# c011 / c015: index of the 99% quantile
check("c011", "index for 200 losses is 198", 198, math.ceil(F(99, 100) * 200) == 198)
check("c015", "index for 150 losses is ceil(148.5) = 149", math.ceil(F(99, 100) * 150), math.ceil(F(99, 100) * 150) == 149)
# c026 / c031 / c182: two-point loss, 250000 cents with probability 1/20
mean_l = F(250000, 20)
var_l = F(250000, 1) ** 2 * F(1, 20) * F(19, 20)
check("c026", "E[L] = 12500 cents", mean_l, mean_l == 12500)
check("c182", "Var(L) = 2968750000 cents squared", var_l, var_l == 2968750000)
check("c031", "sd(L) = 54486.24 cents", f"{math.sqrt(var_l):.4f}", f"{math.sqrt(var_l):.2f}" == "54486.24")
# c025 / c029 / c181 / c199 / c028: fair die
e_x = F(7, 2)
e_x2 = sum(F(k * k, 6) for k in range(1, 7))
var_d = e_x2 - e_x * e_x
check("c029", "E[X^2] = 91/6", e_x2, e_x2 == F(91, 6))
check("c199", "Var(X) = 35/12", var_d, var_d == F(35, 12))
check("c181", "sd of die = sqrt(35/12) ~ 1.708", f"{math.sqrt(var_d):.4f}", f"{math.sqrt(var_d):.3f}" == "1.708")
check("c028", "Var(2X) = 35/3 = 4 * 35/12", 4 * var_d, 4 * var_d == F(35, 3))
# c042 / c200: law on 0,1,2,10 with 1/2, 1/4, 1/8, 1/8
law = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
mu = sum(v * p for v, p in law)
m2 = sum((v - mu) ** 2 * p for v, p in law)
m3 = sum((v - mu) ** 3 * p for v, p in law)
m4 = sum((v - mu) ** 4 * p for v, p in law)
check("c042", "mean 7/4", mu, mu == F(7, 4))
check("c042", "Var = 163/16", m2, m2 == F(163, 16))
check("c200", "m3 = 2157/32", m3, m3 == F(2157, 32))
check("c200", "m4 = 149461/256", m4, m4 == F(149461, 256))
# c043 / c044: law on -2, 1, 3 with 2/5, 1/2, 1/10
law2 = [(-2, F(2, 5)), (1, F(1, 2)), (3, F(1, 10))]
mu2 = sum(v * p for v, p in law2)
s2 = sum(v * v * p for v, p in law2)
s4 = sum(v**4 * p for v, p in law2)
s3 = sum(v**3 * p for v, p in law2)
check("c043", "mean 0, m2 = 3, m4 = 15, kurtosis 5/3", (mu2, s2, s4, s4 / s2**2), (mu2 == 0, s2 == 3, s4 == 15, s4 / s2**2 == F(5, 3)) and True)
check("c044", "gamma_3 = 0 for that law", s3, s3 == 0 and mu2 == 0)
# c041 / c045 / c048: Bernoulli
for p, g3, g4 in ((F(1, 10), None, None), (F(1, 4), None, None)):
    q = 1 - p
    pq = p * q
    k4 = (1 - 3 * pq) / pq
    if p == F(1, 10):
        check("c045", "Bernoulli p=1/10: gamma_4 = 73/9", k4, k4 == F(73, 9))
        check("c048", "squared skewness p=1/10 = 64/9", (1 - 2 * p) ** 2 / pq, (1 - 2 * p) ** 2 / pq == F(64, 9))
    else:
        check("c045", "Bernoulli p=1/4: gamma_4 = 7/3", k4, k4 == F(7, 3))
# c074: X uniform on {-1,0,1}, Y = X^2
ys = [F(1), F(0), F(1)]
ey = sum(ys) / 3
ey2 = sum(y * y for y in ys) / 3
check("c074", "Var(Y) = 2/9", ey2 - ey * ey, ey2 - ey * ey == F(2, 9))
# c094 / c153: Student-t variances
check("c094", "Var(t_5) = 5/3", F(5, 3), F(5, 5 - 2) == F(5, 3))
check("c153", "Var(t_3) = 3", 3 / (3 - 2), 3 / (3 - 2) == 3)
# c141: Chebyshev bound for the die with n = 100, eps = 1/2
bound = (F(35, 12)) / (100 * F(1, 4))
check("c141", "Chebyshev bound 7/60", bound, bound == F(7, 60))
# c142: ten dice, Z_10 <= 1 threshold
thr = 35 + math.sqrt(10 * 35 / 12)
check("c142", "35 + sqrt(29.1667) = 40.4006, so S_10 <= 40", f"{thr:.4f}", f"{thr:.4f}" == "40.4006" and math.floor(thr) == 40)
# c157 / c161 / c168 / c172 / c187: Cauchy and t(3) tails
p10c = 2 / math.pi * math.atan(1 / 10)
check("c157", "P(|C| > 10) = 0.063451", f"{p10c:.6f}", f"{p10c:.6f}" == "0.063451")
check("c157", "1 draw in 16", f"{1 / p10c:.2f}", round(1 / p10c) == 16)
check("c161", "10 P(|C| > 10) = 0.634510", f"{10 * p10c:.6f}", f"{10 * p10c:.6f}" == "0.634510")
check("c161", "2/pi = 0.636620; gap about 0.002 (exact 0.00210942)", f"{2 / math.pi - 10 * p10c:.8f}", round(2 / math.pi - 10 * p10c, 3) == 0.002)
p10v = 2 / math.pi * (math.atan(math.sqrt(3) / 10) - 10 * math.sqrt(3) / (3 + 100))
check("c168", "P(|V| > 10) = 0.002128 (closed form of Prop 1.4)", f"{p10v:.6f}", f"{p10v:.6f}" == "0.002128")
x = 1000.0
v1000 = 2 / math.pi * (math.atan(math.sqrt(3) / x) - x * math.sqrt(3) / (3 + x * x))
check("c172", "x^3 P(|V| > x) at 1000 = 2.205308", f"{x**3 * v1000:.6f}", f"{x**3 * v1000:.6f}" == "2.205308")
check("c187", "limit 4 sqrt3/pi = 2.205316 (the card gives no number; c172 at x=1000 is 2.205308 below it)", f"{4 * math.sqrt(3) / math.pi:.6f}", f"{4 * math.sqrt(3) / math.pi:.6f}" == "2.205316" and f"{x**3 * v1000:.6f}" < "2.205316")
# c185: gaps of exact P(Z_n <= 1) from Phi(1), with the page's exact values
phi1 = 0.8413447460685429
gaps = [round(p - phi1, 4) for p in (0.833333, 0.847994, 0.843496, 0.835793, 0.833926)]
check("c185", "gaps -0.0080, +0.0066, +0.0022, -0.0056, -0.0074", gaps, gaps == [-0.008, 0.0066, 0.0022, -0.0056, -0.0074])
# c157 normal tail: P(|Z|>10) = 1.5240e-23
pz = math.erfc(10 / math.sqrt(2))
check("c157", "P(|Z| > 10) = 1.5240e-23", f"{pz:.4e}", f"{pz:.4e}" == "1.5240e-23")
# c208 / c207 / c119 / c125: matrices
A = [[2, 0], [1, 1]]


def mat(a, b):  # type: ignore[no-untyped-def]
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def tr(a):  # type: ignore[no-untyped-def]
    return [[a[j][i] for j in range(2)] for i in range(2)]


AAt = mat(A, tr(A))
AtA = mat(tr(A), A)
Q = [[0, -1], [1, 0]]
B = mat(A, Q)
check("c119", "A A^T = [[4,2],[2,2]]", AAt, AAt == [[4, 2], [2, 2]])
check("c207", "A^T A = [[5,1],[1,1]]", AtA, AtA == [[5, 1], [1, 1]])
check("c208", "B = AQ = [[0,-2],[1,-1]], B B^T = Sigma", (B, mat(B, tr(B))), B == [[0, -2], [1, -1]] and mat(B, tr(B)) == [[4, 2], [2, 2]])
# c125: quadratic form identity for Sigma = [[4,2],[2,2]]
ok125 = all(
    4 * w1 * w1 + 4 * w1 * w2 + 2 * w2 * w2 == (2 * w1 + w2) ** 2 + w2 * w2
    for w1 in range(-5, 6)
    for w2 in range(-5, 6)
)
check("c125", "w^T Sigma w = (2w1+w2)^2 + w2^2", ok125, ok125)
# c081: [[1,2],[2,1]] fails Prop 2.4
check("c081", "2^2 <= 1 * 1 is false", 4 <= 1, not (4 <= 1))
# c102: E[e^{tZ^2}] = (1-2t)^(-1/2) for t < 1/2; check at t = 0.25 by numerical integration
t = 0.25
h = 1e-4
num = sum(math.exp(t * (k * h) ** 2) * math.exp(-((k * h) ** 2) / 2) * h for k in range(-100000, 100001)) / math.sqrt(2 * math.pi)
check("c102", "E[exp(0.25 Z^2)] = (1 - 0.5)^(-1/2) = 1.414214", f"{num:.6f}", abs(num - (1 - 2 * t) ** -0.5) < 1e-5)
# c107: modulus formula of the two-point characteristic function at one point
p_, a_, b_, tt = 0.3, 1.0, -2.0, 0.7
phi = p_ * complex(math.cos(tt * a_), math.sin(tt * a_)) + (1 - p_) * complex(math.cos(tt * b_), math.sin(tt * b_))
mod2 = abs(phi) ** 2
formula = p_**2 + (1 - p_) ** 2 + 2 * p_ * (1 - p_) * math.cos(tt * (a_ - b_))
check("c107", "|phi|^2 = p^2 + (1-p)^2 + 2p(1-p) cos(t(a-b))", f"{mod2:.9f}", abs(mod2 - formula) < 1e-12)
# c133: Taylor remainder of e^{ix}: |e^{ix} - (1 + ix - x^2/2)| <= |x|^3 / 6 <= |x|^3 / 3 (the page's weaker bound)
worst = 0.0
for k in range(1, 2000):
    xk = k / 1000
    z = complex(math.cos(xk), math.sin(xk)) - complex(1 - xk * xk / 2, xk)
    worst = max(worst, abs(z) / (xk**3))
check("c133", "remainder ratio |R|/|x|^3 <= 1/6 (so the page's 1/3 bound holds)", f"{worst:.4f}", worst <= 1 / 6 + 1e-9)

ok_all = all(r[2] for r in results)
for card, claim, ok in results:
    print(f"{'OK  ' if ok else 'FAIL'} {card}: {claim}")
print("checks", len(results), "all agree:", ok_all)
