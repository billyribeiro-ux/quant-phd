"""Independent recomputation for M4 slice b, round 5 (L05-L07). Run: python -I <this file>.

Re-implements the seeded draws from the docstrings (not by importing the twins) and prints unrounded values."""
import math
import random

# L05 Lab 1
S1, S2, RHO, SEED = 0.02, 0.03, 0.6, 20260501


def draws(n, seed):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        out.append((S1 * z1, S2 * (RHO * z1 + math.sqrt(1.0 - RHO * RHO) * z2)))
    return out


def sample_cov(xs):
    n = len(xs)
    m1 = sum(x for x, _ in xs) / n
    m2 = sum(y for _, y in xs) / n
    s11 = sum((x - m1) ** 2 for x, _ in xs) / (n - 1)
    s22 = sum((y - m2) ** 2 for _, y in xs) / (n - 1)
    s12 = sum((x - m1) * (y - m2) for x, y in xs) / (n - 1)
    return [[s11, s12], [s12, s22]]


xs20 = draws(20000, SEED)
s = sample_cov(xs20)
print("L05 s11 unrounded", repr(s[0][0]))
print("L05 E1 relative error (s11-0.0004)/0.0004 unrounded", (s[0][0] - 0.0004) / 0.0004)
print("L05 E1 from printed 0.00039491", (0.00039491 - 0.0004) / 0.0004)
corr = s[0][1] / math.sqrt(s[0][0] * s[1][1])
print("L05 sample corr unrounded", corr, "error", corr - RHO)
sig = [[S1 * S1, RHO * S1 * S2], [RHO * S1 * S2, S2 * S2]]
print("L05 max entry error n=20000 unrounded", max(abs(s[i][j] - sig[i][j]) for i in range(2) for j in range(2)))
s100 = sample_cov(draws(100, SEED))
print("L05 n=100 entry errors", [abs(s100[0][0] - 0.0004), abs(s100[0][1] - 0.00036), abs(s100[1][1] - 0.0009)])
vals = []
for k in range(9):
    a = k * math.pi / 8
    w = (math.cos(a), math.sin(a))
    vals.append(sum(w[i] * s[i][j] * w[j] for i in range(2) for j in range(2)))
print("L05 quad forms", vals)
print("L05 ratio max/min unrounded", max(vals) / min(vals), "argmax", vals.index(max(vals)), "argmin", vals.index(min(vals)))
print("L05 ratio from printed 0.0010539032/0.0002187758", 0.0010539032 / 0.0002187758)

# L06 Lab 1
SEED6 = 20260602


def chi_t(rng, nu):
    z = rng.gauss(0.0, 1.0)
    w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))
    return w, z / (w / nu) ** 0.5


def mv(xs):
    n = len(xs)
    m = sum(xs) / n
    return m, sum((x - m) ** 2 for x in xs) / (n - 1)


for nu in (5, 10):
    rng = random.Random(SEED6 + nu)
    ts = [chi_t(rng, nu)[1] for _ in range(100000)]
    m, v = mv(ts)
    ex = nu / (nu - 2)
    print(f"L06 nu {nu} mean {m!r} var {v!r} rel_err {(v - ex) / ex!r}")
rng = random.Random(SEED6 + 500)
ws, invs = [], []
for _ in range(100000):
    w, _ = chi_t(rng, 5)
    ws.append(w)
    invs.append(1.0 / w)
print("L06 meanW", sum(ws) / 100000, "mean1/W", sum(invs) / 100000)
print("L06 E1 from printed", (1.669114 - 1.666667) / 1.666667)
print("L06 E2 ratio |-0.007740|/0.001469", 0.007740 / 0.001469)
print("L06 E3 rel err", (4.997415 - 5) / 5)

# L07 Lab 1
MU, SIG = 0.5, 1.5
P_A, SEED7, N7 = 0.25, 20260701, 100000


def dens(x):
    return math.exp(-((x - MU) ** 2) / (2.0 * SIG * SIG)) / (SIG * math.sqrt(2.0 * math.pi))


def simpson(t):
    lo, hi = MU - 12 * SIG, MU + 12 * SIG
    N = 20000
    h = (hi - lo) / N
    tot = 0.0
    for k in range(N + 1):
        x = lo + k * h
        w = 1.0 if k in (0, N) else (4.0 if k % 2 else 2.0)
        tot += w * math.exp(t * x) * dens(x)
    return tot * h / 3.0


def closed(t):
    return math.exp(MU * t + SIG * SIG * t * t / 2.0)


for t in (-1.0, 0.0, 0.5, 1.0, 2.0):
    print("L07 t", t, "abs diff", abs(simpson(t) - closed(t)))
rng = random.Random(SEED7)
cs = ss = 0.0
for _ in range(N7):
    x = 0.0 if rng.random() < P_A else 2.0
    cs += math.cos(x)
    ss += math.sin(x)
mc, ms = cs / N7, ss / N7
phi1 = P_A * complex(1, 0) + (1 - P_A) * complex(math.cos(2.0), math.sin(2.0))
print("L07 sample mean cos unrounded", mc, "real phi(1)", phi1.real, "diff", mc - phi1.real)
print("L07 diff from printed", -0.062124 - (-0.062110))
print("L07 E2 rel err", 7.10543e-13 / 244.69193226, "over eps", 7.10543e-13 / 244.69193226 / 2.220446049250313e-16)
print("L07 modulus t=1", abs(phi1), "sq formula", 0.625 + 0.375 * math.cos(-2.0), math.sqrt(0.625 + 0.375 * math.cos(-2.0)))
print("L07 M2 e^3", math.exp(3))
