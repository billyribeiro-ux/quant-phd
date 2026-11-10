"""volatility_target_weights scales weights by target_vol**2 / curr_vol**2 instead of target_vol / curr_vol."""

from __future__ import annotations

from typing import Any

import numpy as np
from numpy.typing import NDArray


def shrinkage_covariance(
    returns: NDArray[np.float64] | list[list[float]],
    target: str = "scaled_identity",
) -> NDArray[np.float64]:
    ret = np.asarray(returns, dtype=np.float64)
    if ret.ndim != 2:
        raise ValueError(f"returns must be 2-dimensional, got {ret.ndim}D")
    if not np.all(np.isfinite(ret)):
        raise ValueError("returns contains non-finite (NaN or Inf) values")

    t, n = ret.shape
    if t < 3:
        raise ValueError(f"At least 3 observation periods required, got {t}")
    if n < 2:
        raise ValueError(f"At least 2 assets required, got {n}")

    mean_ret = np.mean(ret, axis=0)
    centered = ret - mean_ret
    sample_cov = (centered.T @ centered) / (t - 1)

    if target == "scaled_identity":
        mu_var = float(np.trace(sample_cov) / n)
        target_mat = mu_var * np.eye(n, dtype=np.float64)
    elif target == "constant_correlation":
        var = np.diag(sample_cov)
        if np.any(var <= 0):
            raise ValueError("All asset variances must be positive for constant correlation target")
        std = np.sqrt(var)
        corr = sample_cov / np.outer(std, std)
        mean_corr = float((np.sum(corr) - n) / (n * (n - 1)))
        target_mat = mean_corr * np.outer(std, std)
        np.fill_diagonal(target_mat, var)
    else:
        raise ValueError(f"Unsupported shrinkage target '{target}'")

    d2 = float(np.sum((sample_cov - target_mat) ** 2))
    if d2 < 1e-15:
        sample_res: NDArray[np.float64] = np.asarray(sample_cov, dtype=np.float64)
        return sample_res

    q = np.zeros((n, n), dtype=np.float64)
    for k in range(t):
        dev = np.outer(centered[k], centered[k]) - sample_cov
        q += dev**2
    b2 = float(np.sum(q) / (t**2))

    shrinkage = max(0.0, min(1.0, b2 / d2))
    shrunk: NDArray[np.float64] = (1.0 - shrinkage) * sample_cov + shrinkage * target_mat
    shrunk = 0.5 * (shrunk + shrunk.T)
    return shrunk


def _validate_cov_and_weights(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
) -> tuple[NDArray[np.float64], NDArray[np.float64], int]:
    w = np.asarray(weights, dtype=np.float64)
    sigma = np.asarray(cov, dtype=np.float64)

    if w.ndim != 1:
        raise ValueError("weights must be a 1-dimensional array")
    if sigma.ndim != 2:
        raise ValueError("cov must be a 2-dimensional array")
    if sigma.shape[0] != sigma.shape[1]:
        raise ValueError("cov must be a square matrix")
    if len(w) != sigma.shape[0]:
        raise ValueError(f"weights length ({len(w)}) does not match cov dimension ({sigma.shape[0]})")
    if not np.all(np.isfinite(w)) or not np.all(np.isfinite(sigma)):
        raise ValueError("weights or cov contains non-finite values")
    if not np.allclose(sigma, sigma.T, atol=1e-8):
        raise ValueError("cov matrix must be symmetric")

    return w, sigma, len(w)


def marginal_risk_contributions(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
) -> NDArray[np.float64]:
    w, sigma, _ = _validate_cov_and_weights(weights, cov)
    variance = float(w @ sigma @ w)
    if variance <= 0:
        raise ValueError(f"Portfolio variance must be strictly positive, got {variance:g}")
    vol = np.sqrt(variance)
    mrc: NDArray[np.float64] = (sigma @ w) / vol
    return mrc


def component_risk_contributions(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
) -> NDArray[np.float64]:
    w, _, _ = _validate_cov_and_weights(weights, cov)
    mrc = marginal_risk_contributions(w, cov)
    trc: NDArray[np.float64] = w * mrc
    return trc


def percent_risk_contributions(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
) -> NDArray[np.float64]:
    trc = component_risk_contributions(weights, cov)
    vol = float(np.sum(trc))
    if vol <= 0:
        raise ValueError("Portfolio volatility must be strictly positive")
    prc: NDArray[np.float64] = trc / vol
    return prc


def risk_parity_weights(
    cov: NDArray[np.float64] | list[list[float]],
    budgets: NDArray[np.float64] | list[float] | None = None,
    tol: float = 1e-8,
    max_iter: int = 500,
) -> NDArray[np.float64]:
    sigma = np.asarray(cov, dtype=np.float64)
    if sigma.ndim != 2 or sigma.shape[0] != sigma.shape[1]:
        raise ValueError("cov must be a square 2D matrix")
    if not np.all(np.isfinite(sigma)):
        raise ValueError("cov contains non-finite values")
    if not np.allclose(sigma, sigma.T, atol=1e-8):
        raise ValueError("cov matrix must be symmetric")

    n = sigma.shape[0]
    evals = np.linalg.eigvalsh(sigma)
    if evals[0] <= 1e-12:
        raise ValueError("cov matrix must be strictly positive definite")

    if budgets is None:
        b = np.full(n, 1.0 / n, dtype=np.float64)
    else:
        b = np.asarray(budgets, dtype=np.float64)
        if b.ndim != 1 or len(b) != n:
            raise ValueError(f"budgets must be 1D of length {n}")
        if not np.all(np.isfinite(b)):
            raise ValueError("budgets contains non-finite values")
        if np.any(b <= 0):
            raise ValueError("All risk budgets must be strictly positive")
        if not np.isclose(float(np.sum(b)), 1.0, atol=1e-4):
            raise ValueError("budgets must sum to 1.0")
        b = b / np.sum(b)

    diag_var = np.diag(sigma)
    y = 1.0 / np.sqrt(diag_var)

    def obj_func(curr_y: NDArray[np.float64]) -> float:
        return float(0.5 * (curr_y @ sigma @ curr_y) - np.sum(b * np.log(curr_y)))

    for _ in range(max_iter):
        grad = (sigma @ y) - (b / y)
        if float(np.max(np.abs(grad))) < tol:
            break

        hessian = sigma + np.diag(b / (y**2))
        try:
            delta_y = np.linalg.solve(hessian, -grad)
        except np.linalg.LinAlgError:
            raise ValueError("Hessian inversion failed during risk parity optimization") from None

        step = 1.0
        curr_obj = obj_func(y)
        grad_dot_delta = float(grad @ delta_y)

        while True:
            y_cand = y + step * delta_y
            if np.all(y_cand > 0):
                cand_obj = obj_func(y_cand)
                if cand_obj <= curr_obj + 1e-4 * step * grad_dot_delta:
                    break
            step *= 0.5
            if step < 1e-12:
                break

        y = y + step * delta_y
    else:
        grad = (sigma @ y) - (b / y)
        if float(np.max(np.abs(grad))) > tol * 10:
            raise ValueError("Risk parity optimizer did not converge within max_iter")

    weights: NDArray[np.float64] = y / np.sum(y)
    return weights


def _project_simplex(v: NDArray[np.float64]) -> NDArray[np.float64]:
    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)
    indices = np.arange(1, n + 1)
    cond = u * indices > (cssv - 1.0)
    rho = int(np.nonzero(cond)[0][-1])
    theta = float((cssv[rho] - 1.0) / (rho + 1))
    proj: NDArray[np.float64] = np.maximum(v - theta, 0.0)
    return proj


def mean_variance_weights(
    mean: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
    risk_aversion: float = 1.0,
    long_only: bool = False,
) -> NDArray[np.float64]:
    mu = np.asarray(mean, dtype=np.float64)
    sigma = np.asarray(cov, dtype=np.float64)

    if mu.ndim != 1:
        raise ValueError("mean must be 1-dimensional")
    if sigma.ndim != 2 or sigma.shape[0] != sigma.shape[1]:
        raise ValueError("cov must be a square 2D matrix")
    if len(mu) != sigma.shape[0]:
        raise ValueError("mean length does not match cov dimension")
    if not np.all(np.isfinite(mu)) or not np.all(np.isfinite(sigma)):
        raise ValueError("mean or cov contains non-finite values")
    if not np.allclose(sigma, sigma.T, atol=1e-8):
        raise ValueError("cov matrix must be symmetric")
    if risk_aversion <= 0:
        raise ValueError("risk_aversion must be strictly positive")

    n = len(mu)
    n = sigma.shape[0]
    evals = np.linalg.eigvalsh(sigma)
    if evals[0] <= 1e-12:
        raise ValueError("cov matrix must be strictly positive definite")

    if not long_only:
        inv_sigma = np.linalg.inv(sigma)
        iota = np.ones(n, dtype=np.float64)
        a = float(iota @ inv_sigma @ iota)
        b = float(iota @ inv_sigma @ mu)
        w_unconstrained: NDArray[np.float64] = (1.0 / risk_aversion) * (inv_sigma @ mu) + (
            (1.0 - (b / risk_aversion)) / a
        ) * (inv_sigma @ iota)
        return w_unconstrained

    lipschitz = risk_aversion * float(evals[-1])
    step_size = 1.0 / lipschitz
    w = np.full(n, 1.0 / n, dtype=np.float64)

    for _ in range(2000):
        grad = risk_aversion * (sigma @ w) - mu
        w_next = _project_simplex(w - step_size * grad)
        if float(np.max(np.abs(w_next - w))) < 1e-9:
            break
        w = w_next

    return w


def volatility_target_weights(
    weights: NDArray[np.float64] | list[float],
    cov: NDArray[np.float64] | list[list[float]],
    target_vol: float,
    max_leverage: float | None = None,
) -> NDArray[np.float64]:
    w, sigma, _ = _validate_cov_and_weights(weights, cov)
    if target_vol <= 0:
        raise ValueError(f"target_vol must be strictly positive, got {target_vol}")
    if max_leverage is not None and max_leverage <= 0:
        raise ValueError(f"max_leverage must be strictly positive, got {max_leverage}")

    var = float(w @ sigma @ w)
    if var <= 0:
        raise ValueError("Baseline portfolio variance must be strictly positive")
    curr_vol = np.sqrt(var)

    # Mutant bug: scales by variance ratio instead of standard deviation ratio
    scale_factor = (target_vol**2) / (curr_vol**2)
    scaled_w: NDArray[np.float64] = scale_factor * w

    if max_leverage is not None:
        gross_leverage = float(np.sum(np.abs(scaled_w)))
        if gross_leverage > max_leverage:
            scaled_w = scaled_w * (max_leverage / gross_leverage)

    return scaled_w


def run_benchmark(instance: dict[str, Any]) -> dict[str, Any]:
    returns = np.asarray(instance["returns"], dtype=np.float64)
    budgets = np.asarray(instance["budgets"], dtype=np.float64)
    target_vol = float(instance["target_vol"])
    risk_aversion = float(instance["risk_aversion"])
    max_leverage = float(instance["max_leverage"])
    mean = np.asarray(instance["mean"], dtype=np.float64)

    shrunk_cov = shrinkage_covariance(returns, target="scaled_identity")
    rp_weights = risk_parity_weights(shrunk_cov, budgets=budgets)
    rp_prc = percent_risk_contributions(rp_weights, shrunk_cov)

    mv_weights_lo = mean_variance_weights(mean, shrunk_cov, risk_aversion=risk_aversion, long_only=True)
    vt_weights = volatility_target_weights(rp_weights, shrunk_cov, target_vol, max_leverage=max_leverage)

    return {
        "shrunk_cov_diag": [round(float(x), 6) for x in np.diag(shrunk_cov)],
        "risk_parity_weights": [round(float(x), 6) for x in rp_weights],
        "risk_parity_prc": [round(float(x), 6) for x in rp_prc],
        "mean_variance_long_only": [round(float(x), 6) for x in mv_weights_lo],
        "vol_target_weights": [round(float(x), 6) for x in vt_weights],
        "vol_target_gross_leverage": round(float(np.sum(np.abs(vt_weights))), 4),
    }
