"""Round-5 recomputation of numbers stated in M2 L07 and L10 (changed pages) and the L09 card numbers (c124-c131)."""
from fractions import Fraction as F
import math
import struct

def ulp(x):
    return math.ulp(x)

out = []
def show(name, value, stated=None):
    out.append(f"{name}: {value}" + (f"  | stated {stated}" if stated is not None else ""))

x = F(3, 10)
show("L07 f(3/10)", F(1) / (1 - x), "10/7")
show("L07 P_1(3/10)", 1 + x, "1.3")
show("L07 err deg1 exact", F(10, 7) - (1 + x), "9/70")
show("L07 x^2/(1-x)", x**2 / (1 - x), "9/70")
e10 = x**11 / (1 - x)
show("L07 err deg10 float", float(e10), "2.5307e-6 (5 s.f.); printed 0.0000025307")
show("L07 err deg10 to 5 s.f.", f"{float(e10):.4e}")
show("L07 (3/10)^11/(7/10) numer", float(x**11 / F(7, 10)))
show("L07 Ex1.5 f''(1/2)", 2 / F(1, 2) ** 3, "16")
show("L07 Ex1.5 f'''(1/2)", 6 / F(1, 2) ** 4, "96")
show("L07 M1 f''(0), f'''(0)", (2, 6))
show("L07 M3 P2(1/2)", 1 + F(1, 2) + F(1, 4), "7/4")
show("L07 M3 err", 2 - F(7, 4), "1/4")
show("L07 E1 ratio 0.0010414286/0.0034714286", 0.0010414286 / 0.0034714286, "0.3000000058")
r = 0.0010414286 / 0.0034714286
show("L07 E1 rel diff", abs(r - 0.3) / 0.3, "about 2e-8")
show("L07 E2 n=8 bound (2/3)/512", float(F(2, 3) / 512), "0.0013")
show("L07 E2 n=9 bound (2/3)/1024", float(F(2, 3) / 1024), "0.00065")
show("L07 R2 2^19 < 1e6 <= 2^20", (2**19 < 10**6, 2**20 >= 10**6))
show("L07 P3(1/2) err deg3", 2 - (1 + F(1, 2) + F(1, 4) + F(1, 8)), "1/8")
show("L07 quiz err deg1 at 3/10 numeric", float(F(9, 70)), "0.128571 within 1e-6")
show("L07 lab part C P_n(2)", [2**(n + 1) - 1 for n in range(11)][-1], "2047; error -2048")
show("L07 sign E3 x=-1/2 err deg10", float(F(-1, 2) ** 11 / F(3, 2)), "negative")
show("L07 Prop 2.3 at x=2 error deg10", float(2**11 / (1 - 2)), "-2048")
# L10
def Ua(n):
    return sum((F(i, n) ** 3 - 2 * F(i, n) for i in range(1, n + 1)), F(0)) if False else None
fa = lambda t: 3 * t * t - 2
for n in (8, 128, 256):
    up = sum((fa(F(i, n)) / n for i in range(1, n + 1)), F(0))
    lo = sum((fa(F(i - 1, n)) / n for i in range(1, n + 1)), F(0))
    show(f"L10 A n={n} L,U,U-L float", (float(lo), float(up), float(up - lo)))
show("L10 E1 3/8", float(F(3, 8)), "0.375")
for n in (128,):
    fb = lambda t: 1 / (1 + t) ** 2
    up = sum((fb(F(i - 1, n)) / n for i in range(1, n + 1)), F(0))
    lo = sum((fb(F(i, n)) / n for i in range(1, n + 1)), F(0))
    show("L10 B n=128 L,U,U-L float", (float(lo), float(up), float(up - lo)))
    show("L10 E2 3/(4*128)", float(F(3, 4 * 128)), "0.005859375")
show("L10 E3 F'''(0.3)=6/1.3^4", 6 / 1.3**4, "2.1")
show("L10 E3 truncation h^2 F'''/6", 1e-12 * (6 / 1.3**4) / 6, "3.5e-13")
show("L10 E3 ulp(0.3)/2", ulp(0.3) / 2, "2.8e-17")
show("L10 E3 ulp(1.3)/2", ulp(1.3) / 2, "1.1e-16")
show("L10 E3 ulp(0.23)/2", ulp(0.23) / 2, "1.4e-17")
show("L10 E3 dF/dx at 0.3 (1/(1+y)^2)", 1 / 1.3**2, "0.59")
show("L10 E3 y/(1+y)^2", 0.3 / 1.3**2, "0.18")
per_value = (1 / 1.3**2) * ulp(0.3) / 2 + (0.3 / 1.3**2) * ulp(1.3) / 2 + ulp(0.23) / 2
show("L10 E3 per-value bound", per_value, "about 5.0e-17")
show("L10 E3 difference bound / 2h", 2 * per_value / 2e-6, "about 5e-11")
show("L10 E3 F(0.3)", 0.3 / 1.3, "about 0.23")
show("L10 Ex2.2 int 1/(1+x)^2", F(1, 2))
show("L10 Ex3.2 F(1)-F(0)", (1 - 2) - 0)
show("L10 M1 F(2)-F(0)", (8 - 4) - 0)
show("L10 M2 (27-1)/3", F(26, 3))
show("L10 M3 F(2)-F(1) with F=-1/(1+x)", (-F(1, 3)) - (-F(1, 2)), "1/6")
show("L10 Misc2 G(1)", F(1, 2) + 5, "11/2")
show("L10 R3 U-L formula n=4 sum", None)
show("L09 c126 mesh/U-L for (i/10)^2", None)
pts = [F(i * i, 100) for i in range(11)]
w = [pts[i] - pts[i - 1] for i in range(1, 11)]
U = sum(pts[i] * w[i - 1] for i in range(1, 11))
L = sum(pts[i - 1] * w[i - 1] for i in range(1, 11))
show("L09 c126 mesh", float(max(w)), "0.19")
show("L09 c126 U-L", float(U - L), "0.15933400")
show("L09 c123 U_128", float(F(129 * 257, 6 * 128 * 128)), "0.33724976")
show("L09 c125 L_128", float(F(127 * 255, 6 * 128 * 128)), "0.32943726")
show("L09 c127 midpoint n=8 error", float(F(680, 2048) - F(1, 3)), "-0.00130208")
show("L09 c129 left and right sums x(1-x) n=2", (F(1, 2) * (0 + F(1, 4)), F(1, 2) * (F(1, 4) + 0)), "1/8, 1/8")
show("L09 c423 integral 1/6", F(1, 2) - F(1, 3), "1/6 (F=x^2/2-x^3/3)")
show("L09 c131 1/3 - L_n = (3n-1)/(6n^2) n=5", float(F(1, 3) - F(4 * 9, 6 * 25)) - float(F(3 * 5 - 1, 6 * 25)), "0")
show("L09 c128 U_n-1/3 (3n+1)/(6n^2) n=5", float(F(6 * 11, 6 * 25) - F(1, 3)) - float(F(16, 150)), "0")
print("\n".join(out))
