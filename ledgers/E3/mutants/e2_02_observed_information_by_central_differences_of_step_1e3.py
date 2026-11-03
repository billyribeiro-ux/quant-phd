"""The standard errors use the observed information by central differences of step 1e-3, not 1e-5 or 1e-6."""


from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence
from fractions import Fraction
from typing import Any

MODELS: tuple[str, str] = ("crra", "prospect")
CENTS_PER_UNIT = 10_000.0  # the logit uses differences in units of $100: z = kappa * dCE / 10000
_H = 1e-5  # finite-difference step in the transformed coordinates
_MAX_ITER = 200
_BOUND = 40.0  # |c|, |a|, |b| beyond this would overflow the transforms; such points get -infinity

Parsed = tuple[list[int], list[Fraction], list[int], list[Fraction], str]


def _check_model(model: object) -> str:
    if not isinstance(model, str) or model not in MODELS:
        raise ValueError('model must be "crra" or "prospect"')
    return model


def _check_prizes(prizes_cents: Sequence[object]) -> list[int]:
    prizes: list[int] = []
    for x in prizes_cents:
        if isinstance(x, bool) or not isinstance(x, int):
            raise ValueError("prizes must be whole numbers of cents")
        prizes.append(x)
    if not prizes:
        raise ValueError("a lottery needs at least one prize")
    return prizes


def _check_probabilities(probabilities: Sequence[object], count: int) -> list[Fraction]:
    if len(probabilities) != count:
        raise ValueError("each prize needs exactly one probability")
    probs: list[Fraction] = []
    for p in probabilities:
        if isinstance(p, str):
            try:
                probs.append(Fraction(p))
            except (ValueError, ZeroDivisionError) as err:
                raise ValueError('probabilities written as text must read "numerator/denominator"') from err
        elif isinstance(p, bool) or not isinstance(p, int | Fraction):
            raise ValueError("probabilities must be exact Fraction values")
        else:
            probs.append(Fraction(p))
    if any(p < 0 for p in probs) or sum(probs, Fraction(0)) != 1:
        raise ValueError("probabilities must sum to 1 (and be non-negative)")
    return probs


def _check_prospect(gamma: float, lam: float) -> None:
    if not 0.0 <= gamma < 1.0:
        raise ValueError("the prospect model needs 0 <= gamma < 1")
    if not lam > 0.0:
        raise ValueError("the prospect model needs lambda > 0")


def _half_up(y: float) -> int:
    """The nearest whole cent with an exact half going up (toward plus infinity): floor(y + 1/2)."""
    return math.floor(y + 0.5)


def _crra_change(prizes: list[int], probs: list[Fraction], gamma: float, wealth: int) -> float:
    """Unrounded CRRA certainty equivalent as a change from wealth, in cents (gamma != 0 path or the log case)."""
    finals = [wealth + x for x in prizes]
    if gamma == 1.0:
        return math.exp(sum(float(p) * math.log(w) for p, w in zip(probs, finals, strict=True))) - wealth
    expected = sum(float(p) * w ** (1.0 - gamma) for p, w in zip(probs, finals, strict=True))
    return math.pow(expected, 1.0 / (1.0 - gamma)) - wealth


def _value(x: int, gamma: float, lam: float) -> float:
    """Loss-averse power value on a change x from the reference point 0."""
    if x >= 0:
        return math.pow(float(x), 1.0 - gamma)
    return -lam * math.pow(float(-x), 1.0 - gamma)


def _prospect_ce(prizes: list[int], probs: list[Fraction], gamma: float, lam: float) -> float:
    """Unrounded prospect certainty equivalent: v inverse of the lottery's value, in cents."""
    total = sum(float(p) * _value(x, gamma, lam) for x, p in zip(prizes, probs, strict=True))
    if total >= 0.0:
        return math.pow(total, 1.0 / (1.0 - gamma))
    return -math.pow(-total / lam, 1.0 / (1.0 - gamma))


def certainty_equivalent_cents(
    model: str,
    prizes_cents: list[int],
    probabilities: list[Fraction],
    params: dict[str, float],
    wealth_cents: int,
) -> int:
    """The certainty equivalent of a lottery in whole cents, rounded once, an exact half going up.

    For "crra" the result is the sure change from wealth whose CRRA utility equals the lottery's expected utility of
    final wealth. For "prospect" the result is the sure change from the reference point 0 whose value equals the
    lottery's value. Money in, money out: every returned value is an int.
    """
    name = _check_model(model)
    prizes = _check_prizes(prizes_cents)
    probs = _check_probabilities(probabilities, len(prizes))
    if isinstance(wealth_cents, bool) or not isinstance(wealth_cents, int):
        raise ValueError("wealth_cents must be a whole number of cents")
    gamma = float(params["gamma"])
    if name == "crra":
        if any(wealth_cents + x <= 0 for x in prizes):
            raise ValueError("wealth plus prize must stay positive")
        if gamma == 0.0:
            expected_change = sum((p * x for p, x in zip(probs, prizes, strict=True)), Fraction(0))
            return math.floor(expected_change + Fraction(1, 2))
        return _half_up(_crra_change(prizes, probs, gamma, wealth_cents))
    lam = float(params["lambda"])
    _check_prospect(gamma, lam)
    return _half_up(_prospect_ce(prizes, probs, gamma, lam))


def _parse(response: Mapping[str, Any]) -> Parsed:
    prizes_a = _check_prizes(response["prizes_a"])
    probs_a = _check_probabilities(response["probs_a"], len(prizes_a))
    prizes_b = _check_prizes(response["prizes_b"])
    probs_b = _check_probabilities(response["probs_b"], len(prizes_b))
    choice = response["choice"]
    if choice not in ("A", "B"):
        raise ValueError('choice must be "A" or "B"')
    return prizes_a, probs_a, prizes_b, probs_b, str(choice)


def _mixed(prizes: list[int], probs: list[Fraction]) -> bool:
    """A lottery mixes gains and losses when it has a gain and a loss, each with positive probability."""
    gains = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    losses = any(x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    return gains and losses


def _log1pexp(t: float) -> float:
    """log(1 + exp(t)), stable for large |t|."""
    if t > 0.0:
        return t + math.log1p(math.exp(-t))
    return math.log1p(math.exp(t))


def _logit_sum(parsed: list[Parsed], gamma: float, lam: float, kappa: float) -> float:
    total = 0.0
    for prizes_a, probs_a, prizes_b, probs_b, choice in parsed:
        ce_a = _prospect_ce(prizes_a, probs_a, gamma, lam)
        ce_b = _prospect_ce(prizes_b, probs_b, gamma, lam)
        z = kappa * (ce_a - ce_b) / CENTS_PER_UNIT
        total += -_log1pexp(-z) if choice == "A" else -_log1pexp(z)
    return total


def log_likelihood(responses: list[dict[str, object]], params: dict[str, float]) -> float:
    """Log-likelihood of the logit choice model: the sum over responses of log P(chosen) (A: 1/(1+exp(-z)) with
    z = kappa (CE_A - CE_B) / 10000); a response that chose B contributes log(1 - P(A)) = -log(1 + exp(z))."""
    gamma = float(params["gamma"])
    lam = float(params["lambda"])
    kappa = float(params["kappa"])
    _check_prospect(gamma, lam)
    if not kappa > 0.0:
        raise ValueError("the choice precision kappa must be positive")
    return _logit_sum([_parse(r) for r in responses], gamma, lam, kappa)


def _objective(theta: Sequence[float], parsed: list[Parsed]) -> float:
    c, a, b = theta
    if max(abs(c), abs(a), abs(b)) > _BOUND:
        return -math.inf
    gamma = 1.0 / (1.0 + math.exp(-c))
    return _logit_sum(parsed, gamma, math.exp(a), math.exp(b))


def _gradient_and_hessian(f: Callable[[list[float]], float], x: list[float]) -> tuple[list[float], list[list[float]]]:
    n = len(x)

    def shifted(*moves: tuple[int, float]) -> list[float]:
        y = list(x)
        for idx, amount in moves:
            y[idx] += amount
        return y

    f0 = f(list(x))
    grad = [0.0] * n
    hess = [[0.0] * n for _ in range(n)]
    for i in range(n):
        up = f(shifted((i, _H)))
        down = f(shifted((i, -_H)))
        grad[i] = (up - down) / (2.0 * _H)
        hess[i][i] = (up - 2.0 * f0 + down) / (_H * _H)
    for i in range(n):
        for j in range(i + 1, n):
            value = (
                f(shifted((i, _H), (j, _H)))
                - f(shifted((i, _H), (j, -_H)))
                - f(shifted((i, -_H), (j, _H)))
                + f(shifted((i, -_H), (j, -_H)))
            ) / (4.0 * _H * _H)
            hess[i][j] = value
            hess[j][i] = value
    return grad, hess


def _cholesky(a: list[list[float]]) -> list[list[float]] | None:
    n = len(a)
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(lower[i][k] * lower[j][k] for k in range(j))
            if i == j:
                if not (s > 0.0 and math.isfinite(s)):
                    return None
                lower[i][i] = math.sqrt(s)
            else:
                lower[i][j] = s / lower[j][j]
    return lower


def _solve(lower: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    y = [0.0] * n
    for i in range(n):
        y[i] = (rhs[i] - sum(lower[i][k] * y[k] for k in range(i))) / lower[i][i]
    x = [0.0] * n
    for i in reversed(range(n)):
        x[i] = (y[i] - sum(lower[k][i] * x[k] for k in range(i + 1, n))) / lower[i][i]
    return x


def _maximise(parsed: list[Parsed]) -> list[float]:
    def f(t: list[float]) -> float:
        return _objective(t, parsed)

    best: tuple[float, list[float]] | None = None
    for gamma in (0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95):
        for lam in (1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
            for kappa in (0.5, 1.0, 2.0, 3.0, 5.0, 8.0):
                t = [math.log(gamma / (1.0 - gamma)), math.log(lam), math.log(kappa)]
                v = f(t)
                if best is None or v > best[0]:
                    best = (v, t)
    if best is None:
        raise RuntimeError("the starting grid is empty")
    theta = list(best[1])
    value = best[0]
    mu = 1e-3
    for _ in range(_MAX_ITER):
        grad, hess = _gradient_and_hessian(f, theta)
        if max(abs(g) for g in grad) < 1e-7:
            return theta
        while True:
            lower = _cholesky([[-h + (mu if i == j else 0.0) for j, h in enumerate(row)] for i, row in enumerate(hess)])
            if lower is not None:
                step = _solve(lower, grad)
                trial = [x + s for x, s in zip(theta, step, strict=True)]
                new_value = f(trial)
                if new_value > value:
                    break
            mu = max(mu * 4.0, 1e-9)
            if mu > 1e12:
                return theta
        theta, value = trial, new_value
        mu = max(mu / 3.0, 1e-12)
        if max(abs(s) for s in step) < 1e-10:
            return theta
    raise RuntimeError("the likelihood maximisation did not converge")


def estimate(responses: list[dict[str, object]]) -> dict[str, float]:
    """Maximum-likelihood estimates of gamma, lambda and kappa under the "prospect" model, with standard errors.

    Raises ValueError when there are no responses, or when no lottery in any response mixes gains and losses, since
    loss aversion is then not identified.
    """
    if not responses:
        raise ValueError("need at least one response, and mixed-sign lotteries, to identify loss aversion")
    parsed = [_parse(r) for r in responses]
    if not any(_mixed(a, pa) or _mixed(b, pb) for a, pa, b, pb, _ in parsed):
        raise ValueError("need mixed-sign lotteries to identify loss aversion")
    theta = _maximise(parsed)

    def f(t: list[float]) -> float:
        return _objective(t, parsed)

    global _H
    _H = 1e-3
    _, hess = _gradient_and_hessian(f, theta)
    lower = _cholesky([[-h for h in row] for row in hess])
    if lower is None:
        raise RuntimeError("the observed information is not positive definite at the estimate")
    cov_diag: list[float] = []
    for i in range(3):
        unit = [1.0 if k == i else 0.0 for k in range(3)]
        cov_diag.append(_solve(lower, unit)[i])
    c, a, b = theta
    gamma = 1.0 / (1.0 + math.exp(-c))
    lam = math.exp(a)
    kappa = math.exp(b)
    return {
        "gamma_hat": gamma,
        "lambda_hat": lam,
        "kappa_hat": kappa,
        "se_gamma": gamma * (1.0 - gamma) * math.sqrt(cov_diag[0]),
        "se_lambda": lam * math.sqrt(cov_diag[1]),
        "se_kappa": kappa * math.sqrt(cov_diag[2]),
        "log_likelihood": _objective(theta, parsed),
    }
