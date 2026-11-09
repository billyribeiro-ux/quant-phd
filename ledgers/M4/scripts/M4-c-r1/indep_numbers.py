"""Independent re-derivation of the numbers printed or stated in L08, L09 and L10 (verifier, round 1).

Written from the lesson text, not from the twins. Standard library only. Usage: python -I indep_numbers.py
"""
import math
import random
import statistics
from fractions import Fraction

print("== L08 exact ==")
A = [[2, 0], [1, 1]]
Q = [[0, -1], [1, 0]]


def mm(x, y):
    return [[sum(x[i][k] * y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def tr(x):
    return [[x[j][i] for j in range(2)] for i in range(2)]


AAt = mm(A, tr(A))
B = mm(A, Q)
BBt = mm(B, tr(B))
AtA = mm(tr(A), A)
print("AA^T", AAt, "B", B, "BB^T", BBt, "A^TA", AtA)
print("A^TA - Sigma", [[AtA[i][j] - AAt[i][j] for j in range(2)] for i in range(2)])
print("w^T Sigma w for w=(1,1):", sum(AAt[i][j] for i in range(2) for j in range(2)))
rng = random.Random(2026)
n = 20000
rowsX, rowsY = [], []
for _ in range(n):
    z1 = rng.gauss(0.0, 1.0)
    z2 = rng.gauss(0.0, 1.0)
    rowsX.append((1 + 2 * z1, -2 + z1 + z2))
    rowsY.append((1 + 0 * z1 - 2 * z2, -2 + z1 - z2))


def stats(rows):
    m = [sum(r[i] for r in rows) / n for i in range(2)]
    c = [[sum((r[i] - m[i]) * (r[j] - m[j]) for r in rows) / (n - 1) for j in range(2)] for i in range(2)]
    return m, c


mX, cX = stats(rowsX)
mY, cY = stats(rowsY)
sig = [[4, 2], [2, 2]]
atA = [[5, 1], [1, 1]]


def gap(c, t):
    return max(abs(c[i][j] - t[i][j]) for i in range(2) for j in range(2))


print("mean X", [round(v, 4) for v in mX], "cov X", [[round(v, 4) for v in r] for r in cX])
print("gap X from Sigma", round(gap(cX, sig), 4), "from A^TA", round(gap(cX, atA), 4))
print("cov Y", [[round(v, 4) for v in r] for r in cY], "gap Y from Sigma", round(gap(cY, sig), 4))

print("== L09 exact and seeded ==")
phi1 = 0.5 * (1 + math.erf(1 / math.sqrt(2)))
print("Phi(1)", round(phi1, 6), repr(phi1))


def pmf_counts(k):
    counts = [1]
    for _ in range(k):
        new = [0] * (len(counts) + 5)
        for s, c in enumerate(counts):
            for f in range(1, 7):
                new[s + f - 1] += c
        counts = new
    return counts  # counts[s - k] for sum s


for k in (1, 5, 10, 20, 40):
    cnt = pmf_counts(k)
    thr = math.floor(3.5 * k + math.sqrt(35 * k / 12))
    tot = sum(cnt[: thr - k + 1]) if thr >= k else 0
    p = Fraction(tot, 6**k)
    print(f"n={k} thr={thr} P={float(p):.6f} gap={float(p) - phi1:+.6f}")
rng = random.Random(2026)
path = [rng.randint(1, 6) for _ in range(10000)]
for m in (10, 100, 1000, 10000):
    mean = sum(path[:m]) / m
    print(f"path n={m} mean={mean:.4f} gap={mean - 3.5:+.4f} chebyshev={(35 / 12) / (m * 0.25):.4f}")
for k in (5, 30, 200):
    r = random.Random(2026)
    hits = 0
    for _ in range(4000):
        s = sum(r.randint(1, 6) for _ in range(k))
        z = (s / k - 3.5) / (math.sqrt(35 / 12) / math.sqrt(k))
        if z <= 1.0:
            hits += 1
    p = hits / 4000
    se = math.sqrt(p * (1 - p) / 4000)
    print(f"MC n={k} hits={hits} p={p:.4f} se={se:.4f} gap={p - phi1:+.4f}")

print("== L10 ==")
s3 = math.sqrt(3.0)
print("P(|Z|>10) erfc", math.erfc(10 / math.sqrt(2)))
print("P(|C|>10)", 2 / math.pi * math.atan(0.1), "arctan(0.1)", math.atan(0.1))
y = 10 / s3
print("P(|V|>10) closed", 2 / math.pi * (math.atan(1 / y) - y / (1 + y * y)))
print("ratio C/Z", (2 / math.pi * math.atan(0.1)) / math.erfc(10 / math.sqrt(2)))
print("2/pi", 2 / math.pi, "4sqrt3/pi", 4 * s3 / math.pi)
for x in (10.0, 100.0, 1000.0):
    yy = s3 / x
    print(f"x={x:.0f} xP(|C|>x)={x * 2 / math.pi * math.atan(1 / x):.6f} x^3P(|V|>x)={x**3 * 2 / math.pi * (math.atan(yy) - yy / (1 + yy * yy)):.6f}")


def draw_t3(r):
    z = r.gauss(0.0, 1.0)
    w = sum(r.gauss(0.0, 1.0) ** 2 for _ in range(3))
    return z / math.sqrt(w / 3.0)


def draw_c(r):
    return math.tan(math.pi * (r.random() - 0.5))


laws = (("normal", lambda r: r.gauss(0.0, 1.0), 2026, 1.0), ("t3", draw_t3, 2027, s3), ("cauchy", draw_c, 2028, None))
for name, f, seed, sigma in laws:
    for k in (10, 100):
        r = random.Random(seed + 100 * k)
        means = [sum(f(r) for _ in range(k)) / k for _ in range(400)]
        q1, _, q3 = statistics.quantiles(means, n=4, method="inclusive")
        extra = ""
        if sigma is not None:
            extra = f" var(sqrt(n)Xbar/sigma)={statistics.variance([math.sqrt(k) * m / sigma for m in means]):.4f}"
        print(f"{name} n={k} IQR={q3 - q1:.4f}{extra}")
