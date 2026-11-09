"""Independent re-derivation of every printed number in CS2 lessons L01-L04 (verifier round 2).

Each block re-implements the quantity from its definition, not by importing the lab twin.
Usage: python3 -I rederive.py   (exit 0 and "ALL DERIVATIONS MATCH" when every check holds)
"""

import itertools
import math
import random

fails: list[str] = []


def check(label: str, got: object, want: object) -> None:
    ok = got == want
    print(f"{'OK  ' if ok else 'FAIL'} {label}: got {got!r} want {want!r}")
    if not ok:
        fails.append(label)


# ---------- L01 ----------
def scan(n: int) -> int:
    # comparisons of the maximum scan over n values, counted by a loop (n - 1 by construction)
    count = 0
    best = 0
    for x in range(1, n):
        count += 1
        if x > best:
            best = x
    return count


for k in range(11):
    n = 2**k
    check(f"L01 k={k} scan comparisons = 2^k - 1", scan(n), 2**k - 1)
    check(f"L01 k={k} pair steps = 4^k", n * n, 4**k)
check("L01 ratio 2^10 vs 2^9 comparisons to 4 dp", f"{1023 / 511:.4f}", "2.0020")
check("L01 exact ratio 2 + 1/511", 1023 / 511 - (2 + 1 / 511) < 1e-15, True)
for k in range(2, 11):
    print(f"     L01 comparison ratio k={k}: {(2**k - 1) / (2 ** (k - 1) - 1):.6f} = 2 + 1/{2 ** (k - 1) - 1}")
check("L01 first failure of n*n > 1000*n", min(n for n in range(1, 5000) if n * n > 1000 * n), 1001)
check("L01 n^2 <= 1000 n for n = 1..1000 (count)", sum(1 for n in range(1, 1001) if n * n <= 1000 * n), 1000)
check("L01 1000n > n^2 for n in 1..999 only", [n for n in range(1, 2001) if 1000 * n > n * n] == list(range(1, 1000)), True)

# ---------- L02 ----------
M = 2654435761


def h(x: int, m: int = 64) -> int:
    return ((x * M) % 2**32) % m


check("L02 h(64 j) == 0 for j in 0..5000", all(h(64 * j) == 0 for j in range(5001)), True)
rng = random.Random(2026)
keys = rng.sample(range(10**9), 256)
stored = set(keys)
absent_pool = rng.sample(range(10**9), 2000)
absent = [x for x in absent_pool if x not in stored][:500]
check("L02 absent test keys count", len(absent), 500)
for n in (16, 32, 64, 128, 256):
    chains: list[list[int]] = [[] for _ in range(64)]
    for key in keys[:n]:
        chains[h(key)].append(key)
    succ_total = 0
    for key in keys[:n]:
        chain = chains[h(key)]
        succ_total += chain.index(key) + 1
    unsucc_total = 0
    for x in absent:
        chain = chains[h(x)]
        unsucc_total += len(chain)  # an unsuccessful search compares with every key in the chain
    model = 1 + (n - 1) / 128
    print(f"     L02 n={n}: succ total {succ_total} avg {succ_total / n:.7f}; unsucc total {unsucc_total} avg {unsucc_total / 500:.7f}; model {model:.7f}")
    check(f"L02 n={n} successful average printed 4 dp", f"{succ_total / n:.4f}", {16: "1.0000", 32: "1.1562", 64: "1.5156", 128: "2.0078", 256: "3.0156"}[n])
    check(f"L02 n={n} unsuccessful average printed 4 dp", f"{unsucc_total / 500:.4f}", {16: "0.2680", 32: "0.5400", 64: "1.0960", 128: "2.0320", 256: "4.0280"}[n])
    check(f"L02 n={n} model successful 4 dp", f"{model:.4f}", {16: "1.1172", 32: "1.2422", 64: "1.4922", 128: "1.9922", 256: "2.9922"}[n])
check("L02 exact 257/128", 257 / 128, 2.0078125)
check("L02 exact 193/64", 193 / 64, 3.015625)
check("L02 increase 193/64 - 257/128", 193 / 64 - 257 / 128, 1.0078125)
colliding = [64 * j for j in range(1, 51)]
check("L02 colliding total 50*51/2", sum(range(1, 51)), 1275)
check("L02 colliding buckets", {h(k) for k in colliding}, {0})
check("L02 unsuccessful 3264 probes in colliding set", len([k for k in colliding if h(k) == h(3264)]), 50)
check("L02 P2 bucket probability m*(1/m)*(1/m) = 1/m", 64 * (1 / 64) * (1 / 64) == 1 / 64, True)
check("L02 example 2.5 64*(1/64)^50 = 64^-49", math.isclose(64 * (1 / 64) ** 50, 64.0**-49, rel_tol=1e-12), True)
check("L02 M2 1+9/64", 1 + 9 / 64, 73 / 64)
gaps_e1 = [round(t / n - (1 + (n - 1) / 128), 7) for n, t in [(16, 16), (32, 37), (64, 97), (128, 257), (256, 772)]]
check("L02 E1 successful gaps (measured minus model)", gaps_e1, [-0.1171875, -0.0859375, 0.0234375, 0.015625, 0.0234375])
for n, t, mv in [(16, 16, 1 + 15 / 128), (32, 37, 1 + 31 / 128), (64, 97, 1 + 63 / 128), (128, 257, 1 + 127 / 128), (256, 772, 1 + 255 / 128)]:
    print(f"     L02 E1 gap n={n}: {t / n - mv:+.7f}")
for m_u, tot in [(0.25, 134), (0.5, 270), (1.0, 548), (2.0, 1016), (4.0, 2014)]:
    print(f"     L02 E1 unsuccessful: total {tot} /500 - {m_u} = {tot / 500 - m_u:+.4f}")
check("L02 M1 alpha 100/40", 100 / 40, 2.5)
check("L02 R3 sign: (n-2m+1)/(2m) identity at m=64 n=200",
      math.isclose(200 / 64 - 1 - 199 / 128, (200 - 128 + 1) / 128), True)

# ---------- L03 ----------
def heap_run(n: int) -> tuple[list[tuple[int, int]], int, int]:
    # independent heap with comparison and move counts (push/pop by definition)
    heap: list[tuple[int, int]] = []
    comps = 0
    moves = 0

    def push(key: tuple[int, int]) -> None:
        nonlocal comps, moves
        heap.append(key)
        moves += 1
        i = len(heap) - 1
        while i > 0:
            p = (i - 1) // 2
            comps += 1
            if heap[i] < heap[p]:
                heap[i], heap[p] = heap[p], heap[i]
                moves += 2
                i = p
            else:
                break

    def pop() -> tuple[int, int]:
        nonlocal comps, moves
        top = heap[0]
        last = heap.pop()
        if heap:
            heap[0] = last
            moves += 1
            i = 0
            while True:
                lft, rgt = 2 * i + 1, 2 * i + 2
                small = i
                if lft < len(heap):
                    comps += 1
                    if heap[lft] < heap[small]:
                        small = lft
                if rgt < len(heap):
                    comps += 1
                    if heap[rgt] < heap[small]:
                        small = rgt
                if small == i:
                    break
                heap[i], heap[small] = heap[small], heap[i]
                moves += 2
                i = small
        return top

    rng = random.Random(2026)
    for seq in range(n):
        push((rng.randrange(1_000_000), seq))
    delays = [rng.randint(1, 1000) for _ in range(n)]
    out = []
    for step in range(n):
        t, _ = pop()
        out.append((t, step))
        push((t + delays[step], n + step))
    while heap:
        out.append(pop())
    return out, comps, moves


def sorted_run(n: int) -> tuple[list[tuple[int, int]], int, int]:
    # sorted list in descending order; minimum last; push = binary search + insert; moves = tail shift + 1
    items: list[tuple[int, int]] = []
    comps = 0
    moves = 0

    def push(key: tuple[int, int]) -> None:
        nonlocal comps, moves
        lo, hi = 0, len(items)
        while lo < hi:
            mid = (lo + hi) // 2
            comps += 1
            if items[mid] > key:
                lo = mid + 1
            else:
                hi = mid
        moves += len(items) - lo + 1
        items.insert(lo, key)

    def pop() -> tuple[int, int]:
        return items.pop()

    rng = random.Random(2026)
    for seq in range(n):
        push((rng.randrange(1_000_000), seq))
    delays = [rng.randint(1, 1000) for _ in range(n)]
    out = []
    for step in range(n):
        t, _ = pop()
        out.append((t, step))
        push((t + delays[step], n + step))
    while items:
        out.append(pop())
    return out, comps, moves


for k in (4, 5, 6, 7, 8, 9, 10, 11, 12):
    n = 2**k
    hp, hc, hm = heap_run(n)
    sp, sc, sm = sorted_run(n)
    check(f"L03 N={n} pop orders equal", hp == sp, True)
    check(f"L03 N={n} heap comparisons within 6N floor(log2 N)", hc <= 6 * n * (n.bit_length() - 1), True)
    print(f"     L03 N={n}: heap comps {hc} moves {hm}; sorted comps {sc} moves {sm}")
    if k == 12:
        check("L03 N=4096 heap comparisons", hc, 166912)
        check("L03 N=4096 sorted moves", sm, 4378444)
        check("L03 N=4096 sorted comparisons", sc, 92609)
        check("L03 N=4096 heap moves", hm, 181761)
        check("L03 bound 6*4096*12", 6 * 4096 * 12, 294912)
        check("L03 margin", 294912 - 166912, 128000)
        check("L03 2N(N+1)", 2 * 4096 * 4097, 33562624)
        check("L03 ratio 4378444/33562624 two dp", f"{4378444 / 33562624:.4f}", "0.1305")
    if k == 4:
        check("L03 N=16 sorted total", sc + sm, 205)
        check("L03 N=16 heap total", hc + hm, 602)
check("L03 E3 ratio printed sorted-moves 4378444/1086043", f"{4378444 / 1086043:.4f}", "4.0316")
check("L03 2^12 = 4096 pops 2N = 8192", 2 * 4096, 8192)
check("L03 M1 floor(log2 6) = 2", (6).bit_length() - 1, 2)
check("L03 M2 height of 10 keys", (10).bit_length() - 1, 3)
check("L03 quiz 2*floor(log2 8)", 2 * ((8).bit_length() - 1), 6)

# ---------- L04 ----------
def insertion(xs: list[int]) -> int:
    a = list(xs)
    comps = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] <= key:
                break
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return comps


def merge_sort_count(xs: list[int]) -> tuple[list[int], int]:
    if len(xs) <= 1:
        return list(xs), 0
    mid = len(xs) // 2
    left, cl = merge_sort_count(xs[:mid])
    right, cr = merge_sort_count(xs[mid:])
    out: list[int] = []
    comps = cl + cr
    i = j = 0
    while i < len(left) and j < len(right):
        comps += 1
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out += left[i:] + right[j:]
    return out, comps


def ceil_log2_exact(n: int) -> int:
    c = 0
    while (1 << c) < n:
        c += 1
    return c


check("L04 ceil(log2 1024!) exact", ceil_log2_exact(math.factorial(1024)), 8770)
check("L04 (1024 keys) merge sorted input 10*2^9", 10 * 2**9, 5120)
check("L04 insertion sorted input n-1", 1023, 1023)
check("L04 ratio 262431/8886 to 2dp", f"{262431 / 8886:.2f}", "29.53")
check("L04 E3 ratio 5120/8770 to 2dp", f"{5120 / 8770:.2f}", "0.58")
check("L04 E1 8886*29", 8886 * 29, 257694)
rng2 = random.Random(20261028)
xs_all = []
for n in (8, 64, 256, 1024):
    xs = list(range(n))
    rng2.shuffle(xs)
    xs_all.append((n, xs))
for n, xs in xs_all:
    ins = insertion(xs)
    _, mer = merge_sort_count(xs)
    print(f"     L04 Part A n={n}: insertion {ins} merge {mer} bound {n * ceil_log2_exact(n)}")
    if n == 8:
        check("L04 Part A n=8 insertion 21", ins, 21)
        check("L04 Part A n=8 merge 15", mer, 15)
    if n == 1024:
        check("L04 Part A n=1024 insertion 262431", ins, 262431)
        check("L04 Part A n=1024 merge 8886", mer, 8886)
        check("L04 Part A n=1024 bound 10240", n * ceil_log2_exact(n), 10240)
for n in (64, 256):
    xs = [x for m_, xx in xs_all if m_ == n for x in xx]
    print(f"     L04 Part A n={n} (sample) insertion {insertion(xs)} merge {merge_sort_count(xs)[1]}")
check("L04 sorted 1024 insertion", insertion(list(range(1024))), 1023)
check("L04 sorted 1024 merge", merge_sort_count(list(range(1024)))[1], 5120)

for n in range(2, 8):
    maxi = 0
    maxm = 0
    for perm in itertools.permutations(range(n)):
        xs = list(perm)
        maxi = max(maxi, insertion(xs))
        maxm = max(maxm, merge_sort_count(xs)[1])
    lo = ceil_log2_exact(math.factorial(n))
    up = n * ceil_log2_exact(n)
    print(f"     L04 Part B n={n}: max insertion {maxi} max merge {maxm} lower {lo} upper {up}")
    check(f"L04 Part B n={n} insertion max = n(n-1)/2", maxi, n * (n - 1) // 2)
    check(f"L04 Part B n={n} merge max within [lower, upper]", lo <= maxm <= up, True)
    if n == 7:
        check("L04 Part B n=7 merge max 14", maxm, 14)
        check("L04 Part B n=7 lower 13", lo, 13)

# Part C: exact integer check of (n!)^2 * 2^n >= n^n  <=>  log2(n!) >= (n/2) log2(n/2)  for 2..1000
exact_ok = all((math.factorial(n) ** 2) * (2**n) >= n**n for n in range(2, 1001))
check("L04 Part C exact integer inequality for n = 2..1000", exact_ok, True)
margins = [(math.lgamma(n + 1) / math.log(2) - (n / 2) * math.log2(n / 2), n) for n in range(2, 1001)]
mn, mn_n = min(margins)
check("L04 Part C smallest margin at n", mn_n, 2)
check("L04 Part C margin at 2 is 1", round(mn, 6), 1.0)
check("L04 log2(1000!) to 4 dp", f"{math.lgamma(1001) / math.log(2):.4f}", "8529.3980")
check("L04 (1000/2) log2 500 to 4 dp", f"{500 * math.log2(500):.4f}" if False else f"{(1000 / 2) * math.log2(500):.4f}", "4482.8921")
check("L04 n=3 log2 6 dp", f"{math.log2(6):.4f}", "2.5850")
check("L04 n=100 log2(100!) to 4 dp", f"{math.lgamma(101) / math.log(2):.4f}", "524.7650")
check("L04 n=100 (50) log2 50 to 4 dp", f"{50 * math.log2(50):.4f}", "282.1928")

# Part D: exact unsuccessful binary search worst case over all gaps of 0,2,..,2(n-1)


def probes(vals: list[int], key: int) -> int:
    lo, hi, p = 0, len(vals) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        p += 1
        if vals[mid] == key:
            return p
        if vals[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return p


bad = 0
gaps = 0
for n in range(1, 1001):
    vals = [2 * i for i in range(n)]
    queries = [-1] + [2 * i + 1 for i in range(n - 1)] + [2 * n - 1]
    gaps += len(queries)
    worst = max(probes(vals, q) for q in queries)
    if worst != n.bit_length():
        bad += 1
check("L04 Part D gaps total 501500", gaps, 501500)
check("L04 Part D n with worst != floor(log2 n)+1", bad, 0)
check("L04 Part D n=4 worst 3 (key 7)", probes([0, 2, 4, 6], 7), 3)
check("L04 Part D 13 keys above-all probes", probes(list(range(13)), 99), 4)

print("ALL DERIVATIONS MATCH" if not fails else f"MISMATCHES: {fails}")
