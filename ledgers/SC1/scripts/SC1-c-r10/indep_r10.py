"""Independent recomputation for SC1 slice c, round 10 (L07 and L08 numbers).

Written by the verifier from the prose and the twins' seeds only. It does not import the twins. Algorithms differ
from the twins: killed-walk dynamic programme with exact integers and Fractions, explicit loops for the seeded draws.

Usage: python3 -I ledgers/SC1/scripts/SC1-c-r10/indep_r10.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction


def tail_dp(n: int, level: int) -> int:
    """Number of length-n walks (S_0 = 0, steps +-1) whose maximum over 0..n is at least level, by killing at level."""
    if level <= 0:
        return 2**n
    alive: dict[int, int] = {0: 1}  # positions strictly below level, with counts of walks that never reached level
    for _ in range(n):
        nxt: dict[int, int] = {}
        for pos, c in alive.items():
            for step in (1, -1):
                q = pos + step
                if q >= level:
                    continue
                nxt[q] = nxt.get(q, 0) + c
        alive = nxt
    return 2**n - sum(alive.values())


def part_a_exact() -> None:
    print("A-DP: tails P(M_N >= m), m = isqrt(N)")
    for n in (4, 16, 64, 256, 1024):
        m = math.isqrt(n)
        exact = Fraction(tail_dp(n, m), 2**n)
        print(f"A-DP: N={n} m={m} tail={float(exact):.10f} count={tail_dp(n, m)}")
    print("A-DP: N=16 m=4 count of walks with max>=4:", tail_dp(16, 4))


def part_b_c_regenerate() -> None:
    seed = 20260507
    paths = 400
    fine = 256
    grids = (4, 16, 64, 256)
    rng = random.Random(seed)
    scale = math.sqrt(1.0 / fine)
    hits: dict[int, list[int]] = {n: [] for n in grids}
    maxes: dict[int, list[float]] = {n: [] for n in grids}
    violations = 0
    for _ in range(paths):
        values = [0.0]
        for _ in range(fine):
            values.append(values[-1] + rng.gauss(0.0, scale))
        gm = {}
        for n in grids:
            stride = fine // n
            top = max(values[j] for j in range(0, fine + 1, stride))
            gm[n] = top
            maxes[n].append(top)
            hits[n].append(1 if top >= 1.0 else 0)
        for coarse, fine_n in ((4, 16), (16, 64), (64, 256)):
            if gm[coarse] > gm[fine_n]:
                violations += 1
    print("B-regen: nesting violations", violations)
    closed = 2.0 * 0.5 * math.erfc(1.0 / math.sqrt(2.0))
    print(f"B-regen: closed form 2(1-Phi(1)) unrounded = {closed:.12f}")
    for n in grids:
        k = sum(hits[n])
        p = k / paths
        var = sum((h - p) ** 2 for h in hits[n]) / (paths - 1)
        se = math.sqrt(var / paths)
        print(f"B-regen: N={n} count={k} p={p:.6f} se={se:.6f} diff={p - closed:+.6f}")
    target = math.sqrt(2.0 / math.pi)
    print(f"C-regen: sqrt(2/pi) unrounded = {target:.12f}")
    for n in grids:
        xs = maxes[n]
        mean = sum(xs) / paths
        var = sum((x - mean) ** 2 for x in xs) / (paths - 1)
        se = math.sqrt(var / paths)
        print(f"C-regen: N={n} mean={mean:.8f} se={se:.8f} diff={mean - target:+.8f} gap_in_se={(target - mean) / se:.6f}")


def first_passage_exact_means(largest: int) -> dict[int, Fraction]:
    """E[min(nu_1, N)] for N in 1..largest as exact Fractions: sum over k < N of P(nu_1 > k) (killed walk counts)."""
    alive_counts: dict[int, int] = {0: 1}
    survive: list[Fraction] = []
    for k in range(largest):
        survive.append(Fraction(sum(alive_counts.values()), 2**k))
        nxt: dict[int, int] = {}
        for pos, c in alive_counts.items():
            for step in (1, -1):
                q = pos + step
                if q >= 1:
                    continue
                nxt[q] = nxt.get(q, 0) + c
        alive_counts = nxt
    out: dict[int, Fraction] = {}
    running = Fraction(0)
    for k in range(largest):
        running += survive[k]
        out[k + 1] = running
    return out


def part_b_exact_and_c() -> None:
    means = first_passage_exact_means(256)
    for n in (16, 64, 256):
        print(f"B-DP: E[min(nu_1,{n})] = {float(means[n]):.9f}")
    print("B-DP: E[min(nu_1,16)] as fraction:", means[16], " numerator/2^15 check:", means[16] == Fraction(179587, 32768))
    rng = random.Random(20260508)
    sample_paths = 1000
    steps = 256
    capped: list[int] = []
    for _ in range(sample_paths):
        pos = 0
        first = steps
        for k in range(1, steps + 1):
            pos += 1 if rng.random() < 0.5 else -1
            if pos >= 1:
                first = k
                break
        capped.append(first)
    for n in (16, 64, 256):
        xs = [float(min(c, n)) for c in capped]
        mean = sum(xs) / sample_paths
        var = sum((x - mean) ** 2 for x in xs) / (sample_paths - 1)
        se = math.sqrt(var / sample_paths)
        exact = float(means[n])
        print(f"C-regen: N={n} mean={mean:.8f} se={se:.8f} exact={exact:.8f} z={(mean - exact) / se:+.6f}")


def brownian_first_passage() -> None:
    def cdf(a: float, h: float) -> float:
        return math.erfc(a / math.sqrt(2.0 * h))

    def dens(a: float, h: float) -> float:
        return a / (math.sqrt(2.0 * math.pi) * h**1.5) * math.exp(-(a * a) / (2.0 * h))

    for h in (1.0, 2.0):
        d = 1e-5
        numeric = (cdf(1.0, h + d) - cdf(1.0, h - d)) / (2 * d)
        print(f"D-regen: H={h:g} cdf={cdf(1.0, h):.10f} density={dens(1.0, h):.10f} central={numeric:.10f} diff={abs(dens(1.0, h) - numeric):.2e}")
    print(f"D-regen: f_1(1) from rounded factors = {0.398942 * 0.606531:.9f}; unrounded = {math.exp(-0.5) / math.sqrt(2 * math.pi):.10f}")
    print(f"D-regen: f_1(2) from rounded factors = {0.353553 * 0.778801 * 0.398942:.9f}; unrounded = {dens(1.0, 2.0):.10f}")
    print(f"D-regen: 1-Phi(1) = {0.5 * math.erfc(1 / math.sqrt(2)):.12f}; 2(1-Phi(1)) = {math.erfc(1 / math.sqrt(2)):.12f}")
    print(f"D-regen: P(tau_1<=2) = erfc(0.5) = {math.erfc(0.5):.10f}")
    print(f"M-regen: 2(1-Phi(1))-0.3173105 = {math.erfc(1 / math.sqrt(2)) - 0.3173105:+.3e}")
    print(f"M-regen: sqrt(2/pi) - 0.797885 = {math.sqrt(2 / math.pi) - 0.797885:+.3e}")
    print(f"M-regen: sqrt(2/pi) = {math.sqrt(2 / math.pi):.12f}")
    print(f"M-regen: E3 se = sqrt(121*279/(400^2*399)) = {math.sqrt(121 * 279 / (400**2 * 399)):.8f}")


def main() -> None:
    part_a_exact()
    part_b_c_regenerate()
    part_b_exact_and_c()
    brownian_first_passage()


main()
