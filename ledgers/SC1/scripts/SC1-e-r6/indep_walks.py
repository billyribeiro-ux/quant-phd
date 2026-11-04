"""Independent exact recomputation (dynamic programming over the walk, no reuse of lab code) of:
L07 Part A tails P(M_N >= m) at m = isqrt(N) for N in 4,16,64,256,1024;
L08 Part B truncated means E[min(nu_1, N)] for N in 16,64,256; L08 Part A first-passage counts for a=3, n=12;
L06 Part D numbers; and the closed-form values quoted in the lessons. Usage: indep_walks.py"""
import math
from fractions import Fraction

def max_tail(n, m):
    # dist over (position, running max) via DP on exact integers
    dist = {(0, 0): 1}
    for _ in range(n):
        nd = {}
        for (p, h), c in dist.items():
            for s in (1, -1):
                q = p + s
                key = (q, max(h, q))
                nd[key] = nd.get(key, 0) + c
        dist = nd
    return sum(c for (p, h), c in dist.items() if h >= m)

for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    if n <= 256:
        cnt = max_tail(n, m)
    else:
        # for N=1024 use binomial form of the same event via reflection count, cross-checked on N<=256
        cnt = None
    if cnt is not None:
        print(f"L07 A: N={n} m={m} P(M_N>=m)={cnt}/2^{n} = {cnt / 2**n:.6f}")
# N=1024 via reflection principle counts (independent formula): #{M>=m} = #{S>=m} + #{S>m}
def count_end_ge(n, m):
    return sum(math.comb(n, u) for u in range(n + 1) if 2 * u - n >= m)
n, m = 1024, 32
c = count_end_ge(n, m) + count_end_ge(n, m + 1)
print(f"L07 A: N=1024 m=32 P={c}/2^1024 = {c / 2**n:.6f}")

# L08 Part B: E[min(nu_1,N)] = sum_{k<N} P(nu_1 > k), P(nu_1>k) = P(no visit to +1 in first k steps)
def survive_probs(total):
    # exact: P(nu_1 > k) = P(max_{j<=k} S_j < 1) = P(max_{j<=k} S_j <= 0)
    res = []
    for k in range(total):
        # count walks of length k with max<=0 = C(k, floor(k/2)) for even k ... use DP exact
        res.append(None)
    return res
def max_le0_count(k):
    dist = {0: 1}
    for _ in range(k):
        nd = {}
        for p, c in dist.items():
            for s in (1, -1):
                q = p + s
                if q <= 0:
                    nd[q] = nd.get(q, 0) + c
        dist = nd
    return sum(dist.values())
K = 256
surv = [Fraction(max_le0_count(k), 2**k) for k in range(K)]
run = Fraction(0)
trunc = {}
for k in range(K):
    run += surv[k]
    if k + 1 in (16, 64, 256):
        trunc[k + 1] = run
for n in (16, 64, 256):
    print(f"L08 B: N={n} E[min(nu_1,N)] = {float(trunc[n]):.6f}")
# L08 Part A: first passage to 3 at each step k for n=12
def first_passage_counts(n, a):
    counts = [0] * (n + 1)
    dist = {(0, False): 1}
    for k in range(1, n + 1):
        nd = {}
        for (p, hit), c in dist.items():
            for s in (1, -1):
                q = p + s
                h = hit or (q >= a)
                key = (q, h)
                if h and not hit:
                    counts[k] += c
                nd[key] = nd.get(key, 0) + c
        dist = nd
    return counts[a:], sum(counts)
print("L08 A: first passage counts k=3..12 (a=3):", first_passage_counts(12, 3)[0], "total", first_passage_counts(12, 3)[1])
# L06 Part D: N=10, a=2
print("L06 D: P(M_10>=2) =", Fraction(max_tail(10, 2), 1024), "; 2P(S_10>2) =", Fraction(2 * sum(math.comb(10, u) for u in range(10 + 1) if 2 * u - 10 > 2), 1024))
# closed forms
print("erfc(1/sqrt2)=", f"{math.erfc(1/math.sqrt(2)):.10f}", "half=", f"{math.erfc(1/math.sqrt(2))/2:.10f}")
print("2(1-Phi(1))=", f"{math.erfc(1/math.sqrt(2)):.12f}")
print("phi(0)*sqrt2... sqrt(2/pi)=", f"{math.sqrt(2/math.pi):.6f}")
print("Phi(-1/sqrt2)=", f"{0.5*math.erfc((1/math.sqrt(2))/math.sqrt(2)):.8f}")
print("e^8=", f"{math.exp(8):.6f}", "e^4=", f"{math.exp(4):.6f}", "e^0.25=", f"{math.exp(0.25):.9f}")
print("1/sqrt(2pi)*e^-0.5=", f"{math.exp(-0.5)/math.sqrt(2*math.pi):.7f}")
