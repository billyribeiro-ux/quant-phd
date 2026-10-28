import math, sys, re
from fractions import Fraction as F
CK = "/tmp/verify10-CF1-c"
ns5 = {"__name__": "l05"}
src5 = open(f"{CK}/tests/labs/CF1/lab-CF1-L05-1.py").read().replace("\nmain()\n", "\n")
exec(compile(src5, "l05", "exec"), ns5)
ns6 = {"__name__": "l06"}
src6 = open(f"{CK}/tests/labs/CF1/lab-CF1-L06-1.py").read().replace("\nmain()\n", "\n")
exec(compile(src6, "l06", "exec"), ns6)

# L05 numbers
A, B, D = ns5["PROJECT_A"], ns5["PROJECT_B"], ns5["PROJECT_D"]
pb = ns5["payback"]; disc = ns5["discount"]; npv = ns5["npv"]
print("A simple", pb(A), "disc", pb(disc(A, .1)), "B", pb(B), pb(disc(B, .1)), "D", pb(D), pb(disc(D, .1)))
print("npv A B D", npv(A, .1), npv(B, .1), npv(D, .1))
print("D NPV exact fraction-free", float(F(-1000000) + F(500000)/F(11,10) + F(500000)/F(121,100)))
print("gap", npv(A,.1)-npv(B,.1), "closed", 300000/1.1**4+200000/1.1**5+100000/1.1**6)
print("gap/A", (npv(A,.1)-npv(B,.1))/npv(A,.1), "gap/|B|", (npv(A,.1)-npv(B,.1))/abs(npv(B,.1)))
# tails range
print("ex 2.1 check: (-1000,0,0,0,1,1) NPV", -1000+1/1.1**4+1/1.1**5, "; (-1000,0,0,0,1000,0)", -1000+1000/1.1**4)
print("payback (-1000,0,0,0,1000,0)", pb([-1000,0,0,0,1000,0]), "first", pb([-1000,0,0,0,1,1]))
# A discounted cumulative
v=[a/1.1**t for t,a in enumerate(A)]; cum=0; out=[]
for x in v: cum+=x; out.append(round(cum,4))
print("A disc cum", out, "B disc cum", [round(sum(B[:t+1][i]/1.1**i for i in range(t+1)),4) for t in range(7)])
# E1 range
print("E1 range cents", 693692.91-121251.71, "units", (693692.91-121251.71)/100)
# M1 M2 M3
print("M2 terms", 400/1.1, 400/1.1**2, 400/1.1**3, 400/1.1**4, "sum3 unrounded", 400/1.1+400/1.21+400/1.331, "after4", -1000+400/1.1+400/1.21+400/1.331+400/1.4641)
print("M2 payback", 3+ (1000-(400/1.1+400/1.21+400/1.331))/(400/1.4641))
print("M2 payback using displayed 5.26/273.21", 3+5.26/273.21, "5.2592/273.2054", 3+5.2592/273.2054)
print("M3", 500 and 2+200/300)
# E2
print("E2 ratio", 385535.69/289367.40, "A-B", 289367.40+96168.29)
# Prop 2.2 random-ish check: discounted vs cumulative
import random
rng=random.Random(1); bad=0
for _ in range(20000):
    n=rng.randint(1,8); C0=-rng.uniform(1,100); C=[C0]+[rng.uniform(0,100) for _ in range(n)]
    r=rng.uniform(0,0.5); tS=pb(C); tD=pb(disc(C,r))
    if tS is not None and tD is not None and tD < tS-1e-12: bad+=1
print("prop2.2 witnesses", bad)

# L06 numbers
npvs = None
n_max = ns6["N_MAX"]
# regenerate draws exactly as main() does
import random as R
rng = R.Random(ns6["SEED"])
npvs = [ns6["npv_of"]([rng.randint(ns6["LOW"], ns6["HIGH"]) for _ in range(ns6["YEARS"])]) for _ in range(n_max)]
ordered = sorted(npvs)
q = ns6["quantile"]
q10, q50, q90 = q(ordered,.1), q(ordered,.5), q(ordered,.9)
print("unrounded q10 q90 width", q10, q90, q90-q10, "rounded width", round(q90,2)-round(q10,2))
neg = sum(1 for x in npvs if x<0)/n_max
print("share", neg, math.sqrt(neg*(1-neg)/n_max))
m=100001; print("var", (m*m-1)/12, "expected", -300000+100000*sum(1/1.1**t for t in range(1,6)))
sd_exact = math.sqrt(sum(((m*m-1)/12)/1.1**(2*t) for t in range(1,6))); print("sd", sd_exact)
print("E1 z", (84543.40-79078.68)/4400.22, "p", 2*(1-0.5*(1+math.erf(1.24192/math.sqrt(2)))))
print("E1 unrounded z from lab", (ns6['npv_of'] and 0))
print("19.9", 4400.22/221.01, "sqrt500", math.sqrt(500), "sd ratio", 49419.62/49379.84)
print("E2 band", 0.0552-1.96*0.0010, 0.0552+1.96*0.0010)
print("E3 units", (143406.13-14896.62)/100)
print("R2 and M3 check: annuity", 1/1.1+1/1.21, "NPV", -100+50*(1/1.1+1/1.21))
for mm in range(2,40):
    vals=list(range(mm)); mu=sum(vals)/mm; var=sum((x-mu)**2 for x in vals)/mm
    assert abs(var-(mm*mm-1)/12)<1e-9, mm
print("prop2.2 brute force m=2..39 ok")
print("sample sd check", 221.01*math.sqrt(50000), 4400.22*math.sqrt(100))
