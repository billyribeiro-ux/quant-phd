"""Independent recomputation of every number printed by the SC1 L07 and L08 labs and quoted in their prose (round 9).

Algorithms differ from the twins on purpose:
- walk counts by a killed-walk dynamic programme (paths that stay below a level), not by binomial sums;
- first-passage counts by a DP that absorbs at the level, not by enumeration;
- truncated means by exact Fractions from the DP survival probabilities;
- seeded simulations regenerated with the same RNG draw order, with independent statistics code;
- normal quantities by erfc and by a Simpson rule.

Run: python3 -I ledgers/SC1/scripts/SC1-c-r9/indep_r9.py
"""

from __future__ import annotations

import math
import random
from fractions import Fraction


def stay_below(n: int, level: int) -> int:
    """Number of length-n step sequences whose running maximum over S_0..S_n stays <= level - 1 (level >= 1).

    Killed-walk DP: counts[p] = number of prefixes ending at position p, never reaching `level`.
    """
    counts = {0: 1}
    for _ in range(n):
        nxt: dict[int, int] = {}
        for p, c in counts.items():
            for step in (1, -1):
                q = p + step
                if q < level:
                    nxt[q] = nxt.get(q, 0) + c
        counts = nxt
    return sum(counts.values())


def max_reaches(n: int, level: int) -> int:
    """#{max_{k<=n} S_k >= level}, via the complement of stay_below."""
    return 2**n - stay_below(n, level)


def first_passage_counts(n: int, level: int) -> dict[int, int]:
    """#{nu_level = k} for k = 1..n: prefixes that first reach `level` at step k, extended freely to n steps."""
    alive = {0: 1}
    out: dict[int, int] = {}
    for k in range(1, n + 1):
        nxt: dict[int, int] = {}
        hit = 0
        for p, c in alive.items():
            for step in (1, -1):
                q = p + step
                if q >= level:
                    hit += c
                else:
                    nxt[q] = nxt.get(q, 0) + c
        if hit:
            out[k] = hit * 2 ** (n - k)
        alive = nxt
    return out


def survive_fraction(k: int) -> Fraction:
    """P(nu_1 > k) = P(S_j <= 0 for all j <= k) as an exact Fraction."""
    return Fraction(stay_below(k, 1), 2**k)


def truncated_mean(n: int) -> Fraction:
    """E[min(nu_1, n)] = sum_{k=0}^{n-1} P(nu_1 > k), exact."""
    return sum((survive_fraction(k) for k in range(n)), Fraction(0))


def part_a_l07() -> None:
    ok = True
    for n in range(1, 13):
        for m in range(1, n + 1):
            # the identity of Lesson 6: #{max >= m} = #{S_n >= m} + #{S_n > m}
            ends = {}
            for steps in range(2**n):
                pos = 0
                for i in range(n):
                    pos += 1 if (steps >> i) & 1 else -1
                ends[pos] = ends.get(pos, 0) + 1
            at_least = sum(c for p, c in ends.items() if p >= m)
            above = sum(c for p, c in ends.items() if p > m)
            ok = ok and max_reaches(n, m) == at_least + above
    print(f"L07 A: discrete tail identity with killed-walk counts holds for all 78 pairs: {ok}")
    for n in (4, 16, 64, 256, 1024):
        m = math.isqrt(n)
        p = Fraction(max_reaches(n, m), 2**n)
        print(f"L07 A: N={n} m={m} P(M_N>=m) = {float(p):.6f}  (exact {p.numerator}/2^{n.bit_length()}-ish)")
    print(f"L07 A: 2(1-Phi(1)) via erfc = {math.erfc(1 / math.sqrt(2)):.11f}")


def part_b_c_l07() -> None:
    seed = 20260507
    paths = 400
    fine = 256
    grids = (4, 16, 64, 256)
    rng = random.Random(seed)
    maxima = {g: [] for g in grids}
    scale = math.sqrt(1.0 / fine)
    for _ in range(paths):
        pos = 0.0
        values = [0.0]
        for _ in range(fine):
            pos += rng.gauss(0.0, scale)
            values.append(pos)
        for g in grids:
            stride = fine // g
            maxima[g].append(max(values[j] for j in range(0, fine + 1, stride)))
    violations = 0
    for coarse, nxt in zip(grids, grids[1:]):
        violations += sum(1 for a, b in zip(maxima[coarse], maxima[nxt]) if a > b)
    print(f"L07 B: nesting violations = {violations}")
    closed = erfc_tail = math.erfc(1 / math.sqrt(2))
    for g in grids:
        ind = [1.0 if v >= 1.0 else 0.0 for v in maxima[g]]
        mu = sum(ind) / paths
        var = sum((x - mu) ** 2 for x in ind) / (paths - 1)
        se = math.sqrt(var / paths)
        print(f"L07 B: N={g} proportion {mu:.4f} se {se:.4f} diff {mu - closed:+.4f} count {int(sum(ind))}")
    for g in grids:
        vals = maxima[g]
        mu = sum(vals) / paths
        var = sum((x - mu) ** 2 for x in vals) / (paths - 1)
        se = math.sqrt(var / paths)
        print(f"L07 C: N={g} mean {mu:.4f} se {se:.4f} diff {mu - math.sqrt(2 / math.pi):+.4f}")
    print(f"L07 B: closed form 2(1-Phi(1)) unrounded = {2 * erfc_tail:.11f}")


def part_d_l07() -> None:
    # Simpson on [1, 13] for the normal density, independent of erfc
    def f(x: float) -> float:
        return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)

    n = 4000
    a, b = 1.0, 13.0
    h = (b - a) / n
    s = f(a) + f(b) + sum((4 if i % 2 else 2) * f(a + i * h) for i in range(1, n))
    simpson = s * h / 3
    print(f"L07 D: 1-Phi(1) by Simpson (4000 intervals) = {simpson:.10f}")
    print(f"L07 D: 1-Phi(1) by erfc = {0.5 * math.erfc(1 / math.sqrt(2)):.10f}")


def part_a_l08() -> None:
    by_step = first_passage_counts(12, 3)
    seq = [by_step.get(k, 0) for k in range(3, 13)]
    print(f"L08 A: first-passage counts to 3 at steps 3..12 (DP): {seq}")
    total = sum(seq)
    print(f"L08 A: total {total} (expected 1588), P = {total / 4096:.6f}")
    print(f"L08 A: #{{S_12>=3}} = {sum(math.comb(12, (12 + s) // 2) for s in range(-12, 13, 2) if s >= 3)}")
    # 8190 sequences and 90114 pairs
    print(f"L08 A: sum 2^n n=1..12 = {sum(2**n for n in range(1, 13))}; sum n 2^n = {sum(n * 2**n for n in range(1, 13))}")
    # exact first-passage equals maximum event count for each (n, a), from the DP
    bad = 0
    for n in range(1, 13):
        for a in range(1, n + 1):
            fp = sum(first_passage_counts(n, a).values())
            if fp != max_reaches(n, a):
                bad += 1
    print(f"L08 A: (n,a) pairs where first-passage total differs from max count: {bad} (expected 0)")


def part_b_c_l08() -> None:
    ns = (16, 64, 256)
    vals = {n: truncated_mean(n) for n in ns}
    for n in ns:
        print(f"L08 B: N={n} E[min(nu_1,N)] = {float(vals[n]):.9f} (exact fraction denominator 2^{(n - 1)}-type)")
    print(f"L08 B: 179587/32768 = {179587 / 32768:.10f}; equals N=16 value: {vals[16] == Fraction(179587, 32768)}")
    rng = random.Random(20260508)
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
    for n in ns:
        xs = [min(c, n) for c in capped]
        mu = sum(xs) / 1000
        var = sum((x - mu) ** 2 for x in xs) / 999
        se = math.sqrt(var / 1000)
        z = (mu - float(vals[n])) / se
        print(f"L08 C: N={n} sample mean {mu:.4f} se {se:.4f} exact {float(vals[n]):.4f} z {z:+.4f}")


def part_d_l08() -> None:
    def cdf(a: float, h: float) -> float:
        # erfc form and the Phi form, to check the identity on the page
        erfc_form = math.erfc(a / math.sqrt(2 * h))
        phi = 0.5 * (1 + math.erf((a / math.sqrt(h)) / math.sqrt(2)))
        assert abs(erfc_form - 2 * (1 - phi)) < 1e-14
        return erfc_form

    def dens(a: float, h: float) -> float:
        return a / (math.sqrt(2 * math.pi) * h**1.5) * math.exp(-a * a / (2 * h))

    for h in (1.0, 2.0):
        step = 1e-5
        cd = (cdf(1, h + step) - cdf(1, h - step)) / (2 * step)
        print(f"L08 D: H={h:g} cdf {cdf(1, h):.9f} density {dens(1, h):.9f} central {cd:.9f}")
    print(f"L08 D: density at H=1 unrounded: {1 / math.sqrt(2 * math.pi) * math.exp(-0.5):.10f}")
    print(f"L08 E3: density at H=2 from printed factors: {0.398942 * 0.353553 * 0.778801:.9f}")
    print(f"L08 E3: density at H=2 unrounded: {dens(1, 2):.10f}")
    print(f"L08 Remark 1.6 check H=1e6 ratio to a H^(-3/2)/sqrt(2pi): {dens(1, 1e6) / (1 / (math.sqrt(2 * math.pi) * 1e6**1.5)):.8f}")
    print(f"L08 R3: argmax of f_1 over a grid vs a^2/3 = {1 / 3}:", max((dens(1, h / 10000), h / 10000) for h in range(1, 30000))[1])
    print(f"L08 misc: 2*0.1586552539 = {2 * 0.1586552539:.10f}; unrounded 2(1-Phi(1)) = {2 * 0.5 * math.erfc(1 / math.sqrt(2)):.11f}")
    print(f"L08 E2: sqrt(k(n-k)/(n^2(n-1))) with k=121,n=400 = {math.sqrt(121 * 279 / (400**2 * 399)):.6f}")


def part_l07_e2() -> None:
    n = 16
    ge4 = sum(math.comb(16, u) for u in range(16 + 1) if 2 * u - 16 >= 4)
    gt4 = sum(math.comb(16, u) for u in range(16 + 1) if 2 * u - 16 > 4)
    print(f"L07 E2: #{{S16>=4}} = {ge4}, #{{S16>4}} = {gt4}, total {ge4 + gt4}, ratio {(ge4 + gt4) / 2**n:.6f}")
    print(f"L07 E1: 0.2275*400 = {0.2275 * 400:.4f}; 0.3025*400 = {0.3025 * 400:.4f}")
    print(f"L07 interp: 0.3173105 - 0.2275 = {0.3173105 - 0.2275:.7f}; - 0.2675 = {0.3173105 - 0.2675:.7f}; "
          f"- 0.2825 = {0.3173105 - 0.2825:.7f}; - 0.3025 = {0.3173105 - 0.3025:.7f}")
    print(f"L07 C: finest gap 0.0393 over se 0.0317 = {0.0393 / 0.0317:.3f}")
    print(f"L07 Cor1.5b: sqrt(2/pi) = {math.sqrt(2 / math.pi):.10f}; 0.797885 diff {0.797885 - math.sqrt(2 / math.pi):.3e}")
    print(f"L07 P2: 1/sqrt(2pi) = {1 / math.sqrt(2 * math.pi):.10f}")


if __name__ == "__main__":
    part_a_l07()
    part_b_c_l07()
    part_d_l07()
    part_l07_e2()
    part_a_l08()
    part_b_c_l08()
    part_d_l08()
