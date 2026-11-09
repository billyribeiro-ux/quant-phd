"""Independent recomputation of the numbers printed in CS2 L05, L06 and L07 prose (verifier round 4).

Run: python3 -I numbers_L05_L06_L07_r4.py
Each block is written from the page's definitions, not copied from the lab twin.
"""
import math
import random
from functools import lru_cache

# ---- L05: AVL, written from Definition 2.1 and Definition 2.2 ----
PHI = (1 + math.sqrt(5)) / 2


class T:
    __slots__ = ("k", "l", "r")

    def __init__(self, k):
        self.k, self.l, self.r = k, None, None


def ht(t):
    if t is None:
        return 0
    return 1 + max(ht(t.l), ht(t.r))  # recomputed, not stored


def bf(t):
    return ht(t.l) - ht(t.r)


calls = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}


def rot_r(y):
    x = y.l
    y.l, x.r = x.r, y
    return x


def rot_l(x):
    y = x.r
    x.r, y.l = y.l, x
    return y


def fix(t):
    b = bf(t)
    if b > 1:
        if bf(t.l) < 0:
            calls["LR"] += 1
            t.l = rot_l(t.l)
            # a double rotation is two rotation calls
            calls["LR"] += 0
        else:
            calls["LL"] += 1
        return rot_r(t)
    if b < -1:
        if bf(t.r) > 0:
            calls["RL"] += 1
            t.r = rot_r(t.r)
        else:
            calls["RR"] += 1
        return rot_l(t)
    return t


def ins(t, k):
    if t is None:
        return T(k)
    if k < t.k:
        t.l = ins(t.l, k)
    else:
        t.r = ins(t.r, k)
    return fix(t)


def inorder(t, out):
    if t is not None:
        inorder(t.l, out)
        out.append(t.k)
        inorder(t.r, out)
    return out


def ok_all(t):
    if t is None:
        return True
    return abs(bf(t)) <= 1 and ok_all(t.l) and ok_all(t.r)


rng = random.Random(20261028)
keys = rng.sample(range(1, 1_000_000), 500)
root = None
no_rot = 0
max_calls_one = 0
for n, k in enumerate(keys, 1):
    before = sum(calls.values())
    root = ins(root, k)
    used = sum(calls.values()) - before
    # rebalance events count 1 (single) or 2 (double) rotation calls
    dbl = calls["LR"] + calls["RL"]
    if used == 0:
        no_rot += 1
    assert ok_all(root)
    assert inorder(root, []) == sorted(keys[:n])
print("L05 final height", ht(root), "log_phi 501", round(math.log(501) / math.log(PHI), 4))
print("L05 events LL", calls["LL"], "RR", calls["RR"], "LR", calls["LR"], "RL", calls["RL"])
print("L05 rotation calls", calls["LL"] + calls["RR"] + 2 * (calls["LR"] + calls["RL"]))
print("L05 inserts without rotation", no_rot, "share %", round(100 * no_rot / 500, 2))

# plain BST and AVL on 1..64
r2 = None
for k in range(1, 65):
    r2 = ins(r2, k)
plain = None


def pins(t, k):
    if t is None:
        return T(k)
    if k < t.k:
        t.l = pins(t.l, k)
    else:
        t.r = pins(t.r, k)
    return t


for k in range(1, 65):
    plain = pins(plain, k)
print("L05 plain height", ht(plain), "avl height", ht(r2), "log_phi 65", round(math.log(65) / math.log(PHI), 4))
print("L05 1/log2(phi)", round(1 / math.log2(PHI), 6), "log_phi 8", round(math.log(8) / math.log(PHI), 3))
print("L05 log_phi 377", round(math.log(377) / math.log(PHI), 3), "ln377", round(math.log(377), 3), "lnphi", round(math.log(PHI), 4))
print("L05 log_phi 3", round(math.log(3) / math.log(PHI), 3))

N = [0, 1]
for h in range(2, 14):
    N.append(1 + N[h - 1] + N[h - 2])
print("L05 N(0..13)", N[:14])
print("L05 N(5)", N[5], "N(12)", N[12], "N(4)", N[4])
print("L05 N(h)+1 >= phi^h for h 1..12:", all(N[h] + 1 >= PHI**h for h in range(1, 13)))

# ---- L06: BFS and DFS, written from Definition 1.1 and 3.1 ----
from collections import deque


def rgraph(rng, n, p):
    adj = {v: [] for v in range(n)}
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    for v in adj:
        adj[v].sort()
    return adj


def bfs(adj, s):
    d = {s: 0}
    q = deque([s])
    insp = 0
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            insp += 1
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d, order, insp


def brute(adj, s):
    best = {s: 0}

    def go(v, used, L):
        for u in adj[v]:
            if u in used:
                continue
            if L + 1 < best.get(u, 10**9):
                best[u] = L + 1
            used.add(u)
            go(u, used, L + 1)
            used.remove(u)

    go(s, {s}, 0)
    return best


def dfs(adj):
    dis, fin, clock = {}, {}, [0]

    def visit(v):
        clock[0] += 1
        dis[v] = clock[0]
        for u in adj[v]:
            if u not in dis:
                visit(u)
        clock[0] += 1
        fin[v] = clock[0]

    for v in sorted(adj):
        if v not in dis:
            visit(v)
    return dis, fin


def nested(dis, fin, u, v):
    a, b = (dis[u], fin[u]), (dis[v], fin[v])
    disjoint = b[1] < a[0] or a[1] < b[0]
    contains = (a[0] < b[0] and b[1] < a[1]) or (b[0] < a[0] and a[1] < b[1])
    return disjoint or contains


rng = random.Random(20261028)
pairs = mism = unreach = srcs = 0
for k in range(40):
    n = 3 + k % 5
    p = 0.2 + 0.1 * (k % 4)
    adj = rgraph(rng, n, p)
    for s in range(n):
        srcs += 1
        d, _, _ = bfs(adj, s)
        bb = brute(adj, s)
        pairs += len(d)
        unreach += n - len(d)
        if d != bb:
            mism += 1
print("L06 A graphs 40 sources", srcs, "reachable pairs", pairs, "unreachable", unreach, "mismatches", mism)
vp = vio = 0
for k in range(40):
    n = 3 + k % 5
    p = 0.2 + 0.1 * (k % 4)
    adj = rgraph(rng, n, p)
    dis, fin = dfs(adj)
    for u in range(n):
        for v in range(u + 1, n):
            vp += 1
            if not nested(dis, fin, u, v):
                vio += 1
print("L06 B vertex pairs", vp, "violations", vio)

rng = random.Random(20261028 + 1000)
g = rgraph(rng, 200, 0.03)
edges = sum(len(g[v]) for v in g) // 2
d, order, insp = bfs(g, 0)
print("L06 D edges", edges, "reached", len(d), "inspections", insp, "list work", len(d) + insp, "matrix reads", len(order) * 200)
print("L06 40000/1438", round(40000 / 1438, 4), "avg degree", round(2 * edges / 200, 4), "1238/200", 1238 / 200)

# L06 Part C weighted example
adj = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
w = {(0, 1): 10, (0, 2): 1, (1, 2): 1, (1, 3): 1}
print("L06 C path s-a weight", w[(0, 1)], "s-b-a weight", w[(0, 2)] + w[(1, 2)], "s-a-c", w[(0, 1)] + w[(1, 3)], "s-b-a-c", w[(0, 2)] + w[(1, 2)] + w[(1, 3)])

# ---- L07: LCS and coins, written from Theorem 3.3 and Definition 1.1 ----
def lcs_memo(x, y):
    cache = {}
    calls = [0]
    base = [0]

    def go(i, j):
        calls[0] += 1
        if i == 0 or j == 0:
            base[0] += 1
            return 0
        if (i, j) in cache:
            return cache[(i, j)]
        if x[i - 1] == y[j - 1]:
            v = go(i - 1, j - 1) + 1
        else:
            v = max(go(i - 1, j), go(i, j - 1))
        cache[(i, j)] = v
        return v

    val = go(len(x), len(y))
    return val, len(cache), calls[0], base[0], calls[0] - len(cache) - base[0]


def lcs_naive(x, y):
    c = [0]

    def go(i, j):
        c[0] += 1
        if i == 0 or j == 0:
            return 0
        if x[i - 1] == y[j - 1]:
            return go(i - 1, j - 1) + 1
        return max(go(i - 1, j), go(i, j - 1))

    go(len(x), len(y))
    return c[0]


val, stored, calls47, base, lookups = lcs_memo("ACGTACG", "TGCATGC")
print("L07 LCS ACGTACG/TGCATGC: length", val, "stored", stored, "calls", calls47, "base", base, "lookups", lookups, "naive calls", lcs_naive("ACGTACG", "TGCATGC"), "table cells", 7 * 7)


def coins_memo(D, a):
    cache = {}
    calls = [0]

    def f(b):
        calls[0] += 1
        if b == 0:
            return 0
        if b in cache:
            return cache[b]
        cands = [1 + f(b - c) for c in D if c <= b]
        cache[b] = min(cands) if cands else None
        return cache[b]

    return f(a), len(cache), calls[0]


def coins_naive(D, a):
    c = [0]

    def f(b):
        c[0] += 1
        if b == 0:
            return 0
        cands = [1 + f(b - x) for x in D if x <= b]
        return min(cands) if cands else None

    f(a)
    return c[0]


print("L07 coins (1,3,4) amount 20 memo", coins_memo((1, 3, 4), 20), "naive", coins_naive((1, 3, 4), 20))
print("L07 P3 greedy failure check (1,3,4):", [(a, coins_memo((1, 3, 4), a)[0]) for a in range(1, 8)])
print("L07 2^40 bits", (2**40).bit_length(), "2^40+1 >1e12", 2**40 + 1 > 10**12, "2^40", 2**40)
print("L07 2^20+1", 2**20 + 1, "bits", (2**20).bit_length())
print("L07 1000 bits", (1000).bit_length(), "1025", 1024 + 1)
