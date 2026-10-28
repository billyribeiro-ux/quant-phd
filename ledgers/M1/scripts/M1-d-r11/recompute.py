# Independent recomputation of the numbers on project.html (exact Fractions and 50-digit Decimal).
from fractions import Fraction as F
from decimal import Decimal as D, getcontext, ROUND_FLOOR
import math
getcontext().prec = 60

def near_cent(x):  # x non-negative Fraction or Decimal; tie goes up
    if isinstance(x, F):
        return math.floor(x + F(1, 2))
    return int((x + D("0.5")).to_integral_value(rounding=ROUND_FLOOR))

# Lab 3 loan: exact monthly rate from 4.50% / 12
L = 30_000_000; n = 300
i = F(45, 1000) / 12
v = 1 / (1 + i)
a = (1 - (1 + i) ** -n) / i
P0 = L / a                      # exact payment (Fraction)
P = near_cent(P0)
print("exact payment cents", float(P0), "rounded", P)
bal = F(L); bal_c = L; ints = 0; princ = 0; paid = 0
for k in range(1, n + 1):
    interest = near_cent(F(bal_c) * i)
    pay = P if k < n else bal_c + interest
    pr = pay - interest
    bal_c -= pr
    ints += interest; princ += pr; paid = pay
    if k == 1: first = (pay, interest, pr)
print("month1", first, "final payment", paid, "diff", paid - P, "final bal", bal_c, "principal sum ok", princ == L)
print("total interest", ints, "total paid", ints + L)
bound = n * (1 + D(45) / D(12000)) ** n + 1
print("bound n(1+i)^n+1 =", bound.quantize(D("0.0001")))
print("final-minus-level within bound", abs(paid - P) <= bound)
# annuity factor (float) and due
ia = D(45) / D(12000)
af = (1 - (1 + ia) ** -n) / ia
print("annuity factor", af.quantize(D("0.000000001")), "due", (af * (1 + ia)).quantize(D("0.000000001")))
# lab 3 growing perpetuity and 400-term sum
r = D("0.05"); g = D("0.02")
print("growing perp", (1 / (r - g)).quantize(D("0.000000001")))
q = (1 + g) / (1 + r)
s = sum(((1 + g) ** (k - 1)) / ((1 + r) ** k) for k in range(1, 401))
print("400-term sum", s.quantize(D("0.000000001")), "exact tail", ((q ** 400) / (r - g)))
print("sum+tail check", (1 / (r - g) - s))
v5 = 1 / (1 + r)
N = 1
while v5 ** N / r >= D("1e-6"):
    N += 1
print("least N", N, "error at N-1", v5 ** (N - 1) / r)
print("error at 344 =", (v5 ** 344 / r))
# Lab 1 and Lab 2 quick checks
i1 = D("0.06") / 12
print("lab1 factor", ((1 - (1 + i1) ** -360) / i1).quantize(D("0.000001")))
a1 = (1 - (1 + i1) ** -360) / i1
p1 = near_cent(F(25_000_000) / F(a1))  # approximate in Fraction of Decimal
print("lab1 payment", p1)
