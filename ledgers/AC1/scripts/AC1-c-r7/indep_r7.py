# Independent recomputation (integer cents / Fraction), no reuse of lab code.
from fractions import Fraction as F
# L08 Example 1.4 / Ex 2.2 / M2 / M3 / R2
def roll(C, L, pct, r, P):
    b = F(C, L); tau = [F(C*p, 100) for p in pct]
    K = F(0); dtl_prev = F(0); out = []
    for t in range(L):
        d = tau[t] - b; K += d; dtl = F(r)*K/100
        CT = F(r)*(P[t]-d)/100; DE = dtl - dtl_prev; out.append((CT, DE, CT+DE, dtl, K)); dtl_prev = dtl
    return out
ex = roll(100000, 5, (40,30,20,10,0), 21, [50000]*5)
print("Ex1.4 K", [o[4] for o in ex[:5]] if False else "")
print("Ex2.2 CT,DE,TE", [(float(a),float(b),float(c)) for a,b,c,_,_ in ex])
m2 = roll(60000, 3, (50,30,20), 21, [50000]*3)
print("M2 DTL", [float(o[3]) for o in m2], "DE", [float(o[1]) for o in m2], "K", [float(o[4]) for o in m2])
print("M3 CT,DE,TE", [(float(a),float(b),float(c)) for a,b,c,_,_ in m2])
K2 = F(30000); dtl2 = F(21)*K2/100; dtl3 = F(25)*K2/100; CT3 = F(25)*50000/100; DE3 = dtl3-dtl2
print("R2 dtl2,dtl3,CT3,DE3,TE3", float(dtl2), float(dtl3), float(CT3), float(DE3), float(CT3+DE3), "diff", float(CT3+DE3-F(25*50000,100)))
print("M1 DTL2 at 25%", float(F(25)*30000/100))
# L08 lab table, cost 4,670,000 cents, seed 20260702 pretax from the printed table (cents)
C = 4670000; b = C//5; tp = [40,30,20,10,0]
pre = [4824400, 8408500, 4813000, 4633900, 5902500]
K=0; prev=0
for t in range(5):
    tau = C*tp[t]//100; d = tau-b; K += d; dtl = F(21*K,100); de = dtl-prev; prev=dtl
    CT = F(21*(pre[t]-d),100); TE = CT+de
    print(t+1, float(dtl), float(CT), float(de), float(TE), float(F(21*pre[t],100)), TE == F(21*pre[t],100))
print("E1 K2/cost", F(14010,46700), "0.21*14010", F(21*14010,100))
print("E2 year1 CT+DE", F(816984,100)+F(196140,100), "0.21*48244", F(21*48244,100))
print("Ex 2.3 L07 M1", F(400000,3), 400000-2*133333)
