# Independent exact recomputation for M4-a round 3 (run with python -I). Standard library only.
from fractions import Fraction as Fr
import math, itertools, random

def F_of(law, x):
    return sum((p for v, p in law if v <= x), Fr(0))
def Q_def(law, p):
    return min(v for v, _ in law if F_of(law, v) >= p)
def Q_strict(law, p):
    return min(v for v, _ in law if F_of(law, v) > p)

# L01 Example 3.6 table
L01 = [(-2, Fr(1,10)), (-1, Fr(2,10)), (0, Fr(3,10)), (1, Fr(2,10)), (2, Fr(1,10)), (3, Fr(1,10))]
print("L01 F:", [str(F_of(L01, v)) for v, _ in L01])
for p in [Fr(1,2), Fr(3,5), Fr(61,100), Fr(99,100), Fr(1)]:
    print("L01 Q", p, Q_def(L01, p))
grid = [Fr(j, 100) for j in range(1, 101)]
print("L01 Q(p)=1 set on rational grid of (0,1]: min p, max p:",
      min(p for p in [Fr(i, 1000) for i in range(1, 1001)] if Q_def(L01, p) == 1),
      max(p for p in [Fr(i, 1000) for i in range(1, 1001)] if Q_def(L01, p) == 1))
# R1 strict-rule claim on 996 rational p in (0,1) plus each F_k
Fk = [F_of(L01, v) for v, _ in L01]
test = sorted(set([Fr(i, 1000) for i in range(1, 1000)] + Fk))
test = [p for p in test if 0 < p < 1]
agree_except_Fk = all(Q_strict(L01, p) == Q_def(L01, p) for p in test if p not in Fk)
print("R1: agree at every non-F_k p in test set:", agree_except_Fk, "count", len(test))
print("R1: Q_strict(3/5)=", Q_strict(L01, Fr(3,5)), " Q_strict at F_k rule: p=F_k gives next value:",
      all(Q_strict(L01, Fk[i]) == L01[i+1][0] for i in range(len(L01)-1)))
# Example 3.5 indices
print("n=150 p=0.99 pn=", Fr(150)*Fr(99,100), "ceil", math.ceil(Fr(150)*Fr(99,100)), "floor", math.floor(Fr(150)*Fr(99,100)))
print("n=200 pn=", Fr(200)*Fr(99,100), "ceil", math.ceil(Fr(200)*Fr(99,100)))
print("M2 F(5)=", F_of([(2,Fr(1,5)),(5,Fr(1,2)),(7,Fr(3,10))],5), "Q(7/10)=", Q_def([(2,Fr(1,5)),(5,Fr(1,2)),(7,Fr(3,10))],Fr(7,10)), "Q(71/100)=", Q_def([(2,Fr(1,5)),(5,Fr(1,2)),(7,Fr(3,10))],Fr(71,100)))
print("M3 40*0.9=", 40*Fr(9,10), "40*0.901=", 40*Fr(901,1000), "ceil", math.ceil(40*Fr(901,1000)))
print("M1 Q(1/2)=", Q_def([(0,Fr(1,2)),(1,Fr(1,2))], Fr(1,2)))
print("quiz 1/4,1/2,1/4 Q(1/2)=", Q_def([(0,Fr(1,4)),(1,Fr(1,2)),(2,Fr(1,4))], Fr(1,2)))
# Q(p)=1 iff F(0) < p <= F(1), checked on grid
print("Q=1 iff 3/5<p<=4/5 on grid:", all((Q_def(L01,p)==1) == (Fr(3,5)<p<=Fr(4,5)) for p in test))

# L02
die = [(k, Fr(1,6)) for k in range(1,7)]
mu = sum(v*p for v,p in die); m2 = sum(v*v*p for v,p in die)
print("die mu", mu, "E[X^2]", m2, "Var", m2-mu*mu, "sd", float(m2-mu*mu)**0.5)
loss = [(0,Fr(19,20)),(250000,Fr(1,20))]
mL = sum(v*p for v,p in loss); mL2 = sum(v*v*p for v,p in loss)
VarL = mL2 - mL*mL
print("loss E", mL, "E2", mL2, "Var", VarL, "sd", math.sqrt(VarL))
print("Var(D) = Var(L)/10^4 =", VarL/10000, " sd_D =", math.sqrt(VarL/10000), " from 54486.24/100 =", 54486.24/100)
print("sqrt(296875) =", math.sqrt(296875))
print("E[X] of L01 table =", sum(v*p for v,p in L01), " Var(2X)=", 4*(m2-mu*mu))
print("M2 L02: E", sum(v*p for v,p in [(0,Fr(9,10)),(50000,Fr(1,10))]), "Var", Fr(50000)**2*Fr(1,10) - Fr(5000)**2, "sd", math.sqrt(2.25e8))
# L02 Var(X) for P(X=1)=3/10: Var
print("M1 L02 Var", Fr(3,10)-Fr(9,100))
# L02 P3 counterexample: U=+-1, V=-U
# seeds: printed in lab outputs (checked separately)
# L03
SK = [(0,Fr(1,2)),(1,Fr(1,4)),(2,Fr(1,8)),(10,Fr(1,8))]
mu3 = sum(v*p for v,p in SK)
def cm(law,k,mu): return sum(((v-mu)**k)*p for v,p in law)
m2_,m3_,m4_ = cm(SK,2,mu3), cm(SK,3,mu3), cm(SK,4,mu3)
print("L03 mu",mu3,"m2",m2_,"m3",m3_,"m4",m4_)
print("terms m3:", [str((v-mu3)**3*p) for v,p in SK], "sum*512", m3_*512, "35937-34512", 35937-34512)
print("skew^2", m3_**2/m2_**3, float(m3_**2/m2_**3), "skew", math.sqrt(float(m3_**2/m2_**3)), "kurt", m4_/m2_**2, float(m4_/m2_**2))
print("gap skew 2.073-2.065", round(2.073-2.065,3), "gap kurt 5.625-5.580", round(5.625-5.580,3))
for pp in [Fr(1,10), Fr(1,4)]:
    qq = 1-pp
    g = (1-2*pp)/ (float(pp*qq))**0.5
    print("Bern p",pp,"gamma",g,"kappa",(1-3*pp*qq)/(pp*qq), float((1-3*pp*qq)/(pp*qq)))
print("Bern skew 1/10 =", (Fr(8,10))/Fr(3,10))
ZS = [(-2,Fr(2,5)),(1,Fr(1,2)),(3,Fr(1,10))]
mz = sum(v*p for v,p in ZS); print("L03 §4 mean",mz,"m2",cm(ZS,2,mz),"m3",cm(ZS,3,mz),"m4",cm(ZS,4,mz),"kappa",cm(ZS,4,mz)/cm(ZS,2,mz)**2)
print("L03 M1 p=1/4: sigma", (3/16)**0.5, "gamma", 2/3**0.5, "kappa", Fr(7,16)/Fr(3,16))
print("L03 Bernoulli p=1/10 gamma", (1-2*Fr(1,10))/Fr(3,10), "gamma^2", ((1-2*Fr(1,10))/Fr(3,10))**2)
# R1 kurtosis claims: two-point unequal probability has kappa>1
for pp in [Fr(1,4), Fr(1,3)]:
    print("two-point p",pp,"kappa", (1-3*pp*(1-pp))/(pp*(1-pp)))
# L04
DEP = {(0,0):Fr(1,10),(0,1):Fr(3,10),(1,0):Fr(2,10),(1,1):Fr(2,10),(2,0):Fr(1,10),(2,1):Fr(1,10)}
pxd={}; pyd={}
for (x,y),p in DEP.items(): pxd[x]=pxd.get(x,0)+p; pyd[y]=pyd.get(y,0)+p
print("L04 PX", pxd, "PY", pyd)
print("L04 E[X]", sum(x*p for (x,y),p in DEP.items()), "E[X|Y=0]", sum(x*p for (x,y),p in DEP.items() if y==0)/pyd[0], "E[X|Y=1]", sum(x*p for (x,y),p in DEP.items() if y==1)/pyd[1])
print("L04 ratio (0,0):", DEP[(0,0)]/(pxd[0]*pyd[0]), "product", pxd[0]*pyd[0])
print("L04 Ex1.9 covariance:", sum(Fr(x)*Fr(x*x)*Fr(1,3) for x in (-1,0,1)) - 0)
print("L04 M1 product test:", [DEP[(0,0)] == pxd[0]*pyd[0]])
print("L04 R1 Y=|X| cov:", sum(Fr(x)*Fr(abs(x))*Fr(1,3) for x in (-1,0,1)) - 0, "E[Y]", sum(Fr(abs(x),3) for x in (-1,0,1)))
print("L04 Ex2.5 P(Y=1)", pyd[1], " E[X|Y=1] = 2/3 ->", Fr(2,10)*0 + Fr(1,1)*Fr(2,10)+Fr(2,1)*Fr(1,10), "/", pyd[1])
print("L04 marginal example: p00=1/2 vs 1/4")
# Exact L04 marginals test (M1 of L04): p00 0.1, p01 0.2, p10 0.3, p11 0.4
print("L04 M1: P(X=0)P(Y=0)=", Fr(3,10)*Fr(4,10), "p00=", Fr(1,10))
print("L04 M3 product", Fr(1,4)*Fr(1,2), "E[XY]=", Fr(1,8))
print("L04 E3 (1/10)/(4/25)=", (Fr(1,10))/(Fr(4,25)))
