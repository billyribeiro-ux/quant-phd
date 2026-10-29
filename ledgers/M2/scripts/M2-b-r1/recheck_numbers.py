"""Independent recomputation of the displayed numbers in M2 L07-L12 (verifier round 1, slice M2-b).

Run: .venv/bin/python -I ledgers/M2/scripts/M2-b-r1/recheck_numbers.py
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 60


def show(label: str, value: object) -> None:
    print(f"{label}: {value}")


# L07 Example 2.4 and exercises
x = Fraction(3, 10)
show("L07 10/7 - 1.3 == 9/70", Fraction(10, 7) - Fraction(13, 10) == Fraction(9, 70))
show("L07 x^2/(1-x) == 9/70", x**2 / (1 - x) == Fraction(9, 70))
e10 = x ** 11 / (1 - x)
show("L07 degree-10 error (3/10)^11/(7/10) to 10 places", f"{float(e10):.10f}")
show("L07 ratio printed errors 0.0010414286/0.0034714286", f"{0.0010414286 / 0.0034714286:.12f}")
show("L07 (2/3)/512", f"{(2 / 3) / 512:.8f}")
show("L07 (2/3)/1024", f"{(2 / 3) / 1024:.8f}")
show("L07 n=9 bound <= 0.001", (Fraction(2, 3) / 1024) <= Fraction(1, 1000))
show("L07 n=8 bound > 0.001", (Fraction(2, 3) / 512) > Fraction(1, 1000))
show("L07 2^19 < 10^6 <= 2^20", (2**19 < 10**6 <= 2**20))
show("L07 T_3 at 1/2 error 1/8", Fraction(2) - sum(Fraction(1, 2) ** k for k in range(4)) == Fraction(1, 8))

# L08 xi values (unrounded)
xi_a = 1 - Decimal(3) / Decimal(4)
xi_a = 1 - (Decimal(3) / Decimal(4)) ** (Decimal(1) / Decimal(4))
show("L08 xi(1/4, n=2) = 1-(3/4)^(1/4) to 7 decimals", f"{xi_a:.7f}")
show("L08 (0.5)^(1/5)", f"{(Decimal(1) / Decimal(2)) ** (Decimal(1) / Decimal(5)):.7f}")
show("L08 xi(0.5, n=3)", f"{1 - (Decimal(1) / Decimal(2)) ** (Decimal(1) / Decimal(5)):.7f}")
show("L08 (0.7)^(1/7)", f"{(Decimal(7) / Decimal(10)) ** (Decimal(1) / Decimal(7)):.7f}")
show("L08 xi(0.3, n=5)", f"{1 - (Decimal(7) / Decimal(10)) ** (Decimal(1) / Decimal(7)):.7f}")
show("L08 example 2.4 ratio interval check", all(Fraction(2) ** (n + 2) * (1 - Fraction(1, 2)) >= 2 ** (n + 1) and Fraction(2) ** (n + 2) * (1 - Fraction(1, 2)) < 2 ** (n + 2) for n in range(10)))
show("L08 remark 3.3 at x=0.6, n=1..4 bound", [Fraction(6, 10) ** (n + 1) / Fraction(4, 10) ** (n + 2) for n in range(1, 5)])
show("L08 remark 3.3 at x=0.6, n=1..4 remainder", [Fraction(6, 10) ** (n + 1) / Fraction(4, 10) for n in range(1, 5)])
show("L08 quartic identity", all(Fraction(x) ** 4 == (1 + 4 * (Fraction(x) - 1) + 6 * (Fraction(x) - 1) ** 2 + 4 * (Fraction(x) - 1) ** 3) + (Fraction(x) - 1) ** 4 for x in (Fraction(1, 3), Fraction(7, 2))))
show("L08 Prop 2.3 at 1/4, n=2: T2 = 21/16, remainder 1/48", (Fraction(4, 3) - (1 + Fraction(1, 4) + Fraction(1, 16)), Fraction(1, 64) / Fraction(3, 4)))

# L09 numbers
n = 128
show("L09 U_128 - 1/3 formula 385/98304 (decimal)", f"{Fraction(385, 98304).__float__():.10f}")
U128 = sum(Fraction(i, n) ** 2 / n for i in range(1, n + 1))
show("L09 U_128 printed 0.33724976 check", f"{float(U128):.8f}")
show("L09 U_128 - 1/3 exact equals 385/98304", U128 - Fraction(1, 3) == Fraction(385, 98304))
show("L09 25/384", f"{25 / 384:.8f}")
show("L09 n=50 error 151/15000", f"{151 / 15000:.6f}")
show("L09 n=51 error", f"{154 / (6 * 51 * 51):.6f}")
show("L09 (3n+1)/(6n^2) < 0.01 first n", next(k for k in range(1, 1000) if Fraction(3 * k + 1, 6 * k * k) < Fraction(1, 100)))
show("L09 1/(12*16^2)", f"{1 / (12 * 256):.8f}")
pts = [Fraction(i * i, 100) for i in range(11)]
w = [pts[i] - pts[i - 1] for i in range(1, 11)]
gap = sum((pts[i] ** 2 - pts[i - 1] ** 2) * w[i - 1] for i in range(1, 11))
show("L09 part B number of points", len(pts))
show("L09 part B mesh", float(max(w)))
show("L09 part B U-L (sup/inf of x^2 on partition points)", float(gap))
show("L09 Misconception 2 x(1-x), n=2 left and right sums", (Fraction(0) * Fraction(1, 2) + Fraction(1, 4) * Fraction(1, 2), Fraction(1, 4) * Fraction(1, 2) + 0))
show("L09 integral of x(1-x) = 1/6", Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6))
show("L09 1/(1+x) n=2: U", (Fraction(1) + Fraction(2, 3)) / 2)
show("L09 1/(1+x) n=2: L", (Fraction(2, 3) + Fraction(1, 2)) / 2)

# L10 central difference error estimate
h = Decimal("1e-6")
xv = Decimal("0.3")
F = lambda t: t / (1 + t)  # noqa: E731
exact_d = 1 / (Decimal("1.3")) ** 2
central_hp = (F(xv + h) - F(xv - h)) / (2 * h)
show("L10 high-precision central difference error", f"{abs(central_hp - exact_d):.3E}")
show("L10 claimed truncation error h^2 F'''/6", f"{float(h * h) * 6 / 1.3 ** 4 / 6:.3E}")
cen_float = ((0.3 + 1e-6) / (1 + 0.3 + 1e-6) - (0.3 - 1e-6) / (1 + 0.3 - 1e-6)) / (2e-6)
show("L10 float central difference error (double)", f"{abs(cen_float - 1 / 1.3 ** 2):.3E}")

# L11 numbers
show("L11 midpoint N=816 error", f"{2 / (3 * 816 * 816):.7E}")
show("L11 midpoint N=817 error", f"{2 / (3 * 817 * 817):.7E}")
show("L11 2/(3N^2)<=1e-6 smallest N", next(N for N in range(1, 10000) if Fraction(2, 3 * N * N) <= Fraction(1, 10**6)))
show("L11 residual", f"{8 / 3 - 2.6666666663:.2E}")
show("L11 Example 3.2 integrand expansion ok", all((t**3 + t) ** 2 * (3 * t * t + 1) == 3 * t**8 + 7 * t**6 + 5 * t**4 + t**2 for t in (Fraction(1, 3), Fraction(2, 5))))
show("L11 Example 2.2 expansion sum", Fraction(1, 2) - Fraction(4, 3) + Fraction(3, 2) - Fraction(4, 5) + Fraction(1, 6))
show("L11 Problem x^3(1-x) 1/20", Fraction(3, 2) * (Fraction(1, 3) - Fraction(1, 2) + Fraction(1, 5)))

# L12 numbers
H = [sum(Fraction(1, i) for i in range(1, 2**m + 1)) for m in range(0, 15)]
show("L12 H_{2^m} >= 1+m/2 for m=0..14", all(H[m] >= 1 + Fraction(m, 2) for m in range(15)))
show("L12 H_16384 - 1 float", f"{float(H[14]) - 1:.8f}")
show("L12 1/3072 printed", f"{1 / 3072:.8f}")
show("L12 Problem: sum of k^-4 bound 1/3 check", Fraction(1, 3))
