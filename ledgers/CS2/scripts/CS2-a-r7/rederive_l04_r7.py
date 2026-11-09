# Independent re-derivation of the CS2 L04 printed numbers (own formulas, not the lab's code).
import math, random, itertools

def ins_count_formula(xs):
    # step i compares a[i] with earlier elements from the right until one is <= a[i];
    # k = number of earlier elements > a[i]; comparisons at step i = min(k + 1, i).
    total = 0
    for i in range(1, len(xs)):
        k = sum(1 for j in range(i) if xs[j] > xs[i])
        total += min(k + 1, i)
    return total

def merge_cmp_recursive(a, b):
    # comparisons of the merge with ties to the left = number of outputs up to the first moment one list is
    # exhausted = min over the two lists of the 1-based position of that list's last key in the merged order,
    # where the merged order is the stable sort of (value, side) with side 0 for the left list.
    if not a or not b:
        return 0
    tagged = sorted([(v, 0, i) for i, v in enumerate(a)] + [(v, 1, i) for i, v in enumerate(b)])
    pos_last_left = max(p for p, t in enumerate(tagged, 1) if t[1] == 0)
    pos_last_right = max(p for p, t in enumerate(tagged, 1) if t[1] == 1)
    return min(pos_last_left, pos_last_right)

def merge_sort_cmp(xs):
    if len(xs) < 2:
        return 0
    m = len(xs) // 2
    L, R = xs[:m], xs[m:]
    return merge_sort_cmp(L) + merge_sort_cmp(R) + merge_cmp_recursive(sorted(L), sorted(R))

def ceil_log2_int(N):
    c = 0
    while (1 << c) < N:
        c += 1
    return c

# Part A
rng = random.Random(20261028)
print("Part A")
for n in (8, 64, 256, 1024):
    xs = list(range(n))
    rng.shuffle(xs)
    print(n, ins_count_formula(xs), merge_sort_cmp(xs), n * ceil_log2_int(n))
print("sorted 1024 insertion", ins_count_formula(list(range(1024))), "merge", merge_sort_cmp(list(range(1024))))
print("ceil log2 1024! =", ceil_log2_int(math.factorial(1024)), " log2(1024!) =", round(math.lgamma(1025) / math.log(2), 4))
print("ratio 262431/8886 =", round(262431 / 8886, 6))
# Part B
print("Part B")
for n in range(2, 8):
    perms = list(itertools.permutations(range(n)))
    mi = max(ins_count_formula(list(p)) for p in perms)
    mm = max(merge_sort_cmp(list(p)) for p in perms)
    print(n, len(perms), mi, mm, ceil_log2_int(math.factorial(n)), n * ceil_log2_int(n))
# Part C margins (exact via integer log: log2(n!) vs (n/2)log2(n/2), floats with high precision)
from decimal import Decimal, getcontext
getcontext().prec = 50
ln2 = Decimal(2).ln()
worst = None
ok = True
for n in range(2, 1001):
    lf = sum(Decimal(k).ln() for k in range(2, n + 1)) / ln2
    rhs = Decimal(n) / 2 * (Decimal(n) / 2).ln() / ln2
    if lf < rhs:
        ok = False
    mg = lf - rhs
    if worst is None or mg < worst[1]:
        worst = (n, mg)
print("Part C exact holds", ok, "smallest margin at", worst[0], float(worst[1]))
print("log2(1000!)", float(sum(Decimal(k).ln() for k in range(2, 1001)) / ln2))
# Part E: same RNG call order as the lab (seed 20261028 + 1)
r2 = random.Random(20261028 + 1)
eq = 0; above = 0; minslack = None
for _ in range(2000):
    a = r2.randint(1, 8); b = r2.randint(1, 8)
    L = sorted(r2.randrange(20) for _ in range(a))
    R = sorted(r2.randrange(20) for _ in range(b))
    c = merge_cmp_recursive(L, R)
    s = a + b - 1 - c
    eq += s == 0; above += s < 0
    minslack = s if minslack is None else min(minslack, s)
print("Part E pairs equal bound", eq, "above", above, "min slack", minslack)
# Part D: gaps via independent formula (count of keys below y) and probe count
tot = 0; allok = True
for n in range(1, 1001):
    keys = [2 * i for i in range(n)]
    worst = 0
    ys = [-1] + [2 * i + 1 for i in range(n - 1)] + [2 * n - 1]
    assert len(ys) == n + 1
    for y in ys:
        lo, hi, p = 0, n - 1, 0
        while lo <= hi:
            mid = (lo + hi) // 2; p += 1
            if keys[mid] == y: raise SystemExit("present")
            if keys[mid] < y: lo = mid + 1
            else: hi = mid - 1
        assert lo == sum(1 for k in keys if k < y)
        worst = max(worst, p); tot += 1
    allok &= worst == n.bit_length()
print("Part D gaps", tot, "all worst equal floor(log2 n)+1", allok)
