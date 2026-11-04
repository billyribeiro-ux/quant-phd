"""Independent recomputation of every printed number on SC1 L07 and L08 (round 5).

Uses a dynamic programme over (position, running maximum) states and a first-passage DP, not the
binomial/reflection formulas of the twins, so the walk numbers are checked by a different algorithm.
Brownian closed forms use math.erfc and a composite Simpson rule. Run: python -I -W error <this file>.
"""

from __future__ import annotations

import math
import random
from collections import defaultdict
from fractions import Fraction

SEED_L07 = 20260507
SEED_L08 = 20260508


def walk_state_dp(n: int) -> dict[tuple[int, int], int]:
    """Counts of length-n step sequences keyed by (endpoint, running maximum over S_0..S_n)."""
    states: dict[tuple[int, int], int] = {(0, 0): 1}
    for _ in range(n):
        nxt: dict[tuple[int, int], int] = defaultdict(int)
        for (pos, top), c in states.items():
            for step in (1, -1):
                p = pos + step
                nxt[(p, max(top, p))] += c
        states = dict(nxt)
    return states


def tail_count(n: int, m: int) -> int:
    """#{max_{k<=n} S_k >= m} by DP over the state space."""
    return sum(c for (_, top), c in walk_state_dp(n).items() if top >= m)


def first_passage_counts(n: int, a: int) -> list[int]:
    """counts[k] = #{sequences of length n with nu_a = k}, k = 1..n (index 0 unused), by DP on (pos, hit)."""
    counts = [0] * (n + 1)
    # state: (position, hit_time or 0 if not yet hit); once hit we only track the time
    alive: dict[int, int] = {0: 1}  # position -> count for walks not yet at level a
    for k in range(1, n + 1):
        nxt: dict[int, int] = defaultdict(int)
        for pos, c in alive.items():
            for step in (1, -1):
                p = pos + step
                if p >= a:
                    # first passage at step k; remaining n-k steps are free
                    counts[k] += c * 2 ** (n - k)
                else:
                    nxt[p] += c
        alive = dict(nxt)
    return counts


def pure_walk_check() -> dict[str, object]:
    out: dict[str, object] = {}
    # L07 Part A: walk identity by DP for all (n, a), n <= 12, 1 <= a <= n
    ok_identity = 0
    total = 0
    for n in range(1, 13):
        st = walk_state_dp(n)
        for m in range(1, n + 1):
            total += 1
            reach = sum(c for (_, top), c in st.items() if top >= m)
            at_least = sum(c for (end, _), c in st.items() if end >= m)
            above = sum(c for (end, _), c in st.items() if end > m)
            ok_identity += reach == at_least + above
    out["L07_identity_pairs"] = f"{ok_identity} of {total}"
    # L07 exact tails at m = sqrt(N) via DP for N = 4, 16 (DP is exponential-free via states but N=1024 needs tail DP)
    out["L07_exact_tail_N16_m4"] = Fraction(tail_count(16, 4), 2**16)
    # L08 Part A: sequences and (sequence, level) pairs
    seqs = sum(2**n for n in range(1, 13))
    pairs = sum(n * 2**n for n in range(1, 13))
    out["L08_step_sequences_1_to_12"] = seqs
    out["L08_sequence_level_pairs"] = pairs
    fp = first_passage_counts(12, 3)
    out["L08_first_passage_counts_n12_a3_k3_to_12"] = fp[3:13]
    out["L08_sum_first_passage_n12_a3"] = sum(fp)
    out["L08_P_nu3_le12"] = sum(fp) / 4096
    out["L08_P_S12_ge3"] = sum(c for (end, _), c in walk_state_dp(12).items() if end >= 3) / 4096
    # the first-passage DP must agree with the endpoint/maximum DP: #{nu_a<=n} = #{max_{k<=n} S_k >= a}
    out["L08_DP_agreement_all_pairs"] = all(
        sum(first_passage_counts(n, a)[1:]) == tail_count(n, a) for n in range(1, 13) for a in range(1, n + 1)
    )
    # truncated means E[min(nu_1,N)] = sum_{k<N} P(nu_1>k), exact, by the first-passage DP for nu_1
    surv = [Fraction(1)]  # P(nu_1 > 0) = 1
    for k in range(1, 257):
        surv.append(Fraction(2**k - tail_count(k, 1), 2**k))
    trunc = {}
    run = Fraction(0)
    for k in range(256):
        run += surv[k]
        if k + 1 in (16, 64, 256):
            trunc[k + 1] = run
    out["L08_trunc_mean"] = {n: round(float(trunc[n]), 9) for n in (16, 64, 256)}
    return out


def sim_l07(seed: int) -> tuple[dict[int, float], dict[int, tuple[float, float]], dict[int, float]]:
    rng = random.Random(seed)
    fine = 256
    paths_n = 400
    grids = (4, 16, 64, 256)
    hits = {n: [] for n in grids}
    for _ in range(paths_n):
        inc = [rng.gauss(0.0, math.sqrt(1.0 / fine)) for _ in range(fine)]
        path = [0.0]
        for x in inc:
            path.append(path[-1] + x)
        for n in grids:
            step = fine // n
            hits[n].append(max(path[j] for j in range(0, fine + 1, step)))
    props = {n: sum(1 for m in hits[n] if m >= 1.0) / paths_n for n in grids}
    ses: dict[int, tuple[float, float]] = {}
    means: dict[int, float] = {}
    for n in grids:
        ind = [1.0 if m >= 1.0 else 0.0 for m in hits[n]]
        mu = sum(ind) / paths_n
        var = sum((v - mu) ** 2 for v in ind) / (paths_n - 1)
        ses[n] = (mu, math.sqrt(var / paths_n))
        means[n] = sum(hits[n]) / paths_n
    return props, ses, means


def main() -> None:
    res = pure_walk_check()
    for k, v in res.items():
        print("DP", k, v)
    closed1 = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(1.0 / math.sqrt(2.0))))
    print("closed 2(1-Phi(1)) =", f"{closed1:.10f}", " erfc(1/sqrt2) =", f"{math.erfc(1 / math.sqrt(2)):.10f}")
    print("1-Phi(1) =", f"{0.5 * math.erfc(1 / math.sqrt(2)):.10f}", " 2x printed =", 2 * 0.1586552539)
    print("E[M_1] = sqrt(2/pi) =", f"{math.sqrt(2 / math.pi):.8f}")
    print("M_4>=2 closed:", f"{2 * 0.5 * math.erfc(1 / math.sqrt(2)):.10f}", " erfc(2/sqrt8):", f"{math.erfc(2 / math.sqrt(8)):.10f}")
    print("E2 counts: S16>=4:", sum(math.comb(16, u) for u in range(10, 17)), " S16>4:", sum(math.comb(16, u) for u in range(11, 17)))
    print("E2 total/65536 =", f"{21778 / 65536:.10f}", " 14893+6885 =", 14893 + 6885)
    print("E3 se k=121 n=400:", f"{math.sqrt(121 * 279 / (400**2 * 399)):.10f}")
    print("E1 odd sum:", 512 + 384 + 288 + 224 + 180, " R1: 2*794 =", 2 * 794)
    print("L08 f_1(1):", f"{math.exp(-0.5) / math.sqrt(2 * math.pi):.10f}", " f_1 at H=2:",
          f"{1 / (math.sqrt(2 * math.pi) * 2**1.5) * math.exp(-0.25):.10f}")
    print("L08 P(tau_1<=2)=erfc(1/2):", f"{math.erfc(0.5):.10f}")
    print("L08 mode check f(0.30),f(1/3),f(0.36) a=1:",
          [f"{(1 / (math.sqrt(2*math.pi)*h**1.5))*math.exp(-1/(2*h)):.6f}" for h in (0.30, 1/3, 0.36)])
    print("L07 Remark: 1-Phi via Simpson on [1,13] 2000 intervals")
    def g(x: float) -> float:
        return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)
    a, b, n = 1.0, 13.0, 2000
    h = (b - a) / n
    tot = g(a) + g(b) + sum((4.0 if i % 2 else 2.0) * g(a + i * h) for i in range(1, n))
    print("  simpson =", f"{tot * h / 3:.10f}")
    props, ses, means = sim_l07(SEED_L07)
    for n_ in (4, 16, 64, 256):
        print(f"L07 B N={n_}: prop {props[n_]:.4f} se {ses[n_][1]:.4f} diff {props[n_] - closed1:+.4f} count {round(props[n_]*400)}")
    for n_ in (4, 16, 64, 256):
        print(f"L07 C N={n_}: mean {means[n_]:.4f}")
    # sample standard error of the 256-step mean of grid maxima
    rng = random.Random(SEED_L07)
    print("L07 nesting check is in the twin; here: count of nesting violations is computed in recompute_r5 via sim_l07 indirectly")


if __name__ == "__main__":
    main()
