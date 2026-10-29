from itertools import product
H=4; GRID=(0,100,200,300,400); RW={0:0,100:60,200:100,300:120,400:130}
V={H:{w:w//100 for w in GRID}}
for t in range(H-1,-1,-1):
    V[t]={w:max(RW[c]+V[t+1][w-c] for c in GRID if c<=w) for w in GRID}
for t in range(H+1): print("t",t,[V[t][w] for w in GRID])
cnt=0; ok=True
for t in range(H):
    for w in GRID:
        best=None
        for plan in product(GRID,repeat=H-t):
            wl=w; tot=0; good=True
            for c in plan:
                if c>wl: good=False; break
                tot+=RW[c]; wl-=c
            if not good: continue
            if t==0 and w==400: cnt+=1
            tot+=wl//100
            best=tot if best is None or tot>best else best
        ok = ok and best==V[t][w]
print("feasible from (0,400):",cnt,"recursion==brute:",ok)
# greedy
w=400; g=0; tot=0
for _ in range(H):
    c=max((c for c in GRID if c<=w), key=lambda x: RW[x]); tot+=RW[c]; w-=c
print("greedy total", tot+w//100, "optimal", V[0][400], "ratio", round(tot/V[0][400],4))
print("L07 E1 diffs", [V[t][400]-V[t+1][400] for t in range(4)])
