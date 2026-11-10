"""Lab PR2-project-3: Rung 3 independent project reference benchmark (seed 3).

SIMULATED: generates reference instance for seed 3 and executes the full
Atlas A11 portfolio construction pipeline:
1. Ledoit-Wolf shrinkage covariance.
2. Equal Risk Contribution / risk budgeting.
3. Long-only mean-variance allocation.
4. Volatility targeting with gross leverage capping.
"""

from __future__ import annotations

import random
from typing import Any

import numpy as np
from numpy.typing import NDArray


def make_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    n = 4 + (seed % 3)
    t = 120
    names = [f"Asset_{chr(65 + i)}" for i in range(n)]

    drift = [0.005 + 0.005 * rng.random() for _ in range(n)]
    vol = [0.03 + 0.02 * rng.random() for _ in range(n)]
    beta1 = [0.6 + 0.8 * rng.random() for _ in range(n)]
    beta2 = [-0.3 + 0.6 * rng.random() for _ in range(n)]

    returns: list[list[float]] = []
    for _ in range(t):
        f1 = rng.gauss(0.0, 0.04)
        f2 = rng.gauss(0.0, 0.03)
        row: list[float] = []
        for i in range(n):
            idio = rng.gauss(0.0, vol[i])
            r = drift[i] + beta1[i] * f1 + beta2[i] * f2 + idio
            row.append(round(r, 6))
        returns.append(row)

    risk_aversion = round(2.0 + (seed % 5) * 0.5, 2)
    target_vol = round(0.08 + (seed % 4) * 0.02, 3)
    max_leverage = round(1.5 + (seed % 3) * 0.5, 2)

    raw_b = [1.0] * n if seed % 2 == 0 else [1.0 + (i * 0.5) for i in range(n)]
    tot_b = sum(raw_b)
    budgets = [round(b / tot_b, 6) for b in raw_b]
    budgets[0] += round(1.0 - sum(budgets), 6)

    mean = [round(sum(returns[row_idx][col_idx] for row_idx in range(t)) / t, 6) for col_idx in range(n)]

    return {
        "seed": seed,
        "n_assets": n,
        "n_obs": t,
        "names": names,
        "returns": returns,
        "mean": mean,
        "target_vol": target_vol,
        "risk_aversion": risk_aversion,
        "max_leverage": max_leverage,
        "budgets": budgets,
    }


def shrinkage_covariance(returns: np.ndarray, target: str = "scaled_identity") -> NDArray[np.float64]:
    ret = np.asarray(returns, dtype=np.float64)
    t, n = ret.shape
    mean_ret = np.mean(ret, axis=0)
    centered = ret - mean_ret
    sample_cov = (centered.T @ centered) / (t - 1)

    if target == "scaled_identity":
        mu_var = float(np.trace(sample_cov) / n)
        target_mat = mu_var * np.eye(n, dtype=np.float64)
    elif target == "constant_correlation":
        var = np.diag(sample_cov)
        std = np.sqrt(var)
        corr = sample_cov / np.outer(std, std)
        mean_corr = float((np.sum(corr) - n) / (n * (n - 1)))
        target_mat = mean_corr * np.outer(std, std)
        np.fill_diagonal(target_mat, var)
    else:
        raise ValueError(f"Unknown target {target}")

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
    shrunk = (1.0 - shrinkage) * sample_cov + shrinkage * target_mat
    shrunk_res: NDArray[np.float64] = np.asarray(0.5 * (shrunk + shrunk.T), dtype=np.float64)
    return shrunk_res


def percent_risk_contributions(weights: np.ndarray, cov: np.ndarray) -> NDArray[np.float64]:
    w = np.asarray(weights, dtype=np.float64)
    sigma = np.asarray(cov, dtype=np.float64)
    vol = float(np.sqrt(w @ sigma @ w))
    mrc = (sigma @ w) / vol
    trc = w * mrc
    prc: NDArray[np.float64] = np.asarray(trc / vol, dtype=np.float64)
    return prc


def risk_parity_weights(cov: np.ndarray, budgets: np.ndarray | None = None) -> NDArray[np.float64]:
    sigma = np.asarray(cov, dtype=np.float64)
    n = sigma.shape[0]
    b = np.full(n, 1.0 / n, dtype=np.float64) if budgets is None else np.asarray(budgets, dtype=np.float64)
    b = b / np.sum(b)

    y = 1.0 / np.sqrt(np.diag(sigma))
    for _ in range(500):
        grad = sigma @ y - b / y
        if float(np.max(np.abs(grad))) < 1e-8:
            break
        hessian = sigma + np.diag(b / (y**2))
        delta_y = np.linalg.solve(hessian, -grad)
        step = 1.0
        while np.any(y + step * delta_y <= 0):
            step *= 0.5
        y = y + step * delta_y
    rp_res: NDArray[np.float64] = np.asarray(y / np.sum(y), dtype=np.float64)
    return rp_res


def _project_simplex(v: np.ndarray) -> NDArray[np.float64]:
    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)
    indices = np.arange(1, n + 1)
    cond = u * indices > (cssv - 1.0)
    rho = int(np.nonzero(cond)[0][-1])
    theta = float((cssv[rho] - 1.0) / (rho + 1))
    proj: NDArray[np.float64] = np.asarray(np.maximum(v - theta, 0.0), dtype=np.float64)
    return proj


def mean_variance_long_only(mean: np.ndarray, cov: np.ndarray, risk_aversion: float) -> NDArray[np.float64]:
    mu = np.asarray(mean, dtype=np.float64)
    sigma = np.asarray(cov, dtype=np.float64)
    evals = np.linalg.eigvalsh(sigma)
    lipschitz = risk_aversion * float(evals[-1])
    step_size = 1.0 / lipschitz
    n = len(mu)
    w = np.full(n, 1.0 / n, dtype=np.float64)
    for _ in range(2000):
        grad = risk_aversion * (sigma @ w) - mu
        w_next = _project_simplex(w - step_size * grad)
        if float(np.max(np.abs(w_next - w))) < 1e-9:
            break
        w = w_next
    return w


def volatility_target_weights(
    weights: np.ndarray,
    cov: np.ndarray,
    target_vol: float,
    max_leverage: float | None = None,
) -> NDArray[np.float64]:
    w = np.asarray(weights, dtype=np.float64)
    sigma = np.asarray(cov, dtype=np.float64)
    curr_vol = float(np.sqrt(w @ sigma @ w))
    scale = target_vol / curr_vol
    scaled_w = scale * w
    if max_leverage is not None:
        gross_lev = float(np.sum(np.abs(scaled_w)))
        if gross_lev > max_leverage:
            scaled_w = scaled_w * (max_leverage / gross_lev)
    vt_res: NDArray[np.float64] = np.asarray(scaled_w, dtype=np.float64)
    return vt_res


def main() -> None:
    inst = make_instance(3)
    returns = np.asarray(inst["returns"])
    budgets = np.asarray(inst["budgets"])
    mean = np.asarray(inst["mean"])
    target_vol = float(inst["target_vol"])
    gamma = float(inst["risk_aversion"])
    max_lev = float(inst["max_leverage"])

    shrunk_cov = shrinkage_covariance(returns, target="scaled_identity")
    rp_w = risk_parity_weights(shrunk_cov, budgets=budgets)
    rp_prc = percent_risk_contributions(rp_w, shrunk_cov)
    mv_lo = mean_variance_long_only(mean, shrunk_cov, risk_aversion=gamma)
    vt_w = volatility_target_weights(rp_w, shrunk_cov, target_vol=target_vol, max_leverage=max_lev)
    gross_lev = float(np.sum(np.abs(vt_w)))

    print(f"Shrunk Cov Diagonal: {[round(float(x), 6) for x in np.diag(shrunk_cov)]}")
    print(f"Risk Parity Weights: {[round(float(x), 6) for x in rp_w]}")
    print(f"Risk Parity PRC: {[round(float(x), 6) for x in rp_prc]}")
    print(f"Mean-Variance (Long-Only): {[round(float(x), 6) for x in mv_lo]}")
    print(f"Vol-Target Weights: {[round(float(x), 6) for x in vt_w]}")
    print(f"Vol-Target Gross Leverage: {gross_lev:.4f}")


main()
