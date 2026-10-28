import math, random, statistics
from decimal import Decimal, ROUND_HALF_EVEN
# independent recomputation of L06 lab model (not importing the twin)
RATE=0.10; YEARS=5; INV=300000; LOW=50000; HIGH=150000; N=50000; SEED=6
rng=random.Random(SEED)
npvs=[]
for _ in range(N):
    rec=[rng.randint(LOW,HIGH) for _ in range(YEARS)]
    npvs.append(-INV+math.fsum(x/(1+RATE)**(t+1) for t,x in enumerate(rec)))
s=sorted(npvs)
def q(p):
    r=max(1,math.ceil(p*N)); return s[r-1]
q10,q50,q90=q(0.10),q(0.50),q(0.90)
print("unrounded q10,q50,q90", repr(q10), repr(q50), repr(q90))
w=q90-q10
print("unrounded width", repr(w), "rounded2", f"{w:.2f}")
print("printed width 143406.13-14896.62 =", round(143406.13-14896.62,2))
print("rounding diff printed minus unrounded:", round(143406.13-14896.62-w,6))
m=HIGH-LOW+1; rv=(m*m-1)/12; mu=(LOW+HIGH)/2
exp=-INV+mu*sum((1-(1+RATE)**-YEARS)/RATE for _ in [0])
ann=(1-(1+RATE)**-YEARS)/RATE
exp=-INV+mu*ann
sd=math.sqrt(sum(rv/(1+RATE)**(2*t) for t in range(1,YEARS+1)))
print("closed expected", exp, "sd", sd)
# E1
err=84543.40-79078.68; se100=4400.22
print("E1 error", round(err,2), "z", err/se100)
from statistics import NormalDist
z=err/se100
print("E1 two-sided prob at 1.2419", 2*(1-NormalDist().cdf(1.2419)), " at exact z", 2*(1-NormalDist().cdf(z)))
print("E2 band", 0.0552-1.96*0.0010, 0.0552+1.96*0.0010)
print("se_p check", math.sqrt(0.0552*(1-0.0552)/50000))
print("ratio se 100/50000", 4400.22/221.01, "sqrt500", math.sqrt(500))
print("z 50000", (79216.82-79078.68)/221.01, "sd ratio", 49419.62/49379.84)
print("E3 width/100", 128509.51/100)
print("M2 variance", 35/12, "sd", math.sqrt(35/12))
v=1/1.1+1/1.21; print("M3 A", v, -100+50*v)
print("E1 z printed", round(z,3))
