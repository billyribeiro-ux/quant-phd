"""Re-check L09 identities and worked examples with exact Fractions (CS2 slice c round 1)."""
import random
from fractions import Fraction as F

rng = random.Random(3)
# Welford recursion exact over random rationals
ok = True
for _ in range(200):
    n = rng.randint(2, 12)
    xs = [F(rng.randint(-20, 20), rng.randint(1, 5)) for _ in range(n)]
    M, S = xs[0], F(0)
    for k in range(2, n + 1):
        x = xs[k - 1]
        Mn = M + (x - M) / k
        S = S + (x - M) * (x - Mn)
        M = Mn
    mean = sum(xs) / n
    ss = sum((x - mean) ** 2 for x in xs)
    ok &= (M == mean and S == ss)
print("Welford exact identity over 200 rational streams:", ok)

# R1 weighted analogue, exact
ok = True
for _ in range(200):
    n = rng.randint(2, 10)
    xs = [F(rng.randint(-9, 9)) for _ in range(n)]
    ws = [F(rng.randint(1, 6)) for _ in range(n)]
    W, M, S = ws[0], xs[0], F(0)
    for k in range(1, n):
        w, x = ws[k], xs[k]
        Wn = W + w
        d = x - M
        Mn = M + (w / Wn) * d
        S = S + w * (x - M) * (x - Mn)
        W, M = Wn, Mn
    mean = sum(w * x for w, x in zip(ws, xs)) / W
    ss = sum(w * (x - mean) ** 2 for w, x in zip(ws, xs))
    ok &= (M == mean and S == ss)
print("R1 weighted recursion exact over 200 streams:", ok)
print("R1 example (1,2) weights (1,3):", "M2 =", F(1) + F(3, 4), "S2 =", 3 * 1 * F(1, 4), "check sum =", 1 * (1 - F(7, 4)) ** 2 + 3 * (2 - F(7, 4)) ** 2)

# P3 merge formula exact
ok = True
for _ in range(200):
    a, b = rng.randint(1, 6), rng.randint(1, 6)
    A = [F(rng.randint(-9, 9)) for _ in range(a)]
    B = [F(rng.randint(-9, 9)) for _ in range(b)]
    mA, mB = sum(A) / a, sum(B) / b
    SA = sum((x - mA) ** 2 for x in A)
    SB = sum((x - mB) ** 2 for x in B)
    X = A + B
    m = sum(X) / (a + b)
    S = sum((x - m) ** 2 for x in X)
    ok &= (S == SA + SB + (mB - mA) ** 2 * F(a * b, a + b))
print("P3 merge identity exact:", ok)

# M3 zero-one stream and R3 population variance
xs = [0, 1, 0, 1]
print("M3 S4 =", F(1), "pop var =", F(1, 4))
print("R3 n=10 k=4 pop var =", F(4, 10) * F(6, 10), "S10 =", 4 * F(36, 100) + 6 * F(16, 100))
# M1
v = [2, 4, 4, 4, 5, 5, 7, 9]
m = F(sum(v), len(v))
S = sum((F(x) - m) ** 2 for x in v)
print("M1 mean", m, "S8", S, "sample", S / 7, float(S / 7), "pop", S / 8)
