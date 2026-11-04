# Independent re-derivation of the numbers printed in SC1 L02 and L03 prose (verifier round 6).
# Written from the definitions, not from the lab code. Run with: python3 -I recompute.py
import math
import random
from fractions import Fraction

SEED = 20260101
LEVELS = 8

rng = random.Random(SEED)
xi0 = rng.gauss(0.0, 1.0)
xi = {}
for m in range(1, LEVELS + 1):
    for j in range(1, 2 ** (m - 1) + 1):
        xi[(m, j)] = rng.gauss(0.0, 1.0)

# Level-1 supremum: Lambda_{1,1} peaks at 1 at t=1/2; scale 2^{-(1+1)/2} = 1/2
sup1 = abs(xi[(1, 1)]) * 0.5
print("L02 level-1 unrounded sup:", repr(sup1), "rounded 6dp:", f"{sup1:.6f}")
print("L02 twice unrounded (=|xi_11|):", f"{2*sup1:.9f}", "rounded 6dp:", f"{2*sup1:.6f}")
print("L02 doubling printed 0.116589 gives:", f"{2*0.116589:.6f}")
print("L02 sqrt(4 log 2):", f"{math.sqrt(4*math.log(2)):.7f}", " half:", f"{math.sqrt(4*math.log(2))/2:.7f}")
print("L02 bound lambda_1 2^-1 =", f"{math.sqrt(4*1*math.log(2))*2**(-1):.7f}")

def hat(m, j, t):
    c = (2 * j - 1) / 2.0 ** m
    return max(0.0, 1.0 - 2.0 ** m * abs(t - c))

def sigma(M, t):
    s = xi0 * t
    for m in range(1, M + 1):
        sc = 2 ** (-(m + 1) / 2)
        for j in range(1, 2 ** (m - 1) + 1):
            s += xi[(m, j)] * sc * hat(m, j, t)
    return s

grid = [i / 2 ** 10 for i in range(2 ** 10 + 1)]
tail = max(abs(sigma(8, t) - sigma(4, t)) for t in grid)
bsum = sum(math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(5, 9))
print("L02 grid sup |Sigma_8 - Sigma_4| =", f"{tail:.6f}", "(prose 0.348139)")
print("L02 sum of bounds levels 5..8 =", f"{bsum:.6f}", "(prose 1.309399)")

# Lab-independent check of Lemma 2.2(c): hats vanish at dyadic points of coarser depth, exactly
bad = 0
cases = 0
for n in range(5):
    for k in range(2 ** n + 1):
        t = k / 2 ** n
        for m in range(n + 1, LEVELS + 1):
            for j in range(1, 2 ** (m - 1) + 1):
                cases += 1
                bad += hat(m, j, t) != 0.0
print("L02 Lemma 2.2(c) exact-zero check: cases", cases, "nonzero", bad)

# L03: population SE H*sqrt(2/N)/20 versus printed SE; gap = printed/pop - 1
printed = {
    (1, 1): (0.0718, 0.9994), (1, 2): (0.0538, 1.1288), (1, 4): (0.0373, 1.0436), (1, 8): (0.0249, 0.9815),
    (1, 16): (0.0174, 0.9965), (1, 32): (0.0131, 1.0034), (1, 64): (0.0092, 1.0031), (1, 128): (0.0063, 1.0116),
    (2, 1): (0.1601, 2.1346), (2, 2): (0.0934, 1.9018), (2, 4): (0.0772, 2.0417), (2, 8): (0.0475, 1.9564),
    (2, 16): (0.0364, 2.0463), (2, 32): (0.0256, 2.0134), (2, 64): (0.0190, 2.0048), (2, 128): (0.0125, 1.9948),
}
worst = None
for (H, N), (se, mean) in printed.items():
    pop = H * math.sqrt(2 / N) / 20
    gap = se / pop - 1
    z = (mean - H) / se
    print(f"L03 H={H} N={N:3d} pop_se={pop:.6f} printed_se={se:.4f} gap={100*gap:+.2f}% z={z:+.3f}")
    if worst is None or abs(gap) > abs(worst[1]):
        worst = ((H, N), gap)
print("L03 largest |gap| at", worst[0], f"{100*worst[1]:.2f}%")
print("L03 max |z| over printed rows:", f"{max(abs((m-H)/s) for (H,N),(s,m) in printed.items() for H in [H]):.3f}")
