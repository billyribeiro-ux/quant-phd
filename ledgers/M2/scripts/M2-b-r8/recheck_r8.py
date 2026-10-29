from fractions import Fraction as F
import math
# L08 Example 2.4 ratio and bound
for n in range(0, 7):
    for x in [F(k, 20) for k in range(1, 11)]:
        bound = 2 ** (n + 2) * x ** (n + 1)
        exact = x ** (n + 1) / (1 - x)
        assert exact <= bound
        assert bound / exact == 2 ** (n + 2) * (1 - x)
        assert 2 ** (n + 1) <= bound / exact < 2 ** (n + 2)
print("L08 Ex2.4: bound holds at 70 pairs; ratio 2^(n+2)(1-x) in [2^(n+1), 2^(n+2)): OK")
# L08 M2 / E1 / E2 / E3 / R3
print("L08 M3 M=", F(2) / (F(3, 4) ** 3), "bound", F(128, 27) / 16 / 2, "exact", F(1, 16) / F(3, 4))
print("L08 E1 xi", 1 - 0.5 ** 0.2, "E2 xi", 1 - 0.7 ** (1 / 7), "M2 xi", 1 - 0.75 ** 0.25)
print("L08 E3", [round(0.6 ** (n + 1) / 0.4 ** (n + 2), 6) for n in range(1, 5)], [round(0.6 ** (n + 1) / 0.4, 6) for n in range(1, 5)])
print("L08 R3 bound at 1/2:", [2 ** (n + 2) * F(1, 2) ** (n + 1) for n in range(0, 4)])
# L11 integrals
def mid(f, a, b, n=100000):
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))
print("L11 A:", mid(lambda x: x*x*(1-x)**3, 0, 1), 1/60, "rhs", mid(lambda x: -2*x*(-(1-x)**4/4), 0, 1))
print("L11 Ex2.2 int x(1-x)^4 =", F(1,2)-F(4,3)+F(3,2)-F(4,5)+F(1,6))
print("L11 Ex3.2 int", F(1,3)+1+1+F(1,3))
print("L11 Ex3.3 int 1..2 x =", F(4-1,2), "int 0..1 (2t+2t^3) =", 1+F(1,2))
print("L11 M1 =", F(1,2)-F(2,3)+F(1,4), "M2 =", F(7,3), "M3 = int x^2(1-x)^2*3/2 =", F(3,2)*(F(1,3)-F(1,2)+F(1,5)), "direct", F(1,4)-F(1,5))
# E1: smallest N with 2/(3N^2) <= 1e-6
N = 1
while not (F(2, 3 * N * N) <= F(1, 10**6)):
    N += 1
print("L11 E1 smallest N", N, float(F(2, 3*816*816)), float(F(2, 3*817*817)))
# L11 R1 Beta recursion check small cases
from math import factorial as fa
for m in range(0, 5):
    for n in range(0, 5):
        I = F(fa(m) * fa(n), fa(m + n + 1))
        assert F(n + 1, m + 1) * F(fa(m + 1) * fa(n), fa(m + n + 2)) == F(fa(m) * fa(n + 1), fa(m + n + 2))
print("L11 R1 Beta identity: OK on 25 pairs")
# L12 P1 bound: sum_{k=2}^N k^-p <= int_1^N x^-p <= 1/(p-1)
for p in [2, 3]:
    s = sum(k ** -p for k in range(2, 2000))
    print("L12 P1 p=", p, "partial sum", round(s, 6), "bound 1/(p-1)", 1 / (p - 1), s <= 1 / (p - 1))
