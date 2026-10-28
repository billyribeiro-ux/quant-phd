"""Verifier round 1 (CS2-b): independent recomputation of L07 Lab 1 counts and the lesson's coin/LCS examples.
Run: <checkout>/.venv/bin/python -I <checkout>/ledgers/CS2/scripts/CS2-b-r1/check_L07_counts.py
"""
from functools import lru_cache
import sys

sys.setrecursionlimit(10000)
M, C, MOD = 1103515245, 12345, 2**31


def gen(seed):
    s = seed % MOD
    while True:
        s = (M * s + C) % MOD
        yield (s >> 16)


def pick(g, n):
    return next(g) % n


g = gen(20261028)
lcs_pairs = []
for _ in range(30):
    m = 1 + pick(g, 7)
    n = 1 + pick(g, 7)
    x = "".join("ACGT"[pick(g, 4)] for _ in range(m))
    y = "".join("ACGT"[pick(g, 4)] for _ in range(n))
    lcs_pairs.append((x, y))
coin_cases = []
for _ in range(30):
    size = 2 + pick(g, 3)
    chosen = set()
    while len(chosen) < size:
        chosen.add(1 + pick(g, 9))
    amount = pick(g, 13)
    coin_cases.append((tuple(sorted(chosen)), amount))

# independent LCS: lru_cache memo, count distinct keys and calls
def lcs_counts(x, y):
    calls = [0]
    @lru_cache(maxsize=None)
    def f(i, j):
        calls[0] += 1
        if i == 0 or j == 0:
            return 0
        if x[i - 1] == y[j - 1]:
            return f(i - 1, j - 1) + 1
        return max(f(i - 1, j), f(i, j - 1))
    val = f(len(x), len(y))
    stored = sum(1 for i in range(1, len(x) + 1) for j in range(1, len(y) + 1) if (i, j) in set(_keys(f)))
    return val, f.cache_info().currsize, calls[0]

def _keys(f):
    return []

def lcs_full(x, y):
    """Return (length, set of reached non-base pairs, total calls) for the memo recursion, computed directly."""
    reached = set()
    calls = [0]
    memo = {}
    def go(i, j):
        calls[0] += 1
        if i == 0 or j == 0:
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        reached.add((i, j))
        if x[i - 1] == y[j - 1]:
            v = go(i - 1, j - 1) + 1
        else:
            v = max(go(i - 1, j), go(i, j - 1))
        memo[(i, j)] = v
        return v
    val = go(len(x), len(y))
    return val, len(reached), calls[0]

def lcs_naive_calls(x, y):
    calls = [0]
    def go(i, j):
        calls[0] += 1
        if i == 0 or j == 0:
            return 0
        if x[i - 1] == y[j - 1]:
            return go(i - 1, j - 1) + 1
        return max(go(i - 1, j), go(i, j - 1))
    go(len(x), len(y))
    return calls[0]

def lcs_dp(x, y):
    m, n = len(x), len(y)
    t = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            t[i][j] = t[i-1][j-1] + 1 if x[i-1] == y[j-1] else max(t[i-1][j], t[i][j-1])
    return t[m][n]

def lcs_bruteforce(x, y):
    from itertools import combinations
    def issub(s, t):
        it = iter(t)
        return all(c in it for c in s)
    best = 0
    for k in range(len(x) + 1):
        for idx in combinations(range(len(x)), k):
            s = "".join(x[i] for i in idx)
            if issub(s, y):
                best = max(best, k)
    return best

x, y = "ACGTACG", "TGCATGC"
val, stored, calls = lcs_full(x, y)
print("LCS ACGTACG/TGCATGC length", val, "reached non-base pairs (stored)", stored, "memo calls", calls)
print("naive calls (no memo)", lcs_naive_calls(x, y))
print("dp length", lcs_dp(x, y), "brute length", lcs_bruteforce(x, y))
print("cells", len(x) * len(y))
bad = 0
for a, b in lcs_pairs:
    if not (lcs_dp(a, b) == lcs_bruteforce(a, b) == lcs_full(a, b)[0]):
        bad += 1
print("lcs pairs disagreeing", bad, "of", len(lcs_pairs))

# coins
def coin_min(denoms, amount):
    INF = float("inf")
    f = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in denoms:
            if c <= a and f[a - c] + 1 < f[a]:
                f[a] = f[a - c] + 1
    return None if f[amount] == INF else f[amount]

def coin_exhaustive(denoms, amount):
    best = None
    def rec(k, rem, used):
        nonlocal best
        if k == len(denoms):
            if rem == 0 and (best is None or used < best):
                best = used
            return
        for cnt in range(rem // denoms[k] + 1):
            rec(k + 1, rem - cnt * denoms[k], used + cnt)
    rec(0, amount, 0)
    return best

none_count = 0
bad_c = 0
for d, a in coin_cases:
    v = coin_min(d, a)
    none_count += v is None
    if v != coin_exhaustive(d, a):
        bad_c += 1
print("coin instances with None", none_count, "of", len(coin_cases), "disagreements", bad_c)
print("coin {1,3,4} amount 6 optimum", coin_min((1, 3, 4), 6))

# naive coin calls and memo for amount 20 with {1,3,4}
def coin_memo_stats(denoms, amount):
    memo = {}
    calls = [0]
    def best(a):
        calls[0] += 1
        if a == 0:
            return 0
        if a in memo:
            return memo[a]
        cands = [1 + best(a - c) for c in denoms if c <= a]
        memo[a] = min(cands) if cands else None
        return memo[a]
    best(amount)
    return len(memo), calls[0]

def coin_naive_calls(denoms, amount):
    calls = [0]
    def best(a):
        calls[0] += 1
        if a == 0:
            return 0
        cands = [1 + best(a - c) for c in denoms if c <= a]
        return min(cands) if cands else None
    best(amount)
    return calls[0]

print("coin memo (stored, calls) for {1,3,4} amount 20:", coin_memo_stats((1, 3, 4), 20), "naive calls:", coin_naive_calls((1, 3, 4), 20))
print("1/ 2^20 table entries", 2**20 + 1)
