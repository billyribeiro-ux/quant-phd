"""Independent re-derivation of the numbers cited by SC1 cards (no lab code imported).

Usage: python -I indep_numbers_r8.py
"""
import math
import random
from fractions import Fraction
from itertools import product
from collections import Counter

print("== L01 exact checks")
t_vals = [Fraction(1), Fraction(3, 4), Fraction(5, 2)]
ok = sum(1 for t in t_vals for n in range(5) if sum((t / 2**n for _ in range(2**n)), Fraction(0)) == t)
print(f"dyadic sums equal t: {ok} of {len(t_vals) * 5}")
grid = [Fraction(i, 8) for i in range(9)]
print("cov = min on grid pairs:", sum(1 for i in range(9) for j in range(9) if min(i, j) / 8 == min(grid[i], grid[j])), "of 81")

print("== L02 counts")
print("216 check:", 2 * 9 + 3 * 8 + 5 * 7 + 9 * 6 + 17 * 5, "; pairs:", 2 + 3 + 5 + 9 + 17)
for m in range(1, 9):
    lam = math.sqrt(4 * m * math.log(2))
    print(f"  m={m}: bound lambda_m 2^-(m+1)/2 = {lam * 2 ** (-(m + 1) / 2):.6f}")
print("  sqrt(4 log2) / 2 =", f"{math.sqrt(4 * math.log(2)) / 2:.6f}", "; 2*0.116589 =", 2 * 0.116589)

print("== L03 gaps of printed SEs against H sqrt(2/N)/20 (printed values from lab stdout)")
printed = {
    (1, 1): 0.0718, (1, 2): 0.0538, (1, 4): 0.0373, (1, 8): 0.0249, (1, 16): 0.0174, (1, 32): 0.0131, (1, 64): 0.0092,
    (1, 128): 0.0063, (2, 1): 0.1601, (2, 2): 0.0934, (2, 4): 0.0772, (2, 8): 0.0475, (2, 16): 0.0364,
    (2, 32): 0.0256, (2, 64): 0.0190, (2, 128): 0.0125,
}
gaps = {}
for (h, n), se in printed.items():
    pop = h * math.sqrt(2 / n) / 20
    gaps[(h, n)] = se / pop - 1
for k, g in sorted(gaps.items(), key=lambda kv: kv[1]):
    pass
print(f"  largest gap {max(gaps.values()) * 100:+.2f}% at {max(gaps, key=gaps.get)}; smallest {min(gaps.values()) * 100:+.2f}% at {min(gaps, key=gaps.get)}")
print(f"  16 printed SEs: {len(printed)} (lab prints 8 per horizon; SE at N=1 is printed for H=1 and H=2 only for N in 1..128 = 8 each)")
print("  note: the lab prints 8 levels per horizon, so 16 SEs total")

print("== L03 exact sums")
for h, n in [(1, 2), (2, 8), (2, 128), (1, 128), (2, 1)]:
    print(f"  H={h}, N={n}: {Fraction(h) ** 4 * (4 * n * n - 1) / (3 * n**3)} = {float(Fraction(h) ** 4 * (4 * n * n - 1) / (3 * n**3)):.6f}")
print("== L04 closed forms")
print(f"  e^1={math.exp(1):.9f} e^(1/4)={math.exp(0.25):.9f} e^4={math.exp(4):.9f} e^8={math.exp(8):.6f}")
print("== L06 enumeration (own code)")
def summaries(n):
    out = []
    for steps in product((1, -1), repeat=n):
        pos, top = 0, 0
        for s in steps:
            pos += s
            top = max(top, pos)
        out.append((top, pos))
    return out
tri = eq = 0
pairs_ok = pairs = 0
for n in range(1, 13):
    sm = summaries(n)
    ends = Counter(e for _, e in sm)
    for a in range(1, n + 1):
        hit = Counter(e for tp, e in sm if tp >= a)
        for b in range(-n, a):
            tri += 1
            eq += hit[b] == ends[2 * a - b]
        pairs += 1
        pairs_ok += sum(1 for tp, _ in sm if tp >= a) == sum(1 for _, e in sm if e >= a) + sum(1 for _, e in sm if e > a)
print(f"  triples {tri} equal {eq}; pairs {pairs} equal {pairs_ok}")
sm12 = summaries(12)
print("  N=12 a=3: M>=3 count", sum(1 for tp, _ in sm12 if tp >= 3), "of 4096; M>=3 & S=2:", sum(1 for tp, e in sm12 if tp >= 3 and e == 2),
      "; S=4:", sum(1 for _, e in sm12 if e == 4))
sm10 = summaries(10)
print("  N=10 a=2: P(M>=2)=", Fraction(sum(1 for tp, _ in sm10 if tp >= 2), 1024), "; 2P(S>2)=", Fraction(2 * sum(1 for _, e in sm10 if e > 2), 1024),
      "; P(S=2)=", Fraction(sum(1 for _, e in sm10 if e == 2), 1024))
print(f"  erfc(1/sqrt2)={math.erfc(1 / math.sqrt(2)):.10f}; half={math.erfc(1 / math.sqrt(2)) / 2:.10f}")
print("  N=3 a=1 count M>=1:", sum(1 for tp, _ in summaries(3) if tp >= 1), "of 8")
print("== L06 N=16 a=4 tail count (binomial)")
def end_at_least(n, m):
    return sum(math.comb(n, (n + s) // 2) for s in range(-n, n + 1, 2) if s >= m)
cnt = end_at_least(16, 4) + end_at_least(16, 5)
print(f"  endpoint>=4: {end_at_least(16, 4)}; endpoint>4: {end_at_least(16, 5)}; total {cnt} = {cnt / 65536:.6f}")
print("== L07 exact tails")
for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    c = end_at_least(n, m) + end_at_least(n, m + 1)
    print(f"  N={n} m={m}: {c / 2**n:.6f}")
print(f"  2(1-Phi(1))={math.erfc(1 / math.sqrt(2)):.10f}")
print("== L07 Part B (own re-implementation of the seeded algorithm)")
FINE, PATHS = 256, 400
rng = random.Random(20260507)
maxima = {n: [] for n in (4, 16, 64, 256)}
for _ in range(PATHS):
    inc = [rng.gauss(0.0, math.sqrt(1.0 / FINE)) for _ in range(FINE)]
    path = [0.0]
    for x in inc:
        path.append(path[-1] + x)
    for n in maxima:
        maxima[n].append(max(path[:: FINE // n]))
for n in maxima:
    k = sum(1 for m in maxima[n] if m >= 1.0)
    vals = maxima[n]
    mean = sum(vals) / PATHS
    sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (PATHS - 1))
    print(f"  N={n}: count>=1 {k} (p={k / PATHS:.4f}); mean {mean:.4f} se {sd / math.sqrt(PATHS):.4f}")
viol = sum(1 for c, f in [(4, 16), (16, 64), (64, 256)] for x, y in zip(maxima[c], maxima[f]) if x > y)
print("  nesting violations:", viol)
print("== L08 walk first passage (own code)")
seqs = sum(2**n for n in range(1, 13))
pairs_total = sum(n * 2**n for n in range(1, 13))
print(f"  sequences {seqs}; (sequence, level) pairs {pairs_total}")
first = Counter()
for steps in product((1, -1), repeat=12):
    pos = 0
    hit = None
    for k, s in enumerate(steps, 1):
        pos += s
        if hit is None and pos >= 3:
            hit = k
    if hit is not None:
        first[hit] += 1
print("  first passage to 3 at steps 3..12:", [first[k] for k in range(3, 13)], "sum", sum(first.values()))
def trunc_mean(N):
    total = Fraction(0)
    for k in range(N):
        n = k
        if n == 0:
            surv = Fraction(1)
        else:
            cnt = end_at_least(n, 1) + end_at_least(n, 2)
            surv = 1 - Fraction(cnt, 2**n)
        total += surv
    return total
for N in (16, 64, 256):
    tm = trunc_mean(N)
    print(f"  E[min(nu_1,{N})] = {float(tm):.6f}")
print(f"  179587/32768 = {179587 / 32768:.6f}")
print(f"  f_1(1)={math.exp(-0.5) / math.sqrt(2 * math.pi):.6f}; f_1(2)={2**-1.5 * math.exp(-0.25) / math.sqrt(2 * math.pi):.6f}")
print(f"  erfc(1/2)={math.erfc(0.5):.6f}; erfc(1/sqrt2)={math.erfc(1 / math.sqrt(2)):.6f}")
print("== L08 Part C re-implementation")
rng = random.Random(20260508)
capped = []
for _ in range(1000):
    pos = 0
    first_k = 256
    for k in range(1, 257):
        pos += 1 if rng.random() < 0.5 else -1
        if pos >= 1:
            first_k = k
            break
    capped.append(first_k)
for N, exact in ((16, 5.480560), (64, 11.815731), (256, 24.557203)):
    vals = [min(c, N) for c in capped]
    mean = sum(vals) / 1000
    sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / 999)
    se = sd / math.sqrt(1000)
    print(f"  N={N}: mean {mean:.4f} se {se:.4f} z {(mean - exact) / se:+.2f}")
