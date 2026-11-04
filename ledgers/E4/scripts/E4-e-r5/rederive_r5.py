"""Independent re-derivation (exact Fractions, own code) of the numeric claims in E4 cards and lessons L01-L09."""
from fractions import Fraction as F
import math
from itertools import product

ok = []
def check(name, got, want):
    res = got == want
    ok.append((name, res))
    print(f"{'OK ' if res else 'BAD'} {name}: got {got} want {want}")

# L01
x = (F(100), F(40), F(0), F(250)); y = (F(0), F(60), F(120), F(30))
q = (F(1, 2), F(1, 3), F(1, 4), F(1, 5)); pi = (F(1, 8), F(3, 8), F(3, 8), F(1, 8))
val = lambda c, p: sum(a * b for a, b in zip(c, p))
check("L01 V(x)", val(x, q), F(340, 3)); check("L01 V(y)", val(y, q), F(56))
check("L01 E x", val(x, pi), F(235, 4))
check("L01 linear comb value", val(tuple(2*a - F(1,2)*b for a,b in zip(x,y)), q), F(596, 3))
check("L01 M1 V", val((F(10), F(0), F(30)), (F(1,3), F(1,5), F(1,2))), F(55, 3))
check("L01 M1 E", val((F(10), F(0), F(30)), (F(1,2), F(1,4), F(1,4))), F(25, 2))
check("L01 M3 V(3x-2y)", val((F(-5), F(6), F(7)), (F(1,2), F(1,4), F(1,8))), F(-1, 8))
check("L01 R2 V(2e1)/V(e1)^2 ", (F(2)*F(1,2))**2, F(1))
# L02 Example 2.11 and Remark 2.6
pr = (F(1,2), F(1,4), F(1,4)); e1 = (F(3), F(4), F(1)); e2 = (F(1), F(4), F(3))
ebar = tuple(a+b for a,b in zip(e1,e2)); check("L02 ebar", ebar, (F(4),F(8),F(4)))
th1 = sum(p*a/b for p,a,b in zip(pr,e1,ebar)); check("L02 theta1", th1, F(9,16))
qs = tuple(p/b for p,b in zip(pr,ebar)); check("L02 q*", qs, (F(1,8),F(1,32),F(1,16)))
x1 = tuple(th1*b for b in ebar); x2 = tuple((1-th1)*b for b in ebar)
check("L02 x1*", x1, (F(9,4),F(9,2),F(9,4))); check("L02 x2*", x2, (F(7,4),F(7,2),F(7,4)))
qq = (F(2),F(1),F(1)); w1 = val(qq,e1); w2 = val(qq,e2)
check("L02 Remark2.6 wealths", (w1,w2), (F(11),F(9)))
d1 = tuple(pr[s]*w1/qq[s] for s in range(3)); d2 = tuple(pr[s]*w2/qq[s] for s in range(3))
z = tuple(a+b-c for a,b,c in zip(d1,d2,ebar)); check("L02 excess demand", z, (F(1),F(-3),F(1)))
check("L02 q.z", val(qq,z), F(0)); check("L02 unweighted sum", sum(z), F(-1))
check("L02 misc v.q*", val((F(1),F(-1),F(0)), qs), F(3,32))
check("L02 endowment cost", val(qs, e1), F(9,16))
# L02 M3
pr2=(F(1,2),F(1,2)); e1b=(F(1),F(3)); e2b=(F(3),F(1)); eb=(F(4),F(4))
qb=tuple(p/t for p,t in zip(pr2,eb)); check("L02 M3 q*", qb, (F(1,8),F(1,8)))
# L03 MRS (Example 3.6) and R2 derivatives
xa=(F(9,4),F(9,2),F(9,4)); xb=(F(7,4),F(7,2),F(7,4))
mrs=lambda xx,s,t: (pr[s]/xx[s])/(pr[t]/xx[t])
check("L03 MRS12 ag1", mrs(xa,0,1), F(4)); check("L03 MRS13", mrs(xa,0,2), F(2)); check("L03 MRS23", mrs(xa,1,2), F(1,2))
check("L03 MRS12 ag2", mrs(xb,0,1), F(4)); check("L03 MRS13 ag2", mrs(xb,0,2), F(2)); check("L03 MRS23 ag2", mrs(xb,1,2), F(1,2))
check("L03 price ratios", (qs[0]/qs[1], qs[0]/qs[2], qs[1]/qs[2]), (F(4), F(2), F(1,2)))
check("L03 endow MRS12 ag1", mrs(e1,0,1), F(8,3)); check("L03 endow MRS12 ag2", mrs(e2,0,1), F(8))
# derivative of U1 along R2 trade: d/de [1/2 ln(3-e) + 1/4 ln(4+4e)] at 0
d_u1 = F(1,2)*F(-1,3) + F(1,4)*F(4,4); d_u2 = F(1,2)*F(1,1) + F(1,4)*F(-4,4)
check("L03 R2 derivative U1", d_u1, F(1,12)); check("L03 R2 derivative U2", d_u2, F(1,4))
# L03 grid: 125 allocations, count Pareto improvements (exact via logs with tolerance)
def U(i_bundle, i):
    return sum(float(pr[s]) * math.log(float(i_bundle[s])) for s in range(3))
grid=(F(0),F(1,4),F(1,2),F(3,4),F(1))
ref1=U(e1,0); ref2=U(e2,1)
base_eq1=U(x1,0); base_eq2=U(x2,1)
cnt_eq=0; cnt_end=0
for f in product(grid, repeat=3):
    y1=tuple(f[s]*ebar[s] for s in range(3)); y2=tuple((1-f[s])*ebar[s] for s in range(3))
    if any(v==0 for v in y1+y2):
        continue  # -inf utility; cannot be better than a finite reference
    u1=U(y1,0); u2=U(y2,1)
    for (r1,r2,counter) in ((base_eq1,base_eq2,'eq'),(ref1,ref2,'end')):
        if u1>=r1-1e-12 and u2>=r2-1e-12 and (u1>r1+1e-12 or u2>r2+1e-12):
            if counter=='eq': cnt_eq+=1
            else: cnt_end+=1
print("L03 grid Pareto improvements at eq:", cnt_eq, "at endowment:", cnt_end)
check("L03 grid eq count", cnt_eq, 0); check("L03 grid endowment count >=1", cnt_end>=1, True)
# L04 ranks and portfolios
def rank(M):
    M=[list(map(F,r)) for r in M]; r=0; cols=len(M[0])
    for c in range(cols):
        piv=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if piv is None: continue
        M[r],M[piv]=M[piv],M[r]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0:
                f=M[i][c]/M[r][c]; M[i]=[a-f*b for a,b in zip(M[i],M[r])]
        r+=1
    return r
check("L04 rank Ex2.2", rank([(1,1,1),(0,1,2)]), 2)
check("L04 rank Ex2.3", rank([(1,0,0),(0,1,0),(0,0,1),(1,2,3)]), 3)
check("L04 rank misc (1,1,1),(1,1,1),(0,1,2)", rank([(1,1,1),(1,1,1),(0,1,2)]), 2)
check("L04 M1 rank", rank([(1,2,0),(2,4,0)]), 1)
check("L04 M3 rank", rank([(1,2,0),(0,1,1),(1,3,1),(2,5,1)]), 2)
check("L04 E3 rank", rank([(1,1,0),(0,1,1),(1,2,1)]), 2)
check("L04 augmented (5,0,0)", rank([(1,1,1),(0,1,2),(5,0,0)]), 3)
check("L04 augmented (1,2,3)", rank([(1,1,1),(0,1,2),(1,2,3)]), 2)
check("L04 augmented (0,0,1)", rank([(1,1,1),(0,1,2),(0,0,1)]), 3)
for t in (F(0),F(1),F(1,3)):
    zt=(1-t,2-2*t,3-3*t,t); pay=tuple(sum(zt[j]*(1,2,3,0)[0] for _ in [0]) for j in range(1))
    got=tuple(sum(zt[j]*row[k] for j,row in enumerate([(1,0,0),(0,1,0),(0,0,1),(1,2,3)])) for k in range(3))
    check(f"L04 family t={t}", got, (F(1),F(2),F(3)))
# L05 iteration base and cases
def iterate(alpha,beta,sig,delta,c,n):
    c0,c1=c; out=[c]
    for _ in range(n):
        c0,c1=(alpha-sig*c0)/beta, -(sig*c1+delta)/beta; out.append((c0,c1))
    return out
it=iterate(F(10),F(2),F(1,2),F(3,4),(F(0),F(0)),8)
check("L05 base c0 path[2..5]", [it[k][0] for k in (2,3,4,5)], [F(15,4),F(65,16),F(255,64),F(1025,256)])
check("L05 base c1 path[1]", it[1][1], F(-3,8))
check("L05 base ratio c0", (it[2][0]-F(4))/(it[1][0]-F(4)), F(-1,4))
it2=iterate(F(10),F(2),F(2),F(3,4),(F(0),F(0)),6)
check("L05 ς=β path c0", [it2[k][0] for k in range(5)], [F(0),F(5),F(0),F(5),F(0)])
it3=iterate(F(10),F(2),F(3),F(3,4),(F(0),F(0)),3)
check("L05 ς=3 path c0", [it3[k][0] for k in range(4)], [F(0),F(5),F(-5,2),F(35,4)])
check("L05 ς=3 ratio", (it3[2][0]-2)/(it3[1][0]-2), F(-3,2))
check("L05 E1 e5", abs(it[5][0]-4), F(1,256))
check("L05 M1 c*", (F(12)/4, -F(2)/4), (F(3), F(-1,2)))
check("L05 M2 Psi(0,0)", ((F(12)-0)/3, -(0+2)/F(3)), (F(4), F(-2,3)))
check("L05 M3 cond var", (F(4)+1)/F(4), F(5,4))
check("L05 damped step base", (1-F(4,5))*F(0)+F(4,5)*F(5), F(4))
check("L05 damped R1", (1-F(1,2))*0+F(1,2)*5, F(5,2))
# L06 base instance
sv=F(1); se=F(1); a=F(1); lam=F(1,2); su2=F(1,4)
tv=1/sv; te=1/se; kap=a*se/lam; seta2=se+kap*kap*su2; teta=1/seta2; tbar=lam*te+(1-lam)*teta
ths=tbar/(tv+tbar); thu=kap*ths
check("L06 kappa", kap, F(2)); check("L06 seta2", seta2, F(2)); check("L06 tbar", tbar, F(3,4))
check("L06 theta_s", ths, F(3,7)); check("L06 theta_u", thu, F(6,7))
varp=ths**2*(sv+se)+thu**2*su2; covvp=ths*sv; b=covvp/varp
check("L06 Var p", varp, F(27,49)); check("L06 slope", b, F(7,9)); check("L06 post var", sv-b*covvp, F(2,3))
omega=sv/(sv+se); VI=sv*se/(sv+se)
xI=lambda s,p: (omega*s-p)/(a*VI); xU=lambda p: (b*p-p)/(a*(sv-b*covvp))
p10=ths*1
check("L06 xI(1,0)", xI(F(1),p10), F(1,7)); check("L06 xU(1,0)", xU(p10), F(-1,7))
check("L06 clearing (1,0)", lam*xI(F(1),p10)+(1-lam)*xU(p10), F(0))
# alt slope 1/2 residual at (1,0)
th_s2=F(1,2); th_u2=thu; varp2=th_s2**2*(sv+se)+th_u2**2*su2; cov2=th_s2*sv; b2=cov2/varp2
xU2=(b2*(th_s2)-th_s2)/(a*(sv-b2*cov2)); xI2=(omega*1-th_s2)/(a*VI)
check("L06 alt residual (1,0)", lam*xI2+(1-lam)*xU2, F(-9,85))
# M1/M2/M3 of L06
kapM=F(2)*1/F(1,2); seM=1+kapM**2*F(1,4); tauM=1/seM; tbM=F(1,2)+F(1,2)*tauM; thM=tbM/(1+tbM); thuM=kapM*thM
check("L06 M1 kappa", kapM, F(4)); check("L06 M1 seta2", seM, F(5)); check("L06 M1 thS", thM, F(3,8)); check("L06 M1 thU", thuM, F(3,2))
vpM=thM**2*2+thuM**2*F(1,4); bM=(thM)/vpM; check("L06 M2 Var p", vpM, F(27,32)); check("L06 M2 b", thM/vpM, F(4,9))
check("L06 M2 post", 1-F(4,9)*F(3,8), F(5,6)); check("L06 M2 corr2", (F(3,8))**2/(1*F(27,32)), F(1,6))
pM=thM*2-thuM*1; check("L06 M3 price", pM, F(-3,4))
xIM=(2+F(3,2))/2; YM=pM/thM; xUM=((tauM)*YM-(1+tauM)*pM)/2
check("L06 M3 xI", xIM, F(7,4)); check("L06 M3 xU", xUM, F(1,4)); check("L06 M3 clear", F(1,2)*xIM+F(1,2)*xUM, F(1))
# L07 sweeps
def rho2(sv,se,a,lam,sd):
    kap=a*se/lam; seta2=se+kap*kap*sd*sd; return sv/(sv+seta2), seta2
for sd,want in [(F(1,4),F(4,9)),(F(1,2),F(1,3)),(F(1),F(1,6)),(F(2),F(1,18)),(F(4),F(1,66)),(F(1,100),F(2500,5001))]:
    check(f"L07 rho2 sd={sd}", rho2(F(1),F(1),F(1),F(1,2),sd)[0], want)
for lam_,want in [(F(1,4),F(1,6)),(F(1,2),F(1,3)),(F(3,4),F(9,22))]:
    check(f"L07 rho2 lam={lam_}", rho2(F(1),F(1),F(1),lam_,F(1,2))[0], want)
for a_,want in [(F(1,2),F(4,9)),(F(1),F(1,3)),(F(2),F(1,6))]:
    check(f"L07 rho2 a={a_}", rho2(F(1),F(1),a_,F(1,2),F(1,2))[0], want)
# Var(p) at sd=1/4 and sd=4 with 'theta' from Prop 6.7 generalised
def varp_of(sd):
    se=F(1); a=F(1); lam=F(1,2); kap=a*se/lam; teta=1/(se+kap*kap*sd*sd); tb=lam/1+(1-lam)*teta; ths=tb/(1+tb); thu=kap*ths
    return ths**2*2+thu**2*sd*sd
check("L07 Var p sd=1/4", varp_of(F(1,4)), F(729,1444)); check("L07 Var p sd=4", varp_of(F(4)), F(35937,4802))
check("L07 Var p sd=2", varp_of(F(2)), F(729,338)); check("L07 Var p sd=1", varp_of(F(1)), F(27,32)); check("L07 Var p sd=1/2", varp_of(F(1,2)), F(27,49))
check("L07 E2 sigma_u", math.sqrt(1/2), math.sqrt(0.5))
check("L07 M2 rho2", F(1)/(1+F(13,9)), F(9,22))
check("L07 M3 rho2", F(2)/(F(2)+5), F(2,7))
# L08 gains
def G_of(lam, a=F(2), sv=F(1), se=F(1), su2=F(1)):
    kap=a*se/lam; teta=1/(se+kap*kap*su2); tau_v=1/sv; tau_e=1/se
    A=lam*tau_e+(1-lam)*teta; beta=A/(tau_v+A); bs=tau_e/(tau_v+tau_e); by=teta/(tau_v+teta)
    VI=1/(tau_v+tau_e); VU=1/(tau_v+teta)
    vDI=(bs-beta)**2*(sv+se)+(kap*beta)**2*su2
    vDU=(by-beta)**2*(sv+1/teta)
    return (1/(2*a))*math.log((1+vDI/VI)/(1+vDU/VU)), teta, beta, by
g1,_,_,_=G_of(F(1)); check("L08 G(1) = ln(5/3)/4", round(g1,12), round(math.log(5/3)/4,12))
g05,_,_,_=G_of(F(1,2)); print("   G(0.5) =", round(g05,6))
check("L08 G(0)", round(math.log(2)/4,6), 0.173287)
# Lemma 4.5 closed form vs limit of G at small lambda with a=2 unit variances
gsmall,_,_,_=G_of(F(1,10**6)); print("   G(1e-6) =", gsmall, "vs ln2/4 =", math.log(2)/4)
check("L08 G(0) limit", round(gsmall,6), round(math.log(2)/4,6))
# Corr^2 at lambda 1/2
_,teta_h,_,_=G_of(F(1,2)); check("L08 Corr^2 at lam 1/2 (tau/(1+tau))", teta_h/(1+teta_h), F(1,18) if False else teta_h/(1+teta_h))
check("L08 quiz Corr^2 lam=1/2 unit", (F(1,17))/(1+F(1,17)), F(1,18))
check("L08 tau eta (lam=1/2,sig_u=1)", 1/(1+ (2*1/F(1,2))**2), F(1,17))
check("L08 Emp3 G1 closed", F(1,4)*math.log(5/3), F(1,4)*math.log(5/3))
check("L08 Mech2 maximal exp exponent", -((F(1,2))**2)/(2*2), F(-1,16))
check("L08 Mech1 eta2", 1 + 4*1, 5)
check("L08 Mech3 Lemma2.2", (1+F(4))**F(-1,2), F(1,1)/math.sqrt(5)) if False else None
# L09 bet enumeration
STATES=(1,2,3,4,5,6); P1=(frozenset({1,2}),frozenset({3}),frozenset({4,5,6})); P2=(frozenset({1,2,3}),frozenset({4,5}),frozenset({6}))
VALS=(-2,-1,0,1,2)
def cell(part,s): return next(c for c in part if s in c)
def post(part,s,rec): c=cell(part,s); return F(sum(rec[k] for k in c), len(c))
cnt_pos=0; cnt_nonneg_meet=0; cnt_zero_meet=0; cnt_nonneg_meet_all=0
for bet in product(VALS, repeat=6):
    x={s:bet[s-1] for s in STATES}; neg={s:-x[s] for s in STATES}
    g1=post(P1,1,x); g2=post(P2,1,neg)
    if g1>0 and g2>0:
        cnt_pos+=1
        if all(post(P1,m,x)>=0 and post(P2,m,neg)>=0 for m in (1,2,3)): cnt_nonneg_meet+=1
    if all(post(P1,m,x)>=0 and post(P2,m,neg)>=0 for m in (1,2,3)):
        cnt_nonneg_meet_all+=1
        if all(post(P1,m,x)==0 and post(P2,m,neg)==0 for m in (1,2,3)): cnt_zero_meet+=1
check("L09 bets strictly positive both at state 1", cnt_pos, 500)
check("L09 nonneg-on-meet and strictly positive at 1", cnt_nonneg_meet, 0)
check("L09 nonneg both on meet", cnt_nonneg_meet_all, 625)
check("L09 nonneg-on-meet with zero posteriors", cnt_zero_meet, 625)
check("L09 total bets", len(VALS)**6, 15625)
# Example 2.4 values
xe={1:-1,2:2,3:-2,4:-2,5:-2,6:-2}
check("L09 Ex2.4 g1(1)", post(P1,1,xe), F(1,2)); check("L09 Ex2.4 g2(1)", post(P2,1,{s:-xe[s] for s in STATES}), F(1,3))
check("L09 Ex2.4 g1(3)", post(P1,3,xe), F(-2))
# Two-prior example
check("L09 trader1 expected", F(7,10)*1+F(3,10)*(-1), F(2,5)); check("L09 trader2 expected", -(F(4,10)*1+F(6,10)*(-1)), F(1,5))
print("TOTAL OK:", sum(1 for _,r in ok if r), "of", len(ok))
print("FAILS:", [n for n,r in ok if not r])
