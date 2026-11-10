"""Autograder test suite for AP2 project (CAPM on trial).

Tests capm_tests.py against properties, oracle computations, and exception conditions.
"""

from __future__ import annotations

import os
import random
from fractions import Fraction
from typing import cast

import pytest
from capm_tests import (
    capm_beta,
    frontier_weights,
    is_tangency,
    jensen_regression,
    minimum_variance_weights,
    security_market_line,
    tangency_weights,
)
from instance import make_instance


def _get_current_instance() -> dict[str, object]:
    seed = int(os.environ.get("QF_SEED", "0"))
    return cast(dict[str, object], make_instance(seed))


def _unpack_fractions(
    inst: dict[str, object],
) -> tuple[int, list[Fraction], list[list[Fraction]], Fraction, Fraction, list[list[float]], list[float]]:
    n = cast(int, inst["n"])
    mu_strs = cast(list[str], inst["mu"])
    cov_strs = cast(list[list[str]], inst["cov"])
    r_f_str = cast(str, inst["r_f"])
    target_str = cast(str, inst["target"])
    asset_returns = cast(list[list[float]], inst["asset_excess_returns"])
    market_returns = cast(list[float], inst["market_excess_returns"])

    mu = [Fraction(x) for x in mu_strs]
    cov = [[Fraction(x) for x in row] for row in cov_strs]
    r_f = Fraction(r_f_str)
    target = Fraction(target_str)
    return n, mu, cov, r_f, target, asset_returns, market_returns


def test_gmv_weights() -> None:
    __tracebackhide__ = True
    inst = _get_current_instance()
    n, _, cov, _, _, _, _ = _unpack_fractions(inst)

    w = minimum_variance_weights(cov)
    assert len(w) == n, "GMV weights vector length must equal number of assets"
    assert sum(w, Fraction(0, 1)) == Fraction(1, 1), "GMV weights must sum to 1"

    # Stationarity condition: Sigma @ w proportional to iota (all entries equal)
    sig_w = [sum((cov[i][j] * w[j] for j in range(n)), Fraction(0, 1)) for i in range(n)]
    for i in range(1, n):
        assert sig_w[i] == sig_w[0], "stationarity fails: Sigma @ w must be constant across coordinates"

    # Variance check against 200 random portfolios
    w_var = sum((w[i] * sig_w[i] for i in range(n)), Fraction(0, 1))
    rng = random.Random(42)
    for _ in range(200):
        rand_w_raw = [Fraction(rng.randint(1, 10), 1) for _ in range(n)]
        tot = sum(rand_w_raw, Fraction(0, 1))
        rand_w = [rw / tot for rw in rand_w_raw]
        rand_sig_w = [sum((cov[i][j] * rand_w[j] for j in range(n)), Fraction(0, 1)) for i in range(n)]
        rand_var = sum((rand_w[i] * rand_sig_w[i] for i in range(n)), Fraction(0, 1))
        assert w_var <= rand_var, "GMV variance must not exceed variance of any feasible portfolio"


def test_tangency_weights() -> None:
    __tracebackhide__ = True
    inst = _get_current_instance()
    n, mu, cov, r_f, _, _, _ = _unpack_fractions(inst)

    w_t = tangency_weights(mu, cov, r_f)
    assert len(w_t) == n, "Tangency weights vector length must equal number of assets"
    assert sum(w_t, Fraction(0, 1)) == Fraction(1, 1), "Tangency weights must sum to 1"

    # Must satisfy is_tangency
    assert is_tangency(mu, cov, r_f, w_t), "Tangency weights must satisfy is_tangency predicate"

    # Perturbed weights must fail is_tangency
    perturbed = list(w_t)
    perturbed[0] += Fraction(1, 1000)
    perturbed[1] -= Fraction(1, 1000)
    assert not is_tangency(mu, cov, r_f, perturbed), "Perturbed portfolio must not satisfy is_tangency"


def test_frontier_weights() -> None:
    __tracebackhide__ = True
    inst = _get_current_instance()
    n, mu, cov, _, target, _, _ = _unpack_fractions(inst)

    w_f = frontier_weights(mu, cov, target)
    assert len(w_f) == n, "Frontier weights vector length must equal number of assets"
    assert sum(w_f, Fraction(0, 1)) == Fraction(1, 1), "Frontier weights must sum to 1"

    achieved_mu = sum((mu[i] * w_f[i] for i in range(n)), Fraction(0, 1))
    assert achieved_mu == target, "Frontier portfolio must achieve target expected return exactly"

    # Two-fund separation: any third frontier portfolio is a linear combination of two frontier portfolios
    target2 = target + Fraction(1, 500)
    target3 = target + Fraction(2, 500)
    w_f2 = frontier_weights(mu, cov, target2)
    w_f3 = frontier_weights(mu, cov, target3)

    # Solve for alpha such that (1 - alpha)*target + alpha*target2 == target3
    # alpha * (target2 - target) = target3 - target  => alpha = 2
    alpha = (target3 - target) / (target2 - target)
    combo = [(Fraction(1, 1) - alpha) * w_f[i] + alpha * w_f2[i] for i in range(n)]
    for i in range(n):
        assert abs(combo[i] - w_f3[i]) < Fraction(1, 1000000000), "Two-fund separation must hold across frontier"


def test_is_tangency() -> None:
    __tracebackhide__ = True
    inst = _get_current_instance()
    _, mu, cov, r_f, _, _, _ = _unpack_fractions(inst)

    w_t = tangency_weights(mu, cov, r_f)
    assert is_tangency(mu, cov, r_f, w_t) is True

    # Bad sum
    bad_sum = [Fraction(2, 1) * x for x in w_t]
    assert is_tangency(mu, cov, r_f, bad_sum) is False


def test_capm_beta() -> None:
    __tracebackhide__ = True
    mkt = [Fraction(1, 100), Fraction(3, 100), Fraction(-2, 100), Fraction(4, 100), Fraction(0, 1)]
    asset = [Fraction(2, 100), Fraction(5, 100), Fraction(-3, 100), Fraction(7, 100), Fraction(1, 100)]

    b = capm_beta(asset, mkt)
    assert isinstance(b, Fraction), "capm_beta must return an exact Fraction"

    # Scale property: beta(c * asset, mkt) == c * beta(asset, mkt)
    c = Fraction(3, 2)
    asset_scaled = [c * a for a in asset]
    assert capm_beta(asset_scaled, mkt) == c * b, "beta must scale linearly with asset return"

    # Scale property: beta(asset, c * mkt) == beta(asset, mkt) / c
    mkt_scaled = [c * m for m in mkt]
    assert capm_beta(asset, mkt_scaled) == b / c, "beta must scale inversely with market return"


def test_jensen_regression() -> None:
    __tracebackhide__ = True
    inst = _get_current_instance()
    _, _, _, _, _, asset_returns, market_returns = _unpack_fractions(inst)

    res = jensen_regression(asset_returns[0], market_returns)
    for key in ("alpha", "beta", "se_alpha", "t_alpha", "residual_variance"):
        assert key in res, f"jensen_regression result missing key '{key}'"

    # Check relation t_alpha = alpha / se_alpha
    if res["se_alpha"] > 0:
        expected_t = res["alpha"] / res["se_alpha"]
        assert abs(res["t_alpha"] - expected_t) < 1e-9, "t_alpha must equal alpha / se_alpha"

    # Permutation invariance: permuting (asset, market) pairs jointly must preserve estimates
    combined = list(zip(asset_returns[0], market_returns, strict=True))
    rng = random.Random(123)
    rng.shuffle(combined)
    perm_a, perm_m = zip(*combined, strict=True)
    res_perm = jensen_regression(list(perm_a), list(perm_m))
    assert abs(res["alpha"] - res_perm["alpha"]) < 1e-9, "Jensen regression must be permutation invariant"
    assert abs(res["beta"] - res_perm["beta"]) < 1e-9, "Jensen regression must be permutation invariant"


def test_security_market_line() -> None:
    __tracebackhide__ = True
    # Exact linear test: mean_excess = 1/20 + 3/20 * beta
    betas = [Fraction(1, 2), Fraction(1, 1), Fraction(3, 2), Fraction(2, 1)]
    gamma_0_true = Fraction(1, 20)
    gamma_1_true = Fraction(3, 20)
    mean_excess = [gamma_0_true + gamma_1_true * b for b in betas]

    g0, g1 = security_market_line(betas, mean_excess)
    assert g0 == gamma_0_true, "SML must recover true intercept on exact linear line"
    assert g1 == gamma_1_true, "SML must recover true slope on exact linear line"


def test_named_exceptions() -> None:
    __tracebackhide__ = True
    # 1. Non-symmetric / non-SPD covariance
    bad_cov1 = [[Fraction(1), Fraction(2)], [Fraction(0), Fraction(1)]]  # non-symmetric
    with pytest.raises(ValueError, match="covariance matrix must be square, symmetric and positive definite"):
        minimum_variance_weights(bad_cov1)

    bad_cov2 = [[Fraction(1), Fraction(2)], [Fraction(2), Fraction(1)]]  # indefinite
    with pytest.raises(ValueError, match="covariance matrix must be square, symmetric and positive definite"):
        minimum_variance_weights(bad_cov2)

    # 2. Equal expected returns for frontier_weights
    cov = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(2)]]
    mu_equal = [Fraction(1, 10), Fraction(1, 10)]
    with pytest.raises(ValueError, match="expected returns must not all be equal"):
        frontier_weights(mu_equal, cov, Fraction(1, 10))

    # 3. Tangency denominator zero
    mu_zero_denom = [Fraction(1, 10), Fraction(-1, 10)]
    with pytest.raises(ValueError, match="no tangency portfolio: excess returns are not identified"):
        tangency_weights(mu_zero_denom, cov, Fraction(0, 1))

    # 4. capm_beta observations
    with pytest.raises(ValueError, match="need matching series of at least two observations"):
        capm_beta([Fraction(1)], [Fraction(1)])

    with pytest.raises(ValueError, match="market variance must be positive"):
        capm_beta([Fraction(1), Fraction(2)], [Fraction(1), Fraction(1)])

    # 5. jensen_regression observations
    with pytest.raises(ValueError, match="need matching series of at least three observations"):
        jensen_regression([0.01, 0.02], [0.01, 0.02])

    with pytest.raises(ValueError, match="market variance must be positive"):
        jensen_regression([0.01, 0.02, 0.03], [0.05, 0.05, 0.05])

    # 6. security_market_line equal betas
    with pytest.raises(ValueError, match="betas must not all be equal"):
        security_market_line([Fraction(1), Fraction(1)], [Fraction(1, 10), Fraction(2, 10)])
