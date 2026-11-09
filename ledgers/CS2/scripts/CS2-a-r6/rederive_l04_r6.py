# Independent re-derivation of every L04 number (round 6). Own code, not the lab's helpers.
import math, random, itertools, sys
from fractions import Fraction

def ins_count(seq):
    # explicit insertion sort via list.insert on position found by scanning from the right
    a = []
    c = 0
    for x in seq:
        pos = len(a)
        while pos > 0:
            c += 1
            if a[pos - 1] <= x:
                break
            pos -= 1
        a.insert(pos, x)
    assert a == sorted(seq)
    return c

def mrg(L, R):
    i = j = c = 0
    out = []
    while i < len(L) and j < len(R):
        c += 1
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    out += L[i:] + R[j:]
    assert out == sorted(L + R)
    return out, c

def msort(seq):
    if len(seq) < 2:
        return list(seq), 0
    h = len(seq) // 2
    A, ca = msort(seq[:h]); B, cb = msort(seq[h:])
    M, cm = mrg(A, B)
    return M, ca + cb + cm

def ceil_log2_int(n):
    # least c with 2**c >= n, exact
    c = 0
    while (1 << c) < n:
        c += 1
    return c

def ceil_log2_fact(n):
    f = math.factorial(n)
    c = 0
    while (1 << c) < f:
        c += 1
    return c

out = []
# Part A replica of RNG consumption: one Random(SEED) for part A, shuffles in order 8,64,256,1024
rng = random.Random(20261028)
for n in (8, 64, 256, 1024):
    xs = list(range(n)); rng.shuffle(xs)
    out.append(f"A n={n} ins={ins_count(xs)} merge={msort(xs)[1]} bound={n*ceil_log2_int(n)}")
asc = list(range(1024))
out.append(f"A sorted1024 ins={ins_count(asc)} merge={msort(asc)[1]} (expect 1023, 5120; k*2^(k-1)={10*2**9})")
out.append(f"A lower_bound_ceil_log2_1024! = {ceil_log2_fact(1024)}  (float check {math.log2(math.factorial(1024)):.6f})")
out.append(f"A ratio 262431/8886 = {262431/8886:.6f}  exact 8886*29={8886*29} rem={262431-8886*29}")
# Remark 1.4 closed forms for sorted/decreasing
for n in range(2, 60):
    assert ins_count(list(range(n))) == n - 1
    assert ins_count(list(range(n, 0, -1))) == n*(n-1)//2
for k in range(0, 11):
    n = 2**k
    if n >= 1:
        assert msort(list(range(n)))[1] == (k * 2**(k-1) if k >= 1 else 0), k
out.append("Remark 1.4 a,b,c closed forms verified for n<60 and n=2^k, k<=10")
# Part B: all permutations n=2..7
for n in range(2, 8):
    mi = mm = 0; cnt = 0
    for p in itertools.permutations(range(n)):
        cnt += 1
        mi = max(mi, ins_count(list(p)))
        mm = max(mm, msort(list(p))[1])
    lo = ceil_log2_fact(math.factorial(n)) if False else ceil_log2_int(math.factorial(n))
    up = n * ceil_log2_int(n)
    out.append(f"B n={n} perms={cnt} max_ins={mi} (n(n-1)/2={n*(n-1)//2}) max_merge={mm} lower={lo} upper={up} ok={lo<=mm<=up and mi==n*(n-1)//2}")
# Part C exact: log2(n!) >= (n/2) log2(n/2) for 2..1000, exact via integers: (n!)^2 >= (n/2)^n  <=> (2 n!)^2 >= n^n ... use exact integers
bad = []
minmargin = None; minn = None
for n in range(2, 1001):
    # compare n! vs (n/2)^(n/2) using exact power: (n!)^2 * 4^n ... use logs with high precision via Fraction-free check:
    # log2(n!) - (n/2)log2(n/2) >= 0 <=> n!^2 >= (n/2)^n <=> (2*n!)^2 >= n^n / 2^0 ... (n/2)^n = n^n/2^n ; so (2^n)(n!)^2 >= n^n
    lhs = (1 << n) * math.factorial(n) ** 2
    rhs = n ** n
    if lhs < rhs:
        bad.append(n)
    m = math.log2(math.factorial(n)) - (n/2)*math.log2(n/2)
    if minmargin is None or m < minmargin:
        minmargin, minn = m, n
out.append(f"C exact-integer inequality failures in 2..1000: {bad}; smallest float margin at n={minn} value={minmargin:.6f}")
for n in (2, 3, 4, 10, 100, 1000):
    out.append(f"C n={n} log2fact={math.log2(math.factorial(n)):.4f} half={(n/2)*math.log2(n/2):.4f}")
# Part D: all gaps, lists 2i, n=1..1000
def bsearch_probes(vals, key):
    lo, hi, p = 0, len(vals) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        p += 1
        if vals[mid] == key:
            return p, True
        if vals[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1
    return p, False
gaps_total = 0; mismatch = []
for n in range(1, 1001):
    vals = [2 * i for i in range(n)]
    keys = [-1] + [2 * i + 1 for i in range(n - 1)] + [2 * n - 1]
    worst = 0
    for key in keys:
        p, found = bsearch_probes(vals, key)
        assert not found
        worst = max(worst, p)
        gaps_total += 1
    if worst != n.bit_length():
        mismatch.append(n)
out.append(f"D gaps_total={gaps_total} (sum n+1 = {sum(n+1 for n in range(1,1001))}) mismatches={mismatch}")
# Part D also: every absent key in every gap (all integers between), n up to 60 for stronger check
for n in range(1, 61):
    vals = [2 * i for i in range(n)]
    worst = 0
    for key in range(-1, 2 * n):
        if key % 2 == 0 and 0 <= key <= 2 * (n - 1):
            continue  # present
        p, _ = bsearch_probes(vals, key)
        worst = max(worst, p)
    assert worst == n.bit_length(), n
out.append("D all absent integers in [-1, 2n-1] for n<=60: worst == n.bit_length()")
# Part E replica: Random(SEED+1), 2000 pairs
rng = random.Random(20261029)
slacks = []
for _ in range(2000):
    a = rng.randint(1, 8); b = rng.randint(1, 8)
    L = sorted(rng.randrange(20) for _ in range(a))
    R = sorted(rng.randrange(20) for _ in range(b))
    _, c = mrg(L, R)
    slacks.append(a + b - 1 - c)
out.append(f"E pairs={len(slacks)} above={sum(s<0 for s in slacks)} min_slack={min(slacks)} equal={sum(s==0 for s in slacks)}")
# Exhaustive Lemma 1.2 check for all small lists with ties (values 0..2, a,b<=4)
worst_excess = 0
for a in range(1, 5):
    for b in range(1, 5):
        for L in itertools.combinations_with_replacement(range(3), a):
            for R in itertools.combinations_with_replacement(range(3), b):
                _, c = mrg(list(L), list(R))
                worst_excess = max(worst_excess, c - (a + b - 1))
out.append(f"E-exhaustive Lemma 1.2 max(c-(a+b-1)) over a,b<=4 values 0..2 = {worst_excess} (must be <= 0)")
# Prop 1.3 check for n<=64 over all lists is too big; check max merge sort count over permutations n<=7 vs n*ceil(log2 n) done in B
# P3 / Prop 3.2 equality: top gap probes = beta(n)
for n in range(0, 300):
    assert bsearch_probes([2*i for i in range(n)], 10**6)[0] == n.bit_length()
out.append("P3 top-gap probes == n.bit_length() for n<300 (independent)")
# R3 identity ceil(log2(n+1)) == beta(n) for n>=1
for n in range(1, 100000):
    assert ceil_log2_int(n + 1) == n.bit_length()
out.append("R3 identity ceil(log2(n+1)) == n.bit_length() for 1<=n<100000")
# R3 Lemma: binary search reports lo = number of keys smaller than y, for all absent y, n<=40
for n in range(1, 41):
    vals = [2 * i for i in range(n)]
    for y in range(-1, 2 * n):
        if y % 2 == 0 and 0 <= y <= 2 * (n - 1):
            continue
        lo, hi = 0, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if vals[mid] < y: lo = mid + 1
            else: hi = mid - 1
        assert lo == sum(1 for v in vals if v < y), (n, y)
out.append("R3 returned lo == #keys below y, every absent integer y in range, n<=40")
# Insertion-sort comparisons count is exactly the Definition 1.1 count (sanity)
print("\n".join(out))
