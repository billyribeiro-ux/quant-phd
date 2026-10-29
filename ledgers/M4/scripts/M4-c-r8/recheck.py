# Independent recomputation of L08-L10 numbers (round 8). Uses numpy and its own code paths.
import math, random
from fractions import Fraction
from decimal import Decimal, getcontext
import numpy as np

getcontext().prec = 50
print("== L08 ==")
A = np.array([[2.0, 0.0], [1.0, 1.0]])
Q = np.array([[0.0, -1.0], [1.0, 0.0]])
Sig = A @ A.T
B = A @ Q
print("AAt", Sig.tolist(), "AtA", (A.T @ A).tolist(), "B", B.tolist(), "BBt==Sig", np.allclose(B @ B.T, Sig))
rng = random.Random(2026)
N = 20000
Zs = np.array([[rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0)] for _ in range(N)])
mu = np.array([1.0, -2.0])
X = mu + Zs @ A.T
Y = mu + Zs @ B.T
meanX = X.mean(axis=0)
covX = np.cov(X, rowvar=False, ddof=1)
covY = np.cov(Y, rowvar=False, ddof=1)
print("meanX", meanX.round(6).tolist(), "covX", covX.round(6).tolist())
print("gap X from Sig", round(np.abs(covX - Sig).max(), 6), "gap X from AtA", round(np.abs(covX - A.T @ A).max(), 6))
print("covY", covY.round(6).tolist(), "gap Y from Sig", round(np.abs(covY - Sig).max(), 6))
print("entry gaps X", np.abs(covX - Sig).round(6).tolist())
print("AtA-Sig", (A.T @ A - Sig).tolist())

print("== L09 ==")
phi1 = 0.5 * (1 + math.erf(1 / math.sqrt(2)))
print("Phi(1)", round(phi1, 9))
def mass(n):
    # integer counts convolution, exact
    cnt = [1]
    for _ in range(n):
        new = [0] * (len(cnt) + 6)
        for s, c in enumerate(cnt):
            if c:
                for f in range(1, 7):
                    new[s + f] += c
        cnt = new
    return cnt
sig2 = Fraction(35, 12)
for n in (1, 5, 10, 20, 40):
    cnt = mass(n)
    tot = 6 ** n
    assert sum(cnt) == tot
    thr_dec = Decimal(7 * n) / 2 + (Decimal(35 * n) / 12).sqrt()
    m = int(thr_dec.to_integral_value(rounding="ROUND_FLOOR"))
    p = Fraction(sum(cnt[: m + 1]), tot)
    print(f"n={n} thr_real={float(thr_dec):.4f} m={m} P={float(p):.6f} gap={float(p) - phi1:+.6f}")
# Part B path
rng = random.Random(2026)
path = [rng.randint(1, 6) for _ in range(10000)]
for n in (10, 100, 1000, 10000):
    print("running", n, round(sum(path[:n]) / n, 4), "cheb", round((35 / 12) / (n * 0.25), 4))
print("M1 7/60", 7 / 60, "M2 35/48", 35 / 48, "M3 bound", 1 / (2 * 0.25))
# Part C
for n in (5, 30, 200):
    rng = random.Random(2026)
    hits = 0
    s = math.sqrt(35 / 12)
    for _ in range(4000):
        tot_ = sum(rng.randint(1, 6) for _ in range(n))
        z = (tot_ / n - 3.5) / (s / math.sqrt(n))
        hits += z <= 1.0
    ph = hits / 4000
    se = math.sqrt(ph * (1 - ph) / 4000)
    print(f"C n={n} phat={ph:.4f} se={se:.6f} gap={ph - phi1:+.5f}")
p = 0.8552
print("E2 se", math.sqrt(p * (1 - p) / 4000), "ratio printed", (0.8552 - 0.841345) / 0.0056, "unrounded", (0.8552 - 0.841345) / math.sqrt(0.8552 * 0.1448 / 4000))
print("E3 bound", (35 / 12) / (10000 * 0.25))
print("E1 thr", 35 + math.sqrt(35 * 10 / 12))

print("== L10 ==")
def fC(x): return 1 / (math.pi * (1 + x * x))
def fV(t): return 2 / (math.pi * math.sqrt(3)) * (1 + t * t / 3) ** -2
xg, wg = np.polynomial.legendre.leggauss(400)
def tail_num(f, x):
    # integral over [x, inf) via t = x/u, u in (0,1]
    u = 0.5 * (xg + 1); w = 0.5 * wg
    return float(np.sum(w * f(x / u) * x / u ** 2))
for x in (1.0, 2.0, 10.0):
    print(f"C tail x={x}: numeric {2*tail_num(fC, x):.12f} closed {2/math.pi*math.atan(1/x):.12f}")
    print(f"V tail x={x}: numeric {2*tail_num(fV, x):.12f} closed {2/math.pi*(math.atan(math.sqrt(3)/x) - x*math.sqrt(3)/(3+x*x)):.12f}")
for x in (100.0, 1000.0):
    vnum = 2 * tail_num(fV, x)
    print(f"x^3 P(|V|>x) x={x}: numeric {x**3*vnum:.8f}  closed-lab {x**3*2*((math.atan(math.sqrt(3)/x) - (x*math.sqrt(3)/(3+x*x)))/math.pi*math.pi/math.pi):.8f}")
    print(f"x P(|C|>x) x={x}: {x*2/math.pi*math.atan(1/x):.9f}")
print("4sqrt3/pi", 4 * math.sqrt(3) / math.pi, "2/pi", 2 / math.pi)
# F_V(2)-F_V(-2) numeric
def fv_int(a, b, n=200000):
    h = (b - a) / n
    return h * sum(fV(a + (k + 0.5) * h) for k in range(n))
print("F_V(2)-F_V(-2) midpoint", round(fv_int(-2, 2), 9), "closed", round(2 * (0.5 + (math.atan(2/math.sqrt(3)) + (2/math.sqrt(3))/(1+4/3))/math.pi) - 1, 9))
# Lab C-part IQR via numpy linear (= inclusive)
for name, n in (("normal", 10), ("normal", 100)):
    pass
def draws(name, rng):
    if name == "normal": return rng.gauss(0.0, 1.0)
    if name == "t3":
        z = rng.gauss(0.0, 1.0); w = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(3)); return z / math.sqrt(w / 3)
    u = rng.random(); return math.tan(math.pi * (u - 0.5))
for name, seed in (("normal", 2026), ("t3", 2027), ("cauchy", 2028)):
    for n in (10, 100):
        rng = random.Random(seed + 100 * n)
        means = np.array([sum(draws(name, rng) for _ in range(n)) / n for _ in range(400)])
        q1, q3 = np.percentile(means, [25, 75])
        sd = ""
        if name != "cauchy":
            sig = 1.0 if name == "normal" else math.sqrt(3)
            sd = f" var={np.var(math.sqrt(n) * means / sig, ddof=1):.4f}"
        print(f"C {name} n={n} IQR={q3 - q1:.4f}{sd}")
# arctan inequality on a grid
us = np.linspace(0, 50, 200001)
print("arctan u >= u - u^3/3 on grid:", bool(np.all(np.arctan(us) >= us - us**3 / 3 - 1e-15)))
print("E|C| lower-bound check x=1:", 2 * (1 / (2 * math.pi)) * (math.log(1e6) - math.log(2)) > 0)
print("Remark 1.4 / lab probes done")
