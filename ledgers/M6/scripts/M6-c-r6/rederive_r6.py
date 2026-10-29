# Independent re-derivation (own code, not the lab's) of the M6-c slice numbers.
from fractions import Fraction as F
from itertools import product
import math

# L09: hitting time of +1 by 8-step walk
cnt = {}
for k in range(0, 9):
    c = 0
    for p in product((-1, 1), repeat=8):
        s = 0; hit = False
        for st in p[:k]:
            s += st
            if s == 1: hit = True; break
        c += hit
    cnt[k] = c
print("L09 hit counts by k:", cnt)
print("L09 P(tau<=3)=", F(cnt[3], 256), " P(tau=3)=", F(1, 8), " E2 never=", 256 - cnt[8], F(256 - cnt[8], 256))
# M1 3-step check
c1 = sum(1 for p in product((-1,1),repeat=3) if p[0]==1)
print("M1 P(tau=1)=", F(c1,8), "P(tau<=2)=", F(sum(1 for p in product((-1,1),repeat=3) if (p[0]==1 or p[0]+p[1]==1)),8))

# L10: finite-capital doubling, exact
def doubling(K):
    m = int(math.floor(math.log2(K+1)))
    # win prob & ruin wealth from first principles
    ruin_prob = F(1, 2**m)
    win_wealth = K + 1
    ruin_wealth = K + 1 - 2**m
    exp = (1-ruin_prob)*win_wealth + ruin_prob*ruin_wealth
    return m, 1-ruin_prob, ruin_prob, win_wealth, ruin_wealth, exp
for K in (1, 6, 10, 100, 1000):
    print("L10 K", K, doubling(K), "exp==K", doubling(K)[-1] == K)
# Part B: E[stopped] for n
for n in (1, 2, 3, 5, 10):
    e = F(0)
    for p in product((0,1), repeat=n):
        v = 0
        for k, b in enumerate(p, 1):
            stake = 2**(k-1)
            if b: v += stake; break
            v -= stake
        e += F(v, 2**n)
    print("L10 n", n, "E[stopped]=", e, "P(tau>n)=", F(1,2**n))

# L11: ratio lambda P(A)/E[Z_N] for Z=|S_k|, grid j/2
best = {}
for N in range(1, 13):
    EZ = F(0)
    for p in product((-1,1), repeat=N):
        EZ += F(abs(sum(p)), 2**N)
    worst = (F(0), None, None)
    for j in range(1, 2*(N+1)+1):
        lam = F(j, 2)
        pa = F(0)
        for p in product((-1,1), repeat=N):
            s = 0; mx = 0
            for st in p:
                s += st; mx = max(mx, abs(s))
            if mx >= lam: pa += F(1, 2**N)
        r = lam*pa/EZ
        if r > worst[0]: worst = (r, lam, pa)
    best[N] = (float(worst[0]), worst[1], worst[2], EZ)
    print("L11 N", N, "ratio", f"{float(worst[0]):.6f}", "lam", worst[1], "P", worst[2], "E|S_N|", EZ)

# L12: dyadic error and second moment at level n, grid max error
for n in range(0, 11):
    cells = 2**n
    err = F(0); sm = F(0)
    for j in range(cells):
        a, b = F(j, cells), F(j+1, cells)
        c = (a+b)/2
        err += ((b-c)**3 - (a-c)**3)/3
        sm += c*c*(b-a)
    assert err == F(1, 12*4**n) and sm == F(1,3) - F(1, 12*4**n)
print("L12 formulas re-derived for n=0..10")
# L12 grid max error for n=10
n = 10; cells = 2**n; worst = F(0)
for j in range(4097):
    x = F(j, 4096)
    idx = min(int(x*cells), cells-1)
    c = F(2*idx+1, 2*cells)
    worst = max(worst, abs(c-x))
print("L12 n=10 grid max error", worst, float(worst))
print("L12 E[M_2^2]", F(84,64)/4, "1/3-1/192", F(1,3)-F(1,192))
print("L12 1/192 =", f"{1/192:.10f}", " 2^-11 =", F(1,2048), float(F(1,2048)), "1/(12*4^10)=", F(1,12*4**10))
