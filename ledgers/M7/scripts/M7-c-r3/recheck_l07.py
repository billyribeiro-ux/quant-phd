from itertools import product
from fractions import Fraction
H=4; GRID=(0,100,200,300,400); U={0:0,100:60,200:100,300:120,400:130}
def bq(w): return w//100
V=[None]*(H+1); V[H]={w:bq(w) for w in GRID}
for t in range(H-1,-1,-1):
    V[t]={w:max(U[c]+V[t+1][w-c] for c in GRID if c<=w) for w in GRID}
for t in range(H+1): print('t',t,[V[t][w] for w in GRID])
cnt=0; match=True
for t in range(H):
    for w in GRID:
        best=None
        for seq in product(GRID,repeat=H-t):
            x=w; tot=0; ok=True
            for c in seq:
                if c>x: ok=False; break
                tot+=U[c]; x-=c
            if not ok: continue
            tot+=bq(x)
            if t==0 and w==400: cnt+=1
            best=tot if best is None or tot>best else best
        match = match and best==V[t][w]
print('count from (0,400)',cnt,'C(8,4)=',__import__('math').comb(8,4),'match',match)
print('V0(400)',V[0][400],'V1(400)',V[1][400],'V3(400)',V[3][400],'diff',V[0][400]-V[3][400])
print('greedy 130/240=',Fraction(130,240),float(Fraction(130,240)))
print('E1 diffs',[V[t][400]-V[t+1][400] for t in range(4)])
# Remark 2.5 and R2 by hand
print('Remark2.5: V0(x)=max(0+0,1+0)=',max(0,1))
