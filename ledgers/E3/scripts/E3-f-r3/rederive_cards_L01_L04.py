"""Independent re-derivation of every number on the E3 L01-L04 retrieval cards (verifier E3 slice f, round 3).

Written from the lesson text, not from the lab twins. Exact values use fractions.Fraction; floats are used only where
the lesson itself uses floats (square root, CRRA powers). Run with: python3 -I rederive_cards_L01_L04.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction as F

ok_all = True


def check(label: str, cond: bool, detail: str = "") -> None:
    global ok_all
    ok_all = ok_all and cond
    print(f"{'OK  ' if cond else 'FAIL'} {label} {detail}")


# ---- L01 -------------------------------------------------------------------------------------------------
A = [(0, F(1, 4)), (10000, F(1, 2)), (40000, F(1, 4))]  # cents (lab twin layout), used for part A only
B = [(5000, F(1, 2)), (20000, F(1, 2))]
C = [(0, F(1, 3)), (15000, F(1, 3)), (30000, F(1, 3))]


def ev(lot):
    return sum(p * x for x, p in lot)


def eu(lot, u):
    return sum(p * u(x) for x, p in lot)


lin = lambda x: F(x)  # noqa: E731
quad = lambda x: F(x * x, 10000)  # noqa: E731
check("c016 expected values A,B,C = 15000, 12500, 15000", [ev(A), ev(B), ev(C)] == [15000, 12500, 15000])
check("c016 quadratic EU A,B,C = 45000, 21250, 37500", [eu(A, quad), eu(B, quad), eu(C, quad)] == [45000, 21250, 37500])

# Example 1.4 (CU): lottery pays 0, 100, 400 CU with 1/4, 1/2, 1/4
Ex14 = [(F(0), F(1, 4)), (F(100), F(1, 2)), (F(400), F(1, 4))]
check("c014 E X = 150 CU", ev(Ex14) == 150)
check("c014 u(EX) = 150^2 = 22500 CU^2 (quadratic in CU)", F(150) ** 2 == 22500)
check("c014 E u(X) = 45000 CU^2 (quadratic in CU, lesson Example 1.4)", sum(p * x * x for x, p in Ex14) == 45000)

# Example 3.4: C pays 0, 150, 300 CU with 1/3 each; quadratic EU = 37500 CU^2 (CU units)
Ex34 = [(F(0), F(1, 3)), (F(150), F(1, 3)), (F(300), F(1, 3))]
check("L01 Ex3.4 E u(C) quadratic CU = 37500 CU^2", sum(p * x * x for x, p in Ex34) == 37500)

# c011/c012/c173: affine ranking, scale zero
check("c173 b=0 gives E v(L)=a for all L", all(sum(p * (3 + 0 * x) for x, p in lot) == 3 for lot in (A, B, C)))

# ---- L02 -------------------------------------------------------------------------------------------------
W = 100.0
ce_sqrt_float = 0.25 * math.sqrt(40) + 0.5 * math.sqrt(100) + 0.25 * math.sqrt(160)  # E sqrt(W), W in CU
check("Ex1.5 E sqrt(W) about 9.743416", abs(ce_sqrt_float - 9.743416) < 5e-7, f"{ce_sqrt_float:.9f}")
ce = ce_sqrt_float**2
check("Ex1.5 CE = 94.934165 CU", abs(ce - 94.934165) < 5e-7, f"{ce:.9f}")
prem = 100 - ce
check("Ex1.5 premium = 5.065835 CU", abs(prem - 5.065835) < 5e-7, f"{prem:.9f}")
check("c032 ce_cents 9493 (half-up of 9493.4165)", math.floor(ce * 100 + 0.5) == 9493, f"{ce * 100:.4f}")
check("c032 premium_cents 507 (half-up of 506.5835)", math.floor(prem * 100 + 0.5) == 507, f"{prem * 100:.4f}")

# Gamble X: -60, 0, 60 with 1/4, 1/2, 1/4 (exact)
Xg = [(F(-60), F(1, 4)), (F(0), F(1, 2)), (F(60), F(1, 4))]
varX = sum(p * x * x for x, p in Xg) - sum(p * x for x, p in Xg) ** 2
check("L02 Var(X) = 1800 CU^2 exact", varX == 1800)
check("c029 half variance = 900 CU^2", varX / 2 == 900)
rA_100 = 1 / (2 * 100)  # Example 2.3: r_A = 1/(2w)
check("c026/c032 r_A(100) = 0.005 per CU", abs(rA_100 - 0.005) < 1e-15)
check("c026/c032 r_R = 1/2", abs(100 * rA_100 - 0.5) < 1e-15)
pratt = 0.5 * rA_100 * 1800
check("c032 Pratt approximation = 4.5 CU", abs(pratt - 4.5) < 1e-12)
check("c032 error = 0.565835 CU", abs((prem - pratt) - 0.565835) < 5e-7, f"{prem - pratt:.9f}")
share = (prem - pratt) / prem
check("c034 error share 11.17 percent of exact premium", round(share * 100, 2) == 11.17, f"{share * 100:.6f}")

# Part B: premium / eps^2 at five scales, u = sqrt, W = 100 + eps X
limit = 4.5
gaps = []
for eps in (1.0, 0.5, 0.25, 0.1, 0.01):
    e = sum(float(p) * math.sqrt(100 + eps * float(x)) for x, p in Xg)
    cE = e * e
    ratio = (100 - cE) / (eps * eps)
    gaps.append(abs(ratio - limit))
    print(f"      eps {eps}: premium/eps^2 = {ratio:.6f}, gap {abs(ratio - limit):.6f}")
r1 = (100 - sum(float(p) * math.sqrt(100 + 1.0 * float(x)) for x, p in Xg) ** 2) / 1.0
r001 = (100 - sum(float(p) * math.sqrt(100 + 0.01 * float(x)) for x, p in Xg) ** 2) / (0.01 * 0.01)
check("c033 ratio at eps=1 prints 5.065835 and at eps=0.01 prints 4.500046", f"{r1:.6f}" == "5.065835" and f"{r001:.6f}" == "4.500046", f"{r1:.6f} {r001:.6f}")
check("c033 gaps shrink as eps falls", all(b < a for a, b in zip(gaps, gaps[1:])))

# Part C: linear utility premium zero at eps 1, 0.5, 0.1
for eps in (1.0, 0.5, 0.1):
    e = sum(float(p) * (100 + eps * float(x)) for x, p in Xg)
    check(f"c035 linear premium zero at eps={eps}", abs(100 - e) < 1e-12)

# ---- L03 -------------------------------------------------------------------------------------------------
prizes = [5000, 10000, 20000]
probs = [F(1, 4), F(1, 2), F(1, 4)]
mean = sum(p * x for p, x in zip(probs, prizes))
check("c054 expected prize 11250 exact", mean == 11250)


def ce_crra(g: float) -> float:
    if g == 1:
        return math.exp(sum(float(p) * math.log(x) for p, x in zip(probs, prizes)))
    s = 1 - g
    return sum(float(p) * x**s for p, x in zip(probs, prizes)) ** (1 / s)


vals = {g: ce_crra(g) for g in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)}
for g, expect in ((0.0, "11250.0000"), (1.0, "10000.0000"), (2.0, "8888.8889"), (4.0, "7337.6161")):
    check(f"c054 CE at gamma {g} prints {expect}", f"{vals[g]:.4f}" == expect, f"{vals[g]:.6f}")
check("c054 CE falls over the six grid gammas", all(vals[a] >= vals[b] for a, b in zip(sorted(vals), sorted(vals)[1:])))
M2 = sum(p / x for p, x in zip(probs, prizes))
check("c055 M = sum p/x = 9/80000 exact", M2 == F(9, 80000))
check("c055 CE_2 = 80000/9 exact", 1 / M2 == F(80000, 9))
check("c055 80000/9 about 8888.89", round(float(1 / M2), 2) == 8888.89)
check("c047 CE_2 = 1600 for 1000/4000 lottery", abs(1 / (F(1, 2) / 1000 + F(1, 2) / 4000) - 1600) == 0)
check("c047 CE_1 = 2000 for 1000/4000 lottery", abs(math.exp(0.5 * math.log(1000) + 0.5 * math.log(4000)) - 2000) < 1e-9)
check("c046/Prop 2.4 CE_2 = M^{-1}", abs(float(M2) ** -1 - 8888.888888) < 1e-6)
check("c048 homogeneity CE(kX) = k CE(X) at gamma 2, k=3 exact", (F(1, 1) / sum(p / (3 * x) for p, x in zip(probs, prizes))) == 3 * (F(80000, 9)))

# Remark 2.8 bound (k+1)/2, brute force over a grid of values
def half_up(x: float) -> int:
    return math.floor(x + 0.5)


worst = 0.0
rng = random.Random(7)
for _ in range(200000):
    v = rng.uniform(0, 20000)
    k = rng.randint(1, 10)
    d = abs(half_up(k * v) - k * half_up(v))
    worst = max(worst, d - (k + 1) / 2)
check("c168 |R(kv) - k R(v)| <= (k+1)/2 over 200000 random draws (k 1..10)", worst <= 1e-9, f"max excess {worst:.3g}")

# c060/c175 etc. are text; c159 Remark 1.4 (no numbers)

# ---- L04 -------------------------------------------------------------------------------------------------
S = [1000, 2000, 3000, 4000, 5000]


def cdf(pmf, t):
    return sum((p for p, x in zip(pmf, S) if x <= t), F(0))


def icdf(pmf, t):
    return sum((p * max(t - x, 0) for p, x in zip(pmf, S)), F(0))


PX = [F(0), F(1, 2), F(0), F(1, 2), F(0)]
PY = [F(1, 4), F(0), F(1, 2), F(0), F(1, 4)]
check("c067 I_X(3000), I_X(4000), I_X(5000) = 500, 1000, 2000", [icdf(PX, t) for t in (3000, 4000, 5000)] == [500, 1000, 2000])
check(
    "c067 I_Y(2000), I_Y(3000), I_Y(4000), I_Y(5000) = 250, 500, 1250, 2000",
    [icdf(PY, t) for t in (2000, 3000, 4000, 5000)] == [250, 500, 1250, 2000],
)
check("c067 both means 3000", sum(p * x for p, x in zip(PX, S)) == 3000 and sum(p * x for p, x in zip(PY, S)) == 3000)
check("c068 F_X(2000)=1/2 > F_Y(2000)=1/4, F_Y(3000)=3/4 > F_X(3000)=1/2", cdf(PX, 2000) == F(1, 2) and cdf(PY, 2000) == F(1, 4) and cdf(PY, 3000) == F(3, 4) and cdf(PX, 3000) == F(1, 2))
check("c068 X dominates Y second order (I_X <= I_Y at support points)", all(icdf(PX, t) <= icdf(PY, t) for t in S))
PXe = [F(1, 2), F(0), F(0), F(0), F(1, 2)]
PYe = [F(0), F(0), F(1), F(0), F(0)]
def cdf_d(d, t):
    return sum((q for x, q in d.items() if x <= t), F(0))


Fx17 = {2000: F(1, 2), 4000: F(1, 2)}
Fy17 = {3000: F(1, 2), 4000: F(1, 2)}
check("c070/Ex1.7 F_X=(1/2,1/2,1) and F_Y=(0,1/2,1) on 2000,3000,4000", [cdf_d(Fx17, t) for t in (2000, 3000, 4000)] == [F(1, 2), F(1, 2), 1] and [cdf_d(Fy17, t) for t in (2000, 3000, 4000)] == [0, F(1, 2), 1] and all(cdf_d(Fy17, t) <= cdf_d(Fx17, t) for t in (2000, 3000, 4000)))

# Pair data for L04 spreads for Example 2.6 (C): X 1/2 on 1000 and 5000; Y=3000
PXc = [F(1, 2), F(0), F(0), F(0), F(1, 2)]
PYc = [F(0), F(0), F(1), F(0), F(0)]
check("Ex2.6 means both 3000 and I_Y(t)=(t-3000)^+ <= I_X(t) at support points", all(icdf(PYc, t) <= icdf(PXc, t) for t in S))

# ---- Lab L04 seeded pairs, regenerated from the docstring (SIMULATED) ---------------------------------
N_BALLS, N_PAIRS, SEED = 12, 24, 20261028
step = F(1, N_BALLS)


def draw_pmf(rng_):
    counts = [0] * 5
    for _ in range(N_BALLS):
        counts[rng_.randrange(5)] += 1
    return tuple(F(c, N_BALLS) for c in counts)


def shift_up(px, rng_):
    eligible = [i for i in range(4) if px[i] >= step]
    if not eligible:
        return None
    i = rng_.choice(eligible)
    j = rng_.randrange(i + 1, 5)
    q = list(px)
    q[i] -= step
    q[j] += step
    return tuple(q)


def mean_of(pmf):
    return sum((p * x for p, x in zip(pmf, S)), F(0))


def match_mean(pmf, target):
    move = (target - mean_of(pmf)) / (S[-1] - S[0])
    q = list(pmf)
    if move >= 0:
        if q[0] < move:
            return None
        q[0] -= move
        q[-1] += move
    else:
        m = -move
        if q[-1] < m:
            return None
        q[-1] -= m
        q[0] += m
    return tuple(q)


rng = random.Random(SEED)
kinds = ("shift", "equal-mean", "random")
pairs = []
while len(pairs) < N_PAIRS:
    kind = kinds[len(pairs) % 3]
    px = draw_pmf(rng)
    if kind == "shift":
        py = shift_up(px, rng)
    elif kind == "equal-mean":
        py = match_mean(draw_pmf(rng), mean_of(px))
    else:
        py = draw_pmf(rng)
    if py is not None:
        pairs.append((kind, px, py))


def verdict(xf, yf):
    if xf and yf:
        return "identical"
    if xf:
        return "X dominates Y"
    if yf:
        return "Y dominates X"
    return "no ranking"


from collections import Counter  # noqa: E402

fo = Counter()
so = Counter()
so_pairs = []
for n, (kind, px, py) in enumerate(pairs):
    xf = all(cdf(px, t) <= cdf(py, t) for t in S)
    yf = all(cdf(py, t) <= cdf(px, t) for t in S)
    v = verdict(xf, yf)
    fo[v] += 1
    if mean_of(px) == mean_of(py):
        xs = all(icdf(px, t) <= icdf(py, t) for t in S)
        ys = all(icdf(py, t) <= icdf(px, t) for t in S)
        sv = verdict(xs, ys)
        so[sv] += 1
        if sv == "no ranking":
            so_pairs.append(n)
print("      FOSD tally:", dict(sorted(fo.items())))
print("      SOSD tally (equal-mean pairs):", dict(sorted(so.items())), "no-ranking pair indices:", so_pairs)
check(
    "c075 FOSD tally X 3, Y 10, identical 1, none 10",
    dict(fo) == {"X dominates Y": 3, "Y dominates X": 10, "identical": 1, "no ranking": 10},
)
check(
    "c076 SOSD tally X 3, Y 2, identical 1, none 2 over 8 equal-mean pairs",
    dict(so) == {"X dominates Y": 3, "Y dominates X": 2, "identical": 1, "no ranking": 2} and sum(so.values()) == 8,
)
check("c073 equal-mean pairs with no SOSD ranking are pairs 16 and 19", so_pairs == [16, 19], str(so_pairs))

print("ALL CHECKS PASS" if ok_all else "SOME CHECKS FAILED")
