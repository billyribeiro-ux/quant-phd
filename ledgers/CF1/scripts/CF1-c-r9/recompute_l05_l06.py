"""Independent recomputation of L05/L06 numbers (round 9). Run with python -I."""
import math, random, statistics

# L05 flows
A = (-1_000_000, 300_000, 400_000, 400_000, 300_000, 200_000, 100_000)
B = (-1_000_000, 300_000, 400_000, 400_000, 0, 0, 0)
D = (-1_000_000, 500_000, 500_000, 0, 0, 0, 0)
r = 0.10
def pb(f):
    if f[0] >= 0: return 0.0
    tot = float(f[0])
    for t in range(1, len(f)):
        prev = tot; tot += f[t]
        if tot >= 0: return (t-1) + (-prev)/f[t]
    return None
def disc(f): return [x/(1+r)**t for t, x in enumerate(f)]
def npv(f): return math.fsum(disc(f))
for n, f in (("A",A),("B",B),("D",D)):
    print(n, pb(f), pb(disc(f)), round(npv(f),2))
print("gap", npv(A)-npv(B), 300000/1.1**4+200000/1.1**5+100000/1.1**6)
print("gap ratio", 385535.69/289367.40)
# cumulative discounted A and B, years 0..6
dA = disc(A); dB = disc(B)
c=0
for t,x in enumerate(dA):
    c+=x; print("A cum disc", t, round(x,4), round(c,4))
c=0
for t,x in enumerate(dB):
    c+=x; print("B cum disc", t, round(x,4), round(c,4))
# M2 example: -1000 at 0, 400 at 1..3? use page's M2 flows: find via displayed terms
terms=[363.64,330.58,300.53,273.21]
print("sum3 displayed", round(sum(terms[:3]),2), "exact", 1000/1.1*0+ (-1000+400/1.1+400/1.1**2+400/1.1**3)*1)
# 3 + 5.2592/273.2051
cum3 = -1000 + 400/1.1 + 400/1.1**2 + 400/1.1**3
print("M2 cum3", cum3, "x4", 400/1.1**4, "pb", 3 + (-cum3)/(400/1.1**4))
# E1 range
print("E1", round(693692.91-121251.71,2))
# tail variance check of ranges (lab output)
rng = random.Random(2026)
tails=[]
for _ in range(1000):
    tails.append((*A[:5], rng.randint(0,500_000), rng.randint(0,500_000)))
print("tail npv min max", round(min(npv(t) for t in tails),2), round(max(npv(t) for t in tails),2))

# L06 numbers
LOW, HIGH, INV, Y = 50000, 150000, 300000, 5
rng = random.Random(6)
def npv_of(rec): return -INV + math.fsum(x/(1+r)**(t+1) for t,x in enumerate(rec))
npvs=[npv_of([rng.randint(LOW,HIGH) for _ in range(Y)]) for _ in range(50000)]
ordered=sorted(npvs)
def q(p): return ordered[max(1,math.ceil(p*len(ordered)))-1]
q10,q50,q90=q(0.1),q(0.5),q(0.9)
print("quantiles", q10,q50,q90)
print("80% width printed", round(143406.13-14896.62,2), "unrounded", round(q90-q10,4), round(q90-q10,2))
p=0.0552
print("band", p-1.96*0.0010, p+1.96*0.0010)
print("share unrounded", sum(1 for x in npvs if x<0)/50000)
m=HIGH-LOW+1
print("sd check", math.sqrt(sum(((m*m-1)/12)/(1+r)**(2*t) for t in range(1,Y+1))))
print("E1 z", (84543.40-79078.68)/4400.22, 2*(1-0.5*(1+math.erf(((84543.40-79078.68)/4400.22)/math.sqrt(2)))))
