"""Independent recomputation of the numbers on E5 hub, L01, L02, L03 (verifier round 1, slice E5-a)."""
import math
from decimal import Decimal, getcontext
from fractions import Fraction as F

out = []
def p(*a):
    out.append(" ".join(str(x) for x in a))

# ---- L01 ----
p0a, q0a, p1a, q1a = (2, 5), (10, 4), (3, 5), (8, 6)
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
La = F(dot(p1a, q0a), dot(p0a, q0a)); Pa = F(dot(p1a, q1a), dot(p0a, q1a))
p0b, q0b, p1b, q1b = (1, 1), (1, 9), (2, 1), (9, 1)
Lb = F(dot(p1b, q0b), dot(p0b, q0b)); Pb = F(dot(p1b, q1b), dot(p0b, q1b))
p("L01 basket A", La, Pa, La - Pa, float(La - Pa), "basket B", Lb, Pb, Lb - Pb)
p("L01 log 1.25", math.log(1.25), "log 27/23", math.log(27/23), "log 1.1", math.log(1.1), "1.1-ln1.1", 1.1-1-math.log(1.1))
p("L01 x-ln(1+x) at .01,.05,.25", [round(x-math.log(1+x),9) for x in (0.01,0.05,0.25)])
nom = F(1100, 995) - 1; real = (F(1100)/(F(27,23))) / 995 - 1; pi = F(27,23) - 1
p("L01 nominal", float(nom), "real", float(real), float(real), "defl", float(pi), "identity", (1+nom) == (1+real)*(1+pi))
p("L01 E3 real period1", F(1100)/F(27,23), "1565/26865 check", F(-1565,26865) == real)
p("L01 M1 Y", 400+120+150+60-75, "M2 P", F(18,14), float(F(18,14)), "M3 ln1.1", math.log(1.1))
p("L01 R2 price per quality", F(3,2)/F(2,1)-1, "index", F(3,2)-1)
p("L01 flour bread GDP", 10)
p("L01 proof P1 scaling", "algebraic; checked by numeric lambda=2.5 below")
lam = 2.5; pb = [F(v)*F(5,2) for v in p0a]
p("L01 P1 numeric", float(F(sum(a*b for a,b in zip(pb,q0a)), dot(p0a,q0a))), float(F(sum(a*b for a,b in zip(pb,q1a)), dot(p0a,q1a))))

# ---- L02 ----
rng_seed = None
import random
ALPHA=0.3; H=40; SEED=2026
rng = random.Random(SEED)
A=[1.0]; K=[100.0]; L=[50.0]
for _ in range(H):
    A.append(A[-1]*math.exp(rng.uniform(0.005,0.02)))
    K.append(K[-1]*math.exp(rng.uniform(0.02,0.05)))
    L.append(L[-1]*math.exp(rng.uniform(0.0,0.015)))
Y=[a*k**ALPHA*l**(1-ALPHA) for a,k,l in zip(A,K,L)]
lg=lambda x:[math.log(x[t])-math.log(x[t-1]) for t in range(1,len(x))]
dY,dK,dL,dA=lg(Y),lg(K),lg(L),lg(A)
res=lambda al:[y-al*k-(1-al)*l for y,k,l in zip(dY,dK,dL)]
mean=lambda v:sum(v)/len(v)
p("L02 gap", max(abs(r-a) for r,a in zip(res(ALPHA),dA)))
p("L02 means", mean(dY), ALPHA*mean(dK), (1-ALPHA)*mean(dL), mean(res(ALPHA)))
mY=mean(dY); p("L02 shares", ALPHA*mean(dK)/mY, (1-ALPHA)*mean(dL)/mY, mean(res(ALPHA))/mY)
r2,r4=mean(res(0.2)),mean(res(0.4))
p("L02 alt residuals", r2, r4, "diff", r2-r4, "0.2*(meanK-meanL)", 0.2*(mean(dK)-mean(dL)))
simple=[Y[t]/Y[t-1]-1 for t in range(1,len(Y))]
p("L02 simple mean", mean(simple), "log mean", mY)
p("L02 E2 implied meanK", 0.010667/0.3, "meanL", 0.005327/0.7, "E3 alpha .4 cap term", 0.4*0.010667/0.3)
p("L02 misc3", 1.1**0.3, 1.1**0.3-1, 0.3*math.log(1.1), 0.3*0.10)
p("L02 M2 0.3ln2", 0.3*math.log(2))
p("L02 R3 residual", 0.01-0.3*0.05-0.7*0)
# only-when counterexample: dlnK == dlnL in every period, alpha_true = 0.3, test alpha = 0.5
kk=[1.0]; ll=[1.0]; aa=[1.0]
g=0.03
for t in range(5):
    kk.append(kk[-1]*math.exp(g)); ll.append(ll[-1]*math.exp(g))
    aa.append(aa[-1]*math.exp(0.01))
yy=[a*k**0.3*l**0.7 for a,k,l in zip(aa,kk,ll)]
dy=lg(yy); dk=lg(kk); dl=lg(ll); da=lg(aa)
for al in (0.3,0.5,0.9):
    r=[y-al*k-(1-al)*l for y,k,l in zip(dy,dk,dl)]
    p("L02 only-when witness alpha",al,"max|Res-dlnA|", max(abs(x-z) for x,z in zip(r,da)))

# ---- L03 ----
getcontext().prec = 60
al=Decimal("0.3"); s=Decimal("0.2"); d=Decimal("0.05"); n=Decimal("0.01")
ks=(s/(n+d))**(1/(1-al))
p("L03 k*", ks.quantize(Decimal("1e-10")), "y*", (ks**al).quantize(Decimal("1e-10")))
p("L03 k* float", float(ks), "(10/3)^(10/7) float", (10/3)**(10/7))
p("L03 dk/ds", ks/((1-al)*s), "dk/dd", -ks/((1-al)*(n+d)), "elast", s/ks*(ks/((1-al)*s)))
step=lambda k:(s*k**al+(1-d)*k)/(1+n)
k=Decimal(1); first=-1
for t in range(1,1001):
    k=step(k)
    if first<0 and abs(k-ks)<Decimal("1e-12"): first=t
p("L03 first period gap<1e-12", first)
p("L03 ratio gap100/gap50 (printed values)", Decimal("0.0805861272")/Decimal("0.6623874908"))
p("L03 E2 change", Decimal("0.01")*Decimal("39.8879393156"), Decimal("0.3988793932")/ks, "10/7*0.05", Decimal(10)/7*Decimal("0.05"))
p("L03 E3", Decimal("0.001")*Decimal("-132.9597977186"))
p("L03 M2 k2", ((F(1,4))*F(23,20)**0 ) , float((Decimal(1)/4)*Decimal("1.15").sqrt()+Decimal("0.9")*Decimal("1.15")))
p("L03 M1 k*", F(5,2)**2, "y*", F(5,2), "c*", F(3,4)*F(5,2))
p("L03 M3", F(25,4)/(F(1,2)*F(1,4)), -(F(25,4))/(F(1,2)*F(1,10)))
# convergence / sign grid
grid=[Decimal(i)/5 for i in range(1,51)]
below=sum(1 for x in grid if x<ks); mism=sum(1 for x in grid if (step(x)>x)!=(x<ks))
p("L03 grid below", below, "above", 50-below, "mismatch", mism)

print("\n".join(out))
