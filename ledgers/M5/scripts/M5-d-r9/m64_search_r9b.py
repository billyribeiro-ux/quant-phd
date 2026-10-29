import random, math, time
def run(grid, beta, alpha, sweeps):
    def res(k): return k**alpha
    def bell(v):
        out=[]
        for k in grid:
            a=res(k)
            out.append(max(math.sqrt(a-kp)+beta*v[j] for j,kp in enumerate(grid) if kp<=a))
        return out
    v=[0.0]*len(grid); worst=None
    for s in range(sweeps):
        new=bell(v)
        d=[abs(x-y) for x,y in zip(new,v)]
        ratio=d[-1]/max(d) if max(d)>1e-13 else 1.0
        if worst is None or ratio<worst[0]:
            worst=(ratio,s+1,grid,beta,alpha,d)
        v=new
    return worst
rng=random.Random(9)
best=None; t0=time.time(); n=0
while time.time()-t0<150:
    m=rng.randint(2,8)
    pts=sorted(rng.sample([i/100 for i in range(1,301)], m))
    if pts[0]>1: continue
    beta=rng.uniform(0.3,0.99); alpha=rng.uniform(0.02,0.98)
    w=run(pts,beta,alpha,rng.randint(1,200))
    n+=1
    if best is None or w[0]<best[0]: best=w
print('trials',n)
print("min last/max ratio", best[0], "sweep", best[1], "grid", best[2], "beta", best[3], "alpha", best[4])
print("diffs", best[5])
