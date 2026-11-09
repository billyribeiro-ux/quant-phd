"""Independent recomputation of the L05 (AVL), L06 (BFS/DFS) and L07 (LCS, coin change) lab numbers.

Written from the lesson text and the mathematics, not from the twins. Heights are recomputed from
the structure on every call (no stored heights), so an error in the twin's bookkeeping would show.
Run: python -I -W error recompute_L05_L07.py
"""
from __future__ import annotations

import math
import random
from collections import deque

PHI = (1 + math.sqrt(5)) / 2
out: list[str] = []


def say(s: str) -> None:
    out.append(s)


# ---------- L05: AVL, heights recomputed from structure ----------
class N:
    __slots__ = ("k", "l", "r")

    def __init__(self, k: int) -> None:
        self.k, self.l, self.r = k, None, None


def ht(n: N | None) -> int:
    return 0 if n is None else 1 + max(ht(n.l), ht(n.r))


def bf(n: N) -> int:
    return ht(n.l) - ht(n.r)


calls = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}


def rot_r(y: N) -> N:
    x = y.l
    assert x is not None
    y.l, x.r = x.r, y
    return x


def rot_l(x: N) -> N:
    y = x.r
    assert y is not None
    x.r, y.l = y.l, x
    return y


def ins(n: N | None, k: int, per: list[int]) -> N:
    if n is None:
        return N(k)
    if k < n.k:
        n.l = ins(n.l, k, per)
    elif k > n.k:
        n.r = ins(n.r, k, per)
    else:
        raise ValueError("dup")
    b = bf(n)
    if b > 1:
        assert n.l is not None
        if bf(n.l) >= 0:
            calls["LL"] += 1
            per[0] += 1
            return rot_r(n)
        calls["LR"] += 1
        per[0] += 2
        n.l = rot_l(n.l)
        return rot_r(n)
    if b < -1:
        assert n.r is not None
        if bf(n.r) <= 0:
            calls["RR"] += 1
            per[0] += 1
            return rot_l(n)
        calls["RL"] += 1
        per[0] += 2
        n.r = rot_r(n.r)
        return rot_l(n)
    return n


def balanced(n: N | None) -> bool:
    if n is None:
        return True
    return abs(bf(n)) <= 1 and balanced(n.l) and balanced(n.r)


def inorder(n: N | None, acc: list[int]) -> list[int]:
    if n is not None:
        inorder(n.l, acc)
        acc.append(n.k)
        inorder(n.r, acc)
    return acc


def size(n: N | None) -> int:
    return 0 if n is None else 1 + size(n.l) + size(n.r)


def l05() -> None:
    rng = random.Random(20261028)
    keys = rng.sample(range(1, 1_000_000), 500)
    root = None
    per_insert: list[int] = []
    no_rot = 0
    maxc = 0
    seen: list[int] = []
    ok_all = True
    for k in keys:
        cnt = [0]
        root = ins(root, k, cnt)
        seen.append(k)
        maxc = max(maxc, cnt[0])
        if cnt[0] == 0:
            no_rot += 1
        ok_all = ok_all and balanced(root) and inorder(root, []) == sorted(seen)
        ok_all = ok_all and ht(root) <= math.log(len(seen) + 1) / math.log(PHI) + 1e-12
    say(f"L05 A: ok_all={ok_all} final_height={ht(root)} size={size(root)} log_phi_501={math.log(501)/math.log(PHI):.4f}")
    total = sum(calls.values())
    say(f"L05 A: rotation_calls_total={total} kinds LL={calls['LL']} RR={calls['RR']} LR={calls['LR']} RL={calls['RL']}")
    say(f"L05 A: calls_formula LL+RR+2(LR+RL)={calls['LL']+calls['RR']+2*(calls['LR']+calls['RL'])}")
    say(f"L05 A: no_rotation_inserts={no_rot} share={no_rot/500:.4%} max_calls_per_insert={maxc}")
    # Part B
    plain = None
    avl = None
    for k in range(1, 65):
        plain = ins_plain(plain, k)
        avl = ins(avl, k, [0])
    say(f"L05 B: plain_height={ht_plain(plain)} avl_height={ht(avl)} log_phi_65={math.log(65)/math.log(PHI):.4f} balanced={balanced(avl)}")
    # Part C
    Nv = [0, 1]
    for h in range(2, 13):
        Nv.append(1 + Nv[h - 1] + Nv[h - 2])
    say("L05 C: N(0..12)=" + ",".join(map(str, Nv)))
    say(f"L05 C: N(h)+1>=phi^h for h=1..12: {all(Nv[h] + 1 >= PHI**h for h in range(1, 13))}")
    say(f"L05 C: 1/log2(phi)={1/math.log2(PHI):.6f}  log_phi(377)={math.log(377)/math.log(PHI):.4f}  log_phi(8)={math.log(8)/math.log(PHI):.4f} ln377={math.log(377):.4f} lnphi={math.log(PHI):.4f} log_phi3={math.log(3)/math.log(PHI):.4f} log_phi65={math.log(65)/math.log(PHI):.4f}")
    two = ins(ins(None, 2, [0]), 1, [0])
    say(f"L05 C: two-node height={ht(two)}")


def ins_plain(n: N | None, k: int) -> N:
    if n is None:
        return N(k)
    if k < n.k:
        n.l = ins_plain(n.l, k)
    elif k > n.k:
        n.r = ins_plain(n.r, k)
    return n


def ht_plain(n: N | None) -> int:
    return ht(n)


# ---------- L06: BFS, brute force, DFS, Part D ----------
def rgraph(rng: random.Random, n: int, p: float) -> dict[int, list[int]]:
    adj: dict[int, list[int]] = {v: [] for v in range(n)}
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                adj[u].append(v)
                adj[v].append(u)
    for v in adj:
        adj[v].sort()
    return adj


def bfs_dist(adj: dict[int, list[int]], s: int) -> dict[int, int]:
    d = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in d:
                d[v] = d[u] + 1
                q.append(v)
    return d


def simple_path_min(adj: dict[int, list[int]], s: int) -> dict[int, int]:
    best: dict[int, int] = {s: 0}

    def rec(u: int, seen: set[int], depth: int) -> None:
        for v in adj[u]:
            if v in seen:
                continue
            if depth + 1 < best.get(v, 10**9):
                best[v] = depth + 1
            seen.add(v)
            rec(v, seen, depth + 1)
            seen.remove(v)

    rec(s, {s}, 0)
    return best


def dfs_clock(adj: dict[int, list[int]]) -> tuple[dict[int, int], dict[int, int]]:
    d: dict[int, int] = {}
    f: dict[int, int] = {}
    t = [0]

    def visit(u: int) -> None:
        t[0] += 1
        d[u] = t[0]
        for v in adj[u]:
            if v not in d:
                visit(v)
        t[0] += 1
        f[u] = t[0]

    for u in sorted(adj):
        if u not in d:
            visit(u)
    return d, f


def l06() -> None:
    rng = random.Random(20261028)
    gA = 0
    srcs = 0
    pairs = 0
    unreach = 0
    mism = 0
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj = rgraph(rng, n, p)
        gA += 1
        for s in range(n):
            srcs += 1
            a = bfs_dist(adj, s)
            b = simple_path_min(adj, s)
            pairs += len(a)
            unreach += n - len(a)
            if a != b:
                mism += 1
    say(f"L06 A: graphs={gA} sources={srcs} reachable_pairs={pairs} unreachable={unreach} mismatches={mism}")
    viol = 0
    npairs = 0
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj = rgraph(rng, n, p)
        d, f = dfs_clock(adj)
        for u in range(n):
            for v in range(u + 1, n):
                npairs += 1
                disj = f[u] < d[v] or f[v] < d[u]
                nest = (d[u] < d[v] and f[v] < f[u]) or (d[v] < d[u] and f[u] < f[v])
                if not (disj or nest):
                    viol += 1
    say(f"L06 B: vertex_pairs={npairs} violations={viol}")
    rng2 = random.Random(20261028 + 1000)
    adj = rgraph(rng2, 200, 0.03)
    edges = sum(len(adj[v]) for v in adj) // 2
    dist = bfs_dist(adj, 0)
    deg_sum_reached = sum(len(adj[v]) for v in dist)
    entries = deg_sum_reached
    say(f"L06 D: edges={edges} reached={len(dist)} entries={entries} 2E={2*edges} list_work={len(dist)+entries} matrix_reads={len(dist)*200}")
    # Part C weighted 4-vertex graph
    w = {(0, 1): 10, (0, 2): 1, (1, 2): 1, (1, 3): 1}
    adjc = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
    best: dict[int, int] = {}

    def rec(u: int, seen: list[int], total: int) -> None:
        for v in adjc[u]:
            if v in seen:
                continue
            step = total + w[(min(u, v), max(u, v))]
            if v not in best or step < best[v]:
                best[v] = step
            rec(v, seen + [v], step)

    rec(0, [0], 0)
    say(f"L06 C: lightest weights a={best[1]} b={best[2]} c={best[3]}")


# ---------- L07: LCS and coin change ----------
def lcs_dp(x: str, y: str) -> int:
    m, n = len(x), len(y)
    t = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            t[i][j] = t[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else max(t[i - 1][j], t[i][j - 1])
    return t[m][n]


def lcs_brute(x: str, y: str) -> int:
    from itertools import combinations

    def is_sub(s: str, t: str) -> bool:
        it = iter(t)
        return all(c in it for c in s)

    best = 0
    for L in range(len(x), 0, -1):
        for idx in combinations(range(len(x)), L):
            if is_sub("".join(x[i] for i in idx), y):
                return L
    return best


def lcs_memo_stats(x: str, y: str) -> tuple[int, int, int, int, int]:
    """Return (stored, calls, lookups, base_calls, computed) for memoized recursion, my own bookkeeping."""
    memo: dict[tuple[int, int], int] = {}
    stats = {"calls": 0, "lookups": 0, "base": 0, "computed": 0}

    def g(i: int, j: int) -> int:
        stats["calls"] += 1
        if i == 0 or j == 0:
            stats["base"] += 1
            return 0
        if (i, j) in memo:
            stats["lookups"] += 1
            return memo[(i, j)]
        stats["computed"] += 1
        if x[i - 1] == y[j - 1]:
            val = g(i - 1, j - 1) + 1
        else:
            val = max(g(i - 1, j), g(i, j - 1))
        memo[(i, j)] = val
        return val

    g(len(x), len(y))
    return len(memo), stats["calls"], stats["lookups"], stats["base"], stats["computed"]


def naive_calls(x: str, y: str) -> int:
    c = [0]

    def g(i: int, j: int) -> int:
        c[0] += 1
        if i == 0 or j == 0:
            return 0
        if x[i - 1] == y[j - 1]:
            return g(i - 1, j - 1) + 1
        return max(g(i - 1, j), g(i, j - 1))

    g(len(x), len(y))
    return c[0]


class LCG:
    def __init__(self, s: int) -> None:
        self.s = s % (2**31)

    def below(self, n: int) -> int:
        self.s = (1103515245 * self.s + 12345) % (2**31)
        return (self.s >> 16) % n


def coin_min(denoms: tuple[int, ...], amt: int) -> int | None:
    INF = 10**9
    dp = [0] + [INF] * amt
    for a in range(1, amt + 1):
        for c in denoms:
            if c <= a and dp[a - c] < INF:
                dp[a] = min(dp[a], 1 + dp[a - c])
    return dp[amt] if dp[amt] < INF else None


def coin_memo_stats(denoms: tuple[int, ...], amt: int) -> tuple[int, int]:
    memo: dict[int, int | None] = {}
    c = [0]

    def g(a: int) -> int | None:
        c[0] += 1
        if a == 0:
            return 0
        if a in memo:
            return memo[a]
        vals = [1 + s for cc in denoms if cc <= a for s in [g(a - cc)] if s is not None]
        memo[a] = min(vals) if vals else None
        return memo[a]

    g(amt)
    return len(memo), c[0]


def coin_naive(denoms: tuple[int, ...], amt: int) -> int:
    c = [0]

    def g(a: int) -> int | None:
        c[0] += 1
        if a == 0:
            return 0
        vals = [1 + s for cc in denoms if cc <= a for s in [g(a - cc)] if s is not None]
        return min(vals) if vals else None

    g(amt)
    return c[0]


def greedy(denoms: tuple[int, ...], amt: int) -> int | None:
    r, used = amt, 0
    while r > 0:
        fits = [c for c in denoms if c <= r]
        if not fits:
            return None
        r -= max(fits)
        used += 1
    return used


def l07() -> None:
    g = LCG(20261028)
    pairs = []
    for _ in range(30):
        m = 1 + g.below(7)
        n = 1 + g.below(7)
        x = "".join("ACGT"[g.below(4)] for _ in range(m))
        y = "".join("ACGT"[g.below(4)] for _ in range(n))
        pairs.append((x, y))
    cases = []
    for _ in range(30):
        size = 2 + g.below(3)
        ch: set[int] = set()
        while len(ch) < size:
            ch.add(1 + g.below(9))
        amt = g.below(13)
        cases.append((tuple(sorted(ch)), amt))
    agree = all(lcs_dp(x, y) == lcs_brute(x, y) for x, y in pairs)
    say(f"L07 A: 30 LCS pairs dp==brute: {agree}; first pair {pairs[0]} lcs={lcs_dp(*pairs[0])}")
    none = sum(1 for d, a in cases if coin_min(d, a) is None)
    say(f"L07 B: coin cases with no combination={none} of 30; greedy(1,3,4;6)={greedy((1,3,4),6)} opt={coin_min((1,3,4),6)}")
    X, Y = "ACGTACG", "TGCATGC"
    stored, calls, look, base, comp = lcs_memo_stats(X, Y)
    say(f"L07 C: lcs={lcs_dp(X, Y)} memo stored={stored} calls={calls} lookups={look} base={base} computed={comp} naive_calls={naive_calls(X, Y)} table={len(X)*len(Y)}")
    say(f"L07 C: check calls = computed+lookups+base = {comp+look+base}")
    st, cl = coin_memo_stats((1, 3, 4), 20)
    say(f"L07 C: coins(1,3,4;20) min={coin_min((1,3,4),20)} stored={st} memo_calls={cl} naive_calls={coin_naive((1,3,4),20)}")
    say(f"L07 extra: {{1}} amount 3 memo touches {sorted(set([3,2,1,0]))}")
    say(f"L07 R2 check: greedy(1,c) optimal for c=2..30, a<=200: {all(greedy((1,c),a)==coin_min((1,c),a) for c in range(2,31) for a in range(0,201))}")
    say(f"L07 E1: stored amounts for (1,3,4;20) = {coin_memo_stats((1,3,4),20)[0]}")
    say(f"L07 Ex2.4: f(0..6)={[coin_min((1,3,4),a) for a in range(7)]}")
    say(f"L07 M1: f(9) for {{2,5}} = {coin_min((2,5),9)}; f(7)={coin_min((2,5),7)}; f(4)={coin_min((2,5),4)}")
    say(f"L07 P3: first failing amount for (1,3,4): {next(a for a in range(1,100) if greedy((1,3,4),a)!=coin_min((1,3,4),a))}")
    say(f"L07 R1: 2^20+1={2**20+1}; 2^40={2**40}; 1000 bits={1000 .bit_length()}")


if __name__ == "__main__":
    l05()
    l06()
    l07()
    print("\n".join(out))
