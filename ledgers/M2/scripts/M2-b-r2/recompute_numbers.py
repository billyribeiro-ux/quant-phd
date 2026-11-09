"""Independent recomputation of the prose numbers in slice b (L07-L12), from exact fractions and unrounded floats."""
import math
from fractions import Fraction as Fr

out = []
def show(label, value, printed=None):
    out.append(f"{label}: {value!r}" + (f" | page says {printed}" if printed is not None else ""))

# L07
show("L07 f(3/10)-P_1(3/10)", Fr(10, 7) - Fr(13, 10), "9/70")
show("L07 x^2/(1-x) at 3/10", float(Fr(9, 100) / Fr(7, 10)), "9/70 = 0.128571")
show("L07 error deg 10 x=3/10 (float)", (0.3 ** 11) / 0.7, "2.5307e-6")
show("L07 ratio err5/err4 (printed decimals)", 0.0010414286 / 0.0034714286, "0.3000000058")
show("L07 remainder deg 9 for x=-1/2: (2/3)(1/2)^10", (2 / 3) * 0.5 ** 10, "0.00065")
show("L07 (2/3)/512 deg 8", (2 / 3) / 512, "0.0013")
show("L07 n with 2^n >= 1e6", next(n for n in range(100) if 2 ** n >= 10 ** 6), "n = 20")
# L08
for x in (0.1, 0.3, 0.5, 0.9):
    for n in (1, 3, 5):
        xi = 1 - (1 - x) ** (1 / (n + 2))
        print_val = (round(xi, 6), x ** (n + 1) / (1 - x))
        out.append(f"L08 x={x} n={n} xi={xi:.8f} R_n={print_val[1]:.8f}")
show("L08 xi(1/4,n=2)", 1 - (3 / 4) ** 0.25, "0.0693951")
show("L08 xi(0.5,n=3)", 1 - 0.5 ** 0.2, "0.129449")
show("L08 xi(0.3,n=5)", 1 - 0.7 ** (1 / 7), "0.049677")
show("L08 bound 128/27 * (1/16)/2", Fr(128, 27) * Fr(1, 16) / 2, "4/27 = 0.148148")
show("L08 exact R_1(1/4)", Fr(1, 16) / Fr(3, 4), "1/12")
show("L08 bound x=0.6 n=1..4", [0.6 ** (n + 1) / 0.4 ** (n + 2) for n in range(1, 5)], "5.625, 8.4375, 12.65625, 18.984375")
show("L08 exact 0.6 n=1..4", [0.6 ** (n + 1) / 0.4 for n in range(1, 5)], "0.9, 0.54, 0.324, 0.1944")
# L09
pts = [Fr(i * i, 100) for i in range(11)]
w = [pts[i] - pts[i - 1] for i in range(1, 11)]
f = lambda t: t * t
U = sum(f(pts[i]) * w[i - 1] for i in range(1, 11))
L = sum(f(pts[i - 1]) * w[i - 1] for i in range(1, 11))
show("L09 partB U-L (exact)", float(U - L), "0.15933400")
show("L09 partB mesh", float(max(w)), "0.19")
show("L09 U_8-1/3", float(Fr(25, 384)), "0.06510417")
show("L09 midpoint err n=16 vs -1/(12 n^2)", -1 / (12 * 256), "-0.00032552")
show("L09 midpoint err n=8", -1 / (12 * 64), "-0.00130208")
show("L09 U_128-1/3 exact", Fr(385, 98304), "385/98304")
show("L09 U_128 float", float(Fr(1, 3) + Fr(385, 98304)), "0.33724976")
n51 = [(n, float(Fr(3 * n + 1, 6 * n * n))) for n in (50, 51)]
show("L09 (3n+1)/(6n^2) at n=50,51", n51, "0.010067, 0.009868")
show("L09 x(1-x) left=right sums n=2", (0 + Fr(1, 4)) / 2, "1/8")
show("L09 x(1-x)-integral 1/6", Fr(1, 2) - Fr(1, 3), "1/6")
show("L09 1/(1+x) n=2 L", float((Fr(2, 3) + Fr(1, 2)) / 2), "7/12 = 0.583333")
# L10
show("L10 F'''(0.3)", 6 / 1.3 ** 4, "about 2.1")
show("L10 truncation h^2 F'''/6", 1e-12 * (6 / 1.3 ** 4) / 6, "3.5e-13")
show("L10 1/(1.3)^2", 1 / 1.3 ** 2, "0.59171598")
show("L10 U_8-L_8 printed", -0.80468750 - (-1.17968750), "0.375")
show("L10 L_128 U_128 diff", 0.50293859 - 0.49707921, "0.00585938")
# L11
show("L11 1/30 term-by-term", Fr(1, 2) - Fr(4, 3) + Fr(3, 2) - Fr(4, 5) + Fr(1, 6), "1/30")
show("L11 integral x^2(1-x)^3", Fr(1, 2) * Fr(1, 30), "1/60")
show("L11 x^2(1-x)^2 integral", Fr(1, 3) - Fr(1, 2) + Fr(1, 5), "1/30")
show("L11 2/(3N^2) N=816", 2 / (3 * 816 ** 2), "1.0012e-6")
show("L11 2/(3N^2) N=817", 2 / (3 * 817 ** 2), "9.988e-7")
show("L11 residual", 8 / 3 - 2.6666666663, "4e-10")
show("L11 (3t^8+7t^6+5t^4+t^2) integral", Fr(3, 9) + Fr(7, 7) + Fr(5, 5) + Fr(1, 3), "8/3")
# L12
show("L12 1-1/10000 truncated", 1 - 1 / 10000, "0.9999")
show("L12 H_16384 - 1", sum(1 / i for i in range(2, 16385)), "9.28130671")
show("L12 H_2^m-1 for m=1..14 >= m/2", all(sum(1 / i for i in range(2, 2 ** m + 1)) >= m / 2 for m in range(1, 15)), "True")
show("L12 truncated 1/x^3 at b=10", (1 - 1 / 100) / 2, "0.4950000000")
print("\n".join(out))
