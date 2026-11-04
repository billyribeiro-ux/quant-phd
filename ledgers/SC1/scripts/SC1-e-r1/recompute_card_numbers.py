"""Independent recomputation (dynamic programming and closed forms, no reuse of the lab code)
of the exact numbers quoted on the SC1 cards. Read-only, stdlib only.
"""
import math
from fractions import Fraction

# Distribution of (running max, endpoint) by dynamic programming over steps.
def dist_after(n: int) -> dict[tuple[int, int], int]:
    d = {(0, 0): 1}
    for _ in range(n):
        nd: dict[tuple[int, int], int] = {}
        for (top, pos), c in d.items():
            for step in (1, -1):
                np_ = pos + step
                key = (max(top, np_), np_)
                nd[key] = nd.get(key, 0) + c
        d = nd
    return d

# Card L06 c111: triples (N, a, b), N<=12, 1<=a<=N, b<a, where b ranges over every integer below a
# (b far below -N gives 0 on both sides, so only b >= -N needs enumerating).
triples = 0
ok = 0
for n in range(1, 13):
    d = dist_after(n)
    for a in range(1, n + 1):
        for b in range(-n - 3, a):
            triples += 1
            lhs = sum(c for (top, pos), c in d.items() if top >= a and pos == b)
            rhs = sum(c for (top, pos), c in d.items() if pos == 2 * a - b)
            ok += lhs == rhs
print("c111 triples (b over -N-3..a-1):", triples, "equal:", ok)

# Card L07 c147/L06 c112: pairs and tail identity.
pairs = 0; tail_ok = 0
for n in range(1, 13):
    d = dist_after(n)
    for a in range(1, n + 1):
        pairs += 1
        lhs = sum(c for (top, pos), c in d.items() if top >= a)
        rhs = sum(c for (top, pos), c in d.items() if pos >= a) + sum(c for (top, pos), c in d.items() if pos > a)
        tail_ok += lhs == rhs
print("c112 pairs:", pairs, "tail identity holds:", tail_ok)

d12 = dist_after(12)
print("c114 M12>=3 & S12=2:", sum(c for (t, p), c in d12.items() if t >= 3 and p == 2),
      " S12=4:", sum(c for (t, p), c in d12.items() if p == 4))
d10 = dist_after(10)
N = 2 ** 10
p1 = Fraction(sum(c for (t, p), c in d10.items() if t >= 2), N)
p2 = Fraction(2 * sum(c for (t, p), c in d10.items() if p > 2), N)
p3 = Fraction(sum(c for (t, p), c in d10.items() if p == 2), N)
print("c113:", p1, p2, p3, "difference equals P(S10=2):", p1 - p2 == p3)
d16 = dist_after(16)
print("c148 walks M16>=4:", sum(c for (t, p), c in d16.items() if t >= 4), "tail:", sum(c for (t, p), c in d16.items() if t >= 4) / 2 ** 16)
print("c148 binomial sums:", sum(math.comb(16, u) for u in range(10, 17)), sum(math.comb(16, u) for u in range(11, 17)))

# Card L08 c171: first passage counts to level 3 at steps 3..12 (walk never below 0 needed? no: first hit of +3).
def first_hit_counts(n: int, a: int) -> list[int]:
    counts = [0] * (n + 1)
    # DP over (position, hit-yet) with first-hit step recorded
    state = {0: 1}
    for k in range(1, n + 1):
        nstate: dict[int, int] = {}
        for pos, c in state.items():
            for step in (1, -1):
                np_ = pos + step
                if np_ >= a:
                    counts[k] += c * 2 ** (n - k)  # each prefix hitting at step k has 2**(n-k) completions
                else:
                    nstate[np_] = nstate.get(np_, 0) + c
        state = nstate
    return counts[1:]

fh = first_hit_counts(12, 3)
print("c171 first-passage counts k=1..12:", fh, "sum:", sum(fh), "P:", sum(fh) / 4096, sum(fh) == 1588)
s12ge3 = sum(c for (t, p), c in dist_after(12).items() if p >= 3)
print("c171 #{S12>=3}:", s12ge3, Fraction(s12ge3, 4096), float(Fraction(s12ge3, 4096)))

# Card L08 c172/c173: E[min(T_1,N)] = sum_{k<N} P(T_1>k) with P(T_1>k) = P(max_{j<=k} S_j < 1) exactly.
def survive_counts(k: int) -> int:
    # sequences of length k with running max < 1 (i.e., max <= 0)
    return sum(c for (t, p), c in dist_after(k).items() if t < 1)

def trunc_mean_exact(N: int) -> Fraction:
    total = Fraction(0)
    for k in range(N):
        total += Fraction(survive_counts(k), 2 ** k)
    return total

# survive_counts up to k=255 is a 2^255 enumeration; use the reflection count instead:
# #{max_{j<=k} S_j < 1} = 2^k - #{M_k >= 1} with #{M_k>=1} = #{S_k>=1} + #{S_k>1} (verified above for k<=12).
def max_ge1(k: int) -> int:
    def ge(m: int) -> int:
        return sum(math.comb(k, u) for u in range(k + 1) if 2 * u - k >= m)
    return ge(1) + ge(2)

def trunc_mean_exact_fast(N: int) -> Fraction:
    total = Fraction(0)
    for k in range(N):
        total += Fraction(2 ** k - max_ge1(k), 2 ** k)
    return total

for n in (16, 64, 256):
    print("c172 E[min(T1,%d)] =" % n, float(trunc_mean_exact_fast(n)))
# cross-check the fast form against full enumeration for small N
print("cross-check N=16 fast vs enumeration:", trunc_mean_exact_fast(16) == trunc_mean_exact(16))

# Card L08 c174 / L07 c149 closed forms
print("c174 P(tau1<=1)=erfc(1/sqrt2)=%.6f; P(tau1<=2)=erfc(1/sqrt4)=%.6f" % (math.erfc(1/math.sqrt(2)), math.erfc(0.5)))
f = lambda a, t: a / (math.sqrt(2 * math.pi) * t ** 1.5) * math.exp(-a * a / (2 * t))
print("c174 density at t=1: %.6f, t=2: %.6f" % (f(1, 1), f(1, 2)))
print("c159 SE k=121 n=400: %.6f" % math.sqrt(121 * 279 / (400 ** 2 * 399)))
print("c150 sqrt(2/pi)=%.6f; c151 gap/se=%.2f" % (math.sqrt(2 / math.pi), (math.sqrt(2/math.pi) - 0.7586) / 0.0317))
print("c177 P(B1>=1)=%.10f" % (0.5 * math.erfc(1 / math.sqrt(2))))
print("c115/c126 erfc(1/sqrt2)=%.6f, 2P(B1>=1)" % math.erfc(1 / math.sqrt(2)))
print("c181 #{S12=3}:", sum(c for (t, p), c in d12.items() if p == 3), " 2*794:", 2 * 794)
print("c179 P(T1<=3) by DP:", Fraction(sum(c for (t,p),c in dist_after(3).items() if t >= 1), 8))
print("c169/M3 M1 of L03: sum over k of (2j+1)^2 N=3:", sum((2*j+1)**2 for j in range(3)), 3*(4*9-1)/3)
print("c050 H=1,N=2: %s" % (Fraction(1,1) * (4*4-1) / (3*8)))
print("c059 E[(Q-t)^2]/(t|P|) equal grid: N=5 ->", 2 * 5 * (1/5)**2 / (1 * 1/5))
