import math, random
from statistics import NormalDist
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
print("unrounded q10 q50 q90", repr(q10), repr(q50), repr(q90))
w=q90-q10
print("unrounded width", repr(w), "to 2dp", f"{w:.2f}", "printed diff", round(143406.13-14896.62,2))
print("printed minus unrounded", 143406.13-14896.62-w)
ann=(1-(1+RATE)**-YEARS)/RATE
m=HIGH-LOW+1; rv=(m*m-1)/12; mu=(LOW+HIGH)/2
print("closed expected", -INV+mu*ann, "sd", math.sqrt(sum(rv/(1+RATE)**(2*t) for t in range(1,YEARS+1))))
z=(84543.40-79078.68)/4400.22
print("E1 z", z, "two-sided tail at z", 2*(1-NormalDist().cdf(z)), "at 1.2419", 2*(1-NormalDist().cdf(1.2419)))
print("E2 band", 0.0552-1.96*0.0010, 0.0552+1.96*0.0010)
print("se share", math.sqrt(0.0552*(1-0.0552)/50000))
print("ratio", 4400.22/221.01, math.sqrt(500))
print("sd ratio", 49419.62/49379.84)
print("E1 error", 84543.40-79078.68)
# L05 numbers
A=(-1_000_000, 300_000, 400_000, 400_000, 300_000, 200_000, 100_000)
print("pv 4-6 A", 300000/1.1**4+200000/1.1**5+100000/1.1**6)
print("E2 pct", 100*385535.69/289367.40)
print("M3 A", 1/1.1+1/1.21, -100+50*(1/1.1+1/1.21))
