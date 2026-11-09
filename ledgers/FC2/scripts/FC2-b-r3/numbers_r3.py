"""FC2 slice b round 3: independent re-derivation of the numbers in L04-L06 (Fraction arithmetic, own code)."""
from fractions import Fraction as F
import math

def usd2(x):  # cents-as-Fraction -> two-decimal dollars, round half even as Python float format
    return f"{float(x)/100:.2f}"

print("== L04 Example 2.5 (strike 100, D=9/10, path 100,120,90,80,110)")
D = F(9, 10); K = 100
path = [100, 120, 90, 80, 110]
call_int = [max(s-K, 0) for s in path]
put_int = [max(K-s, 0) for s in path]
print("call intrinsic", call_int, "put intrinsic", put_int)
call_pv = [F(call_int[t]) * D**t for t in range(5)]
put_pv = [F(put_int[t]) * D**t for t in range(5)]
print("call PV at 0 by exercise date", [str(x) for x in call_pv])
print("put PV at 0 by exercise date", [str(x) for x in put_pv])
print("call hold PV at 0 =", F(call_int[4])*D**4, float(F(call_int[4])*D**4))
print("call hold value at t (page table)", [str(F(call_int[4])*D**(4-t)) for t in range(5)])
print("put hold PV at 0 =", F(put_int[4])*D**4)
print("ln(10/9) =", math.log(10/9))
print("R1 S_tau =", 100 + F(20000, 729), float(100 + F(20000, 729)))
print("R3 path 100,90,95,110,150 call intrinsic t0..3:", [max(s-100,0) for s in [100,90,95,110]], "best PV", F(10)*D**3, "hold PV", F(50)*D**4, float(F(50)*D**4))
print("E2 path with last 90: put intrinsic", [max(100-s,0) for s in [100,120,90,80,90]], "PVs", [float(F(max(100-s,0))*D**t) for t,s in enumerate([100,120,90,80,90])])
print("E2 call PVs", [float(F(max(s-100,0))*D**t) for t,s in enumerate([100,120,90,80,90])], "hold", float(F(0)))
print("E3 put at t=2 PV", F(10)*D**2, float(F(10)*D**2))
print("L04 M1 payoff 12 profit 8 break-even 54; M2 breakeven 77 profit at 60:", 80-3, max(80-60,0)-3)
print("L04 curve: profit call at 125 =", max(125-100,0)-8, "put break-even", 100-7)

print("== L05 synthetic set (S=100, D=9/10, strikes 80..120, calls max(S-DK,0)+max(100-K,0)/10)")
S = F(100); D5 = F(9, 10)
strikes = [80, 90, 100, 110, 120]
def C(k, DD=D5):
    return max(S - DD*k, 0) + F(max(100-k, 0), 10)
calls = [C(k) for k in strikes]
puts = [c - S + D5*k for c, k in zip(calls, strikes)]
print("calls", [str(x) for x in calls], "puts", [str(x) for x in puts])
def bounds(k, c, p, DD):
    dk = DD*k; v = []
    if not (0 <= c <= S): v.append("call0S")
    if c < max(S-dk, 0): v.append("callLB")
    if not (0 <= p <= dk): v.append("putDK")
    if p < max(dk-S, 0): v.append("putLB")
    return v
print("bound violations at D=9/10:", [bounds(k,c,p,D5) for k,c,p in zip(strikes,calls,puts)])
for DD in [F(1,100), F(1,2), F(1), F(11,10), F(2)]:
    cs = [C(k, DD) for k in strikes]
    ps = [c - S + DD*k for c,k in zip(cs,strikes)]
    print("D=", DD, "calls", [str(x) for x in cs], "bounds", [bounds(k,c,p,DD) for k,c,p in zip(strikes,cs,ps)])
# convexity at D=9/10 and planted
def convex_viol(ks, cs):
    out=[]
    from itertools import combinations
    for i,j,k in combinations(range(len(ks)),3):
        lam = F(ks[k]-ks[j], ks[k]-ks[i]); chord = lam*cs[i] + (1-lam)*cs[k]
        if cs[j] > chord: out.append((ks[i],ks[j],ks[k]))
    return out
print("convex viol synthetic", convex_viol(strikes, calls))
pc = list(calls); pc[1] = pc[1] + 5  # 90 USD call +500 cents = +5 USD
pp = list(puts); pp[1] = pp[1] + 5
print("planted convex (90 call & put +5):", convex_viol(strikes, pc), "parity cost", [str(c - p - S + D5*k) for c,p,k in zip(pc,pp,strikes)])
print("planted parity 100 put +3:", [str(c - (p + (3 if k==100 else 0)) - S + D5*k) for c,p,k in zip(calls,puts,strikes)])
print("second differences at 90,100,110 (cents):", [calls[i-1]*100 - 2*calls[i]*100 + calls[i+1]*100 for i in (1,2,3)])
print("E1 values check (USD):", float(calls[1]), float(calls[2]), float(calls[3]))
print("R2 r=-0.1 bound", 120 - math.exp(0.1)*100, "intrinsic", 20)
print("canon put example", 100*math.exp(-0.1) - 50)
print("M1 put", 8 - 100 + F(97,100)*105, "M2 LB", max(50 - F(95,100)*40, 0), "M2 position", 3 - 50 + F(95,100)*40)
print("M3 second diff 15-18+4 =", 15-2*9+4, "chord", (15+4)/2)
print("L05 E1 check 100 vs 0.97 ok")

print("== L06 numbers")
q = (F(5,4)-F(1,2))/(F(3,2)-F(1,2))
print("Ex1.5 q", q)
Vu, Vd = F(50), F(0)
Delta = (Vu-Vd)/((F(3,2)-F(1,2))*100); B = (F(3,2)*Vd - F(1,2)*Vu)/((F(3,2)-F(1,2))*F(5,4))
print("Ex1.5 Delta", Delta, "B", B, "V0", Delta*100+B, "q-form", (q*Vu+(1-q)*Vd)/F(5,4))
print("Ex1.6 cash", 35-50+20, "lent->", F(5)*F(5,4), "up", F(1,2)*150 - 20*F(5,4) - 50 + F(25,4)*0 + 0, "check up total", F(1,2)*150 - F(20)*F(5,4) - 50 + 0)
# Ex 1.6 totals explicit
up_total = -50 + F(1,2)*150 - 20*F(5,4) + F(5)*F(5,4)
dn_total = 0 + F(1,2)*50 - 20*F(5,4) + F(5)*F(5,4)
print("Ex1.6 totals up/down", up_total, dn_total)
# Example 3.4
S2 = {2:{2:225,1:75,0:25}}
def V(n,k,S0=100,u=F(3,2),d=F(1,2),R=F(5,4),f=lambda s: max(F(s)-100,0)):
    if n==2: return f(S0*u**k*d**(2-k))
    return (q*V(n+1,k+1,S0,u,d,R,f)+(1-q)*V(n+1,k,S0,u,d,R,f))/R
print("Ex3.4 V(0,0)", V(0,0), "V(1,1)", ((q*125)/F(5,4)), "V(1,0)", V(1,0))
EXP = sum(math.comb(2,k)*q**k*(1-q)**(2-k)*max(100*F(3,2)**k*F(1,2)**(2-k)-100,0) for k in range(3))/F(5,4)**2
print("Ex3.4 closed form", EXP)
Es = q**2*225 + 2*q*(1-q)*75 + (1-q)**2*25
print("E^Q[S2]", Es, "R^2 S0", F(25,16)*100, "disc", Es/F(25,16), "payoff at E", max(Es-100,0), "disc payoff", max(Es-100,0)*F(16,25), "E payoff", q**2*125, float(q**2*125))
# M1-M3
q1 = (F(5,4)-F(1,2))/(2-F(1,2)); print("M1 q", q1, "V0", (q1*100)/F(5,4))
print("M2 Delta", (100-0)/((2-F(1,2))*100), "B", (2*0 - F(1,2)*100)/((2-F(1,2))*F(5,4)), "V0", F(100)/((2-F(1,2))*100)*100 + (-F(50)/((2-F(1,2))*F(5,4))))
print("M3 V11", (q1*300)/F(5,4), "V00", (q1*(q1*300/F(5,4)))/F(5,4))
print("E2 doubled", (F(3,4)*100)/F(5,4))
print("E3 quote 28 ok", "cash", -28 + 50 - 20 - 2 + 0)
print("R1 claim B", F(-100)/F(5,4), "claim pays", 150*1 + F(-80)*F(5,4) , 100 + F(-80)*F(5,4), 50 + F(-80)*F(5,4))
print("R2 q", (1-F(1,2))/(F(3,2)-F(1,2)), "V0", (F(1,2)*50)/1, "B", (0 - F(1,2)*50)/((F(3,2)-F(1,2))*1))
print("Canon Sec4 example", "Delta*50 eq 0 -> Delta=0; first eq 0=1")
