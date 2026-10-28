import math, random, sys
def sweep(beta, alpha, grid, V):
    out=[]
    for k in grid:
        a=k**alpha
        out.append(max(math.sqrt(a-kp)+beta*v for kp,v in zip(grid,V) if kp<=a))
    return out
rng=random.Random(int(sys.argv[1]))
viol=0; lastfail=0; tested=0; worst=0.0; worstcase=None
for trial in range(int(sys.argv[2])):
    beta=rng.uniform(0.5,0.99); alpha=rng.uniform(0.05,0.95)
    m=rng.randint(2,12)
    g=[rng.uniform(0.05,1.0)]
    for _ in range(m-1): g.append(g[-1]+rng.uniform(0.01,0.6))
    V=[0.0]*m
    prev=None
    for n in range(1,60):
        new=sweep(beta,alpha,g,V)
        d=[x-y for x,y in zip(new,V)]
        tested+=1
        if min(d)< -1e-13: viol+=1
        if any(d[i]>d[i+1]+1e-13 for i in range(m-1)): viol+=1000000
        sup=max(abs(x) for x in d)
        ratio = abs(d[-1])/sup if sup>1e-9 else 1
        if ratio<1-1e-6:
            lastfail+=1
            if 1-ratio>worst: worst=1-ratio; worstcase=(beta,alpha,g,n)
        V=new
print("tested",tested,"monotone-or-sign violations",viol,"last-point-not-sup",lastfail,"worst",worst)
if worstcase: print(worstcase)
