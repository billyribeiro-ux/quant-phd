"""Verifier round 2, slice M4-c: independent recomputation of the numbers printed or quoted in L08, L09 and L10.

Written from the page statements, not from the twins. Standard library only. Run as: python -I <this file>.
"""
import math
import random
import statistics
from fractions import Fraction

print("== L08")
A = [[2, 0], [1, 1]]
Q = [[0, -1], [1, 0]]
def mm(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))] for i in range(len(X))]
def tr(X):
    return [list(r) for r in zip(*X)]
Sig = mm(A, tr(A))
B = mm(A, Q)
ATA = mm(tr(A), A)
print("AA^T", Sig, "B", B, "BB^T", mm(B, tr(B)), "A^TA", ATA)
print("gap A^TA - Sigma entries", [[ATA[i][j] - Sig[i][j] for j in range(2)] for i in range(2)])
print("w^T Sig w at (1,1) =", sum(Sig[i][j] for i in range(2) for j in range(2)))
rng = random.Random(2026)
n = 20000
rowsX, rowsY = [], []
for _ in range(n):
    z1 = rng.gauss(0.0, 1.0)
    z2 = rng.gauss(0.0, 1.0)
    rowsX.append([1 + 2 * z1, -2 + z1 + z2])
    rowsY.append([1 + 0 * z1 + (B[0][0] * z1 + B[0][1] * z2), -2 + (B[1][0] * z1 + B[1][1] * z2)])
def smean(rows):
    return [sum(r[i] for r in rows) / len(rows) for i in range(2)]
def scov(rows):
    m = smean(rows)
    d = len(rows) - 1
    return [[sum((r[i] - m[i]) * (r[j] - m[j]) for r in rows) / d for j in range(2)] for i in range(2)]
mX = smean(rowsX)
cX = scov(rowsX)
cY = scov(rowsY)
print("mean X", [round(v, 4) for v in mX], "(page: 0.9770, -2.0055)")
print("cov X", [[round(v, 4) for v in r] for r in cX], "(page: ((4.0073, 2.0187), (2.0187, 1.9936)))")
gapS = max(abs(cX[i][j] - Sig[i][j]) for i in range(2) for j in range(2))
gapA = max(abs(cX[i][j] - ATA[i][j]) for i in range(2) for j in range(2))
print("gap X from Sigma", round(gapS, 4), "(page 0.0187); from A^TA", round(gapA, 4), "(page 1.0187)")
print("cov Y", [[round(v, 4) for v in r] for r in cY], "(page ((3.9070, 1.9385), (1.9385, 1.9636)))")
print("gap Y from Sigma", round(max(abs(cY[i][j] - Sig[i][j]) for i in range(2) for j in range(2)), 4), "(page 0.0930)")
print("L08 E1 gaps from Sigma with printed entries:", [round(abs(x - y), 4) for x, y in [(4.0073, 4), (2.0187, 2), (1.9936, 2)]])

print("== L09")
PHI1 = 0.5 * (1 + math.erf(1 / math.sqrt(2)))
print("Phi(1) =", round(PHI1, 6))
def die_pmf(n):
    pmf = {0: Fraction(1)}
    for _ in range(n):
        new = {}
        for s, p in pmf.items():
            for f in range(1, 7):
                new[s + f] = new.get(s + f, Fraction(0)) + p / 6
        pmf = new
    return pmf
for nn in (1, 5, 10, 20, 40):
    pmf = die_pmf(nn)
    thr = math.floor(3.5 * nn + math.sqrt(35 * nn / 12))
    p = sum(v for s, v in pmf.items() if s <= thr)
    print(f"n={nn} threshold={thr} P={float(p):.6f} gap={float(p) - PHI1:+.6f}")
rng = random.Random(2026)
path = [rng.randint(1, 6) for _ in range(10000)]
for nn in (10, 100, 1000, 10000):
    m = sum(path[:nn]) / nn
    print(f"path n={nn} mean={m:.4f} gap={m - 3.5:+.4f} cheb={(35 / 12) / (nn * 0.25):.4f}")
for nn in (5, 30, 200):
    r = random.Random(2026)
    hits = 0
    for _ in range(4000):
        tot = sum(r.randint(1, 6) for _ in range(nn))
        z = (tot / nn - 3.5) / (math.sqrt(35 / 12) / math.sqrt(nn))
        if z <= 1.0:
            hits += 1
    est = hits / 4000
    se = math.sqrt(est * (1 - est) / 4000)
    print(f"MC n={nn} hits={hits} est={est:.4f} se={se:.4f} gap={est - PHI1:+.4f}")
print("E2 check: 0.85525-0.841345 =", round(0.85525 - 0.841345, 6), " se(0.85525)=", round(math.sqrt(0.85525 * 0.14475 / 4000), 6))
print("E2 check: sqrt(0.8552*0.1448/4000)=", round(math.sqrt(0.8552 * 0.1448 / 4000), 6), " 0.0139/0.0056=", round(0.0139 / 0.0056, 3))
print("E1 L09: 35+sqrt(35*10/12)=", round(35 + math.sqrt(35 * 10 / 12), 4))
print("E3 L09 cheb at 10000:", round((35 / 12) / (10000 * 0.25), 7), " M1 7/60=", round(7 / 60, 6), " 35/48=", round(35 / 48, 6))
print("M3 L09 bound", (1) / (2 * 0.25))

print("== L10")
SQ3 = math.sqrt(3.0)
def t3_cdf(x):
    y = x / SQ3
    return 0.5 + (math.atan(y) + y / (1 + x * x / 3)) / math.pi
def t3_den(t):
    return 2 / (math.pi * SQ3) * (1 + t * t / 3) ** -2
N = 200000
h = 4.0 / N
mid = sum(t3_den(-2 + (k + 0.5) * h) for k in range(N)) * h
print("midpoint", f"{mid:.9f}", "closed", f"{t3_cdf(2) - t3_cdf(-2):.9f}")
def cauchy_tail(x):
    return 2 / math.pi * math.atan(1 / x)
def v_tail(x):
    y = x / SQ3
    return 2 / math.pi * (math.atan(1 / y) - y / (1 + y * y))
print("P(|C|>10)", round(cauchy_tail(10), 6), " P(|V|>10)", round(v_tail(10), 6), " erfc normal", f"{math.erfc(10 / math.sqrt(2)):.4e}")
print("ratio", f"{cauchy_tail(10) / math.erfc(10 / math.sqrt(2)):.4e}")
# numerical check of P(|V|>10) by midpoint integral of density on [10, 2000] (tail beyond 2000 ~ 1e-7)
tailnum = 2 * sum(t3_den(10 + (k + 0.5) * (1990 / 400000)) for k in range(400000)) * (1990 / 400000)
print("V tail midpoint on [10,2000] x2:", f"{tailnum:.6f}", "vs closed", f"{v_tail(10):.6f}")
for x in (10, 100, 1000):
    print("Part D x", x, round(x * cauchy_tail(x), 6), round(x ** 3 * v_tail(x), 6))
print("limits 2/pi", round(2 / math.pi, 6), " 4sqrt3/pi", round(4 * SQ3 / math.pi, 6))
print("arctan(0.1)", round(math.atan(0.1), 7), " P(|C|>1)", cauchy_tail(1))
print("F_V(sqrt3)", round(t3_cdf(SQ3), 6), " 3/4+1/(2pi)", round(0.75 + 1 / (2 * math.pi), 6))

def gauss_path(seed):
    r = random.Random(seed)
    return r
def running(draw, seed):
    r = random.Random(seed)
    tot = 0.0
    cnt = 0
    out = []
    for tgt in (10, 100, 1000, 10000):
        while cnt < tgt:
            tot += draw(r)
            cnt += 1
        out.append((tgt, tot / tgt))
    return out
def dn(r):
    return r.gauss(0.0, 1.0)
def dt(r):
    z = r.gauss(0.0, 1.0)
    w = 0.0
    for _ in range(3):
        g = r.gauss(0.0, 1.0)
        w += g * g
    return z / math.sqrt(w / 3)
def dc(r):
    return math.tan(math.pi * (r.random() - 0.5))
for name, d, s in (("normal", dn, 2026), ("t3", dt, 2027), ("cauchy", dc, 2028)):
    print(name, [(n_, round(m, 4)) for n_, m in running(d, s)])
for name, d, s, sig in (("normal", dn, 2026, 1.0), ("t3", dt, 2027, SQ3), ("cauchy", dc, 2028, None)):
    for nn in (10, 100):
        r = random.Random(s + 100 * nn)
        means = []
        for _ in range(400):
            means.append(sum(d(r) for _ in range(nn)) / nn)
        q1, _, q3 = statistics.quantiles(means, n=4, method="inclusive")
        out = f"{name} n={nn} IQR={q3 - q1:.4f}"
        if sig is not None:
            out += f" var(sqrt(n)Xbar/sigma)={statistics.variance([math.sqrt(nn) * m / sig for m in means]):.4f}"
        print(out)
print("exact IQR of one Cauchy", math.tan(math.pi / 4) - math.tan(-math.pi / 4))
print("L10 misc: 0.4116/0.1279 =", round(0.4116 / 0.1279, 3), " sqrt10=", round(math.sqrt(10), 4), " 1.8220/sqrt10=", round(1.8220 / math.sqrt(10), 4))
print("1/0.063451=", round(1 / 0.063451, 2))
print("L10 E3 var check: n*(3/n)/3 =", 1.0)
