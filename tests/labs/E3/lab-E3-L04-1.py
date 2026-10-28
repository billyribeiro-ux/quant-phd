"""E3 lab L04: first- and second-order stochastic dominance on finite-support lotteries, checked by utilities.

SIMULATED: 24 pairs of lotteries on one support of five wealth levels, in cents, are drawn with random.Random(SEED).
Each lottery places 12 balls on the five levels uniformly at random, so its probabilities are multiples of 1/12.
Three named pairs are fixed in the code and are not SIMULATED. Every integrated distribution function and every
dominance verdict from the distribution functions is exact (fractions.Fraction). The expected utilities of the CRRA
utilities are floating-point, and their differences are compared with a tolerance of 1e-12. Standard library only,
no network.

The check of the expected-utility side uses a finite set of test utilities, not all nondecreasing or all concave
utilities. The set holds the indicator utilities 1{s > t} (first order) or the utilities min(s - t, 0) (second order)
at each support point t, which are the witnesses for the verdicts, together with three CRRA utilities.
"""

from __future__ import annotations

import itertools
import math
import random
from collections import Counter
from fractions import Fraction

SUPPORT = (1000, 2000, 3000, 4000, 5000)
SEED = 20261028
N_BALLS = 12
N_PAIRS = 24
GAMMAS = (0.5, 1.0, 2.0)
TOL = 1e-12

PMF = tuple[Fraction, ...]


def crra_utility(w: float, gamma: float) -> float:
    """CRRA utility of positive wealth w in cents: (w**(1 - gamma) - 1) / (1 - gamma) for gamma != 1, ln(w) at 1."""
    if w <= 0.0:
        raise ValueError(f"CRRA utility needs positive wealth, got {w}")
    if gamma == 1.0:
        return math.log(w)
    return float((w ** (1.0 - gamma) - 1.0) / (1.0 - gamma))


def from_dict(masses: dict[int, Fraction]) -> PMF:
    """A pmf on SUPPORT from a dict of outcome -> probability; every key must lie on SUPPORT."""
    if not set(masses) <= set(SUPPORT):
        raise ValueError("every outcome must lie on SUPPORT")
    return tuple(masses.get(x, Fraction(0)) for x in SUPPORT)


def mean(pmf: PMF) -> Fraction:
    """Expected value in cents, exact."""
    return sum((p * x for p, x in zip(pmf, SUPPORT, strict=True)), Fraction(0))


def cdf(pmf: PMF, t: int) -> Fraction:
    """F(t) = P(X <= t), exact."""
    return sum((p for p, x in zip(pmf, SUPPORT, strict=True) if x <= t), Fraction(0))


def integrated_cdf(pmf: PMF, t: int) -> Fraction:
    """I(t) = integral of F from minus infinity to t, which equals E[(t - X)^+] for a finite support. Exact."""
    return sum((p * max(t - x, 0) for p, x in zip(pmf, SUPPORT, strict=True)), Fraction(0))


def verdict(x_first: bool, y_first: bool) -> str:
    """Name the ordering from the two one-way tests: X at least as good as Y, Y at least as good as X, or both."""
    if x_first and y_first:
        return "identical"
    if x_first:
        return "X dominates Y"
    if y_first:
        return "Y dominates X"
    return "no ranking"


def fosd_cdf_verdict(px: PMF, py: PMF) -> str:
    """First-order verdict from distribution functions: X dominates Y when F_X(t) <= F_Y(t) at every support point."""
    fx = [cdf(px, t) for t in SUPPORT]
    fy = [cdf(py, t) for t in SUPPORT]
    return verdict(all(a <= b for a, b in zip(fx, fy, strict=True)), all(b <= a for a, b in zip(fx, fy, strict=True)))


def sosd_cdf_verdict(px: PMF, py: PMF) -> str:
    """Second-order verdict from integrated distribution functions, for equal means. X dominates Y when I_X <= I_Y."""
    if mean(px) != mean(py):
        raise ValueError("the second-order test in this lab needs equal means")
    ix = [integrated_cdf(px, t) for t in SUPPORT]
    iy = [integrated_cdf(py, t) for t in SUPPORT]
    return verdict(all(a <= b for a, b in zip(ix, iy, strict=True)), all(b <= a for a, b in zip(ix, iy, strict=True)))


def eu_verdict(diffs: list[Fraction | float]) -> str:
    """Verdict from the expected-utility differences E u(X) - E u(Y) over a set of test utilities."""
    return verdict(all(d >= -TOL for d in diffs), all(d <= TOL for d in diffs))


def exact_diffs(px: PMF, py: PMF, utilities: list[tuple[Fraction, ...]]) -> list[Fraction | float]:
    """E u(X) - E u(Y) for exact-valued utilities, computed as Fractions."""
    return [sum(((a - b) * v for a, b, v in zip(px, py, u, strict=True)), Fraction(0)) for u in utilities]


def float_diffs(px: PMF, py: PMF, utilities: list[tuple[float, ...]]) -> list[Fraction | float]:
    """E u(X) - E u(Y) for floating-point utilities."""
    return [sum(float(a - b) * v for a, b, v in zip(px, py, u, strict=True)) for u in utilities]


def indicator_utilities() -> list[tuple[Fraction, ...]]:
    """The first-order witnesses 1{s > t} at each support point t."""
    return [tuple(Fraction(1 if x > t else 0) for x in SUPPORT) for t in SUPPORT]


def min_utilities() -> list[tuple[Fraction, ...]]:
    """The second-order witnesses min(s - t, 0) at each support point t: nondecreasing and concave in s."""
    return [tuple(Fraction(min(x - t, 0)) for x in SUPPORT) for t in SUPPORT]


def crra_values() -> list[tuple[float, ...]]:
    """CRRA utilities at the support points, for the gamma values in GAMMAS."""
    return [tuple(crra_utility(float(x), g) for x in SUPPORT) for g in GAMMAS]


def chord_slopes_nonincreasing(values: tuple[Fraction | float, ...]) -> bool:
    """True when the chord slopes of the function through (SUPPORT, values) never increase: concavity on the support."""
    slopes = [(values[j + 1] - values[j]) / (SUPPORT[j + 1] - SUPPORT[j]) for j in range(len(SUPPORT) - 1)]
    return all(a >= b for a, b in itertools.pairwise(slopes))


def draw_pmf(rng: random.Random) -> PMF:
    """A SIMULATED lottery: N_BALLS balls, each placed on a uniformly chosen support point."""
    counts = [0] * len(SUPPORT)
    for _ in range(N_BALLS):
        counts[rng.randrange(len(SUPPORT))] += 1
    return tuple(Fraction(c, N_BALLS) for c in counts)


def shift_up(px: PMF, rng: random.Random) -> PMF | None:
    """Move one ball's probability, 1/N_BALLS, from a lower support point to a higher one. None if no ball can move."""
    step = Fraction(1, N_BALLS)
    eligible = [i for i in range(len(SUPPORT) - 1) if px[i] >= step]
    if not eligible:
        return None
    i = rng.choice(eligible)
    j = rng.randrange(i + 1, len(SUPPORT))
    q = list(px)
    q[i] -= step
    q[j] += step
    return tuple(q)


def match_mean(pmf: PMF, target: Fraction) -> PMF | None:
    """Move mass between the lowest and highest support points until the mean equals target. None if infeasible."""
    move = (target - mean(pmf)) / (SUPPORT[-1] - SUPPORT[0])
    q = list(pmf)
    if move >= 0:
        if q[0] < move:
            return None
        q[0] -= move
        q[-1] += move
    else:
        m = -move
        if q[-1] < m:
            return None
        q[-1] -= m
        q[0] += m
    return tuple(q)


def describe(pmf: PMF) -> str:
    """The pmf as outcome:probability pairs, exact."""
    return ", ".join(f"{x}:{p}" for x, p in zip(SUPPORT, pmf, strict=True) if p)


def main() -> None:
    print(f"support in cents: {list(SUPPORT)}; seed {SEED}; {N_PAIRS} SIMULATED pairs")
    ind, mins, crra = indicator_utilities(), min_utilities(), crra_values()
    concave_ok = all(chord_slopes_nonincreasing(u) for u in mins) and all(chord_slopes_nonincreasing(v) for v in crra)
    print(f"min and CRRA test utilities have nonincreasing chord slopes on the support: {concave_ok}")

    fixed = {
        "A (spread)": (
            from_dict({2000: Fraction(1, 2), 4000: Fraction(1, 2)}),
            from_dict({1000: Fraction(1, 4), 3000: Fraction(1, 2), 5000: Fraction(1, 4)}),
        ),
        "B (shift)": (
            from_dict({2000: Fraction(1, 2), 4000: Fraction(1, 2)}),
            from_dict({3000: Fraction(1, 2), 4000: Fraction(1, 2)}),
        ),
        "C (equal means)": (from_dict({1000: Fraction(1, 2), 5000: Fraction(1, 2)}), from_dict({3000: Fraction(1)})),
    }
    for name, (px, py) in fixed.items():
        print(f"named pair {name}: X = {describe(px)}; Y = {describe(py)}; means {mean(px)} and {mean(py)}")
        fv = fosd_cdf_verdict(px, py)
        fe = eu_verdict(exact_diffs(px, py, ind) + float_diffs(px, py, crra))
        print(f"named pair {name}: FOSD verdict {fv}; expected-utility verdict {fe}; agree: {fv == fe}")
        if mean(px) == mean(py):
            sv = sosd_cdf_verdict(px, py)
            se = eu_verdict(exact_diffs(px, py, mins) + float_diffs(px, py, crra))
            print(f"named pair {name}: SOSD verdict {sv}; expected-utility verdict {se}; agree: {sv == se}")
        print(
            f"named pair {name}: integrated CDF of X at the support points: "
            f"{[str(integrated_cdf(px, t)) for t in SUPPORT]}"
        )
        print(
            f"named pair {name}: integrated CDF of Y at the support points: "
            f"{[str(integrated_cdf(py, t)) for t in SUPPORT]}"
        )

    rng = random.Random(SEED)
    kinds = ("shift", "equal-mean", "random")
    pairs: list[tuple[str, PMF, PMF]] = []
    while len(pairs) < N_PAIRS:
        kind = kinds[len(pairs) % 3]
        px = draw_pmf(rng)
        if kind == "shift":
            py_opt = shift_up(px, rng)
        elif kind == "equal-mean":
            py_opt = match_mean(draw_pmf(rng), mean(px))
        else:
            py_opt = draw_pmf(rng)
        if py_opt is not None:
            pairs.append((kind, px, py_opt))

    fosd_counts: Counter[str] = Counter()
    fosd_agree = 0
    sosd_counts: Counter[str] = Counter()
    sosd_total = 0
    sosd_agree = 0
    integrated_ok = True
    for n, (kind, px, py) in enumerate(pairs):
        fv = fosd_cdf_verdict(px, py)
        fe = eu_verdict(exact_diffs(px, py, ind) + float_diffs(px, py, crra))
        fosd_counts[fv] += 1
        fosd_agree += fv == fe
        if fv == "X dominates Y":
            integrated_ok = integrated_ok and all(integrated_cdf(px, t) <= integrated_cdf(py, t) for t in SUPPORT)
        line = f"pair {n:02d} ({kind}): FOSD {fv}; expected-utility agrees: {fv == fe}"
        if mean(px) == mean(py):
            sv = sosd_cdf_verdict(px, py)
            se = eu_verdict(exact_diffs(px, py, mins) + float_diffs(px, py, crra))
            sosd_total += 1
            sosd_agree += sv == se
            sosd_counts[sv] += 1
            line += f"; equal means, SOSD {sv}; expected-utility agrees: {sv == se}"
        print(line)

    print(f"FOSD verdicts over the 24 pairs: {dict(sorted(fosd_counts.items()))}")
    print(f"FOSD CDF verdict and expected-utility verdict agree on {fosd_agree} of {len(pairs)} pairs")
    print(f"FOSD-dominated pairs also satisfy I_X <= I_Y at every support point: {integrated_ok}")
    print(f"equal-mean pairs: {sosd_total}; SOSD verdicts: {dict(sorted(sosd_counts.items()))}")
    print(
        f"SOSD integrated verdict and expected-utility verdict agree on {sosd_agree} of {sosd_total} equal-mean pairs"
    )


main()
