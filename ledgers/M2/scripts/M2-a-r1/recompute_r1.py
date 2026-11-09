"""Independent recomputation of the numbers printed or quoted on M2 pages L01-L06 (exact rationals where possible).

Run: python -I ledgers/M2/scripts/M2-a-r1/recompute.py
"""
from fractions import Fraction as F
import math


def line(label, value):
    print(f"{label}: {value}")


# L01 Lab 1 and prose
a = lambda n: F(2 * n + 1, n + 1)
line("L01 a_1 - 2 (exact)", a(1) - 2)
line("L01 error n=10 (exact)", abs(a(10) - 2))
line("L01 error n=999 == 1/1000 ?", abs(a(999) - 2) == F(1, 1000))
line("L01 error n=1000 float", f"{float(abs(a(1000) - 2)):.6e}")
line("L01 least N for eps=1/1000 (1/(n+1) < 1/1000)", min(n for n in range(1, 5000) if F(1, n + 1) < F(1, 1000)))
line("L01 a_1000 decimal", f"{float(a(1000)):.9f}")
line("L01 quiz eps=0.0001 least N", min(n for n in range(1, 20000) if F(1, n + 1) < F(1, 10000)))
line("L01 |a_9 - 2|", abs(a(9) - 2))
line("L01 E1 1/1001 scaled by 1e4", f"{1 / 1001 * 1e4:.9f}")
line("L01 M1 least n with 13/(n+4) < 1/100", min(n for n in range(1, 5000) if F(13, n + 4) < F(1, 100)))
line("L01 M2 least N with 1/n^2 < 1/100 for all n>=N",
     min(N for N in range(1, 200) if all(F(1, n * n) < F(1, 100) for n in range(N, 2000))))

# L02
am = lambda n: F(2 * n + 1, n + 1)
bm = lambda n: F(n + 2, n)
for n in (1, 10, 100, 1000, 10000):
    se = abs(am(n) + bm(n) - 3)
    pe = abs(am(n) * bm(n) - 2)
    qe = abs(am(n) / bm(n) - 2)
    assert se == F(n + 2, n * (n + 1)) and pe == F(3 * n + 2, n * (n + 1)) and qe == F(5 * n + 4, (n + 1) * (n + 2))
    line(f"L02 n={n} sum/prod/quot errors", f"{float(se):.6e} {float(pe):.6e} {float(qe):.6e}")
line("L02 sum error n=10 equals 6/55", F(12, 110) == F(6, 55))
line("L02 prod error n=100 = 302/10100 decimal", f"{float(F(302, 10100)):.10f}")
line("L02 quiz product error n=100, |302/10100 - 0.02990099|", float(abs(F(302, 10100) - F(2990099, 100000000))))
line("L02 quiz sum error n=10, |12/110 - 0.1090909|", float(abs(F(12, 110) - F(1090909, 10000000))))

# L03
for k in range(1, 5):
    h = F(1, 10 ** k)
    left, right = (1 - h) ** 2, 2 + 2 * h
    line(f"L03 h={float(h):g}: f(1-h), f(1+h), gap",
         f"{float(left):.6f} {float(right):.6f} {float(right - left):.6f}; 1+4h-h^2={float(1 + 4 * h - h * h):.6f}")
line("L03 quiz gap at h=0.1 exact", 1 + F(4, 10) - F(1, 100))
line("L03 E3 grid point and 3|x-2|", (F(2) + F(19, 20) * F(1, 10), 3 * F(19, 20) * F(1, 10)))

# L04
q = lambda h: ((1 + h) ** 3 - 1) / h
for k in range(1, 7):
    h = F(1, 10 ** k)
    assert q(h) == 3 + 3 * h + h * h
    line(f"L04 h=1e-{k}: Q, |Q-3|", f"{float(q(h)):.6f} {float(abs(q(h) - 3)):.6e}")
line("L04 (|Q-3|)/h at 1e-6", f"{float((abs(q(F(1, 10**6)) - 3)) / F(1, 10**6)):.6f}")
line("L04 E2 3h+h^2 at h=1e-5", f"{float(3 * F(1, 10**5) + F(1, 10**10)):.6e}")

# L05: exact central differences against analytic values at x = 3/2, h = 1e-4
X = F(3, 2)
H = F(1, 10000)
p = lambda x: (x * x + 1) * x ** 3
pp = 2 * X * X ** 3 + (X * X + 1) * 3 * X * X
qf = lambda x: (x * x + 1) / (x + 2)
qp = (X * X + 4 * X - 1) / (X + 2) ** 2
c = lambda x: (x * x + 1) ** 3
cp = 3 * (X * X + 1) ** 2 * 2 * X
for name, fn, an in (("p", p, pp), ("q", qf, qp), ("c", c, cp)):
    cd = (fn(X + H) - fn(X - H)) / (2 * H)
    line(f"L05 {name}: analytic | exact central diff | |diff|",
         f"{float(an):.9f} | {float(cd):.12f} | {float(abs(cd - an)):.4e}")
line("L05 p'''(1.5) = 60x^2+6", 60 * X * X + 6)
line("L05 c'''(1.5) = 120x^3+72x", 120 * X ** 3 + 72 * X)
line("L05 h^2 p'''/6", float(H * H * (60 * X * X + 6) / 6))
line("L05 h^2 c'''/6", float(H * H * (120 * X ** 3 + 72 * X) / 6))
line("L05 cubic central difference equals 3+h^2 at h=1/10",
     ((1 + F(1, 10)) ** 3 - (1 - F(1, 10)) ** 3) / F(2, 10) == 3 + F(1, 100))
line("L05 quotient rule at 1.5 equals 29/49", qp == F(29, 49))
line("L05 quotient decimal to 9 dp", f"{float(qp):.9f}")
line("L05 chain rule c'(1.5)", cp)

# L06
fc = lambda x: x ** 3 - 3 * x
grid = [F(-2) + i * F(1, 4) for i in range(17)]
incr = sum(1 for lo, hi in zip(grid, grid[1:]) if fc(hi) > fc(lo))
mid_agree = sum(1 for lo, hi in zip(grid, grid[1:])
                if (fc(hi) > fc(lo)) == (3 * ((lo + hi) / 2) ** 2 - 3 > 0))
line("L06 grid points", len(grid))
line("L06 increasing grid intervals (of 16)", incr)
line("L06 midpoint agreement (of 16)", mid_agree)
line("L06 f(-1), f(1)", (fc(F(-1)), fc(F(1))))
line("L06 MVT x^3 on [0,2]: c = 2/sqrt3", 2 / math.sqrt(3))
line("L06 MVT x^3 on [0,1]: c = 1/sqrt3", 1 / math.sqrt(3))
line("L06 x^2-4x+1 at 2", 4 - 8 + 1)
line("L06 chord slope of |x-1| on [0,2]", (abs(2 - 1) - abs(0 - 1)) / 2)
line("L06 f(-2), f(-1) for x^3-3x", (fc(F(-2)), fc(F(-1))))
