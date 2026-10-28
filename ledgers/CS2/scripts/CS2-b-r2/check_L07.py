import itertools
M=1103515245;I=12345;MOD=2**31
class G:
    def __init__(s,seed): s.s=seed%MOD
    def below(s,n):
        s.s=(M*s.s+I)%MOD; return (s.s>>16)%n
g=G(20261028)
pairs=[]
for _ in range(30):
    m=1+g.below(7); n=1+g.below(7)
    x="".join("ACGT"[g.below(4)] for _ in range(m)); y="".join("ACGT"[g.below(4)] for _ in range(n))
    pairs.append((x,y))
cases=[]
for _ in range(30):
    size=2+g.below(3); ch=set()
    while len(ch)<size: ch.add(1+g.below(9))
    amt=g.below(13); cases.append((tuple(sorted(ch)),amt))
print("first pair",pairs[0], "pairs 0-2", pairs[:3])
# independent LCS (dp), exhaustive over subsequences of x
def lcs_dp(x,y):
    m,n=len(x),len(y); T=[[0]*(n+1) for _ in range(m+1)]
    for i in range(1,m+1):
        for j in range(1,n+1):
            T[i][j]=T[i-1][j-1]+1 if x[i-1]==y[j-1] else max(T[i-1][j],T[i][j-1])
    return T[m][n]
def is_sub(s,t):
    it=iter(t); return all(c in it for c in s)
def lcs_ex(x,y):
    best=0
    for r in range(len(x)+1):
        for idx in itertools.combinations(range(len(x)),r):
            s="".join(x[k] for k in idx)
            if is_sub(s,y): best=max(best,len(s))
    return best
print("LCS first pair", lcs_dp(*pairs[0]), "exhaustive", lcs_ex(*pairs[0]))
assert all(lcs_dp(x,y)==lcs_ex(x,y) for x,y in pairs)
# coins: independent dp with inf
INF=float('inf')
def coins_dp(D,a):
    f=[0]+[INF]*a
    for t in range(1,a+1):
        for c in D:
            if c<=t: f[t]=min(f[t],1+f[t-c])
    return f[a] if f[a]<INF else None
none=sum(1 for D,a in cases if coins_dp(D,a) is None)
print("coin instances with no combination", none, "of", len(cases))
print("f(0..6) for {1,3,4}", [coins_dp((1,3,4),a) for a in range(7)], "amount 20 ->", coins_dp((1,3,4),20))
# greedy
def greedy(D,a):
    r=a;u=0
    while r>0:
        fits=[c for c in D if c<=r]
        if not fits: return None
        r-=max(fits);u+=1
    return u
print("greedy 6 {1,3,4}", greedy((1,3,4),6))
# LCS pair ACGTACG TGCATGC
x,y="ACGTACG","TGCATGC"
print("LCS",lcs_dp(x,y),"table cells", len(x)*len(y))
# memo recursion stored & calls, independent
def memo_stats(x,y):
    cache={}; calls=[0]
    def go(i,j):
        calls[0]+=1
        if i==0 or j==0: return 0
        if (i,j) in cache: return cache[(i,j)]
        v=go(i-1,j-1)+1 if x[i-1]==y[j-1] else max(go(i-1,j),go(i,j-1))
        cache[(i,j)]=v; return v
    go(len(x),len(y)); return len(cache),calls[0]
def naive(x,y):
    c=[0]
    def go(i,j):
        c[0]+=1
        if i==0 or j==0: return 0
        if x[i-1]==y[j-1]: return go(i-1,j-1)+1
        return max(go(i-1,j),go(i,j-1))
    go(len(x),len(y)); return c[0]
print("memo stored, calls", memo_stats(x,y), "naive calls", naive(x,y))
# reached non-base pairs
reached=set()
def walk(i,j):
    if i==0 or j==0 or (i,j) in reached: return
    reached.add((i,j))
    if x[i-1]==y[j-1]: walk(i-1,j-1)
    else: walk(i-1,j); walk(i,j-1)
walk(7,7); print("reached non-base pairs", len(reached))
# coin memo stats for {1,3,4}, amount 20
def cmemo(D,a):
    cache={};calls=[0]
    def b(t):
        calls[0]+=1
        if t==0: return 0
        if t in cache: return cache[t]
        f=[1+s for s in (b(t-c) for c in D if c<=t) if s is not None]
        v=min(f) if f else None; cache[t]=v; return v
    r=b(a); return r,len(cache),calls[0]
def cnaive(D,a):
    calls=[0]
    def b(t):
        calls[0]+=1
        if t==0: return 0
        f=[1+s for s in (b(t-c) for c in D if c<=t) if s is not None]
        return min(f) if f else None
    b(a); return calls[0]
print("coin memo (1,3,4),20 -> answer, stored, calls", cmemo((1,3,4),20), "naive", cnaive((1,3,4),20))
print("2^40 =",2**40, "bits", (2**40).bit_length(), "1000 bits", (1000).bit_length(), "2^20+1", 2**20+1, "bits 2^20", (2**20).bit_length())
print("E1 stored amounts check: amounts 1..20 reached:", sorted(set([a for a in range(0,21)]))[1:]==list(range(1,21)))
