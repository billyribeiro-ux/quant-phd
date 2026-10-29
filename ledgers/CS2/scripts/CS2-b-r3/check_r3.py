import math, itertools
# L05 R2: tree R(left = M1 tree, right = s with left child t)
class N:
    def __init__(s, k, l=None, r=None): s.k, s.l, s.r = k, l, r
def h(t): return 0 if t is None else 1 + max(h(t.l), h(t.r))
def cnt(t): return 0 if t is None else 1 + cnt(t.l) + cnt(t.r)
def bf(t): return h(t.l) - h(t.r)
def nodes(t): return [] if t is None else [t] + nodes(t.l) + nodes(t.r)
m1 = N(5, N(3, N(2)), N(7))
R = N('R', m1, N('s', N('t')))
print("R height", h(R), "nodes", cnt(R), "bf", {n.k: bf(n) for n in nodes(R)})
print("all AVL", all(-1 <= bf(n) <= 1 for n in nodes(R)))
# N(h) table
Nh = [0, 1]
for k in range(2, 14): Nh.append(1 + Nh[-1] + Nh[-2])
print("N(0..7)", Nh[:8], "N(4)", Nh[4])
# Prop 4.2 check for A in 1..200000
bad = [A for A in range(1, 200001) if not (2**(A.bit_length()-1) < A+1 <= 2**A.bit_length())]
print("Prop4.2 counterexamples in 1..200000:", bad[:5], len(bad))
print("A=0 with b=1:", 2**0 < 0+1 <= 2**1, " (A=0 has no hypothesis A>=1)")
print("2^40 bits", (2**40).bit_length(), 2**40 + 1 > 10**12, 2**40)
print("2^20 bits", (2**20).bit_length(), 2**20+1)
# L06 weighted: simple paths s->c
adj = {0:[1,2],1:[0,2,3],2:[0,1],3:[1]}
w = {(0,1):10,(0,2):1,(1,2):1,(1,3):1}
paths=[]
def dfs(v, path):
    if v==3: paths.append(path[:]); return
    for u in adj[v]:
        if u not in path: path.append(u); dfs(u,path); path.pop()
dfs(0,[0])
print("simple paths s->c:", [(p, sum(w[tuple(sorted(e))] for e in zip(p,p[1:]))) for p in paths])
# L08 M1 / Lemma 2.1-type check: L07 coin greedy vs optimum for {1,3,4}
def opt(D,A):
    f=[0]+[10**9]*A
    for a in range(1,A+1):
        for c in D:
            if c<=a: f[a]=min(f[a],1+f[a-c])
    return f
f=opt((1,3,4),6); print("f(0..6)", f[:7])
def greedy(D,a):
    k=0
    for c in sorted(D,reverse=True):
        while a>=c: a-=c; k+=1
    return k
print("greedy 6:", greedy((1,3,4),6), "greedy 20:", greedy((1,3,4),20), "opt20", opt((1,3,4),20)[20])
print("smallest greedy failure for {1,3,4}:", next(a for a in range(1,100) if greedy((1,3,4),a)!=opt((1,3,4),a)[a]))
