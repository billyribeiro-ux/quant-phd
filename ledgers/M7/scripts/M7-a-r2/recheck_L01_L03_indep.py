"""Independent recomputation of the numbers on the M7 slice pages (M7-a, round 2). Standard library only."""
from fractions import Fraction as F
from itertools import product
import math

# ---- L01: grid counts, written independently of the lab twin
pts = list(product(range(-2, 3), repeat=2))
ws = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
def form(Q, x, y=None):
    v = x if y is None else y
    return sum(Q[i][j] * x[i] * x[j] for i in range(2) for j in range(2))
Q1 = [[2, 1], [1, 2]]
Q2 = [[1, 2], [2, 1]]
def qf(Q, v):
    return sum(F(Q[i][j]) * v[i] * v[j] for i in range(2) for j in range(2))
def chord_ok(Q, x, y, w):
    z = (w * x[0] + (1 - w) * y[0], w * x[1] + (1 - w) * y[1])
    return qf(Q, z) <= w * qf(Q, x) + (1 - w) * qf(Q, y)
cases = [(x, y, w) for x in pts for y in pts for w in ws]
print("L01 cases", len(cases))
print("L01 Q1 chord holds", sum(chord_ok(Q1, x, y, w) for x, y, w in cases))
print("L01 Q2 chord holds", sum(chord_ok(Q2, x, y, w) for x, y, w in cases))
neg = sum(1 for x, y in product(pts, repeat=2) if qf(Q2, (F(x[0]-y[0]), F(x[1]-y[1]))) < 0)
print("L01 Q2 negative ordered pairs", neg, "3*neg", 3 * neg)
# example x=(1,0), y=(0,1), w=1/2 for Q2
mid = qf(Q2, (F(1, 2), F(1, 2)))
chord = F(1, 2) * qf(Q2, (F(1), F(0))) + F(1, 2) * qf(Q2, (F(0), F(1)))
print("L01 example mid", mid, "chord", chord, "gap", chord - mid, "d'Q2d", qf(Q2, (F(1), F(-1))))
# closed-form eigenvalues of 2Q (trace/det check)
for name, Q in (("Q1", Q1), ("Q2", Q2)):
    H = [[2 * Q[i][j] for j in range(2)] for i in range(2)]
    tr = H[0][0] + H[1][1]
    det = H[0][0] * H[1][1] - H[0][1] * H[1][0]
    disc = tr * tr - 4 * det
    print("L01", name, "trace", tr, "det", det, "disc", disc, "sqrt", math.isqrt(disc))
# quiz / R3 / P1 / P3 / M3
print("L01 M3 q(1,1)", qf(Q1, (F(1), F(1))), "gap x=(1,1), y=(-1,-1)", F(1,2)*6 + F(1,2)*6 - qf(Q1, (F(0), F(0))), "(2,2)Q1(2,2)", qf(Q1, (F(2), F(2))))
print("L01 quiz Q2 at (1,-1)", qf(Q2, (F(1), F(-1))))
print("L01 R1 check", [[F(1), F(1)], [F(-1), F(1)]])
print("L01 union-disks midpoint of (-2,0),(2,0)", ((-2 + 2) / 2, 0), "dist to (3,0):", abs(0 - 3), "dist to (-3,0):", abs(0 + 3))

# ---- L02
def lcg(seed, count):
    st = seed
    out = []
    for _ in range(count):
        st = (1103515245 * st + 12345) % 2**31
        out.append(st % 7 - 3)
    return out
ent = lcg(1, 9)
A = [ent[0:3], ent[3:6], ent[6:9]]
S = [[F(sum(A[k][i] * A[k][j] for k in range(3)) + (1 if i == j else 0)) for j in range(3)] for i in range(3)]
print("L02 entries", ent)
print("L02 Sigma", [[int(x) for x in r] for r in S])
def solve3(M, b):
    # Cramer's rule with Fractions
    def det(m):
        return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))
    D = det(M)
    out = []
    for c in range(3):
        Mc = [[b[r] if k == c else M[r][k] for k in range(3)] for r in range(3)]
        out.append(det(Mc) / D)
    return out
u = solve3(S, [F(1)] * 3)
s = sum(u)
lam = 1 / s
w = [lam * x for x in u]
print("L02 s", s, "lambda", lam, "w", w, "budget", sum(w))
Sw = [sum(S[i][j] * w[j] for j in range(3)) for i in range(3)]
print("L02 Sw - lam1", [Sw[i] - lam for i in range(3)])
fw = sum(w[i] * Sw[i] for i in range(3)) / 2
print("L02 f(w)", fw, "lam/2", lam / 2, "lam as decimal", float(lam), "round4", round(float(lam), 4))
ok_id = 0; ok_nn = 0; n = 0
dirs = [(1, -1, 0), (0, 1, -1), (1, 0, -1), (2, -1, -1), (-1, 2, -1), (1, 1, -2)]
steps = [F(-1, 2), F(1, 2), F(1), F(-1), F(2), F(3, 2)]
for d in dirs:
    d = [F(c) for c in d]
    dsd = sum(d[i] * S[i][j] * d[j] for i in range(3) for j in range(3))
    for t in steps:
        m = [w[i] + t * d[i] for i in range(3)]
        mm = sum(m[i] * S[i][j] * m[j] for i in range(3) for j in range(3)) / 2
        gap = mm - fw
        n += 1
        ok_id += gap == t * t * dsd / 2
        ok_nn += gap >= 0
print("L02 identity", ok_id, "of", n, "nonneg", ok_nn)
# M2 diag(1,2)
D = [[F(1), F(0), F(0)], [F(0), F(0)]]  # placeholder
Sd = [[F(1), F(0)], [F(0), F(2)]]
ud = [F(1), F(1, 2)]; sd = sum(ud); ld = 1 / sd; wd = [ld * x for x in ud]
fd = (wd[0] ** 2 * 1 + wd[1] ** 2 * 2) / 2
print("L02 M2", ld, wd, fd)
dd = [F(1), F(-1)]
mv = [wd[0] + dd[0], wd[1] + dd[1]]
inc = (mv[0] ** 2 + 2 * mv[1] ** 2) / 2 - fd
print("L02 M3 increase", inc, "formula", F(1, 2) * (1 * 1 + 2 * 1))
print("L02 E1 first coord", 4 * F(47, 55) + 2 * F(17, 55) + 5 * F(-9, 55))
print("L02 R3 minimum value check c=1: 1/(2s)", 1 / (2 * s), "lam", lam)
print("L02 M1 ", "x=y=1/2 f", F(1, 2) ** 2 * 2)
print("L02 quiz 1x1 A=2: A'A+1", 2 * 2 + 1)
print("L02 quiz diag(5,-1) trace", 5 - 1)

# ---- L03
def fobj(w, mu):
    Sg = [[2, 1], [1, 2]]
    q = sum(Sg[i][j] * w[i] * w[j] for i in range(2) for j in range(2))
    return F(1, 2) * q - (mu[0] * w[0] + mu[1] * w[1])
def grad(w, mu):
    Sg = [[2, 1], [1, 2]]
    return [Sg[0][0] * w[0] + Sg[0][1] * w[1] - mu[0], Sg[1][0] * w[0] + Sg[1][1] * w[1] - mu[1]]
muA = (F(3, 2), F(1, 5)); wA = (F(1), F(0)); nuA = F(-1, 2); lamA = (F(0), F(3, 10))
gA = grad(wA, muA)
print("L03 A stat", gA[0] + nuA - lamA[0], gA[1] + nuA - lamA[1], "obj", fobj(wA, muA))
muB = (F(1), F(1)); wB = (F(1, 2), F(1, 2)); nuB = F(-1, 2)
gB = grad(wB, muB)
print("L03 B stat", gB[0] + nuB, gB[1] + nuB, "obj", fobj(wB, muB))
gW = grad((F(1, 2), F(1, 2)), muA)
print("L03 off-solution stat with active mult", gW[0] + nuA - lamA[0], gW[1] + nuA - (F(3, 10)), "flipped dual", -(-F(3, 10)))
grid = [F(k, 100) for k in range(101)]
vals = [(fobj((g, 1 - g), muA), g) for g in grid]
print("L03 A grid min", min(vals)[0], "at", min(vals)[1], "count", len(vals))
vals = [(fobj((g, 1 - g), muB), g) for g in grid]
print("L03 B grid min", min(vals)[0], "at", min(vals)[1])
# Remark 4.3
Sinv = [[F(2, 3), F(-1, 3)], [F(-1, 3), F(2, 3)]]
wu = [Sinv[0][0] * muA[0] + Sinv[0][1] * muA[1], Sinv[1][0] * muA[0] + Sinv[1][1] * muA[1]]
print("L03 Remark 4.3 w", wu, "sum", wu[0] + wu[1])
# M2 inactive
print("L03 M2 f(3/5,2/5)", fobj((F(3, 5), F(2, 5)), muB), "vs -1/4", fobj((F(3, 5), F(2, 5)), muB) - F(-1, 4))
# M3 active at (1/2,1/2)
print("L03 M3 objective", fobj((F(1, 2), F(1, 2)), muA), "grad", grad((F(1, 2), F(1, 2)), muA))
# P3: lower bound at feasible w2 gives -1/2 + 3/10 w2
for w2 in [F(0), F(1, 3), F(1, 2), F(1)]:
    wv = (1 - w2, w2)
    print("L03 P3 check w2", w2, fobj(wv, muA), ">= ", F(-1, 2) + F(3, 10) * w2, fobj(wv, muA) >= F(-1, 2) + F(3, 10) * w2)
print("L03 E1 norm", math.sqrt(0.5), round(math.sqrt(0.5), 4))
print("L03 Ex2.3 midpoint", (F(-1,2))**3, "avg", F(1,2)*F(-1) + F(1,2)*F(0))
