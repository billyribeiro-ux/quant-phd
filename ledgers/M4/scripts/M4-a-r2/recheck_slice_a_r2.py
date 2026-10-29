# Independent recomputation for M4-a round 2 (verifier scratch; exact Fractions, no reuse of builder code)
from fractions import Fraction as F
import math, random, itertools

def Q_def(law, p):
    # inf{x : F(x) >= p} over support points (law: list of (x, prob) sorted by x)
    cands = [x for x, _ in law if sum(q for y, q in law if y <= x) >= p]
    return min(cands)
def Q_strict(law, p):
    cands = [x for x, _ in law if sum(q for y, q in law if y <= x) > p]
    return min(cands) if cands else None
def F_(law, x): return sum(q for y, q in law if y <= x)

out = []
# L01 table
L01 = [(-2, F(1,10)), (-1, F(2,10)), (0, F(3,10)), (1, F(2,10)), (2, F(1,10)), (3, F(1,10))]
out.append(("L01 F", [str(F_(L01, x)) for x, _ in L01]))
probes = [F(1,20),F(1,10),F(11,100),F(1,2),F(3,5),F(61,100),F(9,10),F(91,100),F(99,100),F(1)]
out.append(("L01 Q", [Q_def(L01,p) for p in probes]))
grid = [F(j,100) for j in range(1,101)]
out.append(("L01 F(Q(p))>=p count", sum(F_(L01,Q_def(L01,p))>=p for p in grid)))
out.append(("L01 Q(F(x)+1e-9)", [Q_def(L01, F_(L01,x)+F(1,10**9)) for x,_ in L01[:-1]]))
# Example 3.5 indices
out.append(("ceil 0.99*150", math.ceil(F(99,100)*150), "ceil 0.99*200", math.ceil(F(99,100)*200)))
# Prop 3.4 / misconception 3: F_149 and F_148 vs 0.99 for n=150
out.append(("F_148,F_149 of 150 uniform", F(148,150) >= F(99,100), F(149,150) >= F(99,100), float(F(148,150)), float(F(149,150))))
# Strict-rule claim (R1 solution): Q^s(p)=Q(p) for every p in (0,1) not equal to F_k (k<m), and Q^s(F_k)=x_{k+1}
L01s = L01
ok = True; bad = []
fk = [F_(L01s,x) for x,_ in L01s]
# test on a dense rational grid plus all F_k
test_ps = set(F(j, 997) for j in range(1, 997)) | set(fk[:-1])
for p in sorted(test_ps):
    if p >= 1: continue
    if p in fk[:-1]:
        k = fk.index(p)
        if Q_strict(L01s,p) != L01s[k+1][0]: ok=False; bad.append(('F_k',p))
    else:
        if Q_strict(L01s,p) != Q_def(L01s,p): ok=False; bad.append(('other',p))
out.append(("R1 strict-rule claim holds on test grid", ok, bad[:3]))
# L02 numbers
die = [(k, F(1,6)) for k in range(1,7)]
mu = sum(x*p for x,p in die); m2 = sum(x*x*p for x,p in die)
out.append(("die", mu, m2, m2-mu*mu, float(math.sqrt(m2-mu*mu))))
loss = [(0,F(19,20)),(250000,F(1,20))]
mul = sum(x*p for x,p in loss); m2l = sum(x*x*p for x,p in loss); vl = m2l-mul*mul
out.append(("loss", mul, m2l, vl, f"{math.sqrt(vl):.2f}", vl/10000, math.sqrt(vl)/100))
out.append(("M2 problem", sum(x*p for x,p in [(0,F(9,10)),(50000,F(1,10))]), F(2.25e8)==F(225000000)))
out.append(("ex2.6 inner", 250000**2*F(1,20)))
# L02 seeded numbers (independent re-run)
rng = random.Random(2026); rolls=[rng.randint(1,6) for _ in range(10000)]
mean = sum(rolls)/10000; var = sum((x-mean)**2 for x in rolls)/10000
out.append(("die seed2026", f"{mean:.3f}", f"{var:.3f}", f"{mean-3.5:+.3f}"))
rng = random.Random(2027); losses=[250000 if rng.random()<0.05 else 0 for _ in range(10000)]
out.append(("loss seed2027", sum(1 for x in losses if x>0), sum(losses), f"{sum(losses)/10000:.1f}"))
# L03 numbers
S=[(0,F(1,2)),(1,F(1,4)),(2,F(1,8)),(10,F(1,8))]
mu3=sum(x*p for x,p in S); mm=lambda k: sum(((x-mu3)**k)*p for x,p in S)
m2s,m3s,m4s=mm(2),mm(3),mm(4)
out.append(("L03 moments", mu3, m2s, m3s, m4s, m3s**2/m2s**3, m4s/m2s**2))
out.append(("L03 m3 term sums", F(-1372,512)+F(-54,512)+F(1,512)+F(35937,512), F(35937,512)-m3s, F(-1372-54+1,512)))
out.append(("L03 m4 terms", sum(((x-mu3)**4)*p for x,p in S)==m4s, F(2401,512)))
out.append(("skew float", f"{float(m3s)/float(m2s)**1.5:.4f}", f"{float(m4s/m2s**2):.4f}"))
rng=random.Random(2026); draws=rng.choices([0,1,2,10],weights=[4,2,1,1],k=20000)
n=len(draws); mu_d=sum(draws)/n
s2=sum((x-mu_d)**2 for x in draws)/n; s3=sum((x-mu_d)**3 for x in draws)/n; s4=sum((x-mu_d)**4 for x in draws)/n
out.append(("L03 sample", f"{s3/math.pow(s2,1.5):.3f}", f"{s4/(s2*s2):.3f}", round(float(m3s)/float(m2s)**1.5 - s3/math.pow(s2,1.5),3), round(float(m4s/m2s**2) - s4/(s2*s2),3)))
# Bernoulli closed forms
for pp in [F(1,10), F(1,4)]:
    qq=1-pp
    bm = [(0,qq),(1,pp)]
    bmu = pp
    b2 = sum(((x-bmu)**2)*p for x,p in bm); b3=sum(((x-bmu)**3)*p for x,p in bm); b4=sum(((x-bmu)**4)*p for x,p in bm)
    out.append(("Bern", pp, b3**2/b2**3, (1-2*pp)**2/(pp*qq), b4/b2**2, (1-3*pp*qq)/(pp*qq)))
# canon example -2,1,3 with 2/5,1/2,1/10
C=[(-2,F(2,5)),(1,F(1,2)),(3,F(1,10))]
cm=sum(x*p for x,p in C); cmm=lambda k: sum(((x-cm)**k)*p for x,p in C)
out.append(("canon", cm, cmm(3), cmm(2), cmm(4), cmm(4)/cmm(2)**2))
# L04 tables
D={(0,0):F(1,10),(0,1):F(3,10),(1,0):F(2,10),(1,1):F(2,10),(2,0):F(1,10),(2,1):F(1,10)}
PXd={};PYd={}
for (x,y),p in D.items(): PXd[x]=PXd.get(x,0)+p; PYd[y]=PYd.get(y,0)+p
out.append(("L04 marg", PXd, PYd, PXd[0]*PYd[0], D[(0,0)]/(PXd[0]*PYd[0])))
cond = {y: sum(x*p for (x,yy),p in D.items() if yy==y)/PYd[y] for y in PYd}
out.append(("L04 cond", cond, sum(cond[y]*PYd[y] for y in PYd), sum(x*p for (x,y),p in D.items())))
out.append(("L04 E3 ratio", (F(1,10))/(F(4,25)), F(1,3)/F(1,9)))
out.append(("L04 M1 M2", F(1,10)*0+F(0.1), (F(3,10)*F(4,10)) if False else F(3,10)*F(4,10)))
# independent product table
PX2={0:F(1,5),1:F(2,5),2:F(2,5)}; PY2={0:F(3,10),1:F(7,10)}
out.append(("product cell", PX2[0]*PY2[0]))
# R1 of L04: Y=|X|
U=[(-1,F(1,3)),(0,F(1,3)),(1,F(1,3))]
out.append(("L04 R1", sum(x*p for x,p in U), sum(abs(x)*p for x,p in U), sum(x*abs(x)*p for x,p in U)))
# Prop 2.4 (L03) and kappa>=1 on random finite laws
rnd=random.Random(1); worst=None
for _ in range(2000):
    k=rnd.randint(2,5); xs=sorted(rnd.sample(range(-9,10),k))
    ws=[rnd.randint(1,9) for _ in xs]; tot=sum(ws); law=[(x,F(w,tot)) for x,w in zip(xs,ws)]
    m=sum(x*p for x,p in law); v=sum(((x-m)**2)*p for x,p in law)
    if v==0: continue
    kap=sum(((x-m)**4)*p for x,p in law)/v**2
    if kap<1: worst=('viol',law)
out.append(("kappa>=1 random 2000 laws (no violation => None)", worst))
for line in out: print(line)
