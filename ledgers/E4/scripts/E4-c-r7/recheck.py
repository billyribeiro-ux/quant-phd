# Independent re-derivation of the numbers quoted in E4 L07-L09 (verifier round 7).
import math, itertools
from fractions import Fraction as F

# ---- L07: closed form of Proposition 7.6 at the lab's parameter sets (exact)
def rho2_closed(sv2, se2, a, lam, su2):
    chi = a * a * se2 * se2 / (lam * lam)
    return sv2 / (sv2 + se2 + chi * su2)
one = F(1)
print("L07 base rho2 (sd=1/2):", rho2_closed(one, one, one, F(1,2), F(1,4)))
print("L07 sd sweep:", [str(rho2_closed(one, one, one, F(1,2), s*s)) for s in [F(1,4),F(1,2),one,F(2),F(4)]])
print("L07 lam sweep:", [str(rho2_closed(one, one, one, l, F(1,4))) for l in [F(1,4),F(1,2),F(3,4)]])
print("L07 a sweep:", [str(rho2_closed(one, one, a, F(1,2), F(1,4))) for a in [F(1,2),one,F(2)]])
print("L07 tiny sd 1/100:", rho2_closed(one, one, one, F(1,2), F(1,10000)), "benchmark", F(1,2))
print("L07 M1 (sd=1):", rho2_closed(one, one, one, F(1,2), one), "M2 (lam=3/4):", rho2_closed(one, one, one, F(3,4), F(1,4)))
print("L07 M3:", rho2_closed(F(2), one, one, F(1,2), one))
# sd=1/2 base value 1/3; closed-form Var(p) sweep from moments (Lab A-E formula) -- recompute from theta
def coef(sv2, se2, a, lam, su2):
    tv = 1/sv2; te = 1/se2; kappa = a/(lam*te); seta2 = se2 + kappa*kappa*su2
    teta = 1/seta2; tbar = lam*te + (1-lam)*teta
    ths = tbar/(tv+tbar); thu = kappa*ths
    return seta2, ths, thu
for sd in [F(1,4),F(1,2),one,F(2),F(4)]:
    s2, ths, thu = coef(one, one, one, F(1,2), sd*sd)
    varp = ths*ths*2 + thu*thu*sd*sd
    cov = ths*one
    r2 = cov*cov/(one*varp)
    print("sweep sd", sd, "sig_eta2", s2, "var_p", varp, "rho2(moments)", r2)
print("L07 E1 diff/tol:", (F(1,3)-F('0.330625'))/F('0.02'), float((F(1,3)-F('0.330625'))/F('0.02')))
print("L07 R2 check chi=4 sigma_u=1/sqrt2 -> sigma_u^2 =", F(1,2))
# ---- L08: independent recomputation of G, roots and corr at the lab's parameters (floats)
CARA=2.0; SV2=1.0; SE2=1.0; SU2=1.0
def gain(lam, su2=SU2):
    if lam == 0.0:
        bs = SV2/(SV2+SE2); V_I = 1/(1/SV2+1/SE2); Vu = SV2
        noise = CARA**2*SV2**2*su2
        VDI = bs*bs*(SV2+SE2) + noise; VDU = noise
        return math.log((1+VDI/V_I)/(1+VDU/Vu))/(2*CARA)
    kappa = CARA*SE2/lam
    teta = 1/(SE2 + kappa*kappa*su2)
    te = 1/SE2; tv = 1/SV2
    A = lam*te + (1-lam)*teta
    beta = A/(tv+A)
    bs = te/(tv+te); by = teta/(tv+teta)
    V_I = 1/(tv+te); V_U = 1/(tv+teta)
    sig_eta2 = 1/teta
    VDI = (bs-beta)**2*(SV2+SE2) + (kappa*beta)**2*su2
    VDU = (by-beta)**2*(SV2+sig_eta2)
    return math.log((1+VDI/V_I)/(1+VDU/V_U))/(2*CARA)
def corr2(lam):
    if lam == 0: return 0.0
    kappa = CARA*SE2/lam; teta = 1/(SE2+kappa*kappa*SU2); tv=1/SV2
    return teta/(tv+teta)
print("L08 G(0)=", gain(0.0), "ln2/4=", math.log(2)/4)
print("L08 G(1)=", gain(1.0), "ln(5/3)/4=", math.log(5/3)/4)
print("L08 G(0.5)=", gain(0.5))
print("L08 G(1e-6)-G(0)=", gain(1e-6)-gain(0.0))
kap=CARA*SE2/0.5; teta=1/(SE2+kap*kap*SU2); tv=1
by=teta/(tv+teta); A=0.5*1+0.5*teta; beta=A/(tv+A)
print("L08 by/beta at lam=0.5 =", by/beta)
print("L08 corr2 at lam=1/2 (exact):", F(1,18), float(F(1,18)))
for cost in [0.12,0.13,0.14,0.15,0.16,0.17,0.18]:
    g0=gain(0.0); g1=gain(1.0)
    if cost>=g0: print("cost",cost,"boundary zero, N=",g0-cost, "corr2 0"); continue
    if cost<=g1: print("cost",cost,"boundary one, N=",g1-cost, "corr2", corr2(1.0)); continue
    # independent root finder: plain bisection on (0,1) with 200 iterations, then report N and corr2
    lo,hi=1e-12,1.0
    for _ in range(200):
        mid=(lo+hi)/2
        if gain(mid)-cost>0: lo=mid
        else: hi=mid
    lam=(lo+hi)/2
    print("cost",cost,"lam*=%.9f"%lam,"N=%.3e"%(gain(lam)-cost),"corr2=%.6f"%corr2(lam))
print("L08 Prop 4.1-style Var checks at lam=1 (Emp 3): VDI=1, VDU=2/3 -> G1=", 0.25*math.log((1+1/0.5)/(1+(2/3)/(5/6))))
# sample slope vs formula check is in the lab; formula value already = 0.16049
# ---- L09: independent enumeration with integer arithmetic (6*posterior)
states=[1,2,3,4,5,6]
P1=[{1,2},{3},{4,5,6}]; P2=[{1,2,3},{4,5},{6}]
def cell(part,w):
    for c in part:
        if w in c: return c
def meet(w):
    seen={w}; stack=[w]
    while stack:
        cur=stack.pop()
        for part in (P1,P2):
            for o in cell(part,cur):
                if o not in seen: seen.add(o); stack.append(o)
    return seen
M1=meet(1); M4=meet(4)
print("L09 meet(1)=",sorted(M1)," meet(4)=",sorted(M4))
def post_times6(part, x, w):
    c=cell(part,w); return sum(x[k] for k in c)*6//len(c) if (sum(x[k] for k in c)*6)%len(c)==0 else F(sum(x[k] for k in c)*6, len(c))
cnt={}
for vals in itertools.product([-2,-1,0,1,2], repeat=6):
    x={s:v for s,v in zip(states,vals)}
    negx={s:-v for s,v in x.items()}
    g1={w:F(sum(x[k] for k in cell(P1,w)),len(cell(P1,w))) for w in states}
    g2={w:F(sum(negx[k] for k in cell(P2,w)),len(cell(P2,w))) for w in states}
    for tag,w,M in [("s1",1,M1),("s4",4,M4)]:
        if g1[w]>0 and g2[w]>0:
            cnt[tag+"_strict"]=cnt.get(tag+"_strict",0)+1
            if all(g1[k]>=0 and g2[k]>=0 for k in M): cnt[tag+"_strict_and_common"]=cnt.get(tag+"_strict_and_common",0)+1
        if all(g1[k]>=0 and g2[k]>=0 for k in M):
            cnt[tag+"_nonneg"]=cnt.get(tag+"_nonneg",0)+1
            if any(g1[k]!=0 or g2[k]!=0 for k in M): cnt[tag+"_nonneg_nonzero"]=cnt.get(tag+"_nonneg_nonzero",0)+1
            if all(g1[k]==0 and g2[k]==0 for k in M): cnt[tag+"_zero"]=cnt.get(tag+"_zero",0)+1
    if vals[0]==-1 and vals[1]==2 and vals[2]==-2 and vals[3:]==(-2,-2,-2): print("example bet g1(1), g2(1), g1(3):", g1[1], g2[1], g1[3])
print("L09 counts:", cnt, "total bets", 5**6)
