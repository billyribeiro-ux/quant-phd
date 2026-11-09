# Independent recomputation of prose numbers in L08-L12 (python -I).
from fractions import Fraction as F
import math
# L08 M2: xi at x=1/4, n=2
print("L08 M2 xi", 1 - (3/4) ** (1/4))
print("L08 M2 P2(1/4)", 1 + 1/4 + 1/16, "remainder", 4/3 - 21/16, "x^3/(1-x)", (1/64)/(3/4))
# L08 E1: xi at x=0.5, n=3 ; R_3(0.5)
print("L08 E1 xi", 1 - 0.5 ** (1/5), "R", (0.5**4)/0.5)
# L08 E2: xi at x=0.3, n=5
print("L08 E2 0.7^(1/7)", 0.7 ** (1/7), "xi", 1 - 0.7 ** (1/7))
# L08 M3: sup and bound on [0,1/4] for n=1
print("L08 M3 M", 2/(3/4)**3, 128/27, "bound", (128/27)*(1/16)/2, 4/27, "exact", (1/16)/(3/4), 1/12)
# L08 E3 table at x=0.6
for n in range(1,5):
    print("L08 E3 n", n, 0.6**(n+1)/0.4**(n+2), 0.6**(n+1)/0.4)
# L09 Part B: nonuniform partition points (i/10)^2, f=x^2
pts=[F(i*i,100) for i in range(11)]
w=[pts[i]-pts[i-1] for i in range(1,11)]
U=sum((pts[i]**2)*w[i-1] for i in range(1,11)); L=sum((pts[i-1]**2)*w[i-1] for i in range(1,11))
print("L09 partB U-L", float(U-L), "mesh", float(max(w)))
# L09 E1,E2,E3
print("L09 E1 25/384", 25/384, "E2 1/3072", 1/3072, "E3 n=50", 151/15000, "n=51", 154/15606)
# L10 E3 central-difference truncation and derivative numbers
print("L10 E3 F'''(0.3)", 6/1.3**4, "trunc", (1e-6)**2*(6/1.3**4)/6)
# L12 E3 harmonic
H=sum(1/i for i in range(1,16385)); print("L12 E3 H16384-1", H-1)
# L10 R1 example check not needed; L10 lab numbers L_128 part B
print("L10 E2 L128 check (3/512)", 3/512)
# L11 E1 midpoint N=816/817 error
print("L11 E1 N=816", 2/(3*816**2), "N=817", 2/(3*817**2))
# L11 E2 residual
print("L11 E2 residual", 8/3 - 2.6666666663)
# L07 Example 1.5 and L12 R2 etc
print("L12 2^19 vs 1e6", 2**19, 2**20)
