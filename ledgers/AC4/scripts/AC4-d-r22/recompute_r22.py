from fractions import Fraction as F
import itertools
def D(q,E,K): return max(0,q+E-K)
def tmin(v,pm,K,E,q): return v + F(D(q,E,K)*(pm-v),q)
# M1 / section 4
v,pm,K,E,q,r=40,60,10000,8000,5000,80
print("S4 D,tmin,tmax,Sigma:", D(q,E,K), tmin(v,pm,K,E,q), r, q*(r-v)-D(q,E,K)*(pm-v))
print("S4 dS(52),dS(46),dB(52):", q*(52-v)-D(q,E,K)*(pm-v), q*(46-v)-D(q,E,K)*(pm-v), q*(r-52))
K2=12000; print("M2 K=12000 D,tmin,Sigma:", D(q,E,K2), tmin(v,pm,K2,E,q), q*(r-v)-D(q,E,K2)*(pm-v))
print("M3 r=50 tmin,tmax,Sigma:", tmin(v,pm,K,E,q), 50, q*(50-v)-D(q,E,K)*(pm-v))
# misconception 2
print("MC2 D,tmin,dB(60),Sigma:", D(2000,8000,10000), tmin(40,60,10000,8000,2000), 2000*(55-60), 2000*(55-40))
print("MC1 full-cost dS(46):", q*(46-v)-D(q,E,K)*(pm-v), "46<52:", 46<52)
# P2 over grid with q<=K, E<=K, pm>=v, q>0
bad=0; n=0
for K_ in range(1,13):
  for q_ in range(1,K_+1):
    for E_ in range(0,K_+1):
      for v_ in range(0,6):
        for pm_ in range(v_, v_+8):
          n+=1
          if tmin(v_,pm_,K_,E_,q_) > pm_: bad+=1
print("P2 grid cases", n, "violations", bad)
# P3 nonempty iff qr >= D pm, with v=0
bad=0;n=0
for K_ in range(1,10):
  for q_ in range(1,K_+1):
    for E_ in range(0,K_+1):
      for pm_ in range(0,8):
        for r_ in range(0,20):
          n+=1
          nonempty = F(D(q_,E_,K_)*pm_,q_) <= r_
          if nonempty != (q_*r_ >= D(q_,E_,K_)*pm_): bad+=1
print("P3 grid", n, "violations", bad)
print("E1 75/187 =", round(75/187,4), " 73/112 =", round(73/112,4), " 4/28 =", round(4/28,4), " 1/7 =", round(1/7,4))
print("L08 S4: RI", 120-0.09*1000, "EVA", 120*0.8-0.09*1000, "dRI", 80-0.09*80, "dEVA", 0.8*80-0.09*80)
print("L08 M3:", 160-0.09*1040, 0.8*160-0.09*1040, 0.8*40-0.09*40)
print("L08 SIM-G gap:", 0.2*13680, 2250-2736)
print("E share pct check 4/28 rounding:", f"{4/28:.4f}")
