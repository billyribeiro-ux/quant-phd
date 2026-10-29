"""Round 7 verifier: exact-rational checks of L09 algebra (R1 weighted update, P3 merge, Lemma 1.3, R3, M-problems)."""
import random
from fractions import Fraction as F

rng = random.Random(99)
bad = 0
for trial in range(300):
    n = rng.randint(1, 12)
    xs = [F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(n)]
    ws = [F(rng.randint(1, 9), rng.randint(1, 4)) for _ in range(n)]
    W = ws[0]; M = xs[0]; S = F(0)
    for k in range(1, n):
        Wn = W + ws[k]
        d = xs[k] - M
        Mn = M + ws[k] / Wn * d
        S = S + ws[k] * (xs[k] - M) * (xs[k] - Mn)
        W, M = Wn, Mn
    mean = sum(w * x for w, x in zip(ws, xs)) / sum(ws)
    SS = sum(w * (x - mean) ** 2 for w, x in zip(ws, xs))
    if M != mean or S != SS:
        bad += 1
print("R1 weighted recursion mismatches over 300 streams:", bad)
# R1 example
print("R1 example M2, S2:", F(1) + F(3, 4) * 1, 0 + 3 * (2 - F(7, 4)) * (2 - F(7, 4)) + 0 * 0 if False else None)
M2 = F(1) + F(3, 4) * (2 - 1)
S2 = F(0) + 3 * (2 - 1) * (2 - M2)
print("R1 example: M2 =", M2, " S2 =", S2, " check sum w(x-M)^2 =", 1 * (1 - M2) ** 2 + 3 * (2 - M2) ** 2)
# P3 merge formula
bad = 0
for trial in range(300):
    a = rng.randint(1, 8); b = rng.randint(1, 8)
    A = [F(rng.randint(-9, 9)) for _ in range(a)]
    B = [F(rng.randint(-9, 9)) for _ in range(b)]
    mA = sum(A) / a; mB = sum(B) / b
    SA = sum((x - mA) ** 2 for x in A); SB = sum((x - mB) ** 2 for x in B)
    allv = A + B
    m = sum(allv) / (a + b)
    S = sum((x - m) ** 2 for x in allv)
    if S != SA + SB + (mB - mA) ** 2 * F(a * b, a + b):
        bad += 1
print("P3 merge formula mismatches:", bad)
# M3 zero-one stream, R3 closed form
print("R3 n=10 k=4 population var:", F(4 * 6 + 0, 1) / 10 if False else F(4, 10) * (1 - F(4, 10)))
# M1
vals = [2, 4, 4, 4, 5, 5, 7, 9]
mu = F(sum(vals), len(vals)); S8 = sum((F(v) - mu) ** 2 for v in vals)
print("M1 mean", mu, "S8", S8, "sample", float(S8 / 7), "pop", S8 / 8)
# M2 / M3 / P1 / P2 small checks
def welford(xs):
    M = F(xs[0]); S = F(0)
    out = [(M, S)]
    for n in range(2, len(xs) + 1):
        x = F(xs[n - 1])
        Mn = M + (x - M) / n
        S = S + (x - M) * (x - Mn)
        M = Mn
        out.append((M, S))
    return out
print("M2 states 1,2,3:", welford([1, 2, 3]))
print("M3 states 0,1,0,1:", welford([0, 1, 0, 1]))
print("P2 constant stream S:", welford([5, 5, 5])[-1])
# P1 n=2
x1, x2 = F(3), F(-2)
print("P1 S2 == (x1-x2)^2/2 ?", welford([3, -2])[-1][1] == (x1 - x2) ** 2 / 2)
# Welford exact check on random streams
bad = 0
for trial in range(200):
    xs = [rng.randint(-50, 50) for _ in range(rng.randint(1, 30))]
    n = len(xs)
    mu = F(sum(xs), n)
    ss = sum((F(x) - mu) ** 2 for x in xs)
    if welford(xs)[-1][1] != ss or welford(xs)[-1][0] != mu:
        bad += 1
print("Theorem 2.2 exact-rational mismatches (200 streams):", bad)
