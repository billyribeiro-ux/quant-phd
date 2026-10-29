from fractions import Fraction as F
import random
# L07 section 4 / M2 / K=12000 / P2 / misconceptions
def D(q,E,K): return max(0,q+E-K)
v,pm,K,E,q,r=40,60,10000,8000,5000,80
d=D(q,E,K); tmin=v+F(d*(pm-v),q); S=q*(r-v)-d*(pm-v)
print("S4", d, tmin, S, q*(r-v)-d*(pm-v)==140000)
K2=12000; d2=D(q,E,K2); t2=v+F(d2*(pm-v),q); S2=q*(r-v)-d2*(pm-v)
print("K12000", d2, t2, S2)
# Delta_S, Delta_B at 52 and 46
print("dS52", q*(52-v)-d*(pm-v), "dB52", q*(r-52), "dS46", q*(46-v)-d*(pm-v))
# misconception 2
print("mis2", D(2000,8000,10000), v+F(0,1), 2000*(55-60), 2000*(55-40))
# P2 / Lemma: D<=q given E<=K, scan random integers with q>K too (scope witness)
import itertools
ok=True
for qq in range(1,300):
  for EE in range(0,120):
    for KK in range(0,200):
      if EE>KK: continue
      dd=D(qq,EE,KK)
      if dd>qq: ok=False
print("D<=q over grid incl q>K:", ok)
# M3 r=50
print("M3", tmin, F(50), 5000*(50-40)-3000*20)
# capitalization L08
rr=F(9,100)
print("L08 4", 120-rr*1000, F(96)-90, 80-rr*80, F(8,10)*80-rr*80)
print("L08 M3", 160-rr*1040, F(8,10)*160-rr*1040, 40-rr*40, F(8,10)*40-rr*40)
# Lab 1 counts, integer recompute (own transcription of generator)
rng=random.Random(20261027)
cases=[]
for i in range(1,201):
    v_=rng.randrange(3000,5001,100); pm_=v_+rng.randrange(500,3001,100)
    cap=rng.randrange(6000,12001,500); ext=rng.randint(4000,min(9000,cap))
    qq=rng.randint(1000,8000); rn=v_+rng.randint(-1500,4000)
    cases.append((v_,pm_,cap,ext,qq,rn))
cases.append((4000,6000,10000,8000,5000,5200))
fits=[c for c in cases if c[4]<=c[2]]
over=len(cases)-len(fits)
def tm(c): return F(c[0])+F(D(c[4],c[3],c[2])*(c[1]-c[0]),c[4])
empty=[c for c in fits if tm(c)>c[5]]
feas=[c for c in fits if tm(c)<=c[5]]
binding=[c for c in feas if D(c[4],c[3],c[2])>0]
print("counts over",over,"fits",len(fits),"empty",len(empty),"feas",len(feas),"binding",len(binding))
print("boundary", tm(cases[-1]), cases[-1][5], cases[-1][1]*0)
print("share", round(75/187,4), round(73/112,4), round(4/28,4))
