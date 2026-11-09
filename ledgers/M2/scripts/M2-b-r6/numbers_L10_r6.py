# Round-6 independent re-derivation of the L10 numbers that the page states (own code; does not read the twin).
from fractions import Fraction as Fr
import math
f = lambda x: 3 * x * x - 2
F = lambda x: x**3 - 2 * x
print("F(1)-F(0) =", F(Fr(1)) - F(Fr(0)), "; F(2)-F(0) =", F(Fr(2)) - F(Fr(0)))
for n in (8, 128, 256):
    U = sum(f(Fr(i, n)) for i in range(1, n + 1)) / n
    L = sum(f(Fr(i - 1, n)) for i in range(1, n + 1)) / n
    print(f"part A n={n}: L={float(L):.8f} U={float(U):.8f} U-L={float(U-L)} 3/n={float(Fr(3,n))} exact_equal={U-L==Fr(3,n)}")
g = lambda x: 1 / (1 + x) ** 2
G = lambda x: x / (1 + x)
for n in (8, 128):
    U = sum(g(Fr(i - 1, n)) for i in range(1, n + 1)) / n
    L = sum(g(Fr(i, n)) for i in range(1, n + 1)) / n
    print(f"part B n={n}: L={float(L):.8f} U={float(U):.8f} U-L={float(U-L)} 3/(4n)={float(Fr(3,4*n))} exact_equal={U-L==Fr(3,4*n)} L<1/2<U={L<Fr(1,2)<U}")
print("Thm 2.1 example x^3-2x, sum upper/lower brackets -1 at n=1..256:",
      all((sum(f(Fr(i-1,n)) for i in range(1,n+1))/n) <= -1 <= (sum(f(Fr(i,n)) for i in range(1,n+1))/n) for n in (1,2,4,8,16,32,64,128,256)))
# part C and E3 (float, as the page states)
x, h = 0.3, 1e-6
central = ((x + h) / (1 + x + h) - (x - h) / (1 + x - h)) / (2 * h)
print("part C central =", f"{central:.8f}", " f(0.3) =", f"{1/(1.3)**2:.8f}", " abs diff =", abs(central - 1/(1.3)**2))
F3 = 6 / 1.3**4
print("F'''(0.3) =", round(F3, 4), " h^2 F'''/6 =", f"{h*h*F3/6:.2e}")
# Example 2.2: integral of 1/(1+x)^2 on [0,1] by the page's F
print("Example 2.2 F(1)-F(0) =", G(Fr(1)) - G(Fr(0)))
# Problem M3: F(x)=-1/(1+x) on [1,2]
print("M3 F(2)-F(1) =", Fr(-1, 3) - Fr(-1, 2))
# Problem M2: (3^3-1^3)/3
print("M2 =", Fr(3**3 - 1**3, 3))
