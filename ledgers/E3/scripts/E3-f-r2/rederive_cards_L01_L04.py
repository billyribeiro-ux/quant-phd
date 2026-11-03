"""Independent re-derivation of the numbers quoted by the E3 cards for L01 to L04 (verifier E3 slice f, round 2).

Exact values use fractions.Fraction; the CRRA and Pratt quantities are floats checked to stated tolerances.
Standard library only. Run with: python3 -I ledgers/E3/scripts/E3-f-r2/rederive_cards_L01_L04.py
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable, Sequence
from fractions import Fraction

ok = True


def check(label: str, got: object, want: object) -> None:
    global ok
    good = got == want
    ok = ok and good
    print(f"{'OK  ' if good else 'FAIL'} {label}: got {got} want {want}")


def check_close(label: str, got: float, want: float, tol: float) -> None:
    global ok
    good = abs(got - want) <= tol
    ok = ok and good
    print(f"{'OK  ' if good else 'FAIL'} {label}: got {got:.9f} want {want:.9f} (tol {tol})")


Lottery = Sequence[tuple[int, Fraction]]


def expected_value(lottery: Lottery) -> Fraction:
    return sum((p * x for x, p in lottery), Fraction(0))


def expected_utility(lottery: Lottery, u: Callable[[int], Fraction]) -> Fraction:
    return sum((p * u(x) for x, p in lottery), Fraction(0))


def linear(x: int) -> Fraction:
    return Fraction(x)


def quadratic(x: int) -> Fraction:
    return Fraction(x * x, 10000)


# ---- L01 ----------------------------------------------------------------------------------------
A: Lottery = [(0, Fraction(1, 4)), (10000, Fraction(1, 2)), (40000, Fraction(1, 4))]
B: Lottery = [(5000, Fraction(1, 2)), (20000, Fraction(1, 2))]
C: Lottery = [(0, Fraction(1, 3)), (15000, Fraction(1, 3)), (30000, Fraction(1, 3))]
check(
    "L01 c016 expected values A,B,C (cents)",
    tuple(expected_value(x) for x in (A, B, C)),
    (Fraction(15000), Fraction(12500), Fraction(15000)),
)
check(
    "L01 c016 quadratic EU A,B,C",
    tuple(expected_utility(x, quadratic) for x in (A, B, C)),
    (Fraction(45000), Fraction(21250), Fraction(37500)),
)
check(
    "L01 c014 u(EX)=150^2=22500 CU^2 vs EU(A)=45000 CU^2",
    (Fraction(150) ** 2, Fraction(45000)),
    (Fraction(22500), Fraction(45000)),
)
check(
    "L01 Ex3.4 EU_quad(C) = 37500 CU^2 (x in CU)",
    sum((Fraction(1, 3) * q for q in (Fraction(0), Fraction(22500), Fraction(90000))), Fraction(0)),
    Fraction(37500),
)
n_true = 0
for alpha in (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2)):
    keys = sorted({x for x, _ in A} | {x for x, _ in C})
    mix: Lottery = [
        (
            x,
            alpha * sum((p for y, p in A if y == x), Fraction(0))
            + (1 - alpha) * sum((p for y, p in C if y == x), Fraction(0)),
        )
        for x in keys
    ]
    for u in (linear, quadratic):
        n_true += expected_utility(mix, u) == alpha * expected_utility(A, u) + (1 - alpha) * expected_utility(C, u)
check("L01 c017 True linearity comparisons (3 weights x 2 utilities)", n_true, 6)

# ---- L02 ----------------------------------------------------------------------------------------
gamble: Lottery = [(-60, Fraction(1, 4)), (0, Fraction(1, 2)), (60, Fraction(1, 4))]
mean = expected_value(gamble)
variance = sum((p * x * x for x, p in gamble), Fraction(0)) - mean * mean
check("L02 gamble mean (CU) and variance (CU^2)", (mean, variance), (Fraction(0), Fraction(1800)))
eu_sqrt = 0.25 * math.sqrt(40) + 0.5 * 10 + 0.25 * math.sqrt(160)
ce_sqrt = eu_sqrt**2
premium = 100 - ce_sqrt
check_close("L02 Ex1.5 E sqrt(W) ~ 9.743416", eu_sqrt, 9.743416, 5e-7)
check_close("L02 Ex1.5 CE ~ 94.934165 CU", ce_sqrt, 94.934165, 5e-7)
check_close("L02 Ex1.5 premium ~ 5.065835 CU", premium, 5.065835, 5e-7)
check("L02 c032 CE in cents, half up of 9493.4165", math.floor(ce_sqrt * 100 + 0.5), 9493)
check("L02 c032 premium in cents, half up of 506.5835", math.floor(premium * 100 + 0.5), 507)
r_a = -(-0.25 * 100**-1.5) / (0.5 * 100**-0.5)
check_close("L02 c026/c032 r_A(100) = 0.005 per CU", r_a, 0.005, 1e-15)
check_close("L02 c026 r_R(100) = 0.5", 100 * r_a, 0.5, 1e-15)
pratt = 0.5 * r_a * float(variance)
check_close("L02 c032 Pratt approximation = 4.5 CU", pratt, 4.5, 1e-12)
check_close("L02 c032 error = 0.565835 CU", premium - pratt, 0.565835, 5e-7)
check_close("L02 c034 error / exact premium = 11.17 percent", 100 * (premium - pratt) / premium, 11.17, 0.005)
check("L02 c029 half of Var(X) is 900 CU^2 (not 900 CU)", Fraction(1, 2) * variance, Fraction(900))
check_close("L02 c029 Pratt approximation 4.5 CU", pratt, 4.5, 1e-12)
check_close("L02 c029 900 / exact premium ~ 177.66 (lesson's 'about 178')", 900 / premium, 177.66, 0.01)


def ce_sqrt_at(eps: float) -> float:
    expected = sum(float(p) * math.sqrt(100 + eps * x) for x, p in gamble)
    return expected * expected


ratios = [(100 - ce_sqrt_at(eps)) / (eps * eps) for eps in (1.0, 0.5, 0.25, 0.1, 0.01)]
check_close("L02 c033 premium/eps^2 at eps=1 = 5.065835", ratios[0], 5.065835, 5e-7)
check_close("L02 c033 premium/eps^2 at eps=0.01 = 4.500046", ratios[-1], 4.500046, 5e-7)
gaps = [abs(r - 4.5) for r in ratios]
check("L02 c033 gaps strictly shrink as eps falls", all(b < a for a, b in itertools.pairwise(gaps)), True)
linear_premia = [100 - sum(float(p) * (100 + eps * x) for x, p in gamble) for eps in (1.0, 0.5, 0.1)]
check("L02 c035 linear premium zero at three scales (|.| < 1e-9)", all(abs(v) < 1e-9 for v in linear_premia), True)
check_close("L02 Ex2.3 r_A(100) = 1/(2w) at w=100", 1 / (2 * 100), 0.005, 1e-15)

# ---- L03 ----------------------------------------------------------------------------------------
prizes = (5000, 10000, 20000)
probs = (Fraction(1, 4), Fraction(1, 2), Fraction(1, 4))
check(
    "L03 c054 expected prize = 11250 cents",
    sum((p * x for p, x in zip(probs, prizes, strict=True)), Fraction(0)),
    Fraction(11250),
)
m_inv = sum((p / x for p, x in zip(probs, prizes, strict=True)), Fraction(0))
check("L03 c055 sum p/x = 9/80000", m_inv, Fraction(9, 80000))
check("L03 c055 CE at gamma=2 = 80000/9 cents", 1 / m_inv, Fraction(80000, 9))
check_close("L03 c055 80000/9 ~ 8888.89", float(1 / m_inv), 8888.89, 0.005)


def crra_ce(gamma: float) -> float:
    if gamma == 1.0:
        return math.exp(sum(float(p) * math.log(x) for p, x in zip(probs, prizes, strict=True)))
    s = 1.0 - gamma
    return sum(float(p) * x**s for p, x in zip(probs, prizes, strict=True)) ** (1.0 / s)


for g, want in ((0.0, 11250.0), (1.0, 10000.0), (2.0, 80000 / 9), (4.0, 7337.6161)):
    check_close(f"L03 c054 CE at gamma={g:g}", crra_ce(g), want, 5e-5)
grid = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)
check(
    "L03 c054 CE strictly falls over the gamma grid",
    all(crra_ce(a) > crra_ce(b) for a, b in itertools.pairwise(grid)),
    True,
)
m_ex = Fraction(1, 2) * Fraction(1, 1000) + Fraction(1, 2) * Fraction(1, 4000)
check("L03 c047 CE_2 of the 1000/4000 lottery = 1600 cents", 1 / m_ex, Fraction(1600))
check_close(
    "L03 c047 CE_1 of the 1000/4000 lottery = 2000 cents",
    math.exp(0.5 * math.log(1000) + 0.5 * math.log(4000)),
    2000.0,
    1e-9,
)
check(
    "L03 Problem M2 CE_2 = 3000 cents",
    1 / (Fraction(1, 4) * Fraction(1, 1000) + Fraction(3, 4) * Fraction(1, 9000)),
    Fraction(3000),
)
check(
    "L03 Problem M3 CE_2(3X) = 9000 cents",
    1 / (Fraction(1, 4) * Fraction(1, 3000) + Fraction(3, 4) * Fraction(1, 27000)),
    Fraction(9000),
)


def half_up(v: float) -> int:
    return math.floor(v + 0.5)


worst = 0.0
for k in range(1, 21):
    for i in range(4001):
        v = i * 0.2371
        worst = max(worst, abs(half_up(k * v) - k * half_up(v)) / ((k + 1) / 2))
check("L03 c168 |R(kv) - kR(v)| <= (k+1)/2 on a grid (worst ratio <= 1)", worst <= 1.0, True)
check(
    "L03 c168 |R(x) - x| <= 1/2 on a grid",
    all(abs(half_up(i * 0.0137) - i * 0.0137) <= 0.5 for i in range(20000)),
    True,
)
check("L03 Remark 2.8 rounding of 10615.8009 = 10616", half_up(10615.8009), 10616)

# ---- L04 ----------------------------------------------------------------------------------------
PMF = Sequence[tuple[int, Fraction]]


def cdf(pmf: PMF, t: int) -> Fraction:
    return sum((p for x, p in pmf if x <= t), Fraction(0))


def integrated_cdf(pmf: PMF, t: int) -> Fraction:
    return sum((p * max(t - x, 0) for x, p in pmf), Fraction(0))


x_ex25 = [(2000, Fraction(1, 2)), (4000, Fraction(1, 2))]
y_ex25 = [(1000, Fraction(1, 4)), (3000, Fraction(1, 2)), (5000, Fraction(1, 4))]
check(
    "L04 Ex2.5 means 3000 and 3000", (expected_value(x_ex25), expected_value(y_ex25)), (Fraction(3000), Fraction(3000))
)
check(
    "L04 Ex2.5 I_X at 3000,4000,5000 = 500,1000,2000",
    [integrated_cdf(x_ex25, t) for t in (3000, 4000, 5000)],
    [Fraction(500), Fraction(1000), Fraction(2000)],
)
check(
    "L04 Ex2.5 I_Y at 2000,3000,4000,5000 = 250,500,1250,2000",
    [integrated_cdf(y_ex25, t) for t in (2000, 3000, 4000, 5000)],
    [Fraction(250), Fraction(500), Fraction(1250), Fraction(2000)],
)
check(
    "L04 Ex2.5 F_X(2000)=1/2 > F_Y(2000)=1/4", (cdf(x_ex25, 2000), cdf(y_ex25, 2000)), (Fraction(1, 2), Fraction(1, 4))
)
check(
    "L04 Ex2.5 F_Y(3000)=3/4 > F_X(3000)=1/2", (cdf(y_ex25, 3000), cdf(x_ex25, 3000)), (Fraction(3, 4), Fraction(1, 2))
)
x_ex17 = [(2000, Fraction(1, 2)), (4000, Fraction(1, 2))]
y_ex17 = [(3000, Fraction(1, 2)), (4000, Fraction(1, 2))]
check(
    "L04 Ex1.7 F_X on 2000,3000,4000 = 1/2,1/2,1",
    [cdf(x_ex17, t) for t in (2000, 3000, 4000)],
    [Fraction(1, 2), Fraction(1, 2), Fraction(1)],
)
check(
    "L04 Ex1.7 F_Y on 2000,3000,4000 = 0,1/2,1",
    [cdf(y_ex17, t) for t in (2000, 3000, 4000)],
    [Fraction(0), Fraction(1, 2), Fraction(1)],
)
check(
    "L04 Ex1.7 means 3000 and 3500", (expected_value(x_ex17), expected_value(y_ex17)), (Fraction(3000), Fraction(3500))
)
x_ex26 = [(1000, Fraction(1, 2)), (5000, Fraction(1, 2))]
y_ex26 = [(3000, Fraction(1))]
support = (1000, 2000, 3000, 4000, 5000)
check(
    "L04 Ex2.6 I_Y(t) <= I_X(t) at every support point",
    all(integrated_cdf(y_ex26, t) <= integrated_cdf(x_ex26, t) for t in support),
    True,
)
check(
    "L04 Ex2.6 I_X on the support = 0,500,1000,1500,2000",
    [integrated_cdf(x_ex26, t) for t in support],
    [Fraction(0), Fraction(500), Fraction(1000), Fraction(1500), Fraction(2000)],
)
check(
    "L04 R3 identity I_X(s_m) = s_m - E X (Ex2.6 X, s_m=5000)",
    integrated_cdf(x_ex26, 5000),
    Fraction(5000) - expected_value(x_ex26),
)

print("ALL OK" if ok else "SOME CHECKS FAILED")
