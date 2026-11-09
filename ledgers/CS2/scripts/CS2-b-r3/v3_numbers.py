"""Independent recomputation of every number in the CS2 slice (L05-L08) prose and lab expected blocks.

Usage: python -I -W error v3_numbers.py   (standard library only; writes nothing)
Written from the definitions in the lesson text, not from the lab twins' code.
"""

import math
import random
from collections import deque
from itertools import combinations, permutations

PHI = (1 + math.sqrt(5)) / 2


# ---------- L05: AVL tree, independent of the twin's code ----------
class T:
    __slots__ = ("k", "l", "r", "h")

    def __init__(self, k):
        self.k, self.l, self.r, self.h = k, None, None, 1


def hh(t):
    return t.h if t else 0


def fix(t):
    t.h = 1 + max(hh(t.l), hh(t.r))


def bf(t):
    return hh(t.l) - hh(t.r)


def rot_r(y, c):
    x = y.l
    y.l, x.r = x.r, y
    fix(y)
    fix(x)
    c["rot"] += 1
    return x


def rot_l(x, c):
    y = x.r
    x.r, y.l = y.l, x
    fix(x)
    fix(y)
    c["rot"] += 1
    return y


def insert(t, k, c):
    if t is None:
        return T(k)
    if k < t.k:
        t.l = insert(t.l, k, c)
    else:
        t.r = insert(t.r, k, c)
    fix(t)
    b = bf(t)
    if b > 1:
        if bf(t.l) < 0:
            c["LR"] += 1
            t.l = rot_l(t.l, c)
        else:
            c["LL"] += 1
        return rot_r(t, c)
    if b < -1:
        if bf(t.r) > 0:
            c["RL"] += 1
            t.r = rot_r(t.r, c)
        else:
            c["RR"] += 1
        return rot_l(t, c)
    return t


def inorder(t, out):
    if t:
        inorder(t.l, out)
        out.append(t.k)
        inorder(t.r, out)
    return out


def ok_avl(t):
    if t is None:
        return True, 0
    a, hl = ok_avl(t.l)
    b, hr = ok_avl(t.r)
    h = 1 + max(hl, hr)
    return a and b and abs(hl - hr) <= 1 and t.h == h, h


def logphi(n):
    return math.log(n) / math.log(PHI)


def l05():
    out = {}
    rng = random.Random(20261028)
    keys = rng.sample(range(1, 1_000_000), 500)
    root = None
    c = {"rot": 0, "LL": 0, "RR": 0, "LR": 0, "RL": 0}
    no_rot = 0
    maxcalls = 0
    every = True
    for i, k in enumerate(keys, 1):
        before = c["rot"]
        root = insert(root, k, c)
        d = c["rot"] - before
        no_rot += d == 0
        maxcalls = max(maxcalls, d)
        every = every and ok_avl(root)[0] and bool(inorder(root, [])) and inorder(root, []) == sorted(keys[:i])
        every = every and hh(root) <= logphi(i + 1)
    out["L05_every_check"] = every
    out["L05_final_height"] = hh(root)
    out["L05_log_phi_501"] = round(logphi(501), 4)
    out["L05_rot_total"] = c["rot"]
    out["L05_kinds"] = (c["LL"], c["RR"], c["LR"], c["RL"])
    out["L05_check_identity"] = c["LL"] + c["RR"] + 2 * (c["LR"] + c["RL"]) == c["rot"]
    out["L05_no_rot_inserts"] = (no_rot, len(keys), round(100 * no_rot / len(keys), 1))
    out["L05_max_calls_one_insert"] = maxcalls
    # Part B: sorted 1..64
    plain = None

    def pins(t, k):
        if t is None:
            return T(k)
        if k < t.k:
            t.l = pins(t.l, k)
        else:
            t.r = pins(t.r, k)
        return t

    def ph(t):
        return 0 if t is None else 1 + max(ph(t.l), ph(t.r))

    cc = {"rot": 0, "LL": 0, "RR": 0, "LR": 0, "RL": 0}
    avl = None
    for k in range(1, 65):
        plain = pins(plain, k)
        avl = insert(avl, k, cc)
    out["L05_plain_height_1_64"] = ph(plain)
    out["L05_avl_height_1_64"] = hh(avl)
    out["L05_log_phi_65"] = round(logphi(65), 4)
    # Part C: N(h) and phi^h
    N = [0, 1]
    for h in range(2, 14):
        N.append(1 + N[h - 1] + N[h - 2])
    out["L05_N_0_12"] = N[:13]
    out["L05_M_ge_phi"] = all(N[h] + 1 >= PHI**h for h in range(1, 13))
    out["L05_N_h_plus_1_ge_phi_h_check_h13"] = N[13] + 1 >= PHI**13
    out["L05_N_nondecreasing"] = all(N[h] - N[h - 1] >= 1 for h in range(2, 14)) and N[1] >= N[0]
    out["L05_inv_log2phi"] = round(1 / math.log2(PHI), 6)
    out["L05_log_phi_3"] = round(logphi(3), 2)
    out["L05_log_phi_8"] = round(logphi(8), 2)
    out["L05_log_phi_377"] = round(logphi(377), 2)
    out["L05_ln377"] = round(math.log(377), 3)
    out["L05_ln_phi"] = round(math.log(PHI), 4)
    out["L05_two_node_height"] = 2
    out["L05_phi_identity_ok"] = abs(PHI**2 - (PHI + 1)) < 1e-12 and PHI < 2
    out["L05_M2_root_after_insert_1_2_3"] = None
    out["L05_E2_log2_64"] = math.log2(64)
    return out


# ---------- L06: graphs ----------
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
    dist = {s: 0}
    q = deque([s])
    insp = 0
    order = []
    while q:
        v = q.popleft()
        order.append(v)
        for u in adj[v]:
            insp += 1
            if u not in dist:
                dist[u] = dist[v] + 1
                q.append(u)
    return dist, order, insp


def brute(adj, s):
    best = {s: 0}
    path = [s]

    def go(v, L):
        for u in adj[v]:
            if u in path:
                continue
            if u not in best or L + 1 < best[u]:
                best[u] = L + 1
            path.append(u)
            go(u, L + 1)
            path.pop()

    go(s, 0)
    return best


def dfs_times(adj):
    d, f, clock = {}, {}, [0]

    def visit(v):
        clock[0] += 1
        d[v] = clock[0]
        for u in adj[v]:
            if u not in d:
                visit(u)
        clock[0] += 1
        f[v] = clock[0]

    for v in sorted(adj):
        if v not in d:
            visit(v)
    return d, f


def l06():
    out = {}
    rng = random.Random(20261028)
    srcs = reach = unreach = mism = 0
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj = rgraph(rng, n, p)
        for s in range(n):
            srcs += 1
            dist, _, _ = bfs(adj, s)
            reach += len(dist)
            unreach += n - len(dist)
            mism += dist != brute(adj, s)
    out["L06_sources"] = srcs
    out["L06_reachable_pairs_incl_self"] = reach
    out["L06_unreachable_pairs"] = unreach
    out["L06_mismatches"] = mism
    out["L06_positive_pairs"] = reach - srcs
    pairs = viol = 0
    for k in range(40):
        n = 3 + k % 5
        p = 0.2 + 0.1 * (k % 4)
        adj = rgraph(rng, n, p)
        d, f = dfs_times(adj)
        for u, v in combinations(range(n), 2):
            pairs += 1
            nested = (f[u] < d[v] or f[v] < d[u]) or (d[u] < d[v] and f[v] < f[u]) or (d[v] < d[u] and f[u] < f[v])
            viol += not nested
    out["L06_dfs_pairs"] = pairs
    out["L06_dfs_violations"] = viol
    # Part C weighted graph by hand (s=0,a=1,b=2,c=3)
    w = {frozenset((0, 1)): 10, frozenset((0, 2)): 1, frozenset((1, 2)): 1, frozenset((1, 3)): 1}
    adjc = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1], 3: [1]}
    res = {}
    for v in (1, 2, 3):
        best = None
        for perm_len in range(0, 4):
            for mid in permutations([1, 2, 3], perm_len):
                seq = [0, *mid]
                if seq[-1] != v and v not in seq:
                    continue
                if seq[-1] != v:
                    continue
                if len(set(seq)) != len(seq):
                    continue
                if any(frozenset((seq[i], seq[i + 1])) not in w for i in range(len(seq) - 1)):
                    continue
                tot = sum(w[frozenset((seq[i], seq[i + 1]))] for i in range(len(seq) - 1))
                key = (tot, len(seq) - 1)
                if best is None or key < best[0]:
                    best = (key, seq)
        res[v] = best
    out["L06_partC_lightest"] = {v: (res[v][0], res[v][1]) for v in res}
    # Part D: 200 vertices
    rng2 = random.Random(20261028 + 1000)
    adj = rgraph(rng2, 200, 0.03)
    edges = sum(len(adj[v]) for v in adj) // 2
    dist, order, insp = bfs(adj, 0)
    out["L06_D_edges"] = edges
    out["L06_D_reached"] = len(dist)
    out["L06_D_inspections"] = insp
    out["L06_D_equals_2E"] = insp == 2 * edges
    out["L06_D_matrix_reads"] = len(order) * 200
    out["L06_D_list_work"] = len(dist) + insp
    out["L06_E2_ratio"] = round(40000 / 1438, 4)
    out["L06_E2_check"] = (1438 * 27, 40000 - 1438 * 27, round(1174 / 1438, 4))
    out["L06_E3_avg_degree"] = round(2 * edges / 200, 2)
    return out


# ---------- L07: DP ----------
def lcs_memo(x, y):
    cache, calls, lookups, base = {}, [0], [0], [0]

    def go(i, j):
        calls[0] += 1
        if i == 0 or j == 0:
            base[0] += 1
            return 0
        if (i, j) in cache:
            lookups[0] += 1
            return cache[(i, j)]
        v = go(i - 1, j - 1) + 1 if x[i - 1] == y[j - 1] else max(go(i - 1, j), go(i, j - 1))
        cache[(i, j)] = v
        return v

    v = go(len(x), len(y))
    return v, len(cache), calls[0], lookups[0], base[0]


def lcs_naive(x, y):
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


def lcs_brute(x, y):
    best = 0
    for mask in range(1 << len(x)):
        s = [x[k] for k in range(len(x)) if mask >> k & 1]
        it = iter(y)
        if all(ch in it for ch in s):
            best = max(best, len(s))
    return best


def coins_f(D, A):
    f = [0] + [None] * A
    for a in range(1, A + 1):
        cand = [1 + f[a - c] for c in D if c <= a and f[a - c] is not None]
        f[a] = min(cand) if cand else None
    return f


def coins_memo(D, A):
    cache, calls, lookups = {}, [0], [0]

    def best(a):
        calls[0] += 1
        if a == 0:
            return 0
        if a in cache:
            lookups[0] += 1
            return cache[a]
        cand = [1 + s for c in D if c <= a for s in [best(a - c)] if s is not None]
        cache[a] = min(cand) if cand else None
        return cache[a]

    return best(A), len(cache), calls[0], lookups[0]


def coins_naive(D, A):
    calls = [0]

    def best(a):
        calls[0] += 1
        if a == 0:
            return 0
        cand = [1 + s for c in D if c <= a for s in [best(a - c)] if s is not None]
        return min(cand) if cand else None

    best(A)
    return calls[0]


def greedy(D, A):
    r, used = A, 0
    while r > 0:
        fits = [c for c in D if c <= r]
        if not fits:
            return None
        r -= max(fits)
        used += 1
    return used


def coin_exhaustive(D, A):
    best = None
    for counts in __import__("itertools").product(*(range(A // c + 1) for c in D)):
        if sum(k * c for k, c in zip(counts, D)) == A:
            n = sum(counts)
            best = n if best is None or n < best else best
    return best


def l07():
    out = {}
    v, stored, calls, lookups, base = lcs_memo("ACGTACG", "TGCATGC")
    out["L07_LCS_ACGTACG_TGCATGC"] = {
        "lcs": v,
        "memo_stored": stored,
        "memo_calls": calls,
        "lookups": lookups,
        "base_calls": base,
        "lookup_plus_base_plus_stored": stored + lookups + base,
        "no_memo_calls": lcs_naive("ACGTACG", "TGCATGC"),
        "table_cells": 7 * 7,
    }
    out["L07_AB_BA_lcs"] = lcs_memo("AB", "BA")[0]
    out["L07_AB_BA_brute"] = lcs_brute("AB", "BA")
    out["L07_f_0_6_134"] = coins_f((1, 3, 4), 6)
    out["L07_f_20_134"] = coins_f((1, 3, 4), 20)[20]
    out["L07_coin_memo_20"] = coins_memo((1, 3, 4), 20)
    out["L07_coin_naive_20"] = coins_naive((1, 3, 4), 20)
    out["L07_greedy_6_134"] = greedy((1, 3, 4), 6)
    out["L07_f9_25"] = coins_f((2, 5), 9)[9]
    out["L07_f7_25"] = coins_f((2, 5), 9)[7]
    out["L07_f4_25"] = coins_f((2, 5), 9)[4]
    out["L07_f5_1"] = coins_f((1,), 5)[5]
    out["L07_memo_touch_coin_1_A3"] = coins_memo((1,), 3)[1:]
    out["L07_first_greedy_fail_134"] = next(a for a in range(1, 40) if greedy((1, 3, 4), a) != coins_f((1, 3, 4), a)[a])
    bad = 0
    for c in range(2, 31):
        f = coins_f((1, c), 200)
        for a in range(0, 201):
            if greedy((1, c), a) != f[a]:
                bad += 1
    out["L07_greedy_1c_mismatches_c2_30_a0_200"] = bad
    out["L07_2_pow_20_plus_1"] = 2**20 + 1
    out["L07_2_pow_40"] = 2**40
    out["L07_bits_2_pow_40"] = (2**40).bit_length()
    out["L07_bits_1000"] = (1000).bit_length()
    out["L07_mn_table_6x9"] = (5 + 1) * (8 + 1), 5 * 8, (5 + 1) * (8 + 1) - 5 * 8
    out["L07_coin_amount_1024_entries"] = 1024 + 1
    out["L07_2^40_plus_1_gt_1e12"] = 2**40 + 1 > 10**12
    out["L07_coin_1_3_4_amount_stored_E1_check"] = len(coins_memo((1, 3, 4), 20)) and coins_memo((1, 3, 4), 20)[1]
    # brute-force check of the 1,3,4 coin example against exhaustive counts
    out["L07_exhaustive_134_6"] = coin_exhaustive((1, 3, 4), 6)
    return out


# ---------- L08: order book, flat reference written independently ----------
class Lcg:
    def __init__(self, s):
        self.s = s % 2**31

    def below(self, n):
        self.s = (1103515245 * self.s + 12345) % 2**31
        return (self.s >> 16) % n


def l08():
    out = {}
    gen = Lcg(20261029)
    orders = []  # resting: [oid, side, price, qty]
    next_id = 1
    cancels = 0
    traded_msgs = 0
    executions = 0
    steps_no_live = []
    steps_with_live = 0
    cancel_draws_from_live = 0
    bests = []
    for step in range(400):
        live_before = sorted(o[0] for o in orders)
        if not live_before:
            steps_no_live.append(step)
        if live_before:
            steps_with_live += 1
        if live_before and gen.below(100) < 25:
            oid = live_before[gen.below(len(live_before))]
            orders = [o for o in orders if o[0] != oid]
            cancels += 1
        else:
            side = "B" if gen.below(2) == 0 else "S"
            price = 10000 - 20 + gen.below(41)
            qty = 1 + gen.below(20)
            opp = "S" if side == "B" else "B"
            if side == "B":
                cand = sorted([o for o in orders if o[1] == opp and o[2] <= price], key=lambda o: (o[2], o[0]))
            else:
                cand = sorted([o for o in orders if o[1] == opp and o[2] >= price], key=lambda o: (-o[2], o[0]))
            rem = qty
            n_tr = 0
            for o in cand:
                if rem == 0:
                    break
                f = min(rem, o[3])
                o[3] -= f
                rem -= f
                n_tr += 1
            executions += n_tr
            traded_msgs += n_tr > 0
            orders = [o for o in orders if o[3] > 0]
            if rem > 0:
                orders.append([next_id, side, price, rem])
            next_id += 1
        bids = [o[2] for o in orders if o[1] == "B"]
        asks = [o[2] for o in orders if o[1] == "S"]
        bests.append((max(bids) if bids else None, min(asks) if asks else None))
    out["L08_steps_no_live_order"] = steps_no_live
    out["L08_steps_with_live_order"] = steps_with_live
    out["L08_orders_added"] = next_id - 1
    out["L08_cancels"] = cancels
    out["L08_traded_messages"] = traded_msgs
    out["L08_executions"] = executions
    out["L08_cancel_share_400"] = round(100 * cancels / 400, 1)
    out["L08_cancel_share_398"] = round(100 * cancels / steps_with_live, 1)
    out["L08_final_best_bid_ask_resting"] = (bests[-1], len(orders))
    return out


if __name__ == "__main__":
    for name, fn in (("L05", l05), ("L06", l06), ("L07", l07), ("L08", l08)):
        print(f"== {name}")
        for key, value in fn().items():
            print(f"{key} = {value}")
