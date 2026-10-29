"""Recompute L04 prose numbers from first principles with exact/high-precision arithmetic."""
from decimal import Decimal as D, getcontext
from fractions import Fraction
import math
getcontext().prec = 60

def p(a):
    return (D(a + 1)).sqrt() - 1

p0 = p(D(120)); dp = 1 / (2 * D(121).sqrt())
print("p0", p0, "dp", dp, "dp=1/22?", abs(dp - D(1)/D(22)) < D("1e-50"))
print("elasticity a/p*dp", D(120)/p0*dp, "6/11", D(6)/D(11))
# exact change for 1% rise in a
pct = (p(D("121.2")) - p0)/p0*100
print("exact pct change in p* for a 120->121.2:", pct)
print("derivative-based pct:", D(120)/p0*dp*D("1"), "(elasticity*1%)")
# finite differences
def fd(h):
    h = D(h)
    up = p(D(120)+h); lo = p(D(120)-h)
    return (up-p0)/h, (up-lo)/(2*h)
err = {}
for h in ["1","0.1","0.01","0.001"]:
    f, c = fd(h)
    err[h] = (abs(f-dp), abs(c-dp))
    print("h",h,"fwd",f,"fwd_err",err[h][0],"cen",c,"cen_err",err[h][1])
ks = ["1","0.1","0.01","0.001"]
for i in range(3):
    print("fwd ratio", ks[i], "/", ks[i+1], err[ks[i]][0]/err[ks[i+1]][0])
    print("cen ratio", ks[i], "/", ks[i+1], err[ks[i]][1]/err[ks[i+1]][1])
print("fwd ratio h=0.01 vs central h=0.01:", err["0.01"][0]/err["0.01"][1])
# leading terms
lead_f = lambda h: D(h)/D(10648)
lead_c = lambda h: D(h)**2/D(2576816)
print("lead fwd at 0.001", lead_f(D("0.001")), "printed", err["0.001"][0], "ratio", err["0.001"][0]/lead_f(D("0.001")))
print("lead cen at 0.001", lead_c(D("0.001")), "printed", err["0.001"][1], "ratio-1", err["0.001"][1]/lead_c(D("0.001"))-1)
print("at h=1 central ratio", err["1"][1]/lead_c(D(1)), "fwd ratio", err["1"][0]/lead_f(D(1)))
print("p''(120) check", -D(1)/(4*D(121)**D("1.5")) if False else None)
# exact second/third derivatives via fractions
print("1/10648 =", Fraction(1,10648), " 1/5324 halved:", Fraction(-1,5324)/2)
print("p''' = 3/(8*121^(5/2)) = 3/(8*161051) =", Fraction(3,8*161051))
print("p'' = -1/(4*1331)=", Fraction(-1,4*1331), "(1/5324)")
print("central coef p'''/6 =", Fraction(3,1288408)/6, " 1/2576816 =", Fraction(1,2576816))
# remark 3.3
f2, c2 = fd("0.01")
print("h=0.01 fwd err", err["0.01"][0], "cen err", err["0.01"][1], "ratio", err["0.01"][0]/err["0.01"][1])
# Problem E2 claim
print("E2 0.5441088 check", pct)
print("Example 1.3 eps(10),eps(40) for Q=120-2p:", -2*D(10)/(120-2*D(10)), -2*D(40)/(120-2*D(40)))
print("M1 eps(10) Q=100-4p:", -4*D(10)/(100-4*D(10)))
print("R2 check", D(1)/(2*D(4).sqrt()))
