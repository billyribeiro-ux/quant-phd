"""Independent recomputation of the numbers printed or quoted in SC1 L01-L03 (verifier round 1).

Written from the page text, not from the lab twins. Run as: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r1/recompute_numbers.py
"""

import math
from fractions import Fraction

print("== L01 exact checks")
ok = 0
for t in (Fraction(1), Fraction(3, 4), Fraction(5, 2)):
    for n in range(5):
        ok += sum(Fraction(t, 2**n) for _ in range(2**n)) == t
print("dyadic sums equal t:", ok, "of 15")
ok = 0
for i in range(9):
    for j in range(9):
        ok += min(i, j) * Fraction(1, 8) == min(Fraction(i, 8), Fraction(j, 8))
print("grid covariance equals min:", ok, "of 81")
print("Cov(B_1/4, B_5/8) =", Fraction(2, 8), "; min =", min(Fraction(1, 4), Fraction(5, 8)))
print("E1: piece length", Fraction(3, 4) / 16, "; 16 * 3/64 =", 16 * Fraction(3, 64))
print("M3: 9*1 + 2 - 6*min(1,2) =", 9 * 1 + 2 - 6 * 1)
print("Quiz: 1/sqrt(1/100) =", 1 / math.sqrt(1 / 100))

print("== L02 numbers")
lam1 = math.sqrt(4 * math.log(2))
print("sqrt(4 log 2) =", round(lam1, 6), "; half =", round(lam1 / 2, 6), "(page 0.832555)")
print("2 * 0.116589 =", 2 * 0.116589)
cases = sum(2**n + 1 for n in range(5))
pairs = sum((2**n + 1) * (9 - n) for n in range(5))
print("dyadic points over depths 0-4 counted with repetition:", cases, "; distinct points:", 2**4 + 1)
print("comparisons (per depth point count x levels n..8):", pairs)
print("per-depth terms:", [(2**n + 1) * (9 - n) for n in range(5)])
print("bounds m=1..8 (lambda_m 2^{-(m+1)/2}):")
for m in range(1, 9):
    b = math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)
    print(f"  m={m} bound={b:.6f}")
print("sum of bounds 5..8:", round(sum(math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(5, 9)), 6))
print("sum_m M_m check: sqrt(2 log 2) sqrt(m) 2^{-m/2} at m=1:", round(math.sqrt(2 * math.log(2)) * 1 * 2 ** (-0.5), 6))
print("depth-3 dyadic points:", 2**3 + 1)
print("sum over m>=1 of 2^{-m} =", sum(2.0**-m for m in range(1, 200)))
print("sum m r^m check r=2^-1/2 vs r/(1-r)^2:", round(sum(m * (2**-0.5) ** m for m in range(1, 400)), 9),
      round((2**-0.5) / (1 - 2**-0.5) ** 2, 9))

print("== L03 numbers")
printed = {
    1: [(1, 0.9994, 0.0718, -0.01), (2, 1.1288, 0.0538, 2.39), (4, 1.0436, 0.0373, 1.17), (8, 0.9815, 0.0249, -0.74),
        (16, 0.9965, 0.0174, -0.20), (32, 1.0034, 0.0131, 0.26), (64, 1.0031, 0.0092, 0.33), (128, 1.0116, 0.0063, 1.84)],
    2: [(1, 2.1346, 0.1601, 0.84), (2, 1.9018, 0.0934, -1.05), (4, 2.0417, 0.0772, 0.54), (8, 1.9564, 0.0475, -0.92),
        (16, 2.0463, 0.0364, 1.27), (32, 2.0134, 0.0256, 0.52), (64, 2.0048, 0.0190, 0.25), (128, 1.9948, 0.0125, -0.42)],
}
max_abs_z = 0.0
worst = (0, 0, 0.0)
for H, rows in printed.items():
    for N, mean, se_printed, z_printed in rows:
        pop = H * math.sqrt(2 / N) / 20
        z_recalc = (mean - H) / se_printed
        max_abs_z = max(max_abs_z, abs(z_printed))
        rel = (se_printed - pop) / pop
        if abs(rel) > abs(worst[2]):
            worst = (H, N, rel)
        print(f"  H={H} N={N:3d} pop_se={pop:.6f} printed_se={se_printed:.4f} rel_diff={rel:+.3f} "
              f"z_printed={z_printed:+.2f} z_recalc={z_recalc:+.2f}")
print("max |z| printed:", max_abs_z, "(page: 2.39 at H=1,N=2; no other above 1.84)")
print("largest relative SE deviation from H*sqrt(2/N)/20:", worst)
print("pop SE H=1,N=1:", round(math.sqrt(2) / 20, 4), "; H=2,N=128:", 2 * (1 / 8) / 20)


def t2(H, N):
    pts = [Fraction(H) * j / N for j in range(N + 1)]
    return sum(((b * b - a * a) ** 2 for a, b in zip(pts, pts[1:])), Fraction(0))


def closed(H, N):
    return Fraction(H) ** 4 * (4 * N * N - 1) / (3 * N**3)


print("t^2 sums equal closed form for H=1,2 and N=1..128 powers of 2:",
      all(t2(H, 2**k) == closed(H, 2**k) for H in (1, 2) for k in range(8)))
print("H=1 N=2:", float(t2(1, 2)), "; H=2 N=8:", float(t2(2, 8)), "=", t2(2, 8), "; H=2 N=128:", float(t2(2, 128)))
print("E2 16*255/1536 =", Fraction(16 * 255, 1536), "=", float(Fraction(16 * 255, 1536)))
print("S(N)=sum (2j+1)^2 == N(4N^2-1)/3 for N=1..200:", all(sum((2 * j + 1) ** 2 for j in range(N)) == Fraction(N * (4 * N * N - 1), 3) for N in range(1, 201)))
print("M1 L03: E[Q]=1, Var=", 2 * 2 * (Fraction(1, 2)) ** 2)
print("E|Z| = sqrt(2/pi) =", math.sqrt(2 / math.pi), "; 2 phi(0) =", 2 / math.sqrt(2 * math.pi))
print("phi(0) with pi: 1/sqrt(2 pi) =", 1 / math.sqrt(2 * math.pi), "(page writes sqrt(2*calP), a typo)")
print("E[Z^4] by quadrature:", round(sum(z**4 * math.exp(-z * z / 2) for z in [i / 1000 for i in range(-10000, 10001)]) / 1000 / math.sqrt(2 * math.pi), 6))
print("expected abs sum N steps:", "sqrt(2Nt/pi) N=4 t=1:", math.sqrt(2 * 4 / math.pi), "=", 4 * math.sqrt(2 / math.pi) * math.sqrt(1 / 4))
