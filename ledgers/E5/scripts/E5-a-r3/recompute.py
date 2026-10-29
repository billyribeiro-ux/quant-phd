"""Round 3 independent recomputation for E5 slice a (hub, L01-L03). Run: python -I recompute.py"""
import math
from decimal import Decimal as D, getcontext
from fractions import Fraction as F

getcontext().prec = 80

# ---- L01 exact values ----
print("L01 basket A P^L", F(2*0+5*0, 1) if False else F(3*10+5*4, 2*10+5*4), "P^P", F(3*8+5*6, 2*8+5*6) if False else F(3*8+5*6, 2*8+5*6))
PL_A = F(3*10+5*4, 2*10+5*4); PP_A = F(3*8+5*6, 2*8+5*6)
print("L01 PL_A", PL_A, "PP_A", PP_A, "gap", PL_A - PP_A, float(PL_A-PP_A))
PL_B = F(2*1+1*9, 1*1+1*9); PP_B = F(2*9+1*1, 1*9+1*1)
print("L01 PL_B", PL_B, "PP_B", PP_B, "gap", PL_B-PP_B)
print("L01 simple A", float(PL_A-1), float(PP_A-1), "log A", math.log(1.25), math.log(float(PP_A)))
print("L01 nominal growth", float(F(1100,995)-1), "real", float(F(25300,27)/995-1), F(25300,27)/995-1, "deflator", float(PP_A-1))
print("L01 identity", (F(1100,995)) == (1+(F(25300,27)/995-1))*(PP_A), )
print("L01 ln1.1 simple-log", 0.1-math.log(1.1), "ln1.25 gap", 0.25-math.log(1.25))
print("L01 x-ln(1+x)", [round(x-math.log(1+x),6) for x in (0.01,0.05,0.25)])
print("L01 M2 Laspeyres", F(2*6+3*2, 1*6+4*2), float(F(2*6+3*2, 1*6+4*2)))
print("L01 R2 price per quality", F(3,2)/1, F(3,2)/2 - 1 if False else F(3,2)*F(1,2)-1, "index rise", F(3,2)-1)
print("L01 Prop2.4 A check PL>PP", PL_A > PP_A, "B check", PL_B < PP_B)

# ---- L02 seeded economy (independent draw order replica) ----
ALPHA, H, SEED = 0.3, 40, 2026
rng = __import__("random").Random(SEED)
A, K, L = [1.0], [100.0], [50.0]
for _ in range(H):
    A.append(A[-1]*math.exp(rng.uniform(0.005, 0.02)))
    K.append(K[-1]*math.exp(rng.uniform(0.02, 0.05)))
    L.append(L[-1]*math.exp(rng.uniform(0.0, 0.015)))
Y = [a*k**ALPHA*l**(1-ALPHA) for a, k, l in zip(A, K, L)]
lg = lambda v: [math.log(v[t]) - math.log(v[t-1]) for t in range(1, len(v))]
dY, dK, dL, dA = lg(Y), lg(K), lg(L), lg(A)
mean = lambda v: sum(v)/len(v)
res = [y - ALPHA*k - (1-ALPHA)*l for y, k, l in zip(dY, dK, dL)]
print("L02 max gap", max(abs(r-a) for r, a in zip(res, dA)))
mY, mK, mL, mR = mean(dY), mean(dK), mean(dL), mean(res)
print("L02 means Y K L res", mY, mK, mL, mR)
print("L02 terms", ALPHA*mK, (1-ALPHA)*mL, "shares", ALPHA*mK/mY, (1-ALPHA)*mL/mY, mR/mY, "sum", (ALPHA*mK + (1-ALPHA)*mL + mR)/mY)
r2 = mean([y-0.2*k-0.8*l for y, k, l in zip(dY, dK, dL)])
r4 = mean([y-0.4*k-0.6*l for y, k, l in zip(dY, dK, dL)])
print("L02 avg res a=0.2", r2, "a=0.4", r4, "diff", r2-r4, "0.2*(mK-mL)", 0.2*(mK-mL))
simpleY = [y/x-1 for x, y in zip(Y[:-1], Y[1:])]
print("L02 simple mean", mean(simpleY), "log mean", mY, "all log<=simple", all(math.log(1+s) <= s for s in simpleY))
print("L02 E2 implied", ALPHA*mK/ALPHA, "0.014223 check", 0.4*(0.010667/0.3))
print("L02 1.1^0.3", 1.1**0.3, 1.1**0.3-1, 0.3*math.log(1.1), 0.3*0.1)
print("L02 M2 0.3ln2", 0.3*math.log(2), "ln2", math.log(2))
print("L02 M3 residual", 0.04-0.25*0.05-0.75*0.02)
print("L02 R3", 0.01-0.3*0.05-0.7*0.0)

# ---- L03 steady state, Decimal ----
al, s, dl, n = D("0.3"), D("0.2"), D("0.05"), D("0.01")
ks = (s/(n+dl)) ** (1/(1-al))
print("L03 k*", f"{ks:.10f}", "y*", f"{ks**al:.10f}")
g = lambda k: (s*k**al + (1-dl)*k)/(1+n)
k = D(1); first = None; gaps = {}
for t in range(1, 1001):
    k = g(k)
    if first is None and abs(k-ks) < D("1e-12"):
        first = t
    if t in (50, 100, 500):
        gaps[t] = ks-k
print("L03 first <1e-12", first, "gap50", f"{gaps[50]:.10f}", "gap100", f"{gaps[100]:.10f}", "gap500", f"{gaps[500]:.10f}")
print("L03 E1 ratio", gaps[100]/gaps[50], f"{float(gaps[100]/gaps[50]):.6f}")
dks = ks/((1-al)*s); dkd = -ks/((1-al)*(n+dl))
print("L03 dk/ds", f"{dks:.10f}", "dk/ddelta", f"{dkd:.10f}", "elasticity", f"{s/ks*dks:.10f}")
print("L03 E2", D("0.01")*dks, D("0.01")*dks/ks, f"{float(D('0.01')*dks/ks)*100:.4f}%")
print("L03 E3 linear", D("0.001")*dkd)
print("L03 Remark2.5 ratio", "expected 1+n =", 1+n)
# finite difference of k* in s with step 1e-10 and in delta
h = D("1e-10")
ksf = lambda ss, dd, nn: (ss/(nn+dd))**(1/(1-al))
fds = (ksf(s+h, dl, n)-ksf(s-h, dl, n))/(2*h)
fdd = (ksf(s, dl+h, n)-ksf(s, dl-h, n))/(2*h)
print("L03 fd ds", f"{fds:.10f}", "fd ddelta", f"{fdd:.10f}", "fd dn", f"{(ksf(s,dl,n+h)-ksf(s,dl,n-h))/(2*h):.10f}")
print("L03 relerr ds", f"{abs(fds-dks)/abs(dks):.3e}", "relerr dd", f"{abs(fdd-dkd)/abs(dkd):.3e}")
# grid sign check, 50 points
below = sum(1 for i in range(1, 51) if D(i)/5 < ks)
print("L03 grid below", below, "above", 50-below)
# M1 / M2 / M3 values
k1 = D(1)/4 + D(9)/10
k2 = D("0.25")*D("1.15").sqrt() + D("0.9")*D("1.15")
print("L03 M1/M2 k1", k1, "k2", f"{k2:.10f}", "sqrt1.15", f"{D('1.15').sqrt():.10f}")
print("L03 M1 y*", D("25")/4 ** D("0.5") if False else (D(25)/4).sqrt(), "c*", D(3)/4*(D(5)/2))
