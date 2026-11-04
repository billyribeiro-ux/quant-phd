# Independent exact recomputation for L03 (Fractions only; its own rounding). Does not import the twin.
from fractions import Fraction as F
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
import math
getcontext().prec = 60
D0, N0 = F(1000000), F(4000000)
delta = F(1, 50); H = 12
def P(m, t): return (1 - delta) ** min(t, m)
def V(m, t): return D0 / P(m, t)
def L(v): 
    n = N0 - (v - D0); assert n > 0; return v / n
L0 = L(D0)
def psi(m, t, phi): return phi * (L(V(m, t)) - L0)
def f(m, t, phi, beta): return beta * psi(m, t, phi)
def depth(m, phi, beta): return max(f(m, t, phi, beta) for t in range(H + 1))
def first(m, phi, beta):
    path = [f(m, t, phi, beta) for t in range(H + 1)]; top = max(path)
    return next(t for t in range(H + 1) if path[t] == top)
def rhu(x, p):  # round half up of an exact Fraction to p places, return string
    s = math.floor(x * 10**p + F(1, 2)); w, fr = divmod(s, 10**p); return f"{w}.{fr:0{p}d}"
def rint(x): return math.floor(x + F(1, 2))
one = F(1)
dX, dY = depth(12, one, one), depth(4, one, one)
print("depth X exact", float(dX), "->", rhu(100 * dX, 2), "first", first(12, one, one))
print("depth Y exact", float(dY), "->", rhu(100 * dY, 2), "first", first(4, one, one))
print("Y exact depth percent", float(100*dY), "X-Y exact percent", float(100*(dX-dY)), rhu(100*(dX-dY), 2))
print("printed-difference 9.20-2.69 =", F(920,100) - F(269,100))
print("X deeper", dX > dY)
ds = [depth(m, one, one) for m in range(H + 1)]
print("Part C", [rhu(100 * d, 2) for d in ds])
print("never falls", all(ds[m] <= ds[m+1] for m in range(H)), "strict", all(ds[m] < ds[m+1] for m in range(H)))
for phi, beta in ((F(1,2), one), (one, one), (F(3), one)):
    r = depth(12, phi, beta) / depth(4, phi, beta); print("ratio", phi, beta, float(r), rhu(r, 4), "exact", float(r))
r_exact = (L(V(12,12)) - L0) / (L(V(4,4)) - L0) if False else None
# closed form check Prop 3.2(b): depth(m) = beta*phi*(V_m/(N0+D-V_m) - D/N0)
for m in (4, 12):
    cf = V(m, m) / (N0 + D0 - V(m, m)) - D0 / N0
    print("closed form m", m, cf == depth(m, one, one))
# square-premium ratio
sq = ((L(V(12,12)) - L0) / (L(V(4,4)) - L0)) ** 2
print("square ratio", float(sq), rhu(sq, 6), "is ratio^2:", sq == (depth(12,one,one)/depth(4,one,one))**2)
# Part A rows for both economies, recomputed independently
ok = 0; tot = 0
for m in (12, 4):
    for t in range(H + 1):
        p = P(m, t); v = V(m, t); lev = L(v); ps = psi(m, t, one); fl = f(m, t, one, one)
        row = f"index {rhu(p,4)}; real debt {rint(v)} cents; leverage {rhu(lev,4)}; premium {rhu(ps,4)}; output fall {rhu(100*fl,2)} percent"
        tot += 1
print("rows computed", tot)
print("baseline leverage", rhu(L0, 4))
# quiz / M-solutions
V4 = V(4, 4); N4 = N0 - (V4 - D0); print("V4", float(V4), rint(V4), "N4", float(N4), rint(N4), "L4", float(V4/N4), rhu(V4/N4, 4))
print("V12", float(V(12, 12)), rint(V(12, 12)), "P4", P(4,4), float(P(4,4)))
print("V4 whole-cent N4 from rounded V4:", N0 - (rint(V4) - D0))
print("Y index t 5..12 unchanged count:", sum(1 for t in range(5, 13) if P(4, t) == P(4, t-1)))
print("Y index t 1..4:", [rhu(P(4,t),4) for t in range(1,5)], "t5..12:", [rhu(P(4,t),4) for t in range(5,13)])
# Remark 4.2 numeric: V12 < C
print("V12 < C=5000000:", V(12,12) < N0 + D0, " V_m<C for m=12 ok")
# E1 exact depth Y
print("E1 exact depth Y 2.686713 check:", float(100*dY))
# R-related: depth(0)
print("depth(0)", depth(0, one, one))
