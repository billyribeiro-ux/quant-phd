"""Independent recomputation of the printed numbers on L08, L09 and L10 (M4 slice c, round 3).

Uses only the standard library. Different code paths from the twins: integer-count convolution for the dice,
Simpson quadrature for the t(3) density, erfc for the normal tail, and direct arithmetic for the matrices.
"""
import math
from fractions import Fraction

print("== L09 Part A: exact P(S_n <= m) by integer-count convolution, m = floor(3.5 n + sqrt(35 n / 12))")
phi1 = 0.5 * (1.0 + math.erf(1.0 / math.sqrt(2.0)))
print(f"Phi(1) = {phi1:.10f}")
counts = [1]  # counts[s] = number of outcomes of the sum so far with sum s (offset 0 for zero dice)
for n in range(1, 41):
    new = [0] * (len(counts) + 6)
    for s, c in enumerate(counts):
        if c:
            for f in range(1, 7):
                new[s + f] += c
    counts = new
    # threshold: smallest-margin check
    raw = 3.5 * n + math.sqrt(35 * n / 12.0)
    if n in (1, 5, 10, 20, 40):
        m = math.floor(raw)
        # m is far from an integer boundary?  distance to next integer
        margin = min(raw - m, m + 1 - raw)
        total = sum(counts)
        assert total == 6 ** n
        p = Fraction(sum(counts[: m + 1]), 6 ** n)
        print(f"n={n:2d} threshold raw={raw:.6f} m={m} margin={margin:.6f} P={float(p):.6f} gap={float(p) - phi1:+.6f}")

print("\n== L09 Part C standard errors sqrt(p(1-p)/4000) at the printed estimates")
for p in (0.8552, 0.8548, 0.8518):
    print(f"p={p} se={math.sqrt(p * (1 - p) / 4000):.6f} gap={p - phi1:+.6f} gap/se={(p - phi1) / math.sqrt(p * (1 - p) / 4000):.3f}")

print("\n== L09 M1 / M2 / E1 / E3 / Chebyshev values")
print(f"M1 (35/12)/(100*0.25) = {(35/12)/25:.6f} = 7/60 = {7/60:.6f}; equal to Fraction: {Fraction(35,12)/25 == Fraction(7,60)}")
print(f"M2 (35/12)/4 = {(35/12)/4:.6f}; 35/48 = {35/48:.6f}")
print(f"E1 35 + sqrt(29.1667) = {35 + math.sqrt(35*10/12):.4f}")
print(f"E3 (35/12)/(10000*0.25) = {(35/12)/(10000*0.25):.7f}")
print(f"chebyshev n=10 eps=0.5: {(35/12)/(10*0.25):.4f}; n=100: {(35/12)/(100*0.25):.4f}; n=1000: {(35/12)/(1000*0.25):.4f}")
print(f"M3 bound: 1/(2*0.25) = {1/(2*0.25)}; exact P = {Fraction(1,2)}")

print("\n== L10 Part A: t(3) density integral versus closed form increment")
def f_t3(t):
    return 2.0 / (math.pi * math.sqrt(3.0)) * (1.0 + t * t / 3.0) ** -2
def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for k in range(1, n):
        s += (4 if k % 2 else 2) * f(a + k * h)
    return s * h / 3
def F_V(x):
    y = x / math.sqrt(3.0)
    return 0.5 + (math.atan(y) + y / (1.0 + x * x / 3.0)) / math.pi
simp = simpson(f_t3, -2.0, 2.0, 20000)
print(f"Simpson int_-2^2 f_V = {simp:.12f}; F_V(2)-F_V(-2) = {F_V(2.0) - F_V(-2.0):.12f}; diff = {abs(simp - (F_V(2.0) - F_V(-2.0))):.3e}")
print(f"F_V(sqrt3) = {F_V(math.sqrt(3)):.6f}; 3/4 + 1/(2 pi) = {0.75 + 1 / (2 * math.pi):.6f}")
# P(|V|>10) by direct tail quadrature: 2 * int_10^infinity f_V, substitution t = 10 / u on (0,1]
tail_quad = 2.0 * simpson(lambda u: f_t3(10.0 / u) * 10.0 / (u * u) if u > 0 else 0.0, 1e-12, 1.0, 200000)
print(f"P(|V|>10) by quadrature = {tail_quad:.8f}; closed form (2/pi)(atan(sqrt3/10) - 10 sqrt3/103) = "
      f"{(2 / math.pi) * (math.atan(math.sqrt(3) / 10) - 10 * math.sqrt(3) / 103):.8f}")
print(f"1 - F_V(10) doubled = {2 * (1 - F_V(10.0)):.8f}")
print(f"P(|Z|>10) = erfc(10/sqrt2) = {math.erfc(10 / math.sqrt(2)):.4e}")
pc = (2 / math.pi) * math.atan(0.1)
print(f"P(|C|>10) = (2/pi) atan(0.1) = {pc:.9f}; ratio to normal tail = {pc / math.erfc(10 / math.sqrt(2)):.4e}")
print(f"10 P(|C|>10) = {10 * pc:.8f}; 2/pi = {2 / math.pi:.8f}; limit gap 2/pi - 10P = {2 / math.pi - 10 * pc:.6f}")
for x in (10.0, 100.0, 1000.0):
    c_prod = x * (2 / math.pi) * math.atan(1 / x)
    v_prod = x ** 3 * 2 * ((math.atan(math.sqrt(3) / x) - (x * math.sqrt(3)) / (3 + x * x)) / math.pi)
    print(f"x={x:6.0f}: x P(|C|>x) = {c_prod:.8f}; x^3 P(|V|>x) = {v_prod:.8f}")
print(f"4 sqrt3/pi = {4 * math.sqrt(3) / math.pi:.8f}; 2/pi = {2 / math.pi:.8f}")
print(f"Cauchy one-draw IQR = tan(pi/4)-tan(-pi/4) = {math.tan(math.pi/4) - math.tan(-math.pi/4):.6f}")
print(f"normal IQR ratio 0.4116/0.1279 = {0.4116 / 0.1279:.4f}; sqrt10 = {math.sqrt(10):.4f}; 1.8220/sqrt10 = {1.8220 / math.sqrt(10):.4f}")
print(f"t3 standardized variances minus 1: {[round(v - 1, 4) for v in (1.0211, 0.9396, 0.8807, 1.1987)]}")
print(f"exact range of Part D 2/pi gap at 10: {2/math.pi - 0.634510:.6f}")

print("\n== L08 matrix checks")
A = [[2, 0], [1, 1]]
Q = [[0, -1], [1, 0]]
def mm(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def T(X):
    return [[X[j][i] for j in range(2)] for i in range(2)]
S = mm(A, T(A)); B = mm(A, Q); ATA = mm(T(A), A)
print("AA^T =", S, "| B=AQ =", B, "| BB^T =", mm(B, T(B)), "| A^TA =", ATA)
print("A^TA - Sigma =", [[ATA[i][j] - S[i][j] for j in range(2)] for i in range(2)])
xs = [[4.0073, 2.0187], [2.0187, 1.9936]]
ys = [[3.9070, 1.9385], [1.9385, 1.9636]]
g = lambda M, E: max(abs(M[i][j] - E[i][j]) for i in range(2) for j in range(2))
print(f"X gap from Sigma = {g(xs, S):.4f}; X gap from A^TA = {g(xs, ATA):.4f}; Y gap from Sigma = {g(ys, S):.4f}")
print("E1 entry gaps:", [round(abs(xs[0][0]-4),4), round(abs(xs[0][1]-2),4), round(abs(xs[1][1]-2),4)])
print("E3 Y entry gaps:", [round(abs(ys[0][0]-4),4), round(abs(ys[0][1]-2),4), round(abs(ys[1][1]-2),4)])
print(f"Part B mean deviations: 1-0.9770 = {1-0.9770:.4f}; -2-(-2.0055) = {-2 - (-2.0055):.4f}")
print(f"Y-sample (1,1) gap 4-3.9070 = {4 - 3.9070:.4f}")
print("L08 canon example: P(X+Y=0) >= 1/2 and the X' pair has P(X+X'=0)=0 (line has zero Lebesgue measure); no numerics needed")
