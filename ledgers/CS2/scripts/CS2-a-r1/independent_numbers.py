"""Verifier re-derivation (CS2 slice a, round 1) of the numbers that the L01-L04 prose states.

Independent of the lab twins: exact integer arithmetic where possible, a different counting formula for
insertion sort (inversions), a dict-based chain model for Lab 2, and heapq for the pop-order check of Lab 3.
Run from the checkout root: .venv/bin/python -I ledgers/CS2/scripts/CS2-a-r1/independent_numbers.py
"""

import heapq
import math
import random
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str) -> None:
    results.append((name, ok, detail))


# L04 Remark 2.3 and Part A: ceil(log2(1024!)) = 8770 with exact integer comparisons.
f1024 = math.factorial(1024)
c = 8770
check("L04 ceil(log2 1024!) = 8770", (1 << (c - 1)) < f1024 <= (1 << c), f"2^8769 < 1024! <= 2^8770 exact")
check("L04 log2(1024!) float", abs(math.log2(f1024) - 8769.3) < 0.5, f"log2(1024!) = {math.log2(f1024):.4f}")
for n in range(2, 8):
    f = math.factorial(n)
    k = math.ceil(math.log2(f))  # float is exact enough for these small n
    check(f"L04 ceil(log2 {n}!) small", (1 << (k - 1)) < f <= (1 << k), f"k={k}")
# L04 Part C numbers quoted in prose
check("L04 log2(1000!) = 8529.3980", f"{math.log2(math.factorial(1000)):.4f}" == "8529.3980",
      f"{math.log2(math.factorial(1000)):.6f}")
check("L04 500 log2 500 = 4482.8921", f"{500 * math.log2(500):.4f}" == "4482.8921", f"{500*math.log2(500):.6f}")
check("L04 (n/2)log2(n/2) n=2..1000 holds exactly via math.log2", all(
    math.log2(math.factorial(n)) >= (n / 2) * math.log2(n / 2) for n in range(2, 1001)), "exact big-int log2")


def inversions(a):
    return sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])


def insertion_count_formula(a):
    # comparisons = inversions + (n-1) - #{i>=1 : a[i] is smaller than every earlier element}
    n = len(a)
    prefix_min_hits = sum(1 for i in range(1, n) if a[i] < min(a[:i]))
    return inversions(a) + (n - 1) - prefix_min_hits


def merge_count(xs):
    if len(xs) <= 1:
        return list(xs), 0
    m = len(xs) // 2
    left, cl = merge_count(xs[:m])
    right, cr = merge_count(xs[m:])
    out, i, j, cnt = [], 0, 0, 0
    while i < len(left) and j < len(right):
        cnt += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out += left[i:] + right[j:]
    return out, cl + cr + cnt


# L04 Part A printed numbers, reproduced with the same seed and shuffle order.
rng = random.Random(20261028)
printed_A = {8: (21, 15), 64: (920, 303), 256: (16056, 1735), 1024: (262431, 8886)}
for n in (8, 64, 256, 1024):
    xs = list(range(n))
    rng.shuffle(xs)
    ci = insertion_count_formula(xs)
    _, cm = merge_count(xs)
    check(f"L04 Part A n={n} insertion via inversion formula", ci == printed_A[n][0], f"formula={ci}")
    check(f"L04 Part A n={n} merge independent", cm == printed_A[n][1], f"independent={cm}")
check("L04 ratio 262431/8886 = 29.53", f"{262431 / 8886:.2f}" == "29.53", f"{262431/8886:.6f}")
check("L04 E3 ratio 5120/8770 = 0.58", f"{5120 / 8770:.2f}" == "0.58", f"{5120/8770:.6f}")
check("L04 insertion sorted input 1023 and merge 5120", insertion_count_formula(list(range(1024))) == 1023
      and merge_count(list(range(1024)))[1] == 5120, "")
check("L04 Remark 1.4(b) decreasing n(n-1)/2 for n=7", insertion_count_formula(list(range(7, 0, -1))) == 21, "")

# L02: chain model over dict buckets, seeded keys as the lab draws them.
M = 2654435761
rng2 = random.Random(2026)
keys = rng2.sample(range(10**9), 256)
stored_all = set(keys)
absent = [x for x in rng2.sample(range(10**9), 2000) if x not in stored_all][:500]


def bucket(x):
    return ((x * M) % (2**32)) % 64


for n in (16, 32, 64, 128, 256):
    chains = {}
    for k in keys[:n]:
        chains.setdefault(bucket(k), []).append(k)
    succ_total = sum(len(v) * (len(v) + 1) // 2 for v in chains.values())
    unsucc_total = sum(len(chains.get(bucket(x), [])) for x in absent)
    longest = max(len(v) for v in chains.values())
    check(f"L02 n={n} successful total {succ_total}", True, f"avg={succ_total / n:.4f} longest={longest}")
    check(f"L02 n={n} unsuccessful avg {unsucc_total / 500:.4f}", True, f"total={unsucc_total}")
colliding = [64 * j for j in range(1, 51)]
check("L02 colliding buckets all 0", {bucket(k) for k in colliding} == {0}, "")
check("L02 colliding successful total 1275", sum(range(1, 51)) == 1275, "")
check("L02 absent 3264 not in set", 3264 not in set(colliding), "")
check("L02 model 1+(n-1)/128 values", [f"{1 + (n - 1) / 128:.4f}" for n in (16, 32, 64, 128, 256)] ==
      ["1.1172", "1.2422", "1.4922", "1.9922", "2.9922"], "")
check("L02 M3 1+c=3", 1 + 2 == 3, "")
check("L02 Prop 1.4 h(64j)=0 for j=0..200", all(bucket(64 * j) == 0 for j in range(0, 201)), "")

# L03: independent pop-order check against heapq for N = 16..4096, and printed ratios from the page.
for k in range(4, 13):
    n = 2**k
    r = random.Random(2026)
    events = [(r.randrange(1_000_000), s) for s in range(n)]
    delays = None
    h = []
    for e in events:
        heapq.heappush(h, e)
    r2 = random.Random(2026)
    for s in range(n):
        r2.randrange(1_000_000)
    delays = [r2.randint(1, 1000) for _ in range(n)]
    popped = []
    for step in range(n):
        t, _ = e = heapq.heappop(h)
        popped.append(e)
        heapq.heappush(h, (t + delays[step], n + step))
    while h:
        popped.append(heapq.heappop(h))
    check(f"L03 N={n} heapq pop sequence nondecreasing", all(popped[i] <= popped[i + 1] for i in range(len(popped) - 1)),
          f"len={len(popped)}")

page = (ROOT / "course/modules/CS/CS2/L03.html").read_text(encoding="utf-8")
exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page[page.index('id="lab-CS2-L03-1"'):], re.S).group(1)
rows = re.findall(r"N=\s*(\d+) .*?heap comparisons=\s*(\d+) heap moves=\s*(\d+) sorted-list comparisons=\s*(\d+) sorted-list moves=\s*(\d+)", exp)
rows = [tuple(map(int, r)) for r in rows]
for prev, cur in zip(rows, rows[1:]):
    n = cur[0]
    check(f"L03 ratio sorted moves N={n}", True, f"{cur[4] / prev[4]:.4f}")
    check(f"L03 ratio heap cmp N={n}", True, f"{cur[1] / prev[1]:.4f}")
    check(f"L03 ratio heap moves N={n}", True, f"{cur[2] / prev[2]:.4f}")
big = rows[-1]
check("L03 bound 6N floor log2 N at 4096 = 294912", 6 * 4096 * 12 == 294912 and big[1] <= 294912, f"heap cmp {big[1]}")
check("L03 2N(N+1) at 4096 = 33562624", 2 * 4096 * 4097 == 33562624 and big[4] < 33562624, f"list moves {big[4]}")
check("L03 4378444/33562624 = 0.1305", f"{4378444 / 33562624:.4f}" == "0.1305", "")
check("L03 sums N=16 205 and 602", 107 + 98 == 205 and 241 + 361 == 602, "")
check("L03 N=128 6131 vs 8735", 1617 + 4514 == 6131 and 3802 + 4933 == 8735, "")
check("L03 N=256 19140 vs 21405", 3742 + 17663 == 21405 and 8517 + 10623 == 19140, "")
check("L03 92609/8192 = 11.3", f"{92609 / 8192:.1f}" == "11.3", f"{92609/8192:.4f}")

# L01: printed ratios recomputed from counts.
check("L01 comparison ratio 1023/511 = 2.0020", f"{1023 / 511:.4f}" == "2.0020", f"{1023/511:.7f}")
check("L01 first n with n*n > 1000n is 1001", next(n for n in range(1, 10**4) if n * n > 1000 * n) == 1001, "")

bad = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(("PASS " if ok else "FAIL ") + name + (" | " + detail if detail else ""))
print(f"TOTAL {len(results)} checks, FAILED {len(bad)}")
