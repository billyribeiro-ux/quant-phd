"""Student error: calculates SML intercept with positive sign (sets gamma_0 = mean_y + gamma_1 * mean_b)."""

from __future__ import annotations

import math
from fractions import Fraction


def _check_spd(cov: list[list[Fraction]]) -> None:
    n = len(cov)
    if n == 0 or any(len(row) != n for row in cov):
        raise ValueError("covariance matrix must be square, symmetric and positive definite")
    for i in range(n):
        for j in range(n):
            if cov[i][j] != cov[j][i]:
                raise ValueError("covariance matrix must be square, symmetric and positive definite")

    mat = [[cov[i][j] for j in range(n)] for i in range(n)]
    for i in range(n):
        p = mat[i][i]
        if p <= 0:
            raise ValueError("covariance matrix must be square, symmetric and positive definite")
        for r in range(i + 1, n):
            f = mat[r][i] / p
            for c in range(i, n):
                mat[r][c] -= f * mat[i][c]


def _invert_spd(cov: list[list[Fraction]]) -> list[list[Fraction]]:
    _check_spd(cov)
    n = len(cov)
    aug = [[cov[i][j] for j in range(n)] + [Fraction(1 if i == k else 0) for k in range(n)] for i in range(n)]
    for i in range(n):
        pivot = i
        while pivot < n and aug[pivot][i] == 0:
            pivot += 1
        if pivot == n:
            raise ValueError("covariance matrix must be square, symmetric and positive definite")
        if pivot != i:
            aug[i], aug[pivot] = aug[pivot], aug[i]
        p = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= p
        for r in range(n):
            if r != i:
                f = aug[r][i]
                for j in range(2 * n):
                    aug[r][j] -= f * aug[i][j]
    return [[aug[i][n + j] for j in range(n)] for i in range(n)]


def minimum_variance_weights(cov: list[list[Fraction]]) -> list[Fraction]:
    inv = _invert_spd(cov)
    n = len(cov)
    iota = [Fraction(1, 1) for _ in range(n)]
    unscaled = [sum((inv[i][j] * iota[j] for j in range(n)), Fraction(0, 1)) for i in range(n)]
    denom = sum(unscaled, Fraction(0, 1))
    return [unscaled[i] / denom for i in range(n)]


def tangency_weights(mu: list[Fraction], cov: list[list[Fraction]], r_f: Fraction) -> list[Fraction]:
    _check_spd(cov)
    n = len(cov)
    if len(mu) != n:
        raise ValueError("expected returns vector length must match covariance matrix dimension")
    inv = _invert_spd(cov)
    excess = [mu[i] - r_f for i in range(n)]
    unscaled = [sum((inv[i][j] * excess[j] for j in range(n)), Fraction(0, 1)) for i in range(n)]
    denom = sum(unscaled, Fraction(0, 1))
    if denom == 0:
        raise ValueError("no tangency portfolio: excess returns are not identified")
    return [unscaled[i] / denom for i in range(n)]


def frontier_weights(mu: list[Fraction], cov: list[list[Fraction]], target: Fraction) -> list[Fraction]:
    _check_spd(cov)
    n = len(cov)
    if len(mu) != n:
        raise ValueError("expected returns vector length must match covariance matrix dimension")
    if all(m == mu[0] for m in mu):
        raise ValueError("expected returns must not all be equal")

    inv = _invert_spd(cov)
    iota = [Fraction(1, 1) for _ in range(n)]
    inv_iota = [sum((inv[i][j] * iota[j] for j in range(n)), Fraction(0, 1)) for i in range(n)]
    inv_mu = [sum((inv[i][j] * mu[j] for j in range(n)), Fraction(0, 1)) for i in range(n)]

    scalar_a = sum((iota[i] * inv_iota[i] for i in range(n)), Fraction(0, 1))
    scalar_b = sum((iota[i] * inv_mu[i] for i in range(n)), Fraction(0, 1))
    scalar_c = sum((mu[i] * inv_mu[i] for i in range(n)), Fraction(0, 1))
    scalar_d = scalar_a * scalar_c - scalar_b * scalar_b
    if scalar_d <= 0:
        raise ValueError("expected returns must not all be equal")

    lambda1 = (scalar_c - scalar_b * target) / scalar_d
    lambda2 = (scalar_a * target - scalar_b) / scalar_d
    return [lambda1 * inv_iota[i] + lambda2 * inv_mu[i] for i in range(n)]


def is_tangency(mu: list[Fraction], cov: list[list[Fraction]], r_f: Fraction, weights: list[Fraction]) -> bool:
    n = len(cov)
    if len(mu) != n or len(weights) != n:
        return False
    if sum(weights, Fraction(0, 1)) != Fraction(1, 1):
        return False

    excess = [mu[i] - r_f for i in range(n)]
    if all(e == Fraction(0, 1) for e in excess):
        return False

    sig_w = [sum((cov[i][j] * weights[j] for j in range(n)), Fraction(0, 1)) for i in range(n)]
    first_idx = next(i for i in range(n) if excess[i] != 0)
    if sig_w[first_idx] == 0:
        return False
    k = sig_w[first_idx] / excess[first_idx]
    if k == 0:
        return False

    return all(sig_w[i] == k * excess[i] for i in range(n))


def capm_beta(asset: list[Fraction], market: list[Fraction]) -> Fraction:
    if len(asset) != len(market) or len(asset) < 2:
        raise ValueError("need matching series of at least two observations")
    t_obs = len(asset)
    mean_m = sum(market, Fraction(0, 1)) / Fraction(t_obs, 1)
    mean_a = sum(asset, Fraction(0, 1)) / Fraction(t_obs, 1)

    s_mm = sum(((m - mean_m) ** 2 for m in market), Fraction(0, 1))
    if s_mm == 0:
        raise ValueError("market variance must be positive")
    s_am = sum(((market[t] - mean_m) * (asset[t] - mean_a) for t in range(t_obs)), Fraction(0, 1))
    return s_am / s_mm


def jensen_regression(asset: list[float], market: list[float]) -> dict[str, float]:
    if len(asset) != len(market) or len(asset) < 3:
        raise ValueError("need matching series of at least three observations")
    t_obs = len(asset)
    mean_m = sum(market) / float(t_obs)
    mean_a = sum(asset) / float(t_obs)

    s_mm = sum((m - mean_m) ** 2 for m in market)
    if s_mm <= 1e-12:
        raise ValueError("market variance must be positive")
    s_am = sum((market[t] - mean_m) * (asset[t] - mean_a) for t in range(t_obs))

    beta = s_am / s_mm
    alpha = mean_a - beta * mean_m

    residuals = [asset[t] - (alpha + beta * market[t]) for t in range(t_obs)]
    sse = sum(e * e for e in residuals)
    df = t_obs - 2
    residual_variance = sse / float(df)

    var_alpha = residual_variance * (1.0 / float(t_obs) + (mean_m * mean_m) / s_mm)
    se_alpha = math.sqrt(var_alpha) if var_alpha > 0 else 0.0
    t_alpha = (alpha / se_alpha) if se_alpha > 0 else 0.0

    return {
        "alpha": float(alpha),
        "beta": float(beta),
        "se_alpha": float(se_alpha),
        "t_alpha": float(t_alpha),
        "residual_variance": float(residual_variance),
    }


def security_market_line(betas: list[Fraction], mean_excess: list[Fraction]) -> tuple[Fraction, Fraction]:
    if len(betas) != len(mean_excess) or len(betas) < 2:
        raise ValueError("need matching series of at least two observations")
    if all(b == betas[0] for b in betas):
        raise ValueError("betas must not all be equal")

    n = len(betas)
    mean_b = sum(betas, Fraction(0, 1)) / Fraction(n, 1)
    mean_y = sum(mean_excess, Fraction(0, 1)) / Fraction(n, 1)

    s_bb = sum(((b - mean_b) ** 2 for b in betas), Fraction(0, 1))
    if s_bb == 0:
        raise ValueError("betas must not all be equal")
    s_by = sum(((betas[i] - mean_b) * (mean_excess[i] - mean_y) for i in range(n)), Fraction(0, 1))

    gamma_1 = s_by / s_bb
    # Bug: plus instead of minus
    gamma_0 = mean_y + gamma_1 * mean_b
    return (gamma_0, gamma_1)
