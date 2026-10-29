"""Independent re-derivation of the numbers printed on L08-L10 (verifier M4-c round 6)."""
import math
from fractions import Fraction
from statistics import NormalDist

# --- L09: exact P(S_n <= m) by a different method: count outcomes with integer convolution via combinations
def count_sum_le(n, m):
    # number of n-tuples of faces 1..6 with sum <= m, via dynamic programming on integer counts
    dp = {0: 1}
    for _ in range(n):
        nd = {}
        for s, c in dp.items():
            for f in range(1, 7):
                nd[s + f] = nd.get(s + f, 0) + c
        dp = nd
    return sum(c for s, c in dp.items() if s <= m)

phi1 = NormalDist().cdf(1.0)
print("L09 Phi(1) =", round(phi1, 6))
for n in (1, 5, 10, 20, 40):
    m = math.floor(3.5 * n + math.sqrt(35 * n / 12))
    p = Fraction(count_sum_le(n, m), 6 ** n)
    print("L09 A n=%d m=%d P=%.6f gap=%+.6f" % (n, m, float(p), float(p) - phi1))
# threshold check: S_n <= threshold iff Z_n <= 1, at n=10 the real threshold is 40.4006
print("L09 n=10 real threshold", 35 + math.sqrt(35 * 10 / 12))
print("L09 SE check", math.sqrt(0.8552 * 0.1448 / 4000), 0.013855 / math.sqrt(0.8552 * 0.1448 / 4000))
print("L09 M1 bound", (35 / 12) / (100 * 0.25), "E3 bound", (35 / 12) / (10000 * 0.25))
print("L09 M2", (35 / 12) / 4)

# --- L10: tails by numerical integration of the t(3) density (independent of closed form)
def f_t3(t):
    return 2 / (math.pi * math.sqrt(3)) * (1 + t * t / 3) ** -2

def tail_numeric(x, upper=2e6, steps=2_000_000):
    # integral of density over [x, upper] by composite Simpson on log-spaced substitution t = x*exp(u)
    a, b = math.log(x), math.log(upper)
    h = (b - a) / steps
    s = 0.0
    for k in range(steps + 1):
        u = a + k * h
        t = math.exp(u)
        w = 1 if k in (0, steps) else (4 if k % 2 else 2)
        s += w * f_t3(t) * t
    return 2 * s * h / 3  # two-sided

print("L10 P(|C|>10) closed", 2 / math.pi * math.atan(0.1))
print("L10 P(|V|>10) numeric (tail to 2e6 approx)", tail_numeric(10.0))
print("L10 P(|V|>10) closed", 2 / math.pi * (math.atan(math.sqrt(3) / 10) - 10 * math.sqrt(3) / (3 + 100)))
print("L10 4sqrt3/pi", 4 * math.sqrt(3) / math.pi, " 2/pi", 2 / math.pi)
for x in (10.0, 100.0, 1000.0):
    print("L10 D x=%g  xC=%.6f  x^3V=%.6f" % (x, x * 2 / math.pi * math.atan(1 / x), x ** 3 * 2 / math.pi * (math.atan(math.sqrt(3) / x) - (x * math.sqrt(3)) / (3 + x * x))))
print("L10 normal tail", math.erfc(10 / math.sqrt(2)), "ratio", (2 / math.pi * math.atan(0.1)) / math.erfc(10 / math.sqrt(2)))
print("L10 F_V(sqrt3) closed", 0.75 + 1 / (2 * math.pi))
print("L10 1/0.063451", 1 / 0.063451)
print("L10 IQR ratio normal", 0.4116 / 0.1279, math.sqrt(10))
print("L10 E1 2/pi-0.634510", 2 / math.pi - 0.634510)
print("L10 Cauchy sqrt-n scaled", 1.8220 / math.sqrt(10))
print("L10 t3 variance check", 3 / 1)

# --- L08: exact integer checks
A = [[2, 0], [1, 1]]
At = [[A[j][i] for j in range(2)] for i in range(2)]
def mm(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
AAt = mm(A, At); AtA = mm(At, A)
Q = [[0, -1], [1, 0]]
B = mm(A, Q)
print("L08 AAt", AAt, "AtA", AtA, "B", B, "BBt", mm(B, [[B[j][i] for j in range(2)] for i in range(2)]))
print("L08 AtA-Sigma", [[AtA[i][j] - AAt[i][j] for j in range(2)] for i in range(2)])
print("L08 E2 exact gap", max(abs(AtA[i][j] - AAt[i][j]) for i in range(2) for j in range(2)))
print("L08 M1 AAt", mm([[1, 1], [0, 2]], [[1, 0], [1, 2]]))
print("L08 R1 check: L=[[2,0],[1,1]] LLt", mm([[2, 0], [1, 1]], [[2, 1], [0, 1]]))
print("L08 E1 gaps", abs(4.0073 - 4), abs(2.0187 - 2), abs(1.9936 - 2))
print("L08 Y gaps", abs(3.9070 - 4), abs(1.9385 - 2), abs(1.9636 - 2))
