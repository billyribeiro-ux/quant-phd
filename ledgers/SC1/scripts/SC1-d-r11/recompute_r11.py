#!/usr/bin/env python3
"""Independent recomputation of every number the SC1 project page prints or quotes (seed 0).

Written by the round-11 verifier from the page's stated definitions, not from the lab code. Run from anywhere:
    .venv/bin/python ledgers/SC1/scripts/SC1-d-r11/recompute_r11.py
"""

from __future__ import annotations

import math
import random
from functools import lru_cache


def instance(seed: int) -> dict[str, float | int]:
    rng = random.Random(1_000_003 * seed + 54_321)
    h = round(rng.uniform(0.25, 4.0), 3)
    a = round(rng.uniform(0.25, 2.5), 3)
    n = rng.randint(4, 256)
    big_n = rng.randint(400, min(800, 200_000 // n))
    return {"H": h, "a": a, "n_steps": n, "N": big_n}


def std_normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def tail(a: float, h: float) -> float:
    return math.erfc(a / math.sqrt(2.0 * h))


def simpson(a: float, h: float, m: int = 4000) -> float:
    top = a + 12.0 * math.sqrt(h)
    step = (top - a) / m

    def dens(x: float) -> float:
        return math.exp(-x * x / (2.0 * h)) / math.sqrt(2.0 * math.pi * h)

    s = dens(a) + dens(top)
    for k in range(1, m):
        s += (4.0 if k % 2 else 2.0) * dens(a + k * step)
    return 2.0 * s * step / 3.0


def explicit_paths(seed: int, big_n: int, h: float, n: int) -> list[list[float]]:
    rng = random.Random(seed)
    sd = math.sqrt(h / n)
    out = []
    for _ in range(big_n):
        x = 0.0
        path = []
        for _ in range(n):
            x += rng.gauss(0.0, sd)
            path.append(x)
        out.append(path)
    return out


def estimate_se(hits: int, big_n: int) -> tuple[float, float]:
    p = hits / big_n
    # sample variance of 0/1 indicators with divisor N - 1 is N p (1 - p) / (N - 1)
    var = big_n * p * (1.0 - p) / (big_n - 1)
    return p, math.sqrt(var) / math.sqrt(big_n)


@lru_cache(maxsize=None)
def walk_dp(n: int, a: int) -> tuple[int, int]:
    """Counts by dynamic programming over (position, running maximum capped at a), independent of enumeration."""
    # state: (position, max_so_far_capped_at_a) -> number of walks; start at position 0, max 0
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = {}
        for (pos, top), w in states.items():
            for step in (1, -1):
                p2 = pos + step
                t2 = min(max(top, p2), a)
                nxt[(p2, t2)] = nxt.get((p2, t2), 0) + w
        states = nxt
    max_hits = sum(w for (pos, top), w in states.items() if top >= a)
    end_hits = sum(w for (pos, top), w in states.items() if pos >= a)
    return max_hits, end_hits


def main() -> None:
    inst = instance(0)
    h, a, n_steps, big_n = inst["H"], inst["a"], inst["n_steps"], inst["N"]
    print(f"instance seed 0: H={h} a={a} N={big_n} n_steps={n_steps}")
    t = tail(a, h)
    q = simpson(a, h)
    print(f"continuous tail erfc(a/sqrt(2H)) = {t:.6f}  (unrounded {t!r})")
    print(f"simpson 2P(B_H>=a) = {q:.6f}  |diff| = {abs(q - t):.2e}  (unrounded diff {abs(q - t)!r})")
    # identity erfc(a/sqrt(2t)) = 2(1 - Phi(a/sqrt t)) on the instance and on a grid of values
    worst = 0.0
    for tt in (0.1, 0.5, 1.0, h, 2.5, 4.0):
        for aa in (0.25, 1.0, 2.474):
            worst = max(worst, abs(math.erfc(aa / math.sqrt(2 * tt)) - 2 * (1 - std_normal_cdf(aa / math.sqrt(tt)))))
    print(f"max |erfc(a/sqrt(2t)) - 2(1-Phi(a/sqrt t))| over grid = {worst:.2e}")

    # one-step (grid of 1 step) estimate on the 1-step draws path by path
    paths1 = explicit_paths(0, big_n, h, 1)
    hits1 = sum(1 for p in paths1 if max(p) >= a)
    est1, se1 = estimate_se(hits1, big_n)
    target = t / 2.0
    target_se = math.sqrt(target * (1 - target) / big_n)
    band = 5 * target_se + 1 / big_n
    print(f"one step: hits {hits1} estimate {est1:.6f} se {se1:.6f}")
    print(f"target {target:.6f} target_se {target_se:.6f} band {band:.6f} |est-target| {abs(est1 - target):.6f}")
    print(f"inside band {abs(est1 - target) <= band}")
    print(f"tail - estimate (printed in Lab 3 row 1) = {t - est1:.6f}")
    print(f"ratio (est-target)/se_sample = {(est1 - target) / se1:.4f}; /target_se = {(est1 - target) / target_se:.4f}")
    print(f"one-step bias tail/2 = {target:.6f}; printed minus bias = {(t - est1) - target:.6f}")

    # grids on separate paths, as Lab 3 draws them
    for n in (1, 4, 16, 64, 256):
        ps = explicit_paths(0, big_n, h, n)
        hits = sum(1 for p in ps if max(p) >= a)
        est, se = estimate_se(hits, big_n)
        print(f"grid n={n:3d}: hits {hits:3d} est {est:.6f} se {se:.6f} tail-est {t - est:.6f} "
              f"5se {5 * se:.6f} within5se {abs(t - est) <= 5 * se}")
    print(f"64-step: est - tail = {-(t - estimate_se(sum(1 for p in explicit_paths(0, big_n, h, 64) if max(p) >= a), big_n)[0]):.6f}")

    # nested on the 256-step paths
    fine_paths = explicit_paths(0, big_n, h, 256)
    fine = sum(1 for p in fine_paths if max(p) >= a)
    print(f"nested fine count (256) = {fine}")
    for coarse_n, stride in ((64, 4), (16, 16), (4, 64), (1, 256)):
        cnt = sum(1 for p in fine_paths if max(p[stride - 1 :: stride]) >= a)
        print(f"nested coarse n={coarse_n} count {cnt}  at most fine: {cnt <= fine}")

    # walks
    for n, aa in ((12, 3), (6, 2), (6, 3)):
        mh, eh = walk_dp(n, aa)
        print(f"walk n={n} a={aa}: maximum>=a {mh}  ending>=a {eh}  (dp)")
    print(f"walk identity n=6 a=2: dp max {walk_dp(6, 2)[0]} == end(2)+end(3) {walk_dp(6, 2)[1] + walk_dp(6, 3)[1]}")

    # quoted ratios in the prose
    print(f"1.52 = 0.016300/0.010735 -> {0.016300 / 0.010735:.4f}")
    print(f"1.77 = 0.016300/0.009218 -> {0.016300 / 0.009218:.4f}")
    print(f"0.14 = 0.001799/0.012870 -> {0.001799 / 0.012870:.4f}")
    print(f"half tail 0.043248 check: tail/2 = {t / 2:.6f}")
    print(f"srw 41 endpoint identity check (small n=5 a=1): {walk_dp(5, 1)[1]} == 2**4 = {2 ** 4}")


if __name__ == "__main__":
    main()
