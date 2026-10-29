"""Independent re-derivation of the numbers printed in M4 hub and lessons L01-L04 (verifier, round 6)."""
from fractions import Fraction as F
import math

def mean(law): return sum((v * p for v, p in law), F(0))
def cm(law, k):
    mu = mean(law); return sum(((v - mu) ** k * p for v, p in law), F(0))

# L01 Example 3.6 table and Def 3.1 quantile Q(p) = least x with F(x) >= p
L01 = [(-2, F(1, 10)), (-1, F(2, 10)), (0, F(3, 10)), (1, F(2, 10)), (2, F(1, 10)), (3, F(1, 10))]
def Fcdf(law, x): return sum((p for v, p in law if v <= x), F(0))
def Q(law, p): return min(v for v, _ in law if Fcdf(law, v) >= p)
def Qs(law, p): return min(v for v, _ in law if Fcdf(law, v) > p) if any(Fcdf(law, v) > p for v, _ in law) else None
print("L01 F:", [str(Fcdf(L01, v)) for v, _ in L01])
for p in [F(1,2), F(3,5), F(61,100), F(9,10), F(99,100), F(1)]:
    print("L01 Q(%s)=%s" % (p, Q(L01, p)))
print("L01 Qs(3/5)=", Qs(L01, F(3,5)), " Qs(1)=", Qs(L01, F(1)))
print("L01 mean of table =", mean(L01))
print("L01 index ceil(0.99*150)=", math.ceil(F(99,100)*150), " 148/150=", F(148,150), float(F(148,150)))
print("L01 index ceil(0.99*200)=", math.ceil(F(99,100)*200), " ceil(0.9*40)=", math.ceil(F(9,10)*40), " ceil(0.901*40)=", math.ceil(F(901,1000)*40))
# L01 hub skill check 1: 0,1,2 with 1/4,1/2,1/4 -> Q(1/2)
S1 = [(0, F(1,4)), (1, F(1,2)), (2, F(1,4))]
print("hub skill1 Q(1/2)=", Q(S1, F(1,2)))

# L02
DIE = [(k, F(1,6)) for k in range(1,7)]
LOSS = [(0, F(19,20)), (250000, F(1,20))]
def var(law): return cm(law, 2)
print("L02 die E=", mean(DIE), "E2=", sum((v*v*p for v,p in DIE), F(0)), "Var=", var(DIE), "Var(2X)=", var([(2*v,p) for v,p in DIE]))
print("L02 loss E=", mean(LOSS), "E2=", sum((v*v*p for v,p in LOSS), F(0)), "Var=", var(LOSS), "sd=", math.sqrt(var(LOSS)))
print("L02 R2 Var(D)=", var([(F(v,100),p) for v,p in LOSS]), "sd=", math.sqrt(var([(F(v,100),p) for v,p in LOSS])))
print("L02 M2 loss 50000 w.p.1/10 Var=", F(50000**2,10) - F(5000)**2, "sd=", math.sqrt(F(50000**2,10) - F(5000)**2))
print("L02 canon mean-of-table ok: (-2-2+0+2+2+3)/10 =", F(-2-2+0+2+2+3,10))
print("L02 E=(s)Var-only ex: E2 die=", float(F(91,6)), "var die=", float(F(35,12)))
print("hub skill2 s^2 =", F(3,5), " 1/(5/3)=", 1/F(5,3), " nu/(nu-2) nu=5:", F(5,3))

# L03
SK = [(0, F(1,2)), (1, F(1,4)), (2, F(1,8)), (10, F(1,8))]
m2, m3, m4 = cm(SK,2), cm(SK,3), cm(SK,4)
print("L03 mean", mean(SK), "m2", m2, "m3", m3, "m4", m4)
print("L03 gamma^2 =", m3*m3/(m2**3), " kappa=", m4/(m2*m2), float(m4/(m2*m2)), " gamma=", float(m3)/float(m2)**1.5)
print("L03 term of value 10:", F(33,4)**3 * F(1,8), " sum of 4 terms:", sum(((v-mean(SK))**3*p for v,p in SK), F(0)))
for p in [F(1,10), F(1,4)]:
    B = [(0, 1-p), (1, p)]
    q = 1-p
    print("L03 Bernoulli p=%s skew^2=%s closed=%s kappa=%s closed=%s gamma=%s" % (p, cm(B,3)**2/cm(B,2)**3, (1-2*p)**2/(p*q), cm(B,4)/cm(B,2)**2, (1-3*p*q)/(p*q), float((1-2*p)/math.sqrt(p*q))))
C = [(-2, F(2,5)), (1, F(1,2)), (3, F(1,10))]
print("L03 canon law mean", mean(C), "m3", cm(C,3), "m2", cm(C,2), "m4", cm(C,4), "kappa", cm(C,4)/cm(C,2)**2)
print("L03 M1 sigma^2 p=1/4:", F(3,16), " gamma=", 2/math.sqrt(3), " kappa=", F(7,3))
print("L03 sample gaps:", round(2.073-2.065,3), round(5.625-5.580,3), " exact skew", round(float(F(18610596,4330747))**0.5,6), " exact kurt", round(float(F(149461,26569)),6))

# L04
DEP = {(0,0):F(1,10),(0,1):F(3,10),(1,0):F(2,10),(1,1):F(2,10),(2,0):F(1,10),(2,1):F(1,10)}
px = {}; py = {}
for (x,y),p in DEP.items():
    px[x]=px.get(x,0)+p; py[y]=py.get(y,0)+p
print("L04 PX", px, "PY", py)
EX = sum((x*p for (x,y),p in DEP.items()), F(0))
print("L04 E[X]=", EX, " E[X|Y=0]=", sum((x*p for (x,y),p in DEP.items() if y==0), F(0))/py[0], " E[X|Y=1]=", sum((x*p for (x,y),p in DEP.items() if y==1), F(0))/py[1])
print("L04 total =", sum((sum((x*p for (x,y),p in DEP.items() if y==yy), F(0))/py[yy])*py[yy] for yy in py))
print("L04 M1 product 0.3*0.4=", F(3,10)*F(4,10), " M2 E[X|Y=1]=", F(4,10)/F(6,10))
print("L04 E3 ratio (1/10)/(4/25)=", F(1,10)/F(4,25), " E2 ratio (1/3)/(1/9)=", F(1,3)/F(1,9))
print("L04 R1 Y=|X| cov:", sum((x*abs(x)/3 for x in (-1,0,1)), F(0)) - F(0)*F(2,3))
print("L04 product table cell (0,0)=", F(1,5)*F(3,10))
