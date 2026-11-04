# Independent re-derivation of the E3 slice-f numbers (round 7). Uses decimal at 40 digits and Fractions;
# shares no code with the lab twins.
import math
import random
from decimal import Decimal, getcontext, ROUND_HALF_UP
from fractions import Fraction as F

getcontext().prec = 50

# ---- L02: CE, premium, Pratt approximation, Part B ratios (Decimal, sqrt via Decimal) ----
W = Decimal(100)
gamble = [(Decimal(-60), F(1, 4)), (Decimal(0), F(1, 2)), (Decimal(60), F(1, 4))]
mean_x = sum(Decimal(p.numerator) / Decimal(p.denominator) * x for x, p in gamble)
var_x = sum(Decimal(p.numerator) / Decimal(p.denominator) * x * x for x, p in gamble) - mean_x ** 2
print("L02 mean", mean_x, "var", var_x)
rA = (Decimal("0.25") / (W ** 3).sqrt()) / (Decimal("0.5") / W.sqrt())  # -u''/u' for sqrt: (1/4 w^-3/2)/(1/2 w^-1/2)
print("L02 rA(100) =", rA, " rR =", rA * W)
limit = Decimal("0.5") * rA * var_x
print("L02 limit =", limit)
for eps in [Decimal(1), Decimal("0.5"), Decimal("0.25"), Decimal("0.1"), Decimal("0.01")]:
    e = sum((Decimal(p.numerator) / Decimal(p.denominator)) * (W + eps * x).sqrt() for x, p in gamble)
    ce = e * e
    prem = W - ce
    ratio = prem / (eps * eps)
    print("eps", eps, "CE", round(ce, 6), "premium", round(prem, 6), "ratio", round(ratio, 6), "gap", round(abs(ratio - limit), 6))
    if eps == 1:
        cents_ce = (ce * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
        cents_p = (prem * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP)
        print("  ce_cents", cents_ce, "premium_cents", cents_p, "error", round(prem - limit, 6), "err share of premium %", round((prem - limit) / prem * 100, 4), "err share of approx %", round((prem - limit) / limit * 100, 4))
print("half var", var_x / 2, "half rA var", limit)
# E1 check
print("E1 ratio 0.25/0.1:", float(Decimal("0.028811") / Decimal("0.004565")), " eps^2 factor:", 0.0625 / 0.01)

# ---- L03: CRRA CE on the fixed lottery (Fraction and Decimal) ----
prizes = [5000, 10000, 20000]
probs = [F(1, 4), F(1, 2), F(1, 4)]
print("L03 expected prize", sum(p * x for p, x in zip(probs, prizes)))
for g in [Decimal("0"), Decimal("0.25"), Decimal("0.5"), Decimal(1), Decimal(2), Decimal(4)]:
    if g == 1:
        m = sum(Decimal(p.numerator) / Decimal(p.denominator) * Decimal(x).ln() for p, x in zip(probs, prizes))
        ce = m.exp()
    else:
        s = 1 - g
        M = sum(Decimal(p.numerator) / Decimal(p.denominator) * (Decimal(x) ** s) for p, x in zip(probs, prizes))
        ce = M ** (1 / s)
    print("gamma", g, "CE", ce.quantize(Decimal("0.0001")), "cents_round", (ce).quantize(Decimal(1), rounding=ROUND_HALF_UP))
M2 = sum(F(p) * F(1, x) for p, x in zip(probs, prizes))
print("gamma2 exact M =", M2, "CE =", 1 / M2, float(1 / M2))
# CRRA gamma 0.5 cents check
# L03 M2/M3 problem values
M = F(1, 4) * F(1, 1000) + F(3, 4) * F(1, 9000)
print("L03 M2: M =", M, "CE2 =", 1 / M, "E =", F(1, 4) * 1000 + F(3, 4) * 9000)
M = F(1, 4) * F(1, 3000) + F(3, 4) * F(1, 27000)
print("L03 M3: CE2(3X) =", 1 / M)
# L03 E2 M
print("L03 E2 M =", F(1, 4) * F(1, 5000) + F(1, 2) * F(1, 10000) + F(1, 4) * F(1, 20000))
# L03 Example 2.5
print("Ex2.5 CE2 =", 1 / (F(1, 2) * F(1, 1000) + F(1, 2) * F(1, 4000)), " CE1 =", math.sqrt(1000 * 4000))
# L03 M1: u_{1/2}, r_A(4)
print("L03 M1 rA(4) =", F(1, 2) / 4)
# L02 M1: W 4 or 16
print("L02 M1 CE =", (0.5 * 2 + 0.5 * 4) ** 2)

# ---- L04: distribution-function and integrated checks on the named pairs and the seeded run ----
SUP = (1000, 2000, 3000, 4000, 5000)
def pmf(d):
    return tuple(d.get(x, F(0)) for x in SUP)
def mean(p):
    return sum(q * x for q, x in zip(p, SUP))
def cdf(p, t):
    return sum(q for q, x in zip(p, SUP) if x <= t)
def icdf(p, t):
    return sum(q * max(t - x, 0) for q, x in zip(p, SUP))
A = (pmf({2000: F(1, 2), 4000: F(1, 2)}), pmf({1000: F(1, 4), 3000: F(1, 2), 5000: F(1, 4)}))
B = (pmf({2000: F(1, 2), 4000: F(1, 2)}), pmf({3000: F(1, 2), 4000: F(1, 2)}))
C = (pmf({1000: F(1, 2), 5000: F(1, 2)}), pmf({3000: F(1)}))
for name, (x, y) in [("A", A), ("B", B), ("C", C)]:
    print(name, "means", mean(x), mean(y), "F_X", [str(cdf(x, t)) for t in SUP], "F_Y", [str(cdf(y, t)) for t in SUP])
    print(name, "I_X", [str(icdf(x, t)) for t in SUP], "I_Y", [str(icdf(y, t)) for t in SUP])
# independent verdicts for seeded pairs: same draw order as the lab (documented in the lab source)
def draw(rng):
    counts = [0] * 5
    for _ in range(12):
        counts[rng.randrange(5)] += 1
    return tuple(F(c, 12) for c in counts)
def shift_up(p, rng):
    step = F(1, 12)
    elig = [i for i in range(4) if p[i] >= step]
    if not elig:
        return None
    i = rng.choice(elig)
    j = rng.randrange(i + 1, 5)
    q = list(p)
    q[i] -= step
    q[j] += step
    return tuple(q)
def match_mean(p, target):
    move = (target - mean(p)) / (5000 - 1000)
    q = list(p)
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
rng = random.Random(20261028)
kinds = ("shift", "equal-mean", "random")
pairs = []
while len(pairs) < 24:
    kind = kinds[len(pairs) % 3]
    px = draw(rng)
    if kind == "shift":
        py = shift_up(px, rng)
    elif kind == "equal-mean":
        py = match_mean(draw(rng), mean(px))
    else:
        py = draw(rng)
    if py is not None:
        pairs.append((kind, px, py))
def verdict(a, b):
    if a and b: return "identical"
    if a: return "X dominates Y"
    if b: return "Y dominates X"
    return "no ranking"
from collections import Counter
fc = Counter(); sc = Counter(); nsec = 0; fo = 0; so = 0
for kind, px, py in pairs:
    fx = [cdf(px, t) for t in SUP]; fy = [cdf(py, t) for t in SUP]
    fv = verdict(all(a <= b for a, b in zip(fx, fy)), all(b <= a for a, b in zip(fx, fy)))
    fc[fv] += 1
    if mean(px) == mean(py):
        nsec += 1
        ix = [icdf(px, t) for t in SUP]; iy = [icdf(py, t) for t in SUP]
        sv = verdict(all(a <= b for a, b in zip(ix, iy)), all(b <= a for a, b in zip(ix, iy)))
        sc[sv] += 1
    print(kind, fv, "means", mean(px), mean(py))
print("FOSD counts", dict(sorted(fc.items())))
print("equal-mean pairs", nsec, "SOSD counts", dict(sorted(sc.items())))
