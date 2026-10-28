import math
from fractions import Fraction as F
# exact-rational recomputation of Lab 3 numbers (independent of the lab code)
L = 30_000_000; i_exact = F(45, 1000) / 12; n = 300
def pw(x, k): return x ** k
A = (1 - pw(1 + i_exact, -n)) / i_exact            # exact annuity factor
P_exact = L / A
P = math.floor(P_exact + F(1, 2))
bal = L; tot_int = 0; pays = 0; prin = 0
for m in range(1, n + 1):
    it = math.floor(bal * i_exact + F(1, 2))
    paid = P if m < n else bal + it
    pr = paid - it; bal -= pr; tot_int += it; pays += paid; prin += pr
print("level payment", P, "final payment", paid, "gap", paid - P, "final balance", bal)
print("principal sum == loan", prin == L, "total interest", tot_int, "total paid", pays)
# bound with float as the lab does, and with exact i
i = 0.00375
print("bound float", round(n * (1 + i) ** n + 1, 4), "bound exact-ish", float(n * (1 + i_exact) ** n + 1))
print("annuity factor", float(A))
# perpetuity: v^N / r, r = 0.05 exact
v = F(1, 1) / F(105, 100); r = F(5, 100)
N = 1
while v ** N / r >= F(1, 10**6): N += 1
print("least N", N, "error at N-1", float(v ** (N - 1) / r))
# growing perpetuity 1/(r-g) and 400-term tail
g = F(2, 100)
q = (1 + g) / F(105, 100)
print("tail q^400/(r-g)", float(q ** 400 / (r - g)))
s = sum(float(((1 + 0.02) ** (k - 1)) / (1.05 ** k)) for k in range(1, 401))
print("direct 400-term sum", s, "closed", 1 / 0.03)
print("(1+0.045/12)^12 =", float((1 + i_exact) ** 12), "> 1.045:", (1 + i_exact) ** 12 > F(1045, 1000))
print("annuity due factor", float(A * (1 + i_exact)))
print("month1 interest", math.floor(L * i_exact + F(1,2)), "principal", P - math.floor(L * i_exact + F(1,2)))
