import random, itertools
from collections import deque
SEED=20261028
def gen(rng,n,p):
    adj={v:[] for v in range(n)}
    for u in range(n):
        for v in range(u+1,n):
            if rng.random()<p: adj[u].append(v); adj[v].append(u)
    for v in adj: adj[v].sort()
    return adj
def all_simple_min(adj,s):
    best={s:0}; npaths=0
    stack=[(s,(s,))]
    while stack:
        v,path=stack.pop()
        npaths+=1
        L=len(path)-1
        if v!=s: best[v]=min(best.get(v,10**9),L)
        for u in adj[v]:
            if u not in path: stack.append((u,path+(u,)))
    return best,npaths
def bfs_d(adj,s):
    d={s:0}; q=deque([s]); insp=0; order=[]
    while q:
        v=q.popleft(); order.append(v)
        for u in adj[v]:
            insp+=1
            if u not in d: d[u]=d[v]+1; q.append(u)
    return d,insp,order
rng=random.Random(SEED)
graphs=0; src=0; reach=0; unreach=0; mism=0; total_paths=0
for k in range(40):
    n=3+k%5; p=0.2+0.1*(k%4)
    adj=gen(rng,n,p); graphs+=1
    for s in range(n):
        src+=1
        d,_,_=bfs_d(adj,s)
        b,np_=all_simple_min(adj,s); total_paths+=np_
        if d!=b: mism+=1
        reach+=len(d); unreach+=n-len(d)
print("indep Part A: graphs",graphs,"sources",src,"reach",reach,"unreach",unreach,"mism",mism,"simple paths enumerated (no pruning)",total_paths)
def dfs_intervals(adj):
    d={};f={};t=[0]
    def visit(v):
        t[0]+=1; d[v]=t[0]
        for u in adj[v]:
            if u not in d: visit(u)
        t[0]+=1; f[v]=t[0]
    for v in range(len(adj)):
        if v not in d: visit(v)
    return d,f
pv=0;viol=0
for k in range(40):
    n=3+k%5; p=0.2+0.1*(k%4); adj=gen(rng,n,p)
    d,f=dfs_intervals(adj)
    for u in range(n):
        for v in range(u+1,n):
            pv+=1
            ok = f[u]<d[v] or f[v]<d[u] or (d[u]<d[v] and f[v]<f[u]) or (d[v]<d[u] and f[u]<f[v])
            if not ok: viol+=1
print("indep Part B: pairs",pv,"violations",viol)
rng=random.Random(SEED+1000)
adj=gen(rng,200,0.03)
E=sum(len(adj[v]) for v in adj)//2
d,insp,order=bfs_d(adj,0)
print("indep D: edges",E,"reached",len(d),"insp",insp,"2E",2*E,"sum",len(d)+insp,"matrix",len(d)*200)
print("40000/1438=",40000/1438,"1438*27=",1438*27,"rem",40000-1438*27,"1238/200=",1238/200)
