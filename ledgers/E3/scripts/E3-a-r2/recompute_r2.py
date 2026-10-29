# Independent recomputation of the displayed numbers in E3 L01-L03 (round 2, verifier-written).
from decimal import Decimal as D, getcontext, ROUND_HALF_UP
from fractions import Fraction as F
import math
getcontext().prec = 50
def dsqrt(x): return D(x).sqrt()
def dln(x): return D(x).ln()
def dexp(x): return x.exp()
# ---- L01 Example 1.4 / M1 / M2 / M3 / Example 3.4 / R3
EV_A = F(0)*F(1,4)+F(100)*F(1,2)+F(400)*F(1,4); assert EV_A == 150
assert F(0)*F(1,4)+F(10000)*F(1,2)+F(160000)*F(1,4) == 45000
assert F(400,5)+F(2500)*F(3,10)+F(6400,2) == 4030 and 59 == 4 + 15 + 40 and 59**2 == 3481 and 4030-3481 == 549
assert F(1,3)*F(100)+F(1,2)*F(200) == F(400,3)
assert F(1,3)*50 + F(2,3)*175 == F(400,3)
assert (10+30)*F(1,2) == 20 and F(0)*F(1,4)+40*F(3,4) == 30
assert (5+3*10)*F(1,2)+(5+3*30)*F(1,2) == 65
assert ((F(1,2)*100+F(1,2)*0) == 50)
assert ((100+200)*0 == 0)
assert (F(0)+F(150)**2 + F(300)**2)/3 == 37500
assert F(1,4)*F(1,1)*0 == 0
assert F(1,3)*F(1,4)+F(2,3)*F(1,2) == F(5,12)
assert F(0,1) + F(1,2) == F(1,2)
print("L01 exact identities: PASS")
# B lottery quadratic (CU): 50 and 200 w.p. 1/2 -> (2500+40000)/2
assert (F(50)**2 + F(200)**2)/2 == 21250
assert (F(125)**2) != 21250
assert (F(45000)-F(37500)) == 7500
assert F(1,3)*45000 + F(2,3)*37500 == 40000
assert (F(0)*F(1,4)+F(100)*F(1,2)) == 50
print("L01 identities checked")
# ---- L02 Example 1.5
EsqrtW = D(1)/4*dsqrt(40) + D(1)/2*10 + D(1)/4*dsqrt(160)
CE = EsqrtW*EsqrtW
prem = D(100)-CE
print("L02 E sqrt W =", EsqrtW.quantize(D('1e-9')), " CE =", CE.quantize(D('1e-6')), " premium =", prem.quantize(D('1e-6')))
print("L02 CE cents (half up):", (CE*100).quantize(D(1), ROUND_HALF_UP), " premium cents:", (prem*100).quantize(D(1), ROUND_HALF_UP))
limit = D('4.5')
var = D(1800)
r_A = D('0.005')
# Part B gaps: CE(eps) for W = 100 + eps X, X in {-60:1/4, 0:1/2, 60:1/4}
def premium(eps):
    E = D(1)/4*dsqrt(100-60*eps) + D(1)/2*dsqrt(100) + D(1)/4*dsqrt(100+60*eps)
    ce = E*E
    return 100 - ce
for e in ['1','0.5','0.25','0.1','0.01']:
    e = D(e)
    p = premium(e)
    ratio = p/(e*e)
    print("L02 eps", e, "premium/eps^2", ratio.quantize(D('1e-6')), "gap", abs(ratio-limit).quantize(D('1e-6')))
print("L02 error share of exact premium:", ((D('5.065835')-D('4.5'))/D('5.065835')*100).quantize(D('0.01')), "percent")
print("L02 error share of approx:", ((D('0.565835'))/D('4.5')*100).quantize(D('0.01')), "percent")
print("L02 half variance / exact premium:", (D(900)/D('5.065835')).quantize(D('0.01')))
print("L02 gap ratio 0.028811/0.004565 =", (D('0.028811')/D('0.004565')).quantize(D('0.0001')), " eps^2 ratio (0.25/0.1)^2 =", (D('0.25')/D('0.1'))**2)
# ---- L03 CRRA
prizes=[5000,10000,20000]; probs=[D(1)/4,D(1)/2,D(1)/4]
def ce(g):
    s = 1 - D(g)
    if s == 0:
        return dexp(sum(p*dln(x) for p,x in zip(probs,prizes)))
    M = sum(p*(D(x)**s) for p,x in zip(probs,prizes))
    return M**(1/s)
for g in ['0','0.25','0.5','1','2','4']:
    c = ce(g)
    print("L03 gamma", g, "CE", c.quantize(D('1e-4')), "cents rounded", (c).quantize(D(1), ROUND_HALF_UP))
print("L03 gamma 2 exact 80000/9 =", (D(80000)/9).quantize(D('1e-4')))
M2 = D(1)/4*D(1)/1000 + D(3)/4*D(1)/9000
print("L03 M2 CE2 =", 1/(D(1)/4*D(1)/1000 + D(3)/4*D(1)/9000))
print("L03 M3 CE2(3X) =", 1/(D(1)/4*D(1)/3000 + D(3)/4*D(1)/27000))
print("L03 Ex 2.5: CE2 =", 1/(D(1)/2*D(1)/1000 + D(1)/2*D(1)/4000), " CE1 =", (dexp(D(1)/2*dln(1000)+D(1)/2*dln(4000))).quantize(D('1e-6')))
# L03 M1: u_{1/2}, r_A(4)
print("L03 M1 r_A(4) direct:", (D(1)/2*D(4)**D('-1.5'))/D(4)**D('-0.5'))
# L03 E3 cents bound check on k=10
print("L03 bound (k+1)/2 at k=10:", (10+1)/2)
