"""Numeric checks of the algebra on L09 (R1 weighted update, P3 block merge, Theorem 2.1 step) and L10 (R3 max
expiry count by exhaustive search over small series; Corollary 2.5(c) worst single push).

Run: python3 -I -W error ledgers/CS2/scripts/CS2-c-r4/algebra_r4.py
"""
import itertools
import random
from fractions import Fraction

# R1: weighted Welford with exact fractions, random positive weights and values
bad = 0
for seed in range(300):
    r = random.Random(seed)
    n = r.randint(1, 12)
    xs = [Fraction(r.randint(-20, 20), r.randint(1, 5)) for _ in range(n)]
    ws = [Fraction(r.randint(1, 9), r.randint(1, 4)) for _ in range(n)]
    W = ws[0]
    M = xs[0]
    S = Fraction(0)
    for k in range(1, n):
        W_new = W + ws[k]
        d = xs[k] - M
        M_new = M + ws[k] / W_new * d
        S = S + ws[k] * (xs[k] - M) * (xs[k] - M_new)
        W, M = W_new, M_new
    mean = sum(w * x for w, x in zip(ws, xs)) / sum(ws)
    SS = sum(w * (x - mean) ** 2 for w, x in zip(ws, xs))
    if M != mean or S != SS:
        bad += 1
print("R1 weighted update failures:", bad, "of 300")
print("R1 worked example x=(1,2), w=(1,3):", end=" ")
W1, M1, S1 = Fraction(1), Fraction(1), Fraction(0)
W2 = W1 + 3
M2 = M1 + Fraction(3) / W2 * (2 - M1)
S2 = S1 + 3 * (2 - M1) * (2 - M2)
print("M2 =", M2, "S2 =", S2, "check sum w(x-M2)^2 =", 1 * (1 - M2) ** 2 + 3 * (2 - M2) ** 2)

# P3: block merge formula S = S_A + S_B + (m_B - m_A)^2 a b / (a + b), exact
bad = 0
for seed in range(200):
    r = random.Random(100 + seed)
    A = [Fraction(r.randint(-9, 9)) for _ in range(r.randint(1, 6))]
    B = [Fraction(r.randint(-9, 9)) for _ in range(r.randint(1, 6))]
    a, b = len(A), len(B)
    mA, mB = sum(A) / a, sum(B) / b
    SA = sum((x - mA) ** 2 for x in A)
    SB = sum((x - mB) ** 2 for x in B)
    allx = A + B
    m = sum(allx) / (a + b)
    S = sum((x - m) ** 2 for x in allx)
    if S != SA + SB + (mB - mA) ** 2 * a * b / (a + b):
        bad += 1
print("P3 block-merge failures:", bad, "of 200")

# R3 (L10): exhaustive maximum number of step-(3) expiries over all series with values in {0,1,2}, n <= 6
def expiries(series, w):
    dq = []
    total = 0
    for i, x in enumerate(series):
        while dq and series[dq[-1]] >= x:
            dq.pop()
        dq.append(i)
        while dq and dq[0] <= i - w:
            dq.pop(0)
            total += 1
    return total

ok = True
for n in range(1, 7):
    for w in range(1, n + 1):
        best = max(expiries(list(s), w) for s in itertools.product((0, 1, 2), repeat=n))
        if best != n - w:
            # the exhaustive maximum over this alphabet may be below n-w; report, the claim needs the increasing series
            print("R3 exhaustive max over {0,1,2}, n", n, "w", w, "=", best, "(bound n-w =", n - w, ")")
        inc = expiries(list(range(n)), w)
        if inc != n - w:
            ok = False
            print("R3 increasing series mismatch", n, w, inc)
print("R3 increasing series attains n-w for all n<=6, w<=n:", ok)

# Corollary 2.5(c) example: x0<...<x_{w-1} then a value below all; count removals at insertion w
for w in range(1, 8):
    series = list(range(1, w + 1)) + [0]
    dq = []
    removed_last = 0
    for i, x in enumerate(series):
        rem = 0
        while dq and series[dq[-1]] >= x:
            dq.pop()
            rem += 1
        dq.append(i)
        while dq and dq[0] <= i - w:
            dq.pop(0)
            rem += 1
        removed_last = rem
    print("Cor2.5(c) w", w, "removals at the last insertion", removed_last)
