# Independent recomputation for M6-c round 2 (DP and closed forms; no lab code reused).
from fractions import Fraction as F
from math import comb, floor, log2

def hit_dist(N):
    # distribution of first hitting time tau of level +1 by fair walk, DP over (time, level, alive)
    dist = {}  # k -> prob of tau == k
    state = {0: F(1)}  # level -> prob, still alive (not yet hit +1), level <= 0
    for k in range(1, N + 1):
        new = {}
        for lev, p in state.items():
            for step in (1, -1):
                nl = lev + step
                if nl == 1:
                    dist[k] = dist.get(k, F(0)) + p / 2
                else:
                    new[nl] = new.get(nl, F(0)) + p / 2
        state = new
    return dist

d = hit_dist(8)
cum = F(0)
for k in range(0, 9):
    cum += d.get(k, F(0))
    print("k", k, "P(tau<=k)", cum, float(cum))
print("P(tau=1)", d[1], "P(tau=3)", d[3], "P(tau<=2)", d.get(1,0)+d.get(2,0))
print("P(tau<=4)==P(tau<=3)", sum(d.get(k,0) for k in range(5)) == sum(d.get(k,0) for k in range(4)))
print("sum first-hit", float(sum(d.values())))

# L10: doubling with capital K
for K in (1, 6, 10, 100, 1000):
    m = floor(log2(K + 1))
    ruin = F(1, 2**m)
    print("K", K, "m", m, "win", 1 - ruin, "ruin wealth", K + 1 - 2**m, "E", (1 - ruin) * (K + 1) + ruin * (K + 1 - 2**m))
# L10 Part B: P(tau>n)=2^-n; E[min(tau,n) gain] = 0; win part = 1-2^-n
for n in (1, 2, 3, 5, 10):
    win_part = sum(F(2**(k-1)) * F(1, 2**k) for k in range(1, n + 1))  # win at k: gain 2^{k-1}, prob 2^{-k}
    loss_part = -(2**n - 1) * F(1, 2**n)
    print("n", n, "win part", win_part, "loss part", loss_part, "total", win_part + loss_part)

# L11: E|S_N| and the largest Doob ratio, exact via binomial distribution of paths
def ES(N):
    return sum(F(comb(N, j) * abs(2*j - N), 2**N) for j in range(N + 1))
for N in (1, 2, 3, 4, 12):
    print("N", N, "E|S_N|", ES(N), float(ES(N)))
# Doob tail at lambda via exact enumeration of max over path with DP on (level, running max)
def tail(N, lam):
    st = {(0, 0): F(1)}  # (position, running max of |S|)
    for k in range(N):
        ns = {}
        for (pos, mx), p in st.items():
            for s in (1, -1):
                q = pos + s
                nm = max(mx, abs(q))
                ns[(q, nm)] = ns.get((q, nm), F(0)) + p / 2
        st = ns
    return sum(p for (pos, mx), p in st.items() if mx >= lam)
for N in (1, 2, 3, 4, 9, 12):
    best = F(0); bl = None; bp = None
    for j in range(1, 2*(N+1)+1):
        lam = F(j, 2)
        P = tail(N, lam)
        r = lam * P / ES(N)
        assert P <= ES(N) / lam
        if r > best: best, bl, bp = r, lam, P
    print("N", N, "largest ratio", float(best), "at", bl, "prob", bp)
