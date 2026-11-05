"""SC1-c round 7: independent recomputation of the numbers printed on L07 and L08 (own code, stdlib only).

Algorithms differ from the lab twins where practical:
- exact tails use a no-hit counting DP (not the reflection identity);
- truncated means use a no-hit DP for P(nu_1 > k) (not the identity);
- the Brownian and erfc values use math.erf / math.erfc and a Simpson rule;
- the seeded simulations are re-drawn with the same RNG call order, and the grid maxima are read by index.
Run as: python3 -I -W error ledgers/SC1/scripts/SC1-c-r7/indep_r7.py   (from the checkout root or any directory).
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from itertools import accumulate

print("== L07 Part A: exact tails P(M_N >= m), m = sqrt(N), by no-hit DP (positions below m)")
for n in (4, 16, 64, 256, 1024):
    m = math.isqrt(n)
    assert m * m == n
    # counts of length-k walks that have stayed strictly below m (never reached m), positions < m
    cnt = {0: 1}
    for _ in range(n):
        nxt: dict[int, int] = {}
        for x, c in cnt.items():
            for y in (x + 1, x - 1):
                if y < m:
                    nxt[y] = nxt.get(y, 0) + c
        cnt = nxt
    no_hit = sum(cnt.values())
    tail = Fraction(2**n - no_hit, 2**n)
    print(f"N={n:5d} m={m:3d} P(M_N>=m)={float(tail):.9f} -> {float(tail):.6f}")

print("== L07 Part A: identity check for N <= 12, all a in 1..N, enumeration (own loops)")
ok = 0
tot = 0
for n in range(1, 13):
    for a in range(1, n + 1):
        hit_count = 0
        end_ge = 0
        end_gt = 0
        for steps in range(2**n):
            s = 0
            top = 0
            for i in range(n):
                s += 1 if (steps >> i) & 1 else -1
                top = max(top, s)
            hit_count += top >= a
            end_ge += s >= a
            end_gt += s > a
        tot += 1
        ok += hit_count == end_ge + end_gt
print(f"identity holds for {ok} of {tot} (n,a) pairs")

print("== L07 closed forms")
phi1 = 0.5 * math.erfc(-1.0 / math.sqrt(2.0))
print(f"1-Phi(1) = {1 - phi1:.12f}; 2(1-Phi(1)) = {2 * (1 - phi1):.11f}; erfc(1/sqrt2) = {math.erfc(1 / math.sqrt(2)):.11f}")
print(f"sqrt(2/pi) = {math.sqrt(2 / math.pi):.10f}")


def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


dens = lambda x: math.exp(-x * x / 2) / math.sqrt(2 * math.pi)
print(f"Simpson 1-Phi(1) = {simpson(dens, 1.0, 40.0, 4000):.12f}")
print(f"int_0^40 (1-Phi(u)) du = {simpson(lambda u: 0.5 * math.erfc(u / math.sqrt(2)), 0.0, 40.0, 4000):.10f}  (1/sqrt(2pi) = {1 / math.sqrt(2 * math.pi):.10f})")
print(f"E[M_1] = 2 * int_0^40 (1-Phi) = {2 * simpson(lambda u: 0.5 * math.erfc(u / math.sqrt(2)), 0.0, 40.0, 4000):.10f}")

print("== L07 Part B/C: re-simulated with the same RNG call order, grid maxima read by index")
rng = random.Random(20260507)
PATHS, FINE = 400, 256
grids = (4, 16, 64, 256)
maxima = {n: [] for n in grids}
for _ in range(PATHS):
    incs = [rng.gauss(0.0, math.sqrt(1 / FINE)) for _ in range(FINE)]
    path = [0.0] + list(accumulate(incs))
    for n in grids:
        idx = range(0, FINE + 1, FINE // n)
        maxima[n].append(max(path[i] for i in idx))
nest_viol = 0
for c, f in zip(grids, grids[1:]):
    nest_viol += sum(1 for x, y in zip(maxima[c], maxima[f]) if x > y)
print(f"nesting violations = {nest_viol}")
closed = 2 * phi1 * 0 + 2 * (1 - phi1)
for n in grids:
    cnt = sum(1 for v in maxima[n] if v >= 1.0)
    p = cnt / PATHS
    sd_ind = math.sqrt(cnt * (PATHS - cnt) / (PATHS * (PATHS - 1))) if True else 0
    se = math.sqrt(p * (1 - p) / (PATHS - 1))
    print(f"N={n:3d}: count={cnt} p={p:.4f} se={se:.4f} diff_from_closed={p - closed:+.4f}")
for n in grids:
    v = maxima[n]
    mu = sum(v) / PATHS
    sd = math.sqrt(sum((x - mu) ** 2 for x in v) / (PATHS - 1))
    print(f"N={n:3d}: mean={mu:.4f} se={sd / math.sqrt(PATHS):.4f} diff={mu - math.sqrt(2 / math.pi):+.4f} gap_in_se={(math.sqrt(2 / math.pi) - mu) / (sd / math.sqrt(PATHS)):.3f}")
print(f"E3 SE k=121,n=400: {math.sqrt(121 * 279 / (400**2 * 399)):.6f}")
print(f"E2 count: {sum(math.comb(16, u) for u in range(10, 17))} + {sum(math.comb(16, u) for u in range(11, 17))} = {sum(math.comb(16, u) for u in range(10, 17)) + sum(math.comb(16, u) for u in range(11, 17))}; /65536 = {(sum(math.comb(16, u) for u in range(10, 17)) + sum(math.comb(16, u) for u in range(11, 17))) / 65536:.9f}")
print(f"M1 erfc(2/sqrt8) = {math.erfc(2 / math.sqrt(8)):.10f}")
print(f"M3 1-Phi(1) = {1 - phi1:.10f}; 2(1-Phi(1)) = {2 * (1 - phi1):.10f}")

print("== L08 Part A: first-passage counts by own DP (nu_3 = k), n = 12")
# count sequences by first hitting step of level 3 within 12 steps
cnt = {0: 1}  # positions < 3 still alive, counts of sequences
by_step = {}
for k in range(1, 13):
    nxt: dict[int, int] = {}
    hit = 0
    for x, c in cnt.items():
        for y in (x + 1, x - 1):
            if y >= 3:
                hit += c
            else:
                nxt[y] = nxt.get(y, 0) + c
    by_step[k] = hit * 2 ** (12 - k)  # the remaining 12 - k steps are free
    cnt = nxt
print("first passage counts to 3 at steps 3..12:", [by_step[k] for k in range(3, 13)])
print("total:", sum(by_step.values()), "of", 2**12, "=", sum(by_step.values()) / 4096)
# S_12 >= 3 count
endcount = 0
for steps in range(4096):
    s = sum(1 if (steps >> i) & 1 else -1 for i in range(12))
    endcount += s >= 3
print("#{S_12>=3} =", endcount, "ratio to first passage total:", sum(by_step.values()) / endcount)
print(f"P(S_12>=3) = {endcount / 4096:.6f}")

print("== L08 Part A: pair count and sequence count")
print("sum 2^n n=1..12 =", sum(2**n for n in range(1, 13)), "; sum n 2^n =", sum(n * 2**n for n in range(1, 13)), "; pairs (n,a)=", sum(range(1, 13)))

print("== L08 Part B: truncated means by no-hit DP, exact fractions")
largest = 256
alive = {0: 1}
running = Fraction(0)
exact = {}
for k in range(largest):
    # P(nu_1 > k) = (sum of counts of walks with S_j < 1 for j<=k) / 2^k
    total_alive = sum(alive.values())
    running += Fraction(total_alive, 2**k)
    if k + 1 in (16, 64, 256):
        exact[k + 1] = running
    nxt: dict[int, int] = {}
    for x, c in alive.items():
        for y in (x + 1, x - 1):
            if y < 1:
                nxt[y] = nxt.get(y, 0) + c
    alive = nxt
for n in (16, 64, 256):
    print(f"N={n}: E[min(nu_1,N)] = {float(exact[n]):.9f}; exact fraction (N=16) = {exact[16]}" if n == 16 else f"N={n}: {float(exact[n]):.9f}")


print("== L08 Part A: pathwise agreement {nu_a <= n} = {max_{k<=n} S_k >= a} over all (sequence, level) pairs, own loops")
agree = 0
pairs_total = 0
seqs_total = 0
for n in range(1, 13):
    for a in range(1, n + 1):
        for steps in range(2**n):
            s_ = 0
            top = 0
            first = None
            for i in range(n):
                s_ += 1 if (steps >> i) & 1 else -1
                top = max(top, s_)
                if first is None and s_ >= a:
                    first = i + 1
            pairs_total += 1
            agree += (first is not None and first <= n) == (top >= a)
        seqs_total += 2**n
print(f"pathwise agreement {agree} of {pairs_total} (sequence, level) pairs; sequences summed over levels = {seqs_total}")

print("== L08 Part C: re-simulated walks (same RNG call order)")
rng = random.Random(20260508)
capped = []
for _ in range(1000):
    pos = 0
    first = 256
    for k in range(1, 257):
        pos += 1 if rng.random() < 0.5 else -1
        if pos >= 1:
            first = k
            break
    capped.append(first)
for n in (16, 64, 256):
    vals = [min(c, n) for c in capped]
    mu = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - mu) ** 2 for v in vals) / (len(vals) - 1))
    se = sd / math.sqrt(len(vals))
    ex = float(exact[n])
    print(f"N={n}: mean={mu:.4f} se={se:.4f} exact={ex:.4f} z={(mu - ex) / se:+.4f}")

print("== L08 Part D and M/R numbers")
def cdf(a, h):
    return math.erfc(a / math.sqrt(2 * h))
def dens_bm(a, h):
    return a / (math.sqrt(2 * math.pi) * h ** 1.5) * math.exp(-a * a / (2 * h))
for h in (1.0, 2.0):
    d = 1e-5
    cd = (cdf(1.0, h + d) - cdf(1.0, h - d)) / (2 * d)
    print(f"H={h}: cdf={cdf(1.0, h):.9f} density={dens_bm(1.0, h):.9f} central diff={cd:.9f} abs diff={abs(cd - dens_bm(1.0, h)):.2e}")
print(f"f_1(1)={dens_bm(1.0, 1.0):.10f}")
print(f"erfc(1/2)={math.erfc(0.5):.10f}")
# R3 mode
import statistics  # noqa: E402
best = max((dens_bm(1.0, h / 10000), h / 10000) for h in range(1, 40000))
print(f"grid argmax of f_1 over H in (0,4): H={best[1]:.4f} (a^2/3 = {1 / 3:.4f})")
print(f"R1: 2*#{{S_12>=3}} = {2 * endcount}; 1588 = {1588}")
print(f"5.480560 to 5 dp: {float(exact[16]):.5f}; 179587/32768 = {179587 / 32768:.10f}; exact == {exact[16] == Fraction(179587, 32768)}")
print(f"walk-level M3 count: #{{S_3>=1}}={sum(1 for st in range(8) if sum(1 if (st>>i)&1 else -1 for i in range(3))>=1)}")
