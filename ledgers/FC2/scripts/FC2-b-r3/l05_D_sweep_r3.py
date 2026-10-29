"""FC2-b round 3: independent sweep of the L05 Lab 1 synthetic set over the discount factor D.

Recomputes the lab's synthetic calls/puts from its formula, C(K) = max(S - D K, 0) + max(A - K, 0)/10, P = C - S + D K,
and reports for which D every model-free bound (Theorem 2.2) and every convexity triple holds, on the lab's grid.
"""
from fractions import Fraction
from itertools import combinations

S = Fraction(100)
A = Fraction(100)
STRIKES = [Fraction(k) for k in (80, 90, 100, 110, 120)]


def call(D, K):
    return max(S - D * K, Fraction(0)) + max(A - K, Fraction(0)) / 10


def put(D, K):
    return call(D, K) - S + D * K


def bounds_ok(D):
    bad = []
    for K in STRIKES:
        c, p = call(D, K), put(D, K)
        if not (0 <= c <= S):
            bad.append(("C<=S or C>=0", K))
        if c < max(S - D * K, 0):
            bad.append(("C>=S-DK", K))
        if not (0 <= p <= D * K):
            bad.append(("0<=P<=DK", K))
        if p < max(D * K - S, 0):
            bad.append(("P>=DK-S", K))
    return bad


def convex_ok(D):
    cs = [call(D, K) for K in STRIKES]
    for i, j, k in combinations(range(len(STRIKES)), 3):
        k1, k2, k3 = STRIKES[i], STRIKES[j], STRIKES[k]
        lam = (k3 - k2) / (k3 - k1)
        if cs[j] > lam * cs[i] + (1 - lam) * cs[k]:
            return False
    return True


print("D=1/100 bound violations:", bounds_ok(Fraction(1, 100))[:3], "C(80)=", float(call(Fraction(1, 100), Fraction(80))))
print("D=1/40 bound violations:", bounds_ok(Fraction(1, 40)))
print("D=9/10 bound violations:", bounds_ok(Fraction(9, 10)), "convex:", convex_ok(Fraction(9, 10)))
first_ok = None
fail_above = []
for n in range(1, 4001):
    D = Fraction(n, 1000)  # D from 0.001 to 4.0
    ok = not bounds_ok(D)
    if ok and first_ok is None:
        first_ok = D
    if not ok and first_ok is not None:
        fail_above.append(D)
print("smallest D in grid (step 1/1000) where all bounds hold:", first_ok)
print("grid D values above that where a bound fails (first 10):", [str(x) for x in fail_above[:10]], "count", len(fail_above))
print("bounds fail at D just below 1/40? D=39/1000:", bool(bounds_ok(Fraction(39, 1000))))
print("convexity holds for every swept D:", all(convex_ok(Fraction(n, 1000)) for n in range(1, 4001)))
