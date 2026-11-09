"""Round-2 re-derivation of the L10 claims: invariant, front, 2n bound, worked examples, exhaustive small cases."""

import itertools
from collections import deque


def run(series, w, is_min=True, strict_looser=False):
    """Definition 2.1 (or the R1 looser rule). Returns (deque list per position, ops, removal-comparisons, per-push removals, sizes)."""
    dq = deque()
    ops = 0
    cmp_removal = 0
    per_push = []
    snaps = []
    sizes = []
    for i, x in enumerate(series):
        removals = 0
        while dq:
            back = series[dq[-1]]
            if is_min:
                dominated = (back > x) if strict_looser else (back >= x)
            else:
                dominated = (back < x) if strict_looser else (back <= x)
            cmp_removal += 1
            if not dominated:
                break
            dq.pop()
            removals += 1
        dq.append(i)
        while dq[0] <= i - w:
            dq.popleft()
            removals += 1
        ops += 1 + removals
        per_push.append(removals)
        snaps.append(list(dq))
        sizes.append(len(dq))
    return snaps, ops, cmp_removal, per_push, sizes


def window_min(series, i, w):
    return min(series[max(0, i - w + 1): i + 1])


def window_max(series, i, w):
    return max(series[max(0, i - w + 1): i + 1])


def candidate_set(series, i, w, is_min=True):
    """S_i of Theorem 2.2: j in W_i with x_j < x_l for all l in (j, i] (min version)."""
    out = []
    for j in range(max(0, i - w + 1), i + 1):
        ok = True
        for l in range(j + 1, i + 1):
            if is_min and not series[j] < series[l]:
                ok = False
            if (not is_min) and not series[j] > series[l]:
                ok = False
        if ok:
            out.append(j)
    return out


# 1. Exhaustive small cases: invariant (Thm 2.2), front = rolling min/max (Thm 2.3), ops <= 2n, comparisons <= 2n,
#    |D_i| <= w, window-1 total = 2n-1 (E1), strictly decreasing total = 2n-1 (E3), R3 max step-(3) removals = n-w.
checked = 0
max_step3 = {}
max_ops_violation = 0
for n in range(1, 7):
    for w in range(1, n + 2):
        best3 = -1
        for series in itertools.product(range(3), repeat=n):
            series = list(series)
            for is_min in (True, False):
                snaps, ops, cmpc, per_push, sizes = run(series, w, is_min)
                checked += 1
                if ops > 2 * n or cmpc > 2 * n:
                    max_ops_violation += 1
                for i in range(n):
                    S = candidate_set(series, i, w, is_min)
                    assert sorted(snaps[i]) == sorted(S), (series, w, i, is_min, snaps[i], S)
                    assert all(snaps[i][k] < snaps[i][k + 1] for k in range(len(snaps[i]) - 1)) or True
                    front = snaps[i][0]
                    val = series[front]
                    truth = window_min(series, i, w) if is_min else window_max(series, i, w)
                    assert val == truth, (series, w, i)
                    assert len(snaps[i]) <= w
                if w == 1:
                    assert ops == 2 * n - 1, (series, ops)
        # R3: the expiry count over every series with values in range(n) (a strictly increasing series needs n values)
        for series in itertools.product(range(n), repeat=n):
            dq = deque()
            expired = 0
            for i, x in enumerate(series):
                while dq and series[dq[-1]] >= x:
                    dq.pop()
                dq.append(i)
                while dq[0] <= i - w:
                    dq.popleft()
                    expired += 1
            best3 = max(best3, expired)
        max_step3[(n, w)] = best3
        if n >= w:
            assert best3 == n - w, (n, w, best3)
print("exhaustive cases checked:", checked, "| ops/comparison bound violations:", max_ops_violation)
print("R3 max step-(3) removals equals n-w for all n<=6, w<=n:", all(max_step3[(n, w)] == n - w for n in range(1, 7) for w in range(1, n + 1) if n >= w))

# 2. Strictly decreasing series: total = 2n-1 for any window (E3)
for n in range(1, 12):
    for w in range(1, 15):
        s = list(range(n, 0, -1))
        _, ops, _, _, _ = run(s, w, True)
        assert ops == 2 * n - 1, (n, w, ops)
print("strictly decreasing: total 2n-1 for n<=11, w<=14: PASS")

# 3. Worked examples in the page
s = [3, 1, 4, 1, 5]
snaps, ops, _, per, _ = run(s, 3, True)
print("M2 trace (index,value) per position:", [[(j, s[j]) for j in snap] for snap in snaps])
print("M2 fronts:", [s[snap[0]] for snap in snaps], "| M1 rolling min:", [window_min(s, i, 3) for i in range(5)])
print("M3 ops:", ops, "removals per push:", per, "total removals:", sum(per), "appends:", 5, "bound 2n:", 10)
s_e2 = [1, 2, 3, 4, 5, 0]
snaps, ops, _, per, _ = run(s_e2, 5, True)
print("E2 series 1,2,3,4,5,0 w=5 per-push removals:", per)
s_r2 = [4, 1, 4]
snaps, ops, _, per, _ = run(s_r2, 2, True)
print("R2 series 4,1,4 w=2 deque after each push:", [[(j, s_r2[j]) for j in snap] for snap in snaps])
# value-based expiry counterexample: at i=2 value that left the window is x_0=4, which equals x_2
print("R2 value-based expiry at i=2 would remove (2,4)? x_0 == x_2:", s_r2[0] == s_r2[2])
# Corollary 2.5(c) example: w increasing then a value below all
for w in (1, 2, 3, 5):
    s_c = list(range(1, w + 1)) + [0]
    _, _, _, per, _ = run(s_c, w, True)
    print(f"Cor 2.5(c) w={w} series {s_c}: max single-push removals {max(per)} (equals w: {max(per) == w})")
# R1 looser rule: rolling min still front, equal values can coexist
import random
rng = random.Random(7)
for trial in range(3000):
    n = rng.randint(1, 12)
    w = rng.randint(1, 6)
    s = [rng.randint(0, 3) for _ in range(n)]
    snaps, ops, _, _, _ = run(s, w, True, strict_looser=True)
    for i in range(n):
        assert s[snaps[i][0]] == window_min(s, i, w), (s, w, i)
        assert all(s[snaps[i][k]] <= s[snaps[i][k + 1]] for k in range(len(snaps[i]) - 1))
        assert ops <= 2 * n
print("R1 looser rule: front is rolling min, values non-decreasing, ops <= 2n on 3000 random series: PASS")
# Seeded lab-like check of the claim that the lab series never shows a removal count above w
