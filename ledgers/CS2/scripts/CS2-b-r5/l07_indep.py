import sys
from functools import lru_cache
x, y = "ACGTACG", "TGCATGC"
def run(memo):
    calls = [0]; store = {}
    def L(i, j):
        calls[0] += 1
        if i == 0 or j == 0: return 0
        if memo and (i, j) in store: return store[(i, j)]
        if x[i-1] == y[j-1]: v = L(i-1, j-1) + 1
        else: v = max(L(i-1, j), L(i, j-1))
        if memo: store[(i, j)] = v
        return v
    v = L(len(x), len(y))
    return v, calls[0], len(store)
print("LCS", run(True), "no-memo", run(False)[1], "table cells", (len(x)+1)*(len(y)+1) - (len(x)+len(y)+1) + len(x)*len(y) if False else len(x)*len(y))
# coin: D=(1,3,4), amount 20 -> fewest coins, memo calls and stored amounts, no-memo calls
D=(1,3,4); A=20
calls=[0]; memo={0:0}
def f(a):
    calls[0]+=1
    if a in memo: return memo[a]
    memo[a]=min(1+f(a-c) for c in D if c<=a); return memo[a]
print("coin f(20)", f(A), "memo calls", calls[0], "stored", len(memo)-0)
calls2=[0]
def g(a):
    calls2[0]+=1
    if a==0: return 0
    return min(1+g(a-c) for c in D if c<=a)
print("no-memo calls for 20", (g(A), calls2[0]))
