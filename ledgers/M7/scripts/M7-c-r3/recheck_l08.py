from fractions import Fraction as F
from itertools import product
D=F(9,10); H=6; S=(0,1,2); PROFIT={0:6,1:4,2:1}
def rew(s,a): return F(PROFIT[s]) if a=='run' else F(-4)
def nxt(s,a): return min(s+1,2) if a=='run' else 0
# independent recursion with explicit dict-of-lists
V=[None]*(H+1); V[H]={s:F(0) for s in S}
for t in range(H-1,-1,-1):
    V[t]={s:max(rew(s,a)+D*V[t+1][nxt(s,a)] for a in ('run','repair')) for s in S}
for t in range(H+1):
    print('t',t,[str(V[t][s]) for s in S], [float(V[t][s]) for s in S])
# policy and ties
for t in range(H):
    row=[]
    for s in S:
        c={a:rew(s,a)+D*V[t+1][nxt(s,a)] for a in ('run','repair')}
        row.append((s,'run' if c['run']>c['repair'] else ('repair' if c['repair']>c['run'] else 'TIE')))
    print('policy',t,row)
# brute force counts
tot=0; ok=True
for t in range(H):
    for s in S:
        best=None
        for plan in product(('run','repair'),repeat=H-t):
            st=s; tot_=F(0); w=F(1)
            for a in plan:
                tot_+=w*rew(st,a); w*=D; st=nxt(st,a)
            best=tot_ if best is None or tot_>best else best
            tot+=1
        ok = ok and best==V[t][s]
print('plans',tot,'match',ok)
# iterates
U={s:F(0) for s in S}; it=[U]
for n in range(6):
    U={s:max(rew(s,a)+D*it[-1][nxt(s,a)] for a in ('run','repair')) for s in S}; it.append(U)
ch=[max(abs(it[n+1][s]-it[n][s]) for s in S) for n in range(6)]
print('changes',[str(c) for c in ch],[float(c) for c in ch])
print('ratios',[str(ch[i]/ch[i-1]) for i in range(1,6)])
print('iter==V', all(it[n][s]==V[H-n][s] for n in range(7) for s in S))
# decimal places of V0(0)
import math
v=V[0][0]; print('V0(0) exact',v, float(v), 'den',v.denominator)
print('V0(0)-V1(0) exact', V[0][0]-V[1][0], 'V4-V5', V[4][0]-V[5][0])
