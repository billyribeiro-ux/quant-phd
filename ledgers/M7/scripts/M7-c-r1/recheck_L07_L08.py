from fractions import Fraction as F
from itertools import product
# L07 instance: wealth grid, reward table, bequest W//100, H=4
G=(0,100,200,300,400); R={0:0,100:60,200:100,300:120,400:130}
def V(H):
    tab={H:{w:F(w//100) for w in G}}
    for t in range(H-1,-1,-1):
        tab[t]={w:max(R[c]+tab[t+1][w-c] for c in G if c<=w) for w in G}
    return tab
v=V(4)
print("L07 W400 column", [int(v[t][400]) for t in range(5)], "diffs", [int(v[t][400]-v[t+1][400]) for t in range(4)])
print("L07 ratio 130/240 =", round(130/240,4), F(130,240))
# plan count
n=sum(1 for p in product(G,repeat=4) if sum(p)<=400); print("L07 feasible seqs from 400 (sum<=400)", n)
# brute force V_1(400) plan 200,100,100
print("L07 plan 200,100,100 reward", R[200]+R[100]+R[100]+0)
# L07 Remark 2.5 counterexample by brute force
# L07 R2 objective
print("L07 R2 totals", max(10,5), max(10,3))
# L08 maintenance
D=F(9,10); P={0:6,1:4,2:1}
def rew(s,a): return F(P[s]) if a=='run' else F(-4)
def nxt(s,a): return min(s+1,2) if a=='run' else 0
def bell(H):
    tab={H:{s:F(0) for s in (0,1,2)}}
    for t in range(H-1,-1,-1):
        tab[t]={s:max(rew(s,a)+D*tab[t+1][nxt(s,a)] for a in ('run','repair')) for s in (0,1,2)}
    return tab
b=bell(6)
for t in range(7): print("L08 t",t,[float(b[t][s]) for s in (0,1,2)])
# brute force count and match
cnt=0; ok=True
for t in range(6):
    for s in (0,1,2):
        best=None
        for plan in product(('run','repair'),repeat=6-t):
            st=s; tot=F(0); w=F(1)
            for a in plan:
                tot+=w*rew(st,a); w*=D; st=nxt(st,a)
            cnt+=1
            best=tot if best is None or tot>best else best
        ok = ok and best==b[t][s]
print("L08 brute match",ok,"plans",cnt)
# value iteration changes
U={s:F(0) for s in (0,1,2)}; ch=[]
for n in range(6):
    NU={s:max(rew(s,a)+D*U[nxt(s,a)] for a in ('run','repair')) for s in (0,1,2)}
    ch.append(max(abs(NU[s]-U[s]) for s in (0,1,2))); U=NU
print("L08 changes",[float(c) for c in ch], "ratios", [float(ch[i]/ch[i-1]) for i in range(1,6)])
# M1/M2/M3 of L08 with beta=1/2
D2=F(1,2)
print("L08 M2 V0x", max(2+D2*F(3), 1+D2*2), "V0y", 3+D2*3, "M3 (a,c)", 2+D2*3)
# L08 E1 differences
print("E1", float(F('13.948890')-F('13.358400')), float(F('9.6')-F(6)))
print("E2", float(F('3.6')/6), round(2.74/3.6,4), round(2.466/2.74,4), round(2.2194/2.466,4), round(1.99746/2.2194,4))
print("E3 plans", 3*sum(2**(6-t) for t in range(6)))
