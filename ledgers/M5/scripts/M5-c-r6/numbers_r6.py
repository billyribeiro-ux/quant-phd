"""Round-6 re-derivation of the numbers that the delta touches (M5 L08-L10 and their cards). Independent of the page text."""
import math
from fractions import Fraction

# L08 Example 1.2 (alpha = 1/2, G = (0.25, 1.0), V = 0)
print("Example 1.2: sqrt(0.75) =", f"{math.sqrt(0.75):.6f}", " sqrt(0) =", math.sqrt(0.0))
print("  (BV)(1.0) =", f"{max(math.sqrt(1.0**0.5 - kp) for kp in (0.25, 1.0) if kp <= 1.0**0.5):.6f}")
print("  exact sqrt(3)/2 =", f"{math.sqrt(3)/2:.10f}")
# L08 M3/quiz: u(k^{1/2} - 0.25) at k = 0.5
v = math.sqrt(math.sqrt(0.5) - 0.25)
print(f"quiz utility at k=0.5: sqrt(sqrt(0.5)-0.25) = {v:.10f} (key 0.676097, tol 1e-6, diff {abs(v-0.676097):.2e})")

# L09 naive stop: actual error and last step (printed values) and their quotient
actual, step = 0.0000085808, 0.0000009534
q = actual / step
print(f"L09 naive stop: actual/step = {q:.10f}; to 4 dp = {q:.4f}; beta/(1-beta) at 0.9 = {0.9/0.1:.0f}")
print(f"  actual/tolerance = {actual/1e-6:.4f} (page: more than eight times the tolerance)")
print(f"  step*9 = {9*step:.10f}; actual - 9*step = {actual - 9*step:.3e}")

# L10 Section 5 and R3 values (exact)
import itertools
def rs_sum(f, G, n, tag):
    pts = [Fraction(i, n) for i in range(n + 1)]
    s = Fraction(0)
    for i in range(1, n + 1):
        xi = pts[i] if tag == "right" else pts[i - 1]
        s += f(xi) * (G(pts[i]) - G(pts[i - 1]))
    return s
n = 1000
f = lambda x: x
G1 = lambda x: x
G2 = lambda x: x * x
G2c = lambda x: x * x + 5
for name, G in (("G=x", G1), ("G=x^2", G2)):
    r = rs_sum(f, G, n, "right"); l = rs_sum(f, G, n, "left")
    print(f"{name} n={n}: right={float(r):.12f} left={float(l):.12f} right-limit={float(r-(Fraction(1,2) if name=='G=x' else Fraction(2,3))):.6e}")
print(f"G=x right-1/2 == 1/(2n): {rs_sum(f,G1,n,'right')-Fraction(1,2) == Fraction(1,2*n)}; left-1/2 == -1/(2n): {rs_sum(f,G1,n,'left')-Fraction(1,2) == -Fraction(1,2*n)}")
# constant shift leaves sums unchanged (R3) for G=x^2+5 vs G=x^2
print("R3 shift invariance (n=1000, right and left):",
      rs_sum(f, G2c, n, "right") == rs_sum(f, G2, n, "right"), rs_sum(f, G2c, n, "left") == rs_sum(f, G2, n, "left"))
# integrals: int_0^1 x * 2x dx = 2/3 ; int_0^1 x dx = 1/2 ; int_0^1 x * 3x^2 dx = 3/4 (exact)
print("int_0^1 x*2x dx =", Fraction(2, 3), " int_0^1 x dx =", Fraction(1, 2), " int x*3x^2 =", Fraction(3, 4))
# Example 3.3 closed forms
for m in (4, 10, 100, 1000):
    r = Fraction((m + 1) * (4 * m - 1), 6 * m * m)
    l = Fraction(4 * m * m - 3 * m - 1, 6 * m * m)
    print(f"Ex3.3 n={m}: right_closed==direct {r == rs_sum(f,G2,m,'right')}, left_closed==direct {l == rs_sum(f,G2,m,'left')}, "
          f"|right-2/3|<=1/(2n) {abs(r-Fraction(2,3)) <= Fraction(1,2*m)}, |left-2/3|<=1/n {abs(l-Fraction(2,3)) <= Fraction(1,m)}")

# L08 a priori counts: least n with beta^n * D/(1-beta) <= 1e-12 (D = sqrt(3)/2, as in the page's E1)
D0 = math.sqrt(3) / 2
for b in (0.5, 0.9, 0.95):
    n = 0
    while b ** n * D0 / (1 - b) > 1e-12:
        n += 1
    print(f"E1 a priori: beta={b} least_n={n} threshold={math.log(1e-12*(1-b)/D0)/math.log(b):.2f}")
# L09 R2 a priori bound at beta = 0.9, ||V1 - V0|| = sqrt(3)/2
for n in (147, 151, 152):
    print(f"L09 R2 bound n={n}: {0.9**n * D0 / 0.1:.6e}")
n = 0
while 0.9 ** n * D0 / 0.1 > 1e-6:
    n += 1
print(f"L09 R2 least n with bound <= 1e-6: {n}")
