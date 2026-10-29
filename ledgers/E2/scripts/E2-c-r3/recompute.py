"""Independent recomputation of the numbers in E2 L07-L09 prose (verifier, round 3)."""
from fractions import Fraction as F
import itertools, math

def half_up(x):
    return math.floor(x + F(1, 2))

# L08: E[M] = -a + sum_{x=-a}^{a-1} (1 - F(x)^n), F(x) = (x+a+1)/(2a+1)
def EM(n, a):
    return -a + sum(1 - F(x + a + 1, 2 * a + 1) ** n for x in range(-a, a))

def EM_brute(n, a):
    vals = range(-a, a + 1)
    tup = list(itertools.product(vals, repeat=n))
    return F(sum(max(t) for t in tup), len(tup))

print("L08 EM(2,1) =", EM(2, 1), " brute =", EM_brute(2, 1))
print("L08 EM(3,1) =", EM(3, 1), " brute =", EM_brute(3, 1))
print("L08 EM(5,2000) fraction =", EM(5, 2000))
e = EM(5, 2000)
print("L08 EM(5,2000) float =", float(e), "decimal 12 places approx:", f"{float(e):.8f}")
print("L08 claimed fraction 85418692002000/64048012001 equals EM?", F(85418692002000, 64048012001) == e)
print("L08 claimed fraction float:", 85418692002000 / 64048012001)
cont = F(2000 * 4, 6)
print("L08 continuous 4000/3 =", float(cont), "diff discrete-cont =", float(e - cont), "rounded 4dp", f"{float(e-cont):.7f}")
print("L08 difference rounded to 4 dp:", round(float(e - cont), 4), " rounded 2 dp of discrete:", round(float(e),2), "cont:", round(float(cont),2))
print("L08 1334 - EM =", float(1334 - e), " 1333 - EM =", float(1333 - e))
print("L08 exact naive total = -20000*EM =", float(-20000 * e), " half_up:", half_up(-20000 * e))
print("L08 exact shaded total = 20000*(1334-EM) =", float(20000 * (1334 - e)), " half_up:", half_up(20000 * (1334 - e)))
print("L08 exact naive total minus 0.25 check: -26673331.25 vs exact", float(-20000 * e))
print("L08 per-auction naive exact =", float(-e), "; simulated per auction -26620718/20000 =", -26620718/20000)
print("L08 SE per auction 79810/20000 =", 79810/20000)
print("L08 diff simulated-exact naive =", -26620718 - half_up(-20000 * e), " /79810 =", (-26620718 - half_up(-20000*e))/79810)
print("L08 shaded diff exact check: 59282 - 6669 =", 59282 - 6669)
print("L08 shift 59282 - (-26620718) =", 59282 + 26620718, " 1334*20000 =", 1334*20000)
print("L08 Example 2.4 EM(2,1) =", EM(2,1), "P(M=-1), P(M=0), P(M=1):")
print("L08 M2 EM(3,1) =", EM(3,1))
print("L08 R3 check 1333 - E[M] =", float(1333 - e))
print("L08 Remark 3.2 expected at 1333 rounded:", round(float(1333-e),2))
print("L08 simulated 0.66 SE: ", (26680000-26680000))
print("L08 Remark2.3 diff 0.3332292:", float(e - cont))

# L08 Prop 2.2 example M2 n=3 a=1 checks
print("L08 M2 detail: P(M<=-1)=", F(1,3)**3, "P(M<=0)=", F(2,3)**3)

# L07 numbers
vL, vH, pL, pH = 6000, 10000, F(3,10), F(7,10)
D = vH - vL
def c_of(pH):
    return (1-pH)*vL - pH*D
print("L07 c at pH=7/10:", c_of(pH), " revenue exclusion:", pH*vH, " pooling:", vL)
print("L07 R3 c(pH)=6000-10000pH check:", all(c_of(F(k,100)) == 6000 - 10000*F(k,100) for k in range(101)))
print("L07 threshold pH:", F(6000,10000))
# grid
steps = [F(k,4) for k in range(5)]
best=None; passing=0; cnt=0
def check(m):
    ic=True; ir=True
    for th in ("L","H"):
        v = vL if th=="L" else vH
        tu = v*m[th][0]-m[th][1]
        if tu<0: ir=False
        for r in ("L","H"):
            u = v*m[r][0]-m[r][1]
            if u>tu: ic=False
    rev = pL*m["L"][1] + pH*m["H"][1]
    return ic, ir, rev
for ql in steps:
    for qh in steps:
        if ql>qh: continue
        cnt+=1
        tl = vL*ql
        th_ = vH*qh - D*ql
        assert tl.denominator==1 and th_.denominator==1
        ic,ir,rev = check({"L":(ql,int(tl)),"H":(qh,int(th_))})
        if ic and ir:
            passing+=1
            if best is None or rev>best[2]: best=(ql,qh,rev)
print("L07 grid pairs", cnt, "passing", passing, "best", best, "half-up", half_up(best[2]))
print("L07 induced low-price tie-break revenue", pH*vL, " decline tie-break revenue", pH*6000)
print("L07 M3 revenue:", F(3,10)*3000 + F(7,10)*8000, " formula:", pH*vH + c_of(pH)*F(1,2))
print("L07 M2 p_H=1/2:", c_of(F(1,2)))
print("L07 E2 exclusion revenue 7000 pool 6000 check", pH*vH, pL*0 + vL)
