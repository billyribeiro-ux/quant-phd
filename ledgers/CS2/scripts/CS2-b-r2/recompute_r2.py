"""CS2 slice b, round 2: independent recomputation of every number printed or quoted in L05-L08.

Written from the definitions, not copied from the lab twins. Seeds and generator draw order follow the
seeded-instance specs in the lab docstrings, so the same instances are regenerated.
Usage: python -I -W error recompute_r2.py
"""

from __future__ import annotations

import math
import random
from collections import deque

PHI = (1 + math.sqrt(5)) / 2
out: list[str] = []


def say(msg: str) -> None:
    out.append(msg)
    print(msg)


# ---------- L05: AVL tree written from the definition ----------
class T:
    __slots__ = ("k", "l", "r", "h")

    def __init__(self, k: int) -> None:
        self.k, self.l, self.r, self.h = k, None, None, 1


def ht(t: T | None) -> int:
    return 0 if t is None else t.h


def bf(t: T) -> int:
    return ht(t.l) - ht(t.r)


def fix(t: T) -> None:
    t.h = 1 + max(ht(t.l), ht(t.r))


def rr(y: T) -> T:  # right rotation: left child becomes root
    x = y.l
    assert x is not None
    y.l, x.r = x.r, y
    fix(y)
    fix(x)
    return x


def rl(x: T) -> T:
    y = x.r
    assert y is not None
    x.r, y.l = y.l, x
    fix(x)
    fix(y)
    return y


calls = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}


def rebal(t: T) -> T:
    fix(t)
    b = bf(t)
    if b > 1:
        assert t.l is not None
        if bf(t.l) < 0:  # LR: rotate left child left, then right at t
            t.l = rl(t.l)
            calls["LR"] += 1
            calls_inc(2)
        else:
            calls["LL"] += 1
            calls_inc(1)
        return rr(t)
    if b < -1:
        assert t.r is not None
        if bf(t.r) > 0:  # RL
            t.r = rr(t.r)
            calls["RL"] += 1
            calls_inc(2)
        else:
            calls["RR"] += 1
            calls_inc(1)
        return rl(t)
    return t


ROT = {"n": 0}


def calls_inc(n: int) -> None:
    ROT["n"] += n


def ins(t: T | None, k: int) -> T:
    if t is None:
        return T(k)
    if k < t.k:
        t.l = ins(t.l, k)
    else:
        t.r = ins(t.r, k)
    return rebal(t)


def valid(t: T | None) -> tuple[bool, int]:
    if t is None:
        return True, 0
    okl, hl = valid(t.l)
    okr, hr = valid(t.r)
    h = 1 + max(hl, hr)
    return okl and okr and abs(hl - hr) <= 1 and t.h == h, h


def inorder(t: T | None, acc: list[int]) -> list[int]:
    if t is not None:
        inorder(t.l, acc)
        acc.append(t.k)
        inorder(t.r, acc)
    return acc


def bst_insert(t: T | None, k: int) -> T:
    if t is None:
        return T(k)
    if k < t.k:
        t.l = bst_insert(t.l, k)
    else:
        t.r = bst_insert(t.r, k)
    return t


def plain_h(t: T | None) -> int:
    return 0 if t is None else 1 + max(plain_h(t.l), plain_h(t.r))


def lphi(n: float) -> float:
    return math.log(n) / math.log(PHI)


def l05() -> None:
    rng = random.Random(20261028)
    keys = rng.sample(range(1, 1_000_000), 500)
    root = None
    seen: list[int] = []
    all_ok = True
    no_rot = 0
    max_per_insert = 0
    for k in keys:
        before = ROT["n"]
        root = ins(root, k)
        seen.append(k)
        d = ROT["n"] - before
        no_rot += d == 0
        max_per_insert = max(max_per_insert, d)
        ok, h = valid(root)
        all_ok = all_ok and ok and h <= lphi(len(seen) + 1) and inorder(root, []) == sorted(seen)
    total = sum(calls.values())
    say(f"L05 A: all_checks {all_ok}; final height {ht(root)}; rotation calls {ROT['n']}; kinds {calls}")
    say(f"L05 A: check 63+53+2(55+57) = {calls['LL'] + calls['RR'] + 2 * (calls['LR'] + calls['RL'])}; kinds sum {total}")
    say(f"L05 A: inserts without rotation {no_rot} of 500 = {100 * no_rot / 500:.1f}%; max calls in one insert {max_per_insert}")
    say(f"L05 A: log_phi(501) = {lphi(501):.4f}")
    # Part B: sorted 1..64
    p = None
    a = None
    for k in range(1, 65):
        p = bst_insert(p, k)
        a = ins(a, k)
    say(f"L05 B: plain height {plain_h(p)}; AVL height {ht(a)}; log_phi(65) = {lphi(65):.4f}; valid {valid(a)[0]}")
    # Part C
    N = [0, 1]
    for h in range(2, 13):
        N.append(1 + N[h - 1] + N[h - 2])
    say(f"L05 C: N(0..12) = {N[:13]}")
    say(f"L05 C: N(h)+1 >= phi^h for h=1..12: {all(N[h] + 1 >= PHI ** h for h in range(1, 13))}")
    say(f"L05 C: N(h)+1 values {[N[h] + 1 for h in range(1, 13)]}")
    say(f"L05 C: phi^h {[round(PHI ** h, 4) for h in range(1, 13)]}")
    say(f"L05: 1/log2(phi) = {1 / math.log2(PHI):.6f}; log_phi 3 = {lphi(3):.4f}; log_phi 8 = {lphi(8):.4f}")
    say(f"L05: log_phi 377 = {lphi(377):.4f}; ln 377 = {math.log(377):.4f}; ln phi = {math.log(PHI):.4f}")
    say(f"L05: log_phi 2 for two-node AVL bound check: {lphi(3):.4f} >= 2 : {lphi(3) >= 2}")
    say(f"L05: N(5) by M3 recurrence = {N[5]}; N(4) = {N[4]}")
    # two-node tree 2 root, 1 left
    t = ins(None, 2)
    t = ins(t, 1)
    say(f"L05: two-node AVL height {ht(t)}; log2 2 = {math.log2(2)}")
    # R1 insertion 3,1,2 case
    t = None
    before = dict(calls)
    for k in (3, 1, 2):
        t = ins(t, k)
    say(f"L05 R1: insert 3,1,2 root {t.k} height {ht(t)} balance {bf(t)} rotations {ROT['n']} new-kinds {({k: calls[k] - before[k] for k in calls})}")
    # M2: insert 1,2,3
    t = None
    for k in (1, 2, 3):
        t = ins(t, k)
    say(f"L05 M2: insert 1,2,3 root {t.k} children {t.l.k}, {t.r.k}; height {ht(t)}")


# ---------- L06 ----------
def adj_random(rng: random.Random, n: int, p: float) -> dict[int, list[int]]:
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
    dist = {s: 0}
    q = deque([s])
    while q:
        v = q.popleft()
        for u in adj[v]:
            if u not in dist:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist


def simple_min_hops(adj: dict[int, list[int]], s: int) -> dict[int, int]:
    best = {s: 0}

    def go(v: int, seen: set[int], length: int) -> None:
        for u in adj[v]:
            if u in seen:
                continue
            best[u] = min(best.get(u, 10**9), length + 1)
            seen.add(u)
            go(u, seen, length + 1)
            seen.remove(u)

    go(s, {s}, 0)
    return best


def l06() -> None:
    rng = random.Random(20261028)
    srcs = 0
    pairs = 0
    unreach = 0
    mism = 0
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj = adj_random(rng, n, p)
        for s in range(n):
            srcs += 1
            d = bfs_dist(adj, s)
            pairs += len(d)
            unreach += n - len(d)
            mism += d != simple_min_hops(adj, s)
    say(f"L06 A: sources {srcs}; reachable pairs {pairs}; unreachable {unreach}; mismatches {mism}; pairs minus sources {pairs - srcs}")
    # Part B: DFS parenthesis, one clock
    rng = random.Random(20261028)
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj_random(rng, n, p)  # Part A consumed this stream; Part B continues from here
    # Part B in the lab uses the SAME rng object after Part A, so regenerate Part A draws above, then B draws:
    viol = 0
    npairs = 0
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj = adj_random(rng, n, p)
        d: dict[int, int] = {}
        f: dict[int, int] = {}
        clock = [0]

        def visit(v: int) -> None:
            clock[0] += 1
            d[v] = clock[0]
            for u in adj[v]:
                if u not in d:
                    visit(u)
            clock[0] += 1
            f[v] = clock[0]

        for v in range(n):
            if v not in d:
                visit(v)
        for u in range(n):
            for v in range(u + 1, n):
                npairs += 1
                nested = (f[u] < d[v] or f[v] < d[u]) or (d[u] < d[v] and f[v] < f[u]) or (d[v] < d[u] and f[u] < f[v])
                viol += not nested
    say(f"L06 B: pairs {npairs}; violations {viol}")
    say(f"L06 D: 1438/40000: 40000/1438 = {40000 / 1438:.4f}; 1238/200 = {1238 / 200:.2f}; 2*619 = {2 * 619}; 200*200 = {200 * 200}; 200+1238 = {200 + 1238}")
    say(f"L06 M1: 1438*27 = {1438 * 27}; 40000 - {1438 * 27} = {40000 - 1438 * 27}")
    # Part D graph
    rng = random.Random(20261028 + 1000)
    adj = adj_random(rng, 200, 0.03)
    edges = sum(len(adj[v]) for v in adj) // 2
    dist = bfs_dist(adj, 0)
    say(f"L06 D: edges {edges}; reached {len(dist)}; degree sum {sum(len(adj[v]) for v in adj)}")
    # Part C weighted
    names = "sabc"
    adjc = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
    w = {(0, 1): 10, (0, 2): 1, (1, 2): 1, (1, 3): 1}
    import itertools

    def wt(path: list[int]) -> int:
        return sum(w[(min(a, b), max(a, b))] for a, b in itertools.pairwise(path))

    paths: dict[int, list[list[int]]] = {}

    def allp(v: int, path: list[int]) -> None:
        if v != 0 or len(path) == 1:
            pass
        for u in adjc[v]:
            if u in path:
                continue
            paths.setdefault(u, []).append(path + [u])
            allp(u, path + [u])

    allp(0, [0])
    for v in (1, 2, 3):
        cands = paths[v]
        best = min(cands, key=lambda q: (wt(q), len(q)))
        fewest = min(cands, key=lambda q: len(q))
        say(f"L06 C: to {names[v]}: fewest-hop simple path {''.join(names[x] for x in fewest)} hops {len(fewest)-1} weight {wt(fewest)}; lightest {''.join(names[x] for x in best)} hops {len(best)-1} weight {wt(best)}")


# ---------- L07 ----------
def lcs_len(x: str, y: str) -> int:
    m, n = len(x), len(y)
    t = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            t[i][j] = t[i - 1][j - 1] + 1 if x[i - 1] == y[j - 1] else max(t[i - 1][j], t[i][j - 1])
    return t[m][n]


def lcs_brute(x: str, y: str) -> int:
    best = 0
    for mask in range(1 << len(x)):
        s = [x[k] for k in range(len(x)) if mask >> k & 1]
        it = iter(y)
        if all(c in it for c in s):
            best = max(best, len(s))
    return best


class LCG:
    def __init__(self, seed: int) -> None:
        self.s = seed % (2**31)

    def draw(self, n: int) -> int:
        self.s = (1103515245 * self.s + 12345) % (2**31)
        return (self.s >> 16) % n


def l07() -> None:
    g = LCG(20261028)
    pairs = []
    for _ in range(30):
        m = 1 + g.draw(7)
        n = 1 + g.draw(7)
        x = "".join("ACGT"[g.draw(4)] for _ in range(m))
        y = "".join("ACGT"[g.draw(4)] for _ in range(n))
        pairs.append((x, y))
    lcs_ok = all(lcs_len(x, y) == lcs_brute(x, y) for x, y in pairs)
    say(f"L07 A: 30 LCS pairs, table == brute: {lcs_ok}")
    cases = []
    for _ in range(30):
        size = 2 + g.draw(3)
        chosen: set[int] = set()
        while len(chosen) < size:
            chosen.add(1 + g.draw(9))
        amount = g.draw(13)
        cases.append((tuple(sorted(chosen)), amount))

    def coin_table(d: tuple[int, ...], A: int) -> float:
        f = [0.0] + [math.inf] * A
        for a in range(1, A + 1):
            f[a] = min([1 + f[a - c] for c in d if c <= a] or [math.inf])
        return f[A]

    def coin_brute(d: tuple[int, ...], A: int) -> float:
        best = math.inf
        def go(k: int, rem: int, used: int) -> None:
            nonlocal best
            if k == len(d):
                if rem == 0:
                    best = min(best, used)
                return
            for cnt in range(rem // d[k] + 1):
                go(k + 1, rem - cnt * d[k], used + cnt)
        go(0, A, 0)
        return best

    impossible = sum(1 for d, A in cases if coin_table(d, A) == math.inf)
    say(f"L07 B: 30 coin cases; table == brute: {all(coin_table(d, A) == coin_brute(d, A) for d, A in cases)}; no-combination {impossible} of 30")
    # memo counts for ACGTACG / TGCATGC
    x, y = "ACGTACG", "TGCATGC"
    cache: dict[tuple[int, int], int] = {}
    calls = {"n": 0, "base": 0, "lookup": 0}

    def memo(i: int, j: int) -> int:
        calls["n"] += 1
        if i == 0 or j == 0:
            calls["base"] += 1
            return 0
        if (i, j) in cache:
            calls["lookup"] += 1
            return cache[(i, j)]
        v = memo(i - 1, j - 1) + 1 if x[i - 1] == y[j - 1] else max(memo(i - 1, j), memo(i, j - 1))
        cache[(i, j)] = v
        return v

    memo(len(x), len(y))
    naive = {"n": 0}

    def nv(i: int, j: int) -> int:
        naive["n"] += 1
        if i == 0 or j == 0:
            return 0
        if x[i - 1] == y[j - 1]:
            return nv(i - 1, j - 1) + 1
        return max(nv(i - 1, j), nv(i, j - 1))

    nv(len(x), len(y))
    say(f"L07 C: stored {len(cache)}; memo calls {calls['n']} = stored {len(cache)} + lookups {calls['lookup']} + base {calls['base']}; table cells {len(x) * len(y)}; no-memo calls {naive['n']}")
    # coins (1,3,4) amount 20 no-memo calls
    def cn(a: int, cnt: list[int]) -> None:
        cnt[0] += 1
        if a == 0:
            return
        for c in (1, 3, 4):
            if c <= a:
                cn(a - c, cnt)
    cnt = [0]
    cn(20, cnt)
    say(f"L07 C: coins (1,3,4) amount 20: no-memo calls {cnt[0]}; f(20) = {coin_table((1, 3, 4), 20)}")
    say(f"L07 E1: stored amounts for {{1,3,4}}, 20 = 20 (amounts 1..20)")
    say(f"L07 P3/Ex2.4: f(0..6) = {[coin_table((1, 3, 4), a) for a in range(7)]}; f(9) for {{2,5}} = {coin_table((2, 5), 9)}; f(7) {{2,5}} = {coin_table((2, 5), 7)}; f(4) = {coin_table((2, 5), 4)}")
    # smallest failing greedy amount for (1,3,4)
    def greedy(d: tuple[int, ...], a: int) -> int:
        rem, used = a, 0
        while rem:
            rem -= max(c for c in d if c <= rem)
            used += 1
        return used
    fail = next(a for a in range(1, 100) if greedy((1, 3, 4), a) != coin_table((1, 3, 4), a))
    say(f"L07: smallest amount where greedy fails for (1,3,4) = {fail}")
    # R2 for {1,c}: greedy optimal for c=2..30, a<=200
    ok = all(greedy((1, c), a) == coin_table((1, c), a) for c in range(2, 31) for a in range(0, 201))
    say(f"L07 R2: greedy optimal for {{1,c}}, c=2..30, a<=200: {ok}")
    say(f"L07 Prop4.2: 2^20+1 = {2**20 + 1}; 2^40 = {2**40}; bits(2^40) = {(2**40).bit_length()}; bits(1000) = {(1000).bit_length()}; 2^10 = {2**10}")
    say(f"L07 M3: (m+1)(n+1) = {6 * 9}, mn = {5 * 8}, boundary = {54 - 40}")
    say(f"L07 M1 ok: f(9) {{2,5}} = {coin_table((2, 5), 9)}")
    # LCS M2: AB vs BA
    say(f"L07 M2: LCS(AB,BA) = {lcs_len('AB', 'BA')}")
    say(f"L07 Prop 4.2 check: floor(log2 1000)+1 = {int(math.log2(1000)) + 1}")
    # 1/log, table entries for amount 1024
    say(f"L07 Q: entries for amount 1024 with 0 = {1024 + 1}")


# ---------- L08 ----------
def l08() -> None:
    g = LCG(20261029)
    MID, HALF, MAXQ, CANCEL = 10000, 20, 20, 25
    resting: list[dict] = []  # flat reference
    levels: dict[str, dict[int, list[dict]]] = {"B": {}, "S": {}}
    prices: dict[str, list[int]] = {"B": [], "S": []}
    orders_added = cancels = traded_msgs = executions = 0
    created = removed = 0
    queue_steps = 0
    searches = 0
    worst_cmp = 0
    trades_all: list[tuple] = []
    next_id = 1
    live_by_id: dict[int, dict] = {}

    def bsearch(lst: list[int], p: int) -> int:
        nonlocal searches, worst_cmp
        lo, hi, cmp = 0, len(lst), 0
        while lo < hi:
            mid = (lo + hi) // 2
            cmp += 1
            if lst[mid] < p:
                lo = mid + 1
            else:
                hi = mid
        searches += 1
        worst_cmp = max(worst_cmp, cmp)
        if cmp > len(lst).bit_length():
            raise AssertionError("bound")
        return lo

    for step in range(400):
        live_ids = sorted(o["id"] for o in resting)
        if live_ids and g.draw(100) < CANCEL:
            oid = live_ids[g.draw(len(live_ids))]
            o = live_by_id.pop(oid)
            o["q"] = 0
            resting = [r for r in resting if r["id"] != oid]
            side = o["s"]
            lev = levels[side][o["p"]]
            if all(x["q"] == 0 for x in lev):
                # level becomes empty -> remove (search + delete)
                idx = bsearch(prices[side], o["p"])
                del prices[side][idx]
                del levels[side][o["p"]]
                removed += 1
            cancels += 1
        else:
            side = "B" if g.draw(2) == 0 else "S"
            price = MID - HALF + g.draw(2 * HALF + 1)
            qty = 1 + g.draw(MAXQ)
            opp = "S" if side == "B" else "B"
            orders_added += 1
            remaining = qty
            this_trades = []
            # match by flat sorted scan
            cands = [r for r in resting if r["s"] == opp and ((side == "B" and r["p"] <= price) or (side == "S" and r["p"] >= price))]
            cands.sort(key=lambda r: (r["p"] if side == "B" else -r["p"], r["id"]))
            for r in cands:
                if remaining == 0:
                    break
                fill = min(remaining, r["q"])
                this_trades.append((r["p"], fill, r["id"], next_id))
                r["q"] -= fill
                remaining -= fill
                # queue-step accounting: the level's head passes dead entries only in FIFO order (see below)
            resting = [r for r in resting if r["q"] > 0]
            for r in list(live_by_id.values()):
                if r["q"] == 0:
                    live_by_id.pop(r["id"], None)
            if this_trades:
                traded_msgs += 1
                executions += len(this_trades)
            trades_all.extend(this_trades)
            if remaining > 0:
                newo = {"id": next_id, "s": side, "p": price, "q": remaining}
                resting.append(newo)
                live_by_id[next_id] = newo
                if price not in levels[side]:
                    idx = bsearch(prices[side], price)
                    prices[side].insert(idx, price)
                    levels[side][price] = []
                    created += 1
                levels[side][price].append(newo)
            next_id += 1
        # keep levels consistent with live orders (drop empty levels on fill)
        for side in ("B", "S"):
            for p in list(levels[side].keys()):
                if all(x["q"] == 0 for x in levels[side][p]):
                    idx = bsearch(prices[side], p)
                    del prices[side][idx]
                    del levels[side][p]
                    removed += 1
    bids = [r["p"] for r in resting if r["s"] == "B"]
    asks = [r["p"] for r in resting if r["s"] == "S"]
    say(f"L08 B: orders added {orders_added}; cancels {cancels}; traded messages {traded_msgs}; executions {executions}")
    say(f"L08 B: final best bid {max(bids) if bids else None}; best ask {min(asks) if asks else None}; resting {len(resting)}")
    say(f"L08 C(ref): levels created {created}; removed {removed}; levels left {created - removed}; binary searches {searches}; worst cmp {worst_cmp}")
    say(f"L08: 102/400 = {102 / 400 * 100:.1f}%; 102/398 = {102 / 398 * 100:.1f}%")


if __name__ == "__main__":
    l05()
    l06()
    l07()
    l08()
