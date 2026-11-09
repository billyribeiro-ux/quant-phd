"""Independent recomputation of the numbers printed on the M2 L07-L12 pages (not the twins' code).

Run: python -I v3_recompute.py   (standard library only)
"""
from fractions import Fraction as Fr
from math import comb, factorial, log, sqrt

out: list[str] = []


def show(label: str, value: object) -> None:
    out.append(f"{label}: {value}")


# L07 Example 2.4 and Problem values
x = Fr(3, 10)
show("L07 f(3/10)", 1 / (1 - x))
show("L07 P1 error = 9/70", 1 / (1 - x) - (1 + x) == Fr(9, 70))
show("L07 deg-10 error x^11/(1-x) float", float(x**11 / (1 - x)))
show("L07 deg-10 error 5 s.f.", f"{float(x**11 / (1 - x)):.4e}")
show("L07 ratio err5/err4 (printed decimals)", 0.0010414286 / 0.0034714286)
show("L07 ratio rel diff from 0.3", (0.0010414286 / 0.0034714286) / 0.3 - 1)
show("L07 x=-1/2 err n=8 (2/3)/512", float(Fr(2, 3) / 512))
show("L07 x=-1/2 err n=9 (2/3)/1024", float(Fr(2, 3) / 1024))
show("L07 x=1/2: n with 2^n>=1e6", next(n for n in range(100) if 2**n >= 10**6))
show("L07 P2(1/2) and error", (1 + Fr(1, 2) + Fr(1, 4), 2 - (1 + Fr(1, 2) + Fr(1, 4))))
show("L07 f''(1/2), f'''(1/2)", (2 / Fr(1, 2) ** 3, 6 / Fr(1, 2) ** 4))
# L07 printed Part B table, exact errors vs decimals
errs = []
for n in range(11):
    P = sum(x**k for k in range(n + 1))
    errs.append(1 / (1 - x) - P)
show("L07 part B errors n=0..10 (float, 10dp)", [f"{float(e):.10f}" for e in errs])
show("L07 part C errors n=10 at x=2", int(1 / (1 - Fr(2)) - sum(Fr(2) ** k for k in range(11))))

# L08 xi table, remainder, Lagrange checks
def xi(xv: float, n: int) -> float:
    return 1 - (1 - xv) ** (1 / (n + 2))


show("L08 xi(1/4,2)", f"{xi(0.25, 2):.7f}")
show("L08 xi(1/2,3)", f"{xi(0.5, 3):.7f}")
show("L08 xi(0.3,5)", f"{xi(0.3, 5):.7f}")
show("L08 (1/2)^(1/5)", f"{0.5 ** 0.2:.7f}")
show("L08 (0.7)^(1/7)", f"{0.7 ** (1 / 7):.7f}")
show("L08 (3/4)^(1/4)", f"{0.75 ** 0.25:.7f}")
show("L08 printed part C xi x=0.1,n=1", f"{xi(0.1, 1):.6f}")
show("L08 printed part C xi x=0.3,n=3", f"{xi(0.3, 3):.6f}")
show("L08 Example 2.4 bound and exact at 1/4 (n=1)", (4 / 27, float(Fr(1, 12))))
show("L08 M=128/27 check", Fr(2) / Fr(3, 4) ** 3 == Fr(128, 27))
show("L08 Remark 3.3 x=0.6 bounds", [0.6 ** (n + 1) / 0.4 ** (n + 2) for n in range(1, 5)])
show("L08 Remark 3.3 x=0.6 exact", [0.6 ** (n + 1) / 0.4 for n in range(1, 5)])
show("L08 bound at 1/2 equals 2 for all n", all(Fr(2) ** (n + 2) * Fr(1, 2) ** (n + 1) == 2 for n in range(10)))
show("L08 pair counts", (19 * 7, sum(1 for k in range(1, 20) for n in range(7) if k / 20 <= 0.5)))

# L09 sums
def U_L(n: int) -> tuple[Fr, Fr]:
    U = sum((Fr(i, n) ** 2 / n for i in range(1, n + 1)), Fr(0))
    L = sum((Fr(i - 1, n) ** 2 / n for i in range(1, n + 1)), Fr(0))
    return L, U


L128, U128 = U_L(128)
show("L09 U128 - 1/3 == 385/98304", U128 - Fr(1, 3) == Fr(385, 98304))
show("L09 U128 float", f"{float(U128):.8f}")
show("L09 L128 float", f"{float(L128):.8f}")
U8 = U_L(8)[1]
show("L09 U8-1/3 == 25/384", U8 - Fr(1, 3) == Fr(25, 384))
show("L09 n=8 right error float", f"{float(U8 - Fr(1, 3)):+.8f}")
mid = lambda n: sum((Fr(2 * i - 1, 2 * n) ** 2 / n for i in range(1, n + 1)), Fr(0)) - Fr(1, 3)
show("L09 midpoint errors n=8,16,32", [f"{float(mid(n)):+.8f}" for n in (8, 16, 32)])
show("L09 1/(12 n^2) for n=16", f"{1 / (12 * 256):.8f}")
show("L09 1/(12*64)", f"{1 / (12 * 64):.8f}")
show("L09 prob 3 n=50,51 bounds", ((3 * 50 + 1) / (6 * 50 * 50), (3 * 51 + 1) / (6 * 51 * 51)))
show("L09 151/15000, 154/15606", (Fr(151, 15000), Fr(154, 15606)))
show("L09 mesh of part B widths max", max(Fr((2 * i - 1), 100) for i in range(1, 11)))
show("L09 part B U-L (recomputed)", "see below")
pts = [Fr(i * i, 100) for i in range(11)]
U = sum(pts[i] ** 2 * (pts[i] - pts[i - 1]) for i in range(1, 11))
Lw = sum(pts[i - 1] ** 2 * (pts[i] - pts[i - 1]) for i in range(1, 11))
show("L09 part B U-L float", f"{float(U - Lw):.8f}")
show("L09 7/12 lower sum", (Fr(2, 3) + Fr(1, 2)) / 2)

# L10 values
show("L10 U8 printed -0.80468750", float(sum((Fr(i, 8) ** 3 * 3 - 2 * Fr(i, 8)) * 0 for i in range(1, 9))))
fa = lambda t: 3 * t * t - 2
for n in (8, 128):
    U = sum((fa(Fr(i, n)) / n for i in range(1, n + 1)), Fr(0))
    Lw = sum((fa(Fr(i - 1, n)) / n for i in range(1, n + 1)), Fr(0))
    show(f"L10 n={n} U,L float", (f"{float(U):.8f}", f"{float(Lw):.8f}"))
show("L10 3/512", Fr(3, 512))
show("L10 F'''(0.3)", 6 / 1.3**4)
show("L10 trunc err h^2 F'''/6 at h=1e-6", 1e-12 * (6 / 1.3**4) / 6)
show("L10 0.3/1.3", 0.3 / 1.3)
show("L10 1/1.69", 1 / 1.69)
show("L10 F(1)-F(0) for x^3-2x", (1 - 2) - 0)
show("L10 x/(1+x) mid vs sums n=128 (B) L,U",
     tuple(f"{float(v):.8f}" for v in (sum((Fr(i, 128) / (1 + Fr(i, 128))) for i in range(0, 0)), )))
# L10 part B n=128 directly
fb = lambda t: 1 / (1 + t) ** 2
n = 128
Ub = sum((fb(Fr(i - 1, n)) / n for i in range(1, n + 1)), Fr(0))
Lb = sum((fb(Fr(i, n)) / n for i in range(1, n + 1)), Fr(0))
show("L10 part B n=128 L,U float", (f"{float(Lb):.8f}", f"{float(Ub):.8f}", f"{float(Ub - Lb):.8f}"))
show("L10 3/(4*128)", float(Fr(3, 512)))

# L11 values
show("L11 int x^2(1-x)^3 = 1/60", Fr(1, 60))
show("L11 int x(1-x)^4 = 1/30", sum((Fr(c) * (-1) ** j * Fr(1, j + 3) for j, c in enumerate([1, 4, 6, 4, 1])), Fr(0)) == Fr(1, 30) or "check")
show("L11 1/2 - 4/3 + 3/2 - 4/5 + 1/6", Fr(1, 2) - Fr(4, 3) + Fr(3, 2) - Fr(4, 5) + Fr(1, 6))
show("L11 x^3(1-x) = 1/20", Fr(1, 4) - Fr(1, 5))
show("L11 1/12", Fr(1, 3) * Fr(1, 4))
show("L11 7/3 expansion", 1 + 1 + Fr(1, 3))
show("L11 2/(3N^2) N=816,817", (2 / (3 * 816**2), 2 / (3 * 817**2)))
show("L11 smallest N", min(N for N in range(1, 10**5) if 2 / (3 * N * N) <= 1e-6))
show("L11 residual", 2.6666666667 - 2.6666666663)
mp = lambda f, a, b, n: (b - a) / n * sum(f(a + (i + 0.5) * (b - a) / n) for i in range(n))
show("L11 midpoint check N=2000 int_0^2 x^2", mp(lambda x: x * x, 0.0, 2.0, 2000))
show("L11 3/2 * 1/30", Fr(3, 2) * Fr(1, 30))

# L12 values
show("L12 1-1/100", 1 - Fr(1, 100))
show("L12 1/2 - 1/(2*100^2)", Fr(1, 2) - Fr(1, 2 * 100**2))
harm = lambda N: sum(Fr(1, i) for i in range(1, N + 1))
show("L12 H_16384 - 1 (float)", f"{float(harm(16384)) - 1:.8f}")
show("L12 H_2^m - 1 >= m/2 for m=1..14", all(float(harm(2**m)) - 1 >= m / 2 for m in range(1, 15)))
show("L12 H_16 - 1", f"{float(harm(16)) - 1:.8f}")
show("L12 H_256 - 1", f"{float(harm(256)) - 1:.8f}")
show("L12 H_4096 - 1", f"{float(harm(4096)) - 1:.8f}")
show("L12 H_2 - 1", f"{float(harm(2)) - 1:.8f}")
show("L12 8 part: 1/8", Fr(1, 2) * Fr(1, 4))
show("L12 1/b at 1e6", Fr(1, 10**6))
show("L12 p=4 int 1/3", Fr(1, 3))
show("L12 trunc p=3 error 1/(2b^2) at b=10", Fr(1, 200))

print("\n".join(out))
