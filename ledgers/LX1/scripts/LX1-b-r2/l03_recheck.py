"""Independent recomputation of LX1 L03 numbers (no imports from the lab twin). Uses floats and mpmath-free Decimal."""
from fractions import Fraction as F
from decimal import Decimal, getcontext, ROUND_HALF_UP
getcontext().prec = 50
D = F(1_000_000); N0 = F(4_000_000); d = F(1, 50); H = 12
def P(m, t): return (1 - d) ** min(t, m)
def V(m, t): return D / P(m, t)
def L(v): return v / (N0 - (v - D))
L0 = L(D)
def f(m, t): return L(V(m, t)) - L0
def depth(m): return max(f(m, t) for t in range(H + 1))
def first(m):
    path = [f(m, t) for t in range(H + 1)]; top = max(path)
    return next(t for t, x in enumerate(path) if x == top)
def dec(x, p): return Decimal(x.numerator) / Decimal(x.denominator)
def rnd(x, p):
    return (dec(x, p)).quantize(Decimal(1).scaleb(-p), rounding=ROUND_HALF_UP)
print("P4 exact", P(4, 4), float(P(4, 4)), "V4 exact", float(V(4, 4)), "V4 round", rnd(V(4,4),0))
print("N4 exact", float(N0 - (V(4,4) - D)), "N4 round", rnd(N0 - (V(4,4) - D), 0))
print("L4 exact", float(L(V(4,4))), "L4 round4", rnd(L(V(4,4)), 4))
print("V12 X exact", float(V(12, 12)), "round", rnd(V(12,12), 0))
print("L0", float(L0))
print("depth X exact %", float(100*depth(12)), "rounded", rnd(100*depth(12), 2))
print("depth Y exact %", float(100*depth(4)), "rounded", rnd(100*depth(4), 2))
print("X first", first(12), "Y first", first(4))
print("diff exact %", float(100*(depth(12)-depth(4))), "rounded", rnd(100*(depth(12)-depth(4)), 2))
print("diff of rounded", rnd(100*depth(12),2) - rnd(100*depth(4),2))
print("ratio exact", float(depth(12)/depth(4)), "rounded", rnd(depth(12)/depth(4), 4))
for phi, beta in ((F(1,2), F(1)), (F(1), F(1)), (F(3), F(1))):
    r = (phi*beta*depth(12)) / (phi*beta*depth(4)); print("ratio with phi,beta", phi, beta, rnd(r,4))
print("depth exact by m (%):")
for m in range(H+1):
    print(m, float(100*depth(m)), rnd(100*depth(m), 2))
print("strict steps", all(depth(m) < depth(m+1) for m in range(H)))
print("ratio of depths X/Y exact:", depth(12)/depth(4), "float", float(depth(12)/depth(4)))
# closed form check Proposition 3.2(b)
C = N0 + D
ell = lambda x: x / (C - x)
for m in (4, 12):
    vm = D * (1 - d) ** (-m)
    print("closed form m", m, float(100*(ell(vm)-ell(D))), float(100*depth(m)))
# R2 (note): check ratio for the square premium counterexample
for m in (4, 12):
    pass
r_lin = (ell(D*(1-d)**(-12)) - ell(D)) / (ell(D*(1-d)**(-4)) - ell(D))
r_sq = r_lin**2
print("linear ratio", float(r_lin), "square-premium ratio", float(r_sq))
# verify square premium claim: depth with phi*(L-L0)^2
def depth_sq(m):
    return max((L(V(m,t)) - L0)**2 for t in range(H+1))
print("square-premium ratio direct", float(depth_sq(12)/depth_sq(4)))
# Problem R2 type G strictly increasing: confirm 1-d relation
print("1-d", float(1-d), "V_m < C check", float(V(12,12)), float(C))
