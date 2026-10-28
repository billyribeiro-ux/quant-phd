"""Per-learner instances for the E3 autograder: the preference-elicitation engine. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws a
SIMULATED participant and a questionnaire, and then simulates that participant's answers:

* the true parameters of the "prospect" model: a curvature gamma in [0.10, 0.80] (three decimals), a loss-aversion
  coefficient lambda in [1.000, 3.000] and a choice precision kappa in [0.500, 5.000];
* a starting wealth in whole cents, from $50,000.00 to $200,000.00 (the "crra" model uses it, the prospect model
  does not);
* 200 choice pairs. Each lottery has 2 or 3 prizes in whole cents, between $5.00 and $500.00 in magnitude, with exact
  probabilities that are positive and sum to 1 (denominators 4, 5, 10 and 20). A lottery is mixed (it has a gain and a
  loss, each with positive probability) or pure (all its prizes are gains);
* the answers. The chosen alternative is drawn with ``random.Random(seed)`` from the logit probability
  P(A) = 1 / (1 + exp(-kappa (CE_A - CE_B) / 100)), where CE is the prospect certainty equivalent in cents.

The instance is returned as JSON text (``responses_json``), which is the form the in-browser questionnaire exports.
Probabilities are written as "numerator/denominator" strings, which ``Fraction`` reads back exactly.

A draw is rejected, and the next draw taken, unless all of the following hold:

* at least 100 of the 200 pairs contain a mixed lottery, so that loss aversion is identified;
* the Hessian of the log-likelihood at the true parameters is negative definite (checked here, on this sample);
* the log-likelihood at the true parameters exceeds, by at least 0.5, its best value on a grid of lambda and kappa at
  gamma = 0.001 (the edge of the domain), so the estimate is not pushed to the edge of the domain;
* no certainty equivalent (prospect at the true parameters, or CRRA at the true gamma from the wealth) lies within 1e-6
  of a half cent. Such a value has no unique nearest cent once floating point is involved, so the rounding rule of the
  specification would not be a fair test of a correct implementation.

Nothing here is a real participant, a real questionnaire or market data.
"""

from __future__ import annotations

import json
import math
import random
from collections.abc import Callable, Sequence
from fractions import Fraction
from functools import partial
from typing import Any

_TIE_MARGIN = 1e-6
_DENOMINATORS = (4, 5, 10, 20)
_PAIRS = 200
_CANDIDATES = 30
_SPREAD_CENTS = 5_000.0
_MIN_MIXED_PAIRS = 100
_CENTS_PER_UNIT = 10_000.0
_MAX_DRAWS = 10_000


def _lottery(rng: random.Random, mixed: bool) -> tuple[list[int], list[Fraction]]:
    """One SIMULATED lottery: positive exact probabilities summing to 1, and whole-cent prizes."""
    count = rng.choice((2, 3))
    denominator = rng.choice(_DENOMINATORS)
    cuts = sorted(rng.sample(range(1, denominator), count - 1))
    bounds = [0, *cuts, denominator]
    probs = [Fraction(bounds[k + 1] - bounds[k], denominator) for k in range(count)]
    magnitudes = [rng.randrange(500, 50_001) for _ in range(count)]
    if mixed:
        signs = [1, -1, *(rng.choice((1, -1)) for _ in range(count - 2))]
        rng.shuffle(signs)
    else:
        signs = [1] * count
    return [s * m for s, m in zip(signs, magnitudes, strict=True)], probs


def _is_mixed(prizes: Sequence[int], probs: Sequence[Fraction]) -> bool:
    gains = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    losses = any(x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    return gains and losses


def _value(x: int, gamma: float, lam: float) -> float:
    if x >= 0:
        return math.pow(float(x), 1.0 - gamma)
    return -lam * math.pow(float(-x), 1.0 - gamma)


def _prospect_ce(prizes: Sequence[int], probs: Sequence[Fraction], gamma: float, lam: float) -> float:
    """Oracle: the prospect certainty equivalent in cents, unrounded, by the closed form of the lessons."""
    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return math.pow(total, 1.0 / (1.0 - gamma))
    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))


def _crra_change(prizes: Sequence[int], probs: Sequence[Fraction], gamma: float, wealth: int) -> float:
    """Oracle: the CRRA certainty equivalent as a change from wealth, in cents, unrounded."""
    finals = [wealth + x for x in prizes]
    if gamma == 1.0:
        return math.exp(sum(float(p) * math.log(w) for p, w in zip(probs, finals, strict=True))) - wealth
    return (
        math.pow(sum(float(p) * w ** (1.0 - gamma) for p, w in zip(probs, finals, strict=True)), 1.0 / (1.0 - gamma))
        - wealth
    )


def _clear_of_half_cent(y: float) -> bool:
    return abs((y - math.floor(y)) - 0.5) > _TIE_MARGIN


def _log1pexp(t: float) -> float:
    """log(1 + exp(t)), stable for large |t|."""
    if t > 0.0:
        return t + math.log1p(math.exp(-t))
    return math.log1p(math.exp(t))


def _sigmoid(z: float) -> float:
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def _loglik_theta(theta: Sequence[float], answers: Sequence[tuple[Any, ...]]) -> float:
    """Oracle log-likelihood in the transformed coordinates (c, a, b) used only by the identification guard."""
    c, a, b = theta
    gamma = 1.0 / (1.0 + math.exp(-c))
    lam = math.exp(a)
    kappa = math.exp(b)
    total = 0.0
    for pa, qa, pb, qb, choice in answers:
        z = kappa * (_prospect_ce(pa, qa, gamma, lam) - _prospect_ce(pb, qb, gamma, lam)) / _CENTS_PER_UNIT
        total += -_log1pexp(-z) if choice == "A" else -_log1pexp(z)
    return total


def _is_positive_definite(a: list[list[float]]) -> bool:
    n = len(a)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if not s > 0.0:
                    return False
                lower[i][i] = math.sqrt(s)
            else:
                lower[i][j] = s / lower[j][j]
    return True


_BOUNDARY_GAMMA = 0.001
_BOUNDARY_MARGIN = 0.5
_BOUNDARY_GRID = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0)


def _boundary_loglik(answers: Sequence[tuple[Any, ...]]) -> float:
    """The best log-likelihood on a grid of lambda and kappa with curvature at the edge of the domain (gamma = 0.001).

    A participant whose likelihood is higher at that edge than at the truth has an estimate at the boundary, where the
    standard errors are meaningless, so such draws are rejected.
    """
    c = math.log(_BOUNDARY_GAMMA / (1.0 - _BOUNDARY_GAMMA))
    return max(
        _loglik_theta([c, math.log(lam), math.log(kappa)], answers)
        for lam in _BOUNDARY_GRID
        for kappa in _BOUNDARY_GRID
    )


def _negative_hessian_is_definite(f: Callable[[list[float]], float], x: list[float]) -> bool:
    h = 1e-4
    n = len(x)

    def at(*moves: tuple[int, float]) -> float:
        y = list(x)
        for idx, amount in moves:
            y[idx] += amount
        return f(y)

    hess = [[0.0] * n for _ in range(n)]
    f0 = at()
    for i in range(n):
        hess[i][i] = (at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, n):
            value = (at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (
                4.0 * h * h
            )
            hess[i][j] = value
            hess[j][i] = value
    return _is_positive_definite([[-v for v in row] for row in hess])


def _closest_candidate(
    candidates: list[tuple[list[int], list[Fraction]]], target: float, gamma: float, lam: float
) -> tuple[list[int], list[Fraction]]:
    """The candidate lottery whose prospect certainty equivalent (in cents) is nearest to ``target``."""
    return min(candidates, key=lambda c: abs(_prospect_ce(c[0], c[1], gamma, lam) - target))


def _serialise(
    pair_id: int, choice: str, pa: list[int], qa: list[Fraction], pb: list[int], qb: list[Fraction]
) -> dict[str, Any]:
    return {
        "pair_id": pair_id,
        "choice": choice,
        "prizes_a": pa,
        "probs_a": [str(p) for p in qa],
        "prizes_b": pb,
        "probs_b": [str(p) for p in qb],
    }


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``: true parameters, wealth and the answers, as JSON."""
    rng = random.Random(seed)
    for _ in range(_MAX_DRAWS):
        gamma = round(rng.uniform(0.10, 0.80), 3)
        lam = round(rng.uniform(1.0, 3.0), 3)
        kappa = round(rng.uniform(0.5, 5.0), 3)
        wealth = rng.randrange(5_000_000, 20_000_001, 100)
        answers: list[tuple[Any, ...]] = []
        records: list[dict[str, Any]] = []
        for pair_id in range(_PAIRS):
            pa, qa = _lottery(rng, rng.random() < 0.6)
            ce_a = _prospect_ce(pa, qa, gamma, lam)
            # The answer is informative only if the certainty equivalents differ by a spread of the order of the
            # logit scale: a target within $50 of A's certainty equivalent is set, and of 30 candidate lotteries B,
            # the one whose certainty equivalent is closest to that target is used.
            candidates = [_lottery(rng, rng.random() < 0.6) for _ in range(_CANDIDATES)]
            target = ce_a + rng.uniform(-_SPREAD_CENTS, _SPREAD_CENTS)
            pb, qb = _closest_candidate(candidates, target, gamma, lam)
            ce_b = _prospect_ce(pb, qb, gamma, lam)
            choice = "A" if rng.random() < _sigmoid(kappa * (ce_a - ce_b) / _CENTS_PER_UNIT) else "B"
            answers.append((pa, qa, pb, qb, choice))
            records.append(_serialise(pair_id, choice, pa, qa, pb, qb))
        mixed_pairs = sum(_is_mixed(pa, qa) or _is_mixed(pb, qb) for pa, qa, pb, qb, _ in answers)
        if mixed_pairs < _MIN_MIXED_PAIRS:
            continue
        theta = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
        if not _negative_hessian_is_definite(partial(_loglik_theta, answers=answers), theta):
            continue
        if _loglik_theta(theta, answers) < _boundary_loglik(answers) + _BOUNDARY_MARGIN:
            continue
        ces = [
            value
            for pa, qa, pb, qb, _ in answers
            for value in (
                _prospect_ce(pa, qa, gamma, lam),
                _prospect_ce(pb, qb, gamma, lam),
                _crra_change(pa, qa, gamma, wealth),
                _crra_change(pb, qb, gamma, wealth),
            )
        ]
        if not all(_clear_of_half_cent(v) for v in ces):
            continue
        return {
            "seed": seed,
            "gamma": gamma,
            "lambda": lam,
            "kappa": kappa,
            "wealth_cents": wealth,
            "responses_json": json.dumps(records, separators=(",", ":")),
        }
    raise RuntimeError(f"no valid instance for seed {seed} within {_MAX_DRAWS} draws")
