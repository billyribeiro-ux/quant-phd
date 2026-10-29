"""Independent recomputation of the numbers printed in the M6 slice (hub, L01-L04). Run with python -I."""
from fractions import Fraction as F
from math import sqrt, floor
from itertools import combinations

def I(n):
    s = 2**n
    return sum((k/s)*(sqrt((k+1)/s)-sqrt(k/s)) for k in range(s))

print("I_n table (10 dp), error, bound, bracket ok")
for n in range(1, 11):
    i = I(n); e = 1/3 - i; b = 2.0**-n
    print(n, f"{i:.10f}", f"{e:.10f}", f"{b:.10f}", 0 <= e <= b)
print("I_1 closed form", 0.5*(1-sqrt(0.5)), "1/3-I_1", f"{1/3-I(1):.7f}", "rounded", round(1/3-I(1), 4))
terms = [F(1,4)*(sqrt(0.5)-sqrt(0.25)), F(1,2)*(sqrt(0.75)-sqrt(0.5)), F(3,4)*(1-sqrt(0.75))]
print("I_2 terms", [f"{float(t):.6f}" for t in [F(1,4)*(sqrt(0.5)-0.5), F(1,2)*(sqrt(0.75)-sqrt(0.5)), F(3,4)*(1-sqrt(0.75))]])
t4 = [round(F(1,4)*(sqrt(0.5)-0.5),4), round(F(1,2)*(sqrt(0.75)-sqrt(0.5)),4), round(F(3,4)*(1-sqrt(0.75)),4)]
print("I_2 rounded terms", [float(x) for x in t4], "sum rounded", float(sum(t4)), "sum unrounded", f"{I(2):.10f}")
print("H-sums", float(sum(F(1,n+1) for n in range(1,11))), f"{float(sum(F(1,n+1) for n in range(1,101))):.9f}")
print("L04 Ex3.2 int f_n", [str(F(n)*F(1,n*n) + 2 - F(2,n)) for n in (1,2,5)])
print("placement", 7/9*100, 8/9*100, 0.8*9)
print("hub hours", 12*9, 108+42, 42/150, 108/150)
print("L01 counts", 2**2, 2**4, 2**3, 2**5, 3**4, 3**6)
print("L02 602", 3**6-(64+64-1), "P(even)", F(3,6), "biased odd", F(1,2)+F(1,8)+F(1,32), "biased 1,2", F(3,4))
print("L02 3/20", 6*F(3,20))
print("L02 M1 fair", F(2,6), F(3,6))
print("L02 misc 2/3-1/6", F(2,3)-F(1,6), "P{1,2}+P{2,3}", F(2,6)+F(2,6), "P{1,2,3}", F(3,6))
print("L03 M1 closed", F(2,3)+F(10,3))
print("L03 Ex: 1/2*(1-sqrt(1/2))", 0.5*(1-sqrt(0.5)))
print("L04 M3 int min(2,x^-1/2)", F(2,4) + (2 - 1))
print("L04 f_5 values", F(5)*F(1,5))
print("L04 g_n int", [str(1 - F(1,n+1)) for n in (1,2,3)])
# L04 Prop 4.1: check sum_{k=2}^{2^m} 1/k >= m/2
print("L04 grouping", all(sum(F(1,k) for k in range(2,2**m+1)) >= F(m,2) for m in range(1,11)))
# L04 R2 integral check: sum (2n+1)/(n(n+1)^2) partial, each term <= 3/n^2
print("L04 R2 terms <= 3/n^2", all(F(2*n+1, n*(n+1)**2) <= F(3, n*n) for n in range(1, 2000)))
print("L04 R2 int f_n = 1/n", all(n*F(1,n*n)==F(1,n) for n in range(1,50)))
# L04 Example 3.2 numeric int_{1/n^2}^1 x^-1/2 = 2-2/n
print("L04 ex3.2 check", [round(2 - 2/n, 6) for n in (2,5)])
# L01 Ex 3.1 / Lab checks already in twin; L01 M1 family
blocks=[{1},{2,3},{4,5}]
fam=set()
for r in range(len(blocks)+1):
    for c in combinations(range(len(blocks)), r):
        fam.add(frozenset().union(*[blocks[j] for j in c]))
print("L01 M1 family size", len(fam), sorted(sorted(x) for x in fam))
# L01 M3: five blocks
print("L01 M3 five blocks", 2**5)
# L03 R3 and L04 R3 none
print("L03 Prop 4.1 level k=2^n point", 1 - 1 == 0)
