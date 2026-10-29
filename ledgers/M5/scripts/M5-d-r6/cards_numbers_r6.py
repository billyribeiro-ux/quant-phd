import math, random
# four-point grid, alpha 0.5
G = (0.25, 0.5, 0.75, 1.0); A = 0.5
def B(vals, beta, grid=G):
    out=[]
    for k in grid:
        o = k**A
        out.append(max(math.sqrt(o-kp)+beta*vals[j] for j,kp in enumerate(grid) if kp<=o))
    return out
def sd(a,b): return max(abs(x-y) for x,y in zip(a,b))
def iters(beta, tol=1e-12):
    v=[0.0]*4; n=0
    while True:
        new=B(v,beta); n+=1
        if sd(new,v)<=tol: return n
        v=new
print("L08 iterations beta .5", iters(0.5), " beta .9", iters(0.9), " beta .95", iters(0.95))
# L08 lab gap rule: check the lab's own definition: "successive gap at most 1e-12"
# L08 seeded ratio: seed 20261028, 2000 pairs (check lab's generation)
src=open("tests/labs/M5/lab-M5-L08-1.py").read()
import re
print([l for l in src.splitlines() if "random" in l or "Random" in l or "uniform" in l or "randrange" in l][:8])
