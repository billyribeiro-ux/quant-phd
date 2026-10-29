# Independent re-derivation of the L05 lab docstring claims over a grid of D (exact Fractions).
from fractions import Fraction as F
from itertools import combinations
S = F(100)
K = [F(80), F(90), F(100), F(110), F(120)]
def call(k, D):
    return max(S - D * k, F(0)) + max(F(100) - k, F(0)) / 10
def bounds_ok(k, c, p, D):
    dk = D * k
    return (0 <= c <= S) and (c >= max(S - dk, 0)) and (0 <= p <= dk) and (p >= max(dk - S, 0))
def convex_ok(cs, ks):
    for i, j, k in combinations(range(len(ks)), 3):
        k1, k2, k3 = ks[i], ks[j], ks[k]
        lam = F(k3 - k2, k3 - k1)
        if cs[j] > lam * cs[i] + (1 - lam) * cs[k]:
            return False
    return True
def check(D):
    cs = [call(k, D) for k in K]
    ps = [c - S + D * k for c, k in zip(cs, K)]  # parity-defined puts
    b = all(bounds_ok(k, c, p, D) for k, c, p in zip(K, cs, ps))
    return b, convex_ok(cs, K)
# claim 1: bounds hold for every D in [1/40, 1] on a fine grid; fail below 1/40
bad_hi = []
for n in range(1, 401):
    D = F(n, 400)  # 1/400 .. 1
    b, cv = check(D)
    if D >= F(1, 40) and not b:
        bad_hi.append(('bound fail above 1/40', str(D)))
    if not cv:
        bad_hi.append(('convexity fail', str(D)))
print('D in (0,1] grid, bound/convexity failures with D>=1/40 or convexity:', bad_hi[:10], len(bad_hi))
for D in [F(1, 40), F(1, 41), F(1, 100), F(9, 10), F(1)]:
    print(str(D), check(D))
# claim: at D=1/100 the 80 USD call exceeds spot
print('call80 at D=1/100 =', float(call(F(80), F(1, 100))), '> spot?', call(F(80), F(1, 100)) > S)
# claim: strict ">= 1/40" boundary, D=1/40 gives call80 = 100 exactly
print('call80 at D=1/40 =', call(F(80), F(1, 40)))
# claim: E1 second differences at 90,100,110 on the synthetic set in cents
cents = [int(call(k, F(9, 10)) * 100) for k in K]
print('synthetic calls cents', cents)
print('second diffs 90,100,110:', cents[0] - 2 * cents[1] + cents[2], cents[1] - 2 * cents[2] + cents[3], cents[2] - 2 * cents[3] + cents[4])
