"""Independent re-derivation of the numbers printed in prose on the CS2 slice-a pages (L01-L04).

Usage: python3 -I ledgers/CS2/scripts/CS2-a-r4/rederive_cs2a_r4.py
Each line prints a claim and the value recomputed here. Nothing is read from the pages.
"""

import itertools
import math
import random
from fractions import Fraction

# ---- L01 ----
print("L01 1023/511 =", Fraction(1023, 511), float(Fraction(1023, 511)), "2+1/511 equal:", Fraction(1023, 511) == 2 + Fraction(1, 511))
print("L01 1/511 =", 1 / 511, "2 + 1/511 =", 2 + 1 / 511)
print("L01 1024^2 =", 1024**2, "2^20 =", 2**20)
print("L01 first n with n*n > 1000*n:", next(n for n in range(1, 10**6) if n * n > 1000 * n))
print("L01 1000n > n^2 exactly for n in 1..999:", all(1000 * n > n * n for n in range(1, 1000)), "equality at 1000:", 1000 * 1000 == 1000**2, "fails 1001+:", all(1000 * n <= n * n for n in range(1001, 1100)))
print("L01 witness 10 for 3n+7 at n>=1:", all(3 * n + 7 <= 10 * n for n in range(1, 10000)), "c=1 fails:", all(3 * n + 7 > n for n in range(1, 10000)))
print("L01 sum_{i<10} i =", sum(range(10)), "equals 10*9/2:", sum(range(10)) == 10 * 9 // 2)

# ---- L02 ----
M = 2654435761


def bucket(key, m=64):
    return ((key * M) % 2**32) % m


print("L02 bucket(64 j) == 0 for j in 0..10000:", all(bucket(64 * j) == 0 for j in range(10001)))
print("L02 64*51 =", 64 * 51)
rng = random.Random(2026)
keys = rng.sample(range(10**9), 256)
stored_all = set(keys)
absent = [x for x in rng.sample(range(10**9), 2000) if x not in stored_all][:500]
for n in (16, 32, 64, 128, 256):
    chains = [[] for _ in range(64)]
    for k in keys[:n]:
        c = chains[bucket(k)]
        if k not in c:
            c.append(k)
    succ_total = 0
    for k in keys[:n]:
        c = chains[bucket(k)]
        succ_total += c.index(k) + 1
    unsucc_total = 0
    for k in absent:
        unsucc_total += len(chains[bucket(k)])
    model_s = 1 + (n - 1) / 128
    print(
        f"L02 n={n} succ_total={succ_total} succ_avg={succ_total / n:.6f} model={model_s:.7f} "
        f"exact_fraction={Fraction(succ_total, n)} unsucc_total={unsucc_total} unsucc_avg={unsucc_total / 500:.4f}"
    )
print("L02 E1 successful gaps:", [float(Fraction(t, n)) - (1 + (n - 1) / 128) for t, n in [(16, 16), (37, 32), (97, 64), (257, 128), (772, 256)]])
print("L02 257/128 =", 257 / 128, "193/64 =", 193 / 64, "772/256 =", 772 / 256, "increase 193/64-257/128 =", 193 / 64 - 257 / 128)
print("L02 colliding total 50*51/2 =", 50 * 51 // 2, "avg", 1275 / 50)
print("L02 Example 2.5: 64*(1/64)^50 =", Fraction(64) * Fraction(1, 64) ** 50 == Fraction(1, 64) ** 49, "equals 64^-49")
print("L02 R3 difference identity (n-2m+1)/(2m) check:", all(Fraction(n, m) - 1 - Fraction(n - 1, 2 * m) == Fraction(n - 2 * m + 1, 2 * m) for n in range(1, 60) for m in range(1, 20)))
print("L02 M2: 1+9/64 =", 1 + Fraction(9, 64), float(1 + Fraction(9, 64)))
print("L02 M1: 100/40 =", 100 / 40)

# ---- L03 ----
print("L03 6*4096*12 =", 6 * 4096 * 12, "margin 294912-166912 =", 294912 - 166912)
print("L03 2*4096*4097 =", 2 * 4096 * 4097, "4378444/bound =", 4378444 / (2 * 4096 * 4097))
print("L03 N=16 totals:", 107 + 98, 241 + 361)
print("L03 N=128 totals:", 1617 + 4514, 3802 + 4933, "N=256 totals:", 3742 + 17663, 8517 + 10623)
print("L03 92609/8192 =", 92609 / 8192)
moves_list = {64: 1002, 128: 4514, 256: 17663, 512: 65561, 1024: 269578, 2048: 1086043, 4096: 4378444}
moves_heap = {64: 2209, 128: 4933, 256: 10623, 512: 21095, 1024: 42401, 2048: 87863, 4096: 181761}
cmp_heap = {64: 1625, 128: 3802, 256: 8517, 512: 17831, 1024: 37178, 2048: 78710, 4096: 166912}
ks = sorted(moves_list)
print("L03 list move ratios:", [round(moves_list[b] / moves_list[a], 4) for a, b in zip(ks, ks[1:])])
print("L03 heap move ratios:", [round(moves_heap[b] / moves_heap[a], 4) for a, b in zip(ks, ks[1:])])
print("L03 heap cmp ratios:", [round(cmp_heap[b] / cmp_heap[a], 4) for a, b in zip(ks, ks[1:])])
print("L03 list total 128 vs heap:", 1617 + 4514 < 3802 + 4933, "256:", 8517 + 10623 < 3742 + 17663)
print("L03 R1 moves 128 list<heap:", 4514 < 4933, "256 heap<list:", 10623 < 17663)

# ---- L04 ----
lg = math.log2(math.factorial(1024))
print("L04 log2(1024!) =", lg, "ceil =", math.ceil(lg))
print("L04 log2(1000!) =", round(math.log2(math.factorial(1000)), 4), "(1000/2)log2(500) =", round(500 * math.log2(500), 4))
margins = [(math.log2(math.factorial(n)) - (n / 2) * math.log2(n / 2), n) for n in range(2, 1001)]
print("L04 smallest margin (exact-ish) =", min(margins))
print("L04 5120 = 10*512:", 10 * 512, "5120/8770 =", 5120 / 8770)
print("L04 262431/8886 =", 262431 / 8886, "8886*29 =", 8886 * 29, "remainder", 262431 - 8886 * 29)
print("L04 insertion n=7 max =", 7 * 6 // 2, "lower ceil(log2 7!) =", math.ceil(math.log2(math.factorial(7))), "merge upper 7*ceil(log2 7) =", 7 * 3)
print("L04 gaps sum:", sum(n + 1 for n in range(1, 1001)))
print("L04 log2(3!) =", math.log2(6), "ceil", math.ceil(math.log2(6)))


def insertion(xs):
    a = list(xs)
    c = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            c += 1
            if a[j] <= key:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return c


def merge_sort_count(xs):
    if len(xs) <= 1:
        return 0, list(xs)
    m = len(xs) // 2
    cl, l = merge_sort_count(xs[:m])
    cr, r = merge_sort_count(xs[m:])
    out, i, j, c = [], 0, 0, 0
    while i < len(l) and j < len(r):
        c += 1
        if l[i] <= r[j]:
            out.append(l[i])
            i += 1
        else:
            out.append(r[j])
            j += 1
    out += l[i:] + r[j:]
    return cl + cr + c, out


for n in range(2, 8):
    mi = max(insertion(p) for p in itertools.permutations(range(n)))
    mm = max(merge_sort_count(list(p))[0] for p in itertools.permutations(range(n)))
    print(f"L04 Part B recheck n={n}: max_insertion={mi} max_merge={mm}")
print("L04 sorted merge count k=10:", merge_sort_count(list(range(1024)))[0], "insertion sorted:", insertion(list(range(1024))))
print("L04 sorted merge formula k*2^(k-1) for k=1..10 ok:", all(merge_sort_count(list(range(2**k)))[0] == k * 2 ** (k - 1) for k in range(1, 11)))
