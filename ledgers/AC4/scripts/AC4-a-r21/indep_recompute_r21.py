"""Independent recomputation for AC4-a round 21 (no import of the twins)."""
from fractions import Fraction as Fr
# L01: the 12 (hours, cost_cents) pairs as printed in L01.html expected block
rows = [(556,4129540),(532,4045990),(1012,6085587),(818,5249755),(632,4449367),(428,3643546),
        (831,5346794),(967,5875098),(480,3856765),(638,4536345),(1161,6721387),(661,4619656)]
hi = max(range(12), key=lambda i: rows[i][0]); lo = min(range(12), key=lambda i: rows[i][0])
v = Fr(rows[hi][1]-rows[lo][1], rows[hi][0]-rows[lo][0]); F = rows[hi][1] - v*rows[hi][0]
print("L01 high month", hi+1, "low month", lo+1, "v cents/h", float(v), "F cents", float(F), "F USD", float(F)/100)
res = [rows[i][1]-(F+v*rows[i][0]) for i in range(12)]
print("residual cents", [float(r) for r in res])
print("nonzero count", sum(1 for r in res if r != 0), "largest abs cents", float(max(abs(r) for r in res)))
print("month by cost max", max(range(12), key=lambda i: rows[i][1])+1, "month by cost min", min(range(12), key=lambda i: rows[i][1])+1)
# E2: residual of month 1 against the generator line (18000 + 42.50*h) and against the fitted line
g = Fr(1800000) + 4250*556
print("month1 vs generator line cents", rows[0][1]-g, "vs fitted", float(res[0]))
print("fitted vs generator at 556h cents", float((F+v*556)-g))
print("v USD/h", float(v)/100, "F USD", float(F)/100)
# L02: direct recomputation
P, Vc, FC, S = 2500, 1150, 120000, 2700000
m = P-Vc
def oi(u): return m*u - FC - (S if u > 2000 else 0)
print("m", m, "ratio", Fr(m,P), "Q* lower", Fr(FC,m), float(Fr(FC,m)), "upper", float(Fr(FC+S,m)))
print("oi88", oi(88), "oi89", oi(89), "oi2000", oi(2000), "oi2001", oi(2001))
runs=[]; st=None
for u in range(5001):
    l = oi(u)<0
    if l and st is None: st=u
    elif not l and st is not None: runs.append((st,u-1)); st=None
if st is not None: runs.append((st,5000))
print("runs", runs)
print("zero check any integer oi==0", [u for u in range(5001) if oi(u)==0])
print("planned oi", oi(2500), "MoS", float(2500-Fr(FC+S,m)), "share%", float((2500-Fr(FC+S,m))/2500*100))
print("DOL", float(Fr(m*2500, oi(2500))), "up1 growth %", float(Fr(oi(2525)-oi(2500), oi(2500))*100))
print("100 USD fixed rise moves break-even", float(Fr(10000,m)))
print("revenue at BE", float(Fr(P)*Fr(FC,m))/100)
print("E2 margin from first BE", 2500-float(Fr(FC,m)))
print("E2 share", 411.11/2500*100, "M2 check", 7*1429-10000, 7*1428-10000)
print("dispersed", float(Fr(FC,1450)-Fr(FC,1350)))
print("E1 run lengths", 88-0+1, 2088-2001+1)
print("step drop", oi(2001)-oi(2000), "oi2000 USD", oi(2000)/100, "oi2001 USD", oi(2001)/100)

# R3 step-cost recomputation (run separately; output in out/indep_recompute_r21.out)
def cost(h): return 0 if h == 0 else (4000 if h <= 400 else (8000 if h <= 800 else 12000))
errs = [(abs(cost(h) - 10 * h), h) for h in range(0, 1201)]
mx = max(errs)
print("R3 max abs error USD", mx[0], "at hours", [h for e, h in errs if e == mx[0]], "ratio", mx[0] / 4000)
