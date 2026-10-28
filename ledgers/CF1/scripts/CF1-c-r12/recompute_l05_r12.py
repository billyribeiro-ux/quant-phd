import math
A=(-1_000_000,300_000,400_000,400_000,300_000,200_000,100_000)
B=(-1_000_000,300_000,400_000,400_000,0,0,0)
r=0.10
npv=lambda f: math.fsum(x/(1+r)**t for t,x in enumerate(f))
print("npvA",round(npv(A),2),"npvB",round(npv(B),2),"gap",round(npv(A)-npv(B),2))
pv46=math.fsum(x/(1+r)**t for t,x in zip((4,5,6),(300000,200000,100000)))
print("pv years4-6",round(pv46,4), "gap unrounded", npv(A)-npv(B))
print("gap/npvA", (npv(A)-npv(B))/npv(A), "pct", round(100*(npv(A)-npv(B))/npv(A),2))
print("E2 printed quotient", 385535.69/289367.40)
print("E1 range", 693692.91-121251.71, "currency", (693692.91-121251.71)/100)
print("M2 unrounded sum3", 400/1.1+400/1.21+400/1.331, "D3", -1000+400/1.1+400/1.21+400/1.331, "D4 tail", 400/1.4641, "pb", 3+5.26/273.21, 3+ (1000-sum([400/1.1**t for t in (1,2,3)]))/(400/1.1**4))
print("disp sum", 363.64+330.58+300.53)
print("D_B cum", [round(sum(B[s]/(1+r)**s for s in range(t+1)),4) for t in range(7)])
print("D_A cum", [round(sum(A[s]/(1+r)**s for s in range(t+1)),4) for t in range(7)])
print("P2 example", -1000+1/1.1**4+1/1.1**5, -1000+1000/1.1**4)
print("E3 A", 289367.40, "D", -132231.40)
# payback check
def pb(f):
    if f[0]>=0: return 0.0
    tot=f[0]
    for t in range(1,len(f)):
        prev=tot; tot+=f[t]
        if tot>=0: return (t-1)+(-prev)/f[t]
    return None
print("pb A", pb(A), "pb B", pb(B), "pb disc A", pb([x/(1+r)**t for t,x in enumerate(A)]))
