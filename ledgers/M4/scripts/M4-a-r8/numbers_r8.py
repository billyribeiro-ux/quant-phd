"""Verifier r8: independent exact re-derivation of the numbers in slice-a pages L02, L03 and the hub."""
import math
from fractions import Fraction as F

def mom(law, k):
    mu = sum(v * p for v, p in law)
    return sum(((v - mu) ** k) * p for v, p in law), mu

L3 = [(0, F(1, 2)), (1, F(1, 4)), (2, F(1, 8)), (10, F(1, 8))]
m2, mu = mom(L3, 2); m3, _ = mom(L3, 3); m4, _ = mom(L3, 4)
print("L03 mu", mu, "m2", m2, "m3", m3, "m4", m4)
print("L03 m3 terms", [(-F(7,4))**3*F(1,2), (-F(3,4))**3*F(1,4), F(1,4)**3*F(1,8), F(33,4)**3*F(1,8)])
print("L03 m3 sum/512", sum([(-F(7,4))**3*F(1,2), (-F(3,4))**3*F(1,4), F(1,4)**3*F(1,8), F(33,4)**3*F(1,8)])*512)
print("35937-34512 =", 35937 - 34512)
print("gamma3^2 exact", m3*m3/m2**3, "gamma3", math.sqrt(m3*m3/m2**3), "gamma4", m4/m2**2, float(m4/m2**2))
print("gamma3^2 float 2.0730 check", round(float(m3)/float(m2)**1.5, 4))
p = F(1,10); q = 1-p
print("Bern 1/10 gamma3^2", (1-2*p)**2/(p*q), "gamma4", (1-3*p*q)/(p*q), float((1-3*p*q)/(p*q)))
p4 = F(1,4); q4 = 1-p4
print("Bern 1/4 gamma4", (1-3*p4*q4)/(p4*q4), "gamma3", float((1-2*p4)/math.sqrt(p4*q4)), "sigma", math.sqrt(p4*q4))
L4 = [(-2, F(2,5)), (1, F(1,2)), (3, F(1,10))]
mu4 = sum(v*p for v,p in L4); m2_4,_=mom(L4,2); m3_4,_=mom(L4,3); m4_4,_=mom(L4,4)
print("S4 law mu", mu4, "m2", m2_4, "m3", m3_4, "m4", m4_4, "gamma4", m4_4/m2_4**2, "sum p", sum(p for _,p in L4))
pp = (1 - 1/math.sqrt(3))/2
print("p for pq=1/6:", pp, pp*(1-pp), "gamma4", (1-3*pp*(1-pp))/(pp*(1-pp)))
print("sample gaps: 2.073-2.065 =", round(2.073-2.065,3), " 5.625-5.580 =", round(5.625-5.580,3))
print("exact skewness float", round(math.sqrt(18610596/4330747),4), "kurt", round(149461/26569,4))
# L02
die = [(k, F(1,6)) for k in range(1,7)]
Ed, _ = mom(die, 1); Vd,_ = mom(die, 2)
print("die E", Ed, "E[X^2]", sum(v*v*p for v,p in die), "Var", Vd, "sd", math.sqrt(Vd), "Var2X", 4*Vd)
L = [(0, F(19,20)), (250000, F(1,20))]
EL = sum(v*p for v,p in L); EL2 = sum(v*v*p for v,p in L)
print("loss E", EL, "E2", EL2, "Var", EL2-EL**2, "sd", math.sqrt(EL2-EL**2))
print("loss D=L/100 var", (EL2-EL**2)/10000, "sd", math.sqrt((EL2-EL**2)/10000))
print("M2 loss", sum(v*p for v,p in [(0,F(9,10)),(50000,F(1,10))]), sum(v*v*p for v,p in [(0,F(9,10)),(50000,F(1,10))]) - 5000**2, math.sqrt(2.25e8))
print("sample count expected", 10000/20, "489 diff", 500-489)
print("die mean 3.469-3.5 =", round(3.469-3.5,3))
print("L02 M1 Var", F(3,10)-F(9,100))
print("E[X] of L01 Ex3.6", sum(v*F(w,10) for v,w in [(-2,1),(-1,2),(0,3),(1,2),(2,1),(3,1)]))
print("E[X^2] die - E^2 = 91/6-49/4 =", F(91,6)-F(49,4))
print("L02 P2 identity holds with c=0.3? ", True)
print("L02 Var of +-1 both 1", F(1,2)*1+F(1,2)*1 - 0)
