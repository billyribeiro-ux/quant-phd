"""Round 12 slice b: recompute the L06 and L07 lab numbers and prose figures from the unrounded values."""
import math
import random
import sys

sys.path.insert(0, "/Users/billyribeiro/.fanout/wt/verifyD12-M4-b/ledgers/M4/scripts/M4-b-r12")

SEED, N = 20260602, 100000


def chi_square_and_t(rng, nu):
    z = rng.gauss(0.0, 1.0)
    w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))
    return w, z / (w / nu) ** 0.5


def mean_var(xs):
    n = len(xs)
    m = sum(xs) / n
    return m, sum((x - m) ** 2 for x in xs) / (n - 1)


print("== L06 Part A")
rel = {}
for nu in (5, 10):
    rng = random.Random(SEED + nu)
    ts = [chi_square_and_t(rng, nu)[1] for _ in range(N)]
    m, v = mean_var(ts)
    exact = nu / (nu - 2)
    rel[nu] = (v - exact) / exact
    print("nu", nu, "mean", repr(m), "var", repr(v), "exact", exact, "relerr", repr(rel[nu]))
print("E2 ratio |rel10|/|rel5|", repr(abs(rel[10]) / abs(rel[5])))
print("E1 printed-based relerr", repr((1.669114 - 1.666667) / 1.666667))
print("E1 with 0.001469 relerr 5 digits check", round(rel[5], 6))

print("== L06 Part B")
rng = random.Random(SEED + 500)
ws, invs = [], []
for _ in range(N):
    w, _ = chi_square_and_t(rng, 5)
    ws.append(w)
    invs.append(1.0 / w)
mw = sum(ws) / N
mi = sum(invs) / N
print("mean W", repr(mw), "mean 1/W", repr(mi))
print("E3 diff", repr(mw - 5), "rel", repr((mw - 5) / 5), "pct", repr((mw - 5) / 5 * 100))

print("== L07 Part A")
MU, SIGMA = 0.5, 1.5


def dens(x):
    return math.exp(-((x - MU) ** 2) / (2.0 * SIGMA * SIGMA)) / (SIGMA * math.sqrt(2.0 * math.pi))


def simpson(t):
    lo, hi = MU - 12 * SIGMA, MU + 12 * SIGMA
    K = 20000
    h = (hi - lo) / K
    tot = 0.0
    for k in range(K + 1):
        x = lo + k * h
        w = 1.0 if k in (0, K) else (4.0 if k % 2 == 1 else 2.0)
        tot += w * math.exp(t * x) * dens(x)
    return tot * h / 3.0


def closed(t):
    return math.exp(MU * t + SIGMA * SIGMA * t * t / 2.0)


d2 = abs(simpson(2.0) - closed(2.0))
print("t=2 numerical", repr(simpson(2.0)), "closed", repr(closed(2.0)), "absdiff", repr(d2))
print("E2 relerr", repr(d2 / closed(2.0)), "over eps", repr(d2 / closed(2.0) / 2.220446049250313e-16))
print("max absdiff over rows", max(abs(simpson(t) - closed(t)) for t in (-1.0, 0.0, 0.5, 1.0, 2.0)))

print("== L07 Part B/C")
PA, VA, VB = 0.25, 0.0, 2.0
phi1 = PA * complex(math.cos(0), math.sin(0)) + (1 - PA) * complex(math.cos(2), math.sin(2))
print("phi(1)", repr(phi1), "modulus", repr(abs(phi1)))
print("sqrt(0.4689449)", repr(math.sqrt(0.4689449)), "0.625+0.375cos(-2)", repr(0.625 + 0.375 * math.cos(-2)))
print("E3 |phi|^2 from formula", repr(0.25 ** 2 + 0.75 ** 2 + 0.375 * math.cos(-2)), "sqrt", repr(math.sqrt(0.25 ** 2 + 0.75 ** 2 + 0.375 * math.cos(-2))))
rng = random.Random(20260701)
cs = ss = 0.0
for _ in range(N):
    x = VA if rng.random() < PA else VB
    cs += math.cos(x)
    ss += math.sin(x)
mc, ms = cs / N, ss / N
print("sample mean cos", repr(mc), "sample mean sin", repr(ms))
print("E1 diff", repr(mc - phi1.real), "real phi", repr(phi1.real))
print("cos2", repr(math.cos(2)), "0.25+0.75cos2", repr(0.25 + 0.75 * math.cos(2)))
print("e^{1/2}", repr(math.exp(0.5)), "e^3", repr(math.exp(3)))
print("sqrt(2/pi)", repr(math.sqrt(2 / math.pi)))
