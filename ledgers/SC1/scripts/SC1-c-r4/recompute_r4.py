"""Independent recomputation of every printed or prose number in SC1 L07 and L08 (round 4).

Written separately from the lab twins: exact Fractions and math.comb for the walk, a fresh
Simpson rule, and a fresh simulation loop that uses the same RNG draw order as the twins.
Run: python -I -W error ledgers/SC1/scripts/SC1-c-r4/recompute_r4.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction
from itertools import product

SEED_L07 = 20260507
SEED_L08 = 20260508


def phi_cdf(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def phi_pdf(x: float) -> float:
    return math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)


def walk_ge(n: int, m: int) -> int:
    """Number of length-n sequences whose endpoint is >= m (exact)."""
    total = 0
    for u in range(n + 1):
        if 2 * u - n >= m:
            total += math.comb(n, u)
    return total


def sign_ok_identity() -> tuple[int, int]:
    """Brute-force check of max>=a iff end>=a plus end>a, for n<=12, a<=n, against counts."""
    checked = 0
    ok = 0
    for n in range(1, 13):
        for a in range(1, n + 1):
            # brute force over all sequences
            cnt_max = 0
            cnt_end_ge = 0
            cnt_end_gt = 0
            for steps in product((1, -1), repeat=n):
                s = 0
                top = 0
                for e in steps:
                    s += e
                    top = max(top, s)
                cnt_max += top >= a
                cnt_end_ge += s >= a
                cnt_end_gt += s > a
            checked += 1
            ok += cnt_max == cnt_end_ge + cnt_end_gt == walk_ge(n, a) + walk_ge(n, a + 1)
    return ok, checked


def part_a_tails() -> dict[int, float]:
    out = {}
    for n in (4, 16, 64, 256, 1024):
        m = math.isqrt(n)
        out[n] = (walk_ge(n, m) + walk_ge(n, m + 1)) / 2**n
    return out


def pathwise_l07() -> tuple[list[int], int, list[list[float]]]:
    rng = random.Random(SEED_L07)
    fine = 256
    grids = (4, 16, 64, 256)
    scale = math.sqrt(1.0 / fine)
    maxima = {g: [] for g in grids}
    for _ in range(400):
        path = [0.0]
        acc = 0.0
        for _j in range(fine):
            acc += rng.gauss(0.0, scale)
            path.append(acc)
        for g in grids:
            stride = fine // g
            maxima[g].append(max(path[::stride]))
    violations = 0
    for c, f in ((4, 16), (16, 64), (64, 256)):
        for cm, fm in zip(maxima[c], maxima[f]):
            violations += cm > fm
    counts = []
    for g in grids:
        ind = [1.0 if v >= 1.0 else 0.0 for v in maxima[g]]
        p = sum(ind) / 400
        var = sum((x - p) ** 2 for x in ind) / 399
        counts.append((g, int(sum(ind)), p, math.sqrt(var / 400)))
    means = []
    for g in grids:
        vals = maxima[g]
        mu = sum(vals) / 400
        var = sum((v - mu) ** 2 for v in vals) / 399
        means.append([g, mu, math.sqrt(var / 400)])
    return [c[1] for c in counts], violations, [[c[0], c[2], c[3]] for c in counts] + [[*m] for m in means]


def simpson(a: float, b: float, n: int) -> float:
    h = (b - a) / n
    s = phi_pdf(a) + phi_pdf(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * phi_pdf(a + i * h)
    return s * h / 3


def l08_walk_stats() -> None:
    # Part A: first-passage counts for n=12, a=3 by brute force
    hits = {}
    pathwise_ok = 0
    total = 0
    for n in range(1, 13):
        for a in range(1, n + 1):
            for steps in product((1, -1), repeat=n):
                s = 0
                first = None
                top = 0
                for k, e in enumerate(steps, start=1):
                    s += e
                    top = max(top, s)
                    if first is None and s >= a:
                        first = k
                total += 1
                pathwise_ok += (first is not None and first <= n) == (top >= a)
                if n == 12 and a == 3 and first is not None:
                    hits[first] = hits.get(first, 0) + 1
    print("L08 A: (sequence, level) triples checked", total, "pathwise agreement", pathwise_ok)
    print("L08 A: first-passage counts n=12 a=3 by step", [hits.get(k, 0) for k in range(3, 13)], "sum", sum(hits.values()))
    print("L08 A: P(nu3<=12)", sum(hits.values()) / 4096, " P(S12>=3)", walk_ge(12, 3) / 4096)
    print("L08 A: #{S12>=3}", walk_ge(12, 3), "2x", 2 * walk_ge(12, 3))
    # Part B: exact truncated means via P(nu_1 > k) = 1 - P(max_{j<=k} S_j >= 1) = 1 - walk tail
    surv = []
    for k in range(256):
        # P(max_{j<=k} S_j >= 1): zero at k = 0 because S_0 = 0 < 1
        tail = Fraction(walk_ge(k, 1) + walk_ge(k, 2), 2**k) if k > 0 else Fraction(0)
        surv.append(1 - tail)
    cum = []
    run = Fraction(0)
    for k in range(256):
        run += surv[k]
        cum.append(run)
    for N in (16, 64, 256):
        val = cum[N - 1]
        print(f"L08 B: E[min(nu1,{N})] exact {float(val):.9f}")
    # Part C: seeded simulation, same draw order as the twin (one rng.random per step, stop at first hit)
    rng = random.Random(SEED_L08)
    capped = []
    for _ in range(1000):
        pos = 0
        first = 256
        for k in range(1, 257):
            pos += 1 if rng.random() < 0.5 else -1
            if pos >= 1:
                first = k
                break
        capped.append(first)
    for N in (16, 64, 256):
        vals = [float(min(c, N)) for c in capped]
        mu = sum(vals) / 1000
        var = sum((v - mu) ** 2 for v in vals) / 999
        se = math.sqrt(var / 1000)
        exact = float(cum[N - 1])
        print(f"L08 C: N={N} mean {mu:.6f} se {se:.6f} exact {exact:.6f} z {(mu - exact) / se:+.4f}")
    # Part D
    for H in (1.0, 2.0):
        cdf = math.erfc(1.0 / math.sqrt(2.0 * H))
        dens = 1.0 / (math.sqrt(2 * math.pi) * H**1.5) * math.exp(-1.0 / (2 * H))
        d = 1e-5
        numeric = (math.erfc(1 / math.sqrt(2 * (H + d))) - math.erfc(1 / math.sqrt(2 * (H - d)))) / (2 * d)
        print(f"L08 D: H={H}: cdf {cdf:.9f} density {dens:.9f} central {numeric:.9f} diff {abs(dens - numeric):.2e}")
    # R3 mode check: f_1 at 1/3 vs nearby
    f = lambda h: 1.0 / (math.sqrt(2 * math.pi) * h**1.5) * math.exp(-1.0 / (2 * h))
    print(f"L08 R3: f1(1/3)={f(1/3):.6f} f1(0.30)={f(0.30):.6f} f1(0.36)={f(0.36):.6f}")
    # E3 density at H=2 by hand
    print(f"L08 E3: (1/sqrt(2pi))*2^(-3/2)*e^(-1/4) = {(1/math.sqrt(2*math.pi))*2**-1.5*math.exp(-0.25):.9f}")
    print(f"L08 M2: f1(1) = {f(1.0):.9f}; (1/sqrt(2pi))=0.398942 times e^-0.5=0.606531 -> {0.398942*0.606531:.7f}")
    print(f"L08 M3: 5/8 = {5/8}; walk identity (#S3>=1)+(#S3>1) = {walk_ge(3,1)+walk_ge(3,2)}")


def main() -> None:
    ok, checked = sign_ok_identity()
    print(f"L07 A: identity brute force {ok} of {checked} (n<=12, a<=n)")
    print("L07 A: sum_{n=1}^{12} n =", sum(range(1, 13)))
    for n, p in part_a_tails().items():
        print(f"L07 A: N={n} P(M_N>=sqrt N)={p:.9f}")
    print("L07 A: E2 counts #{S16>=4} =", walk_ge(16, 4), "#{S16>4} =", walk_ge(16, 5), "total", walk_ge(16, 4) + walk_ge(16, 5))
    print("L07 A: binomials 8008,4368,1820,560,120,16,1 sum", 8008 + 4368 + 1820 + 560 + 120 + 16 + 1)
    counts, viol, rows = pathwise_l07()
    print("L07 B: counts at 4,16,64,256 =", counts, "violations", viol)
    for r in rows[:4]:
        print(f"L07 B: N={r[0]} p={r[1]:.6f} se={r[2]:.6f}")
    closed = 2 * (1 - phi_cdf(1.0))
    print(f"L07 B: closed form {closed:.10f}")
    for r in rows[4:]:
        print(f"L07 C: N={r[0]} mean={r[1]:.6f} se={r[2]:.6f}")
    print(f"L07 C: sqrt(2/pi)={math.sqrt(2/math.pi):.9f}")
    print(f"L07 D: 1-Phi(1) by erfc {0.5*math.erfc(1/math.sqrt(2)):.10f}; by Simpson {simpson(1.0, 13.0, 2000):.10f}")
    print(f"L07 M1: erfc(1/sqrt2) {math.erfc(1/math.sqrt(2)):.10f}; erfc(2/sqrt8) {math.erfc(2/math.sqrt(8)):.10f}")
    print(f"L07 E3: sqrt(33759/63840000) = {math.sqrt(33759/63840000):.6f}; 121*279={121*279}, 400^2*399={400**2*399}")
    print(f"L07 P1-ish: sqrt(2/pi) check via Cor 1.5(b): 2*phi(0)=2/sqrt(2pi)={2/math.sqrt(2*math.pi):.9f}")
    print(f"L07 misc: 0.2275*400={0.2275*400}, 0.3025*400={0.3025*400}")
    print(f"L07 misc: gaps {closed-0.2275:+.6f} {closed-0.2675:+.6f} {closed-0.2825:+.6f} {closed-0.3025:+.6f}; finest 0.7586 gap {0.797885-0.7586:.4f}")
    l08_walk_stats()


if __name__ == "__main__":
    main()
