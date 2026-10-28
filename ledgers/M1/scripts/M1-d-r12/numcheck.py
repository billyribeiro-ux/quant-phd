import math
from decimal import Decimal, localcontext
from fractions import Fraction
def naive(r,n): return (1-(1+r)**-n)/r
def exact(r,n):
    with localcontext() as c:
        c.prec=80
        R=Decimal(repr(r)); return float((1-(1+R)**(-n))/R)
def expm1f(r,n): return -math.expm1(-n*math.log1p(r))/r
for r,n in [(5e-10,100000),(1e-10,100000),(1e-12,100000),(1e-12,10**6),(1e-14,10**6)]:
    e=exact(r,n)
    print(f"r={r} n={n} exact={e!r} naive_rel_err={abs(naive(r,n)-e)/e:.3e} expm1_rel_err={abs(expm1f(r,n)-e)/e:.3e} zero_rule_rel_err={abs(n-e)/e:.3e}")
print("zero rule exact 99997.5:", exact(5e-10,100000), (100000-exact(5e-10,100000))/exact(5e-10,100000))
