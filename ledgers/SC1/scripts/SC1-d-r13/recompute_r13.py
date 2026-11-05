"""Independent recomputation of every number on the SC1 project page (round 13, verifier-written).

Uses algorithms different from the lab twins: Phi via math.erf, a dynamic programme over (position, running max)
for the walk counts instead of enumeration, a grid simulation written from the page text, and the page's own
exemplar arithmetic. Prints one line per check, with PASS or FAIL against the page value.
"""

from __future__ import annotations

import math
import random

FAILS: list[str] = []


def check(name: str, got: object, want: object, tol: float = 0.0) -> None:
    if isinstance(want, float) and isinstance(got, float):
        ok = abs(got - want) <= tol
    else:
        ok = got == want
    print(f"{'PASS' if ok else 'FAIL'} {name}: computed {got!r}, page {want!r}")
    if not ok:
        FAILS.append(name)


def Phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# --- instance (page section "Generated instances and the draw order") -------------------------------------------
rng = random.Random(1_000_003 * 0 + 54_321)
H = round(rng.uniform(0.25, 4.0), 3)
a = round(rng.uniform(0.25, 2.5), 3)
n_steps0 = rng.randint(4, 256)
N = rng.randint(400, min(800, 200_000 // n_steps0))
check("H", H, 2.083)
check("a", a, 2.474)
check("N", N, 487)
print(f"  instance n_steps (seed 0, not printed by labs) = {n_steps0}")

# --- continuous tail and P2 closed form ----------------------------------------------------------------------------
tail = math.erfc(a / math.sqrt(2.0 * H))
check("tail rounded 6", f"{tail:.6f}", "0.086497")
check("P2 erfc = 2(1-Phi(a/sqrt H))", abs(tail - 2.0 * (1.0 - Phi(a / math.sqrt(H)))) < 1e-15, True)


# --- Simpson: independent midpoint rule on 2 P(B_H >= a) -----------------------------------------------------------
def tail_midpoint(level: float, horizon: float, m: int = 200_000) -> float:
    top = level + 14.0 * math.sqrt(horizon)
    h = (top - level) / m
    s = 0.0
    for k in range(m):
        x = level + (k + 0.5) * h
        s += math.exp(-x * x / (2.0 * horizon)) / math.sqrt(2.0 * math.pi * horizon)
    return 2.0 * s * h


mid = tail_midpoint(a, H)
check("midpoint vs closed form within 1e-9", abs(mid - tail) < 1e-9, True)
print(f"  midpoint 2P(B_H>=a) = {mid!r}, closed form = {tail!r}, abs diff = {abs(mid - tail):.2e}")

# --- one-step estimate, the page's draw order ------------------------------------------------------------------------
r1 = random.Random(0)
ind = [1.0 if r1.gauss(0.0, math.sqrt(H)) >= a else 0.0 for _ in range(N)]
p1 = sum(ind) / N
sd1 = math.sqrt(sum((x - p1) ** 2 for x in ind) / (N - 1))
se1 = sd1 / math.sqrt(N)
check("one-step estimate 6dp", f"{p1:.6f}", "0.059548")
check("one-step se 6dp", f"{se1:.6f}", "0.010735")
check("one-step se closed form sqrt(p(1-p)/(N-1))", abs(se1 - math.sqrt(p1 * (1 - p1) / (N - 1))) < 1e-12, True)
target = tail / 2.0
target_se = math.sqrt(target * (1.0 - target) / N)
band = 5.0 * target_se + 1.0 / N
check("target 6dp", f"{target:.6f}", "0.043248")
check("target se 6dp", f"{target_se:.6f}", "0.009218")
check("band 6dp", f"{band:.6f}", "0.048142")
check("difference 6dp", f"{abs(p1 - target):.6f}", "0.016300")
check("inside band", abs(p1 - target) <= band, True)
check("difference over target se (page: 1.77)", f"{abs(p1 - target) / target_se:.2f}", "1.77")
check("difference over sample se (page: 1.52)", f"{abs(p1 - target) / se1:.2f}", "1.52")


# --- grid estimates: page's draw order, path by path, step by step, one fresh Random per grid -------------------------
def grid_hits(n: int) -> int:
    rr = random.Random(0)
    sd = math.sqrt(H / n)
    hits = 0
    for _ in range(N):
        pos = 0.0
        best = -math.inf
        for _k in range(n):
            pos += rr.gauss(0.0, sd)
            best = max(best, pos)
        if best >= a:
            hits += 1
    return hits


expected = {1: ("0.059548", "0.010735", "0.026948"), 4: ("0.049281", "0.009819", "0.037215"),
            16: ("0.065708", "0.011239", "0.020788"), 64: ("0.088296", "0.012870", "-0.001799"),
            256: ("0.082136", "0.012455", "0.004361")}
grid_p: dict[int, float] = {}
for n, (pe, se_pe, diff_pe) in expected.items():
    hits = grid_hits(n)
    p = hits / N
    grid_p[n] = p
    s = math.sqrt(N * p * (1 - p) / (N - 1)) / math.sqrt(N)
    check(f"grid n={n} hits", hits, {1: 29, 4: 24, 16: 32, 64: 43, 256: 40}[n])
    check(f"grid n={n} estimate", f"{p:.6f}", pe)
    check(f"grid n={n} se", f"{s:.6f}", se_pe)
    check(f"grid n={n} tail minus estimate", f"{tail - p:.6f}", diff_pe)
    check(f"grid n={n} within 5 se of tail (page hypothesis)", abs(tail - p) <= 5 * s, True)

# --- nested counts: same 256-step paths, coarse maxima on every 256/n-th point --------------------------------------
rr = random.Random(0)
sd256 = math.sqrt(H / 256)
fine_max: list[float] = []
coarse: dict[int, list[float]] = {64: [], 16: [], 4: [], 1: []}
strides = {64: 4, 16: 16, 4: 64, 1: 256}
for _ in range(N):
    pos = 0.0
    bf = -math.inf
    bc = {c: -math.inf for c in coarse}
    for k in range(1, 257):
        pos += rr.gauss(0.0, sd256)
        bf = max(bf, pos)
        for c, st in strides.items():
            if k % st == 0:
                bc[c] = max(bc[c], pos)
    fine_max.append(bf)
    for c in coarse:
        coarse[c].append(bc[c])
fine_count = sum(1 for m in fine_max if m >= a)
check("nested fine count", fine_count, 40)
for c, want in ((64, 35), (16, 29), (4, 27), (1, 22)):
    cnt = sum(1 for m in coarse[c] if m >= a)
    check(f"nested coarse {c} count", cnt, want)
    check(f"nested coarse {c} <= fine", cnt <= fine_count, True)
    check(f"nested coarse {c} <= fine on every path", all(cm <= fm for cm, fm in zip(coarse[c], fine_max)), True)

# --- walk counts by dynamic programme over (position, running max) ----------------------------------------------


def walk_dp(n: int, level: int) -> tuple[int, int]:
    """Return (walks with max >= level, walks ending >= level) via DP over (position, max) states."""
    # state: (pos, max) -> count, starting at (0, 0)
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, mx), c in states.items():
            for step in (1, -1):
                np_ = pos + step
                key = (np_, max(mx, np_))
                nxt[key] = nxt.get(key, 0) + c
        states = nxt
    total_max = sum(c for (pos, mx), c in states.items() if mx >= level)
    total_end = sum(c for (pos, mx), c in states.items() if pos >= level)
    return total_max, total_end


mx6, end6 = walk_dp(6, 2)
end6_plus = walk_dp(6, 3)[1]
check("lab2 n=6 a=2 max count", mx6, 29)
check("lab2 n=6 a=2 end >= 2", end6, 22)
check("lab2 n=6 a=2 end >= 3", end6_plus, 7)
check("lab2 identity", mx6 == end6 + end6_plus, True)
mx12, end12 = walk_dp(12, 3)
end12_4 = walk_dp(12, 4)[1]
check("walk n=12 a=3 max count", mx12, 1588)
check("walk n=12 a=3 end >= 3", end12, 794)
check("walk n=12 end >= 4 (page: also 794)", end12_4, 794)
check("walk identity 1588 = 794 + 794", mx12 == end12 + end12_4, True)
check("walk total 2**12", 2**12, 4096)

# --- identity sweep for the page's claim 'every n up to 12, every a' is not claimed here; check a range anyway ----
bad = [(n, lv) for n in range(1, 13) for lv in range(1, n + 2)
       if walk_dp(n, lv)[0] != walk_dp(n, lv)[1] + walk_dp(n, lv + 1)[1]]
check("walk identity max = end>=a + end>=a+1, n<=12, a<=n+1", bad, [])

# --- P2 closed form over a sweep ---------------------------------------------------------------------------------
worst = 0.0
for i in range(1, 400):
    for j in range(1, 60):
        lv = i / 100.0
        tt = j / 20.0
        worst = max(worst, abs(math.erfc(lv / math.sqrt(2 * tt)) - 2 * (1 - Phi(lv / math.sqrt(tt)))))
print(f"  P2 sweep max |erfc - 2(1-Phi)| = {worst:.3e}")
check("P2 closed form sweep <= 1e-14", worst <= 1e-14, True)

# --- hours arithmetic ----------------------------------------------------------------------------------------------
check("hours 2+3+10+8+3+2", 2 + 3 + 10 + 8 + 3 + 2, 28)
check("lessons 8 x 9 + 28 = 100", 8 * 9 + 28, 100)

print()
print("FAILS:", FAILS if FAILS else "none")
