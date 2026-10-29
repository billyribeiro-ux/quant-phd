import math, random, re
ALPHA=0.5; GRID=(0.25,0.5,0.75,1.0); SEED=20261028; PAIRS=2000
def bellman(values, grid, beta):
    new=[];pol=[]
    for k in grid:
        out=k**ALPHA
        feas=[j for j,kp in enumerate(grid) if kp<=out]
        best=-math.inf;bi=-1
        for j in feas:
            c=math.sqrt(out-grid[j])+beta*values[j]
            if c>best: best,bi=c,j
        new.append(best);pol.append(bi)
    return new,pol
def solve(grid,beta,tol=1e-12):
    v=[0.0]*len(grid);n=0
    while True:
        nv,p=bellman(v,grid,beta);n+=1
        gap=max(abs(a-b) for a,b in zip(nv,v))
        v=nv
        if gap<=tol: return v,p,n
v,p,n=solve(GRID,0.9)
print("V*",[f"{x:.9f}" for x in v],"iters",n,"policy",[GRID[j] for j in p])
img,_=bellman(v,GRID,0.9)
print("residual",max(abs(a-b) for a,b in zip(img,v)))
rng=random.Random(SEED);worst=0.0
for _ in range(PAIRS):
    a=[rng.uniform(-10.0,10.0) for _ in GRID]; b=[rng.uniform(-10.0,10.0) for _ in GRID]
    bv,_=bellman(a,GRID,0.9); bw,_=bellman(b,GRID,0.9)
    num=max(abs(x-y) for x,y in zip(bv,bw)); den=max(abs(x-y) for x,y in zip(a,b))
    worst=max(worst,num/den)
print("worst ratio repr",repr(worst),"minus beta",worst-0.9)
for beta in (0.5,0.95,0.9):
    print("beta",beta,"count",solve(GRID,beta)[2])
print("one-point beta0.9", solve((0.25,),0.9)[2], solve((0.25,),0.9)[0])
v=[0.0]
for _ in range(1000): v,_=bellman(v,(0.25,),1.0)
print("beta1 n=1000 V", v)
print("1/ln(1/beta)", [1/math.log(1/b) for b in (0.5,0.9,0.95)])
print("sqrt(0.457107)", math.sqrt(0.457107), 0.9*5+math.sqrt(0.457107))
