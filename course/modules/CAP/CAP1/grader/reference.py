"""Reference solution for CAP1: Reading, Refereeing & Replicating.

Implements the complete econometric and data pipeline for replication packages:
- CRSP universe and share code filtering
- Delisting return adjustments with Shumway (1997) imputation
- Monthly cross-sectional winsorization
- Portfolio sorting (Equal-Weighted and Value-Weighted spreads)
- Factor regressions with White, Newey-West, and clustered standard errors
- Stepwise replication divergence decomposition
- Verification manifests and cryptographic auditing
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class RegressionResult:
    """Stores estimation results for linear factor regressions."""

    params: NDArray[np.float64]
    bse: NDArray[np.float64]
    tvalues: NDArray[np.float64]
    pvalues: NDArray[np.float64]
    resid: NDArray[np.float64]
    cov: NDArray[np.float64]
    n_obs: int
    r_squared: float


def apply_share_code_filter(
    permnos: NDArray[np.int64 | np.int32],
    shrcd: NDArray[np.int64 | np.int32],
    exchcd: NDArray[np.int64 | np.int32],
    valid_shrcd: Sequence[int] = (10, 11),
    valid_exchcd: Sequence[int] = (1, 2, 3),
) -> NDArray[np.bool_]:
    """Filter stocks for ordinary US common shares on major exchanges.

    Excludes ADRs, REITs, closed-end funds, foreign shares, and OTC issues.
    """
    shrcd_set = set(valid_shrcd)
    exchcd_set = set(valid_exchcd)

    mask_shrcd = np.isin(shrcd, list(shrcd_set))
    mask_exchcd = np.isin(exchcd, list(exchcd_set))
    return np.asarray(mask_shrcd & mask_exchcd, dtype=np.bool_)


def apply_delisting_adjustment(
    ret: NDArray[np.float64],
    dlret: NDArray[np.float64],
    dlstcd: NDArray[np.int64 | np.int32],
    exchcd: NDArray[np.int64 | np.int32],
    default_nyse_ret: float = -0.30,
    default_nasdaq_ret: float = -0.55,
) -> NDArray[np.float64]:
    """Apply Shumway (1997) delisting return adjustments.

    For delisted stocks:
    1. If dlret is observed and finite, compound: (1 + ret) * (1 + dlret) - 1.
    2. If dlret is missing/NaN and dlstcd indicates performance-related delisting
       (500, 520, 551-574, 580, 584), impute -30% for NYSE/AMEX (exchcd 1, 2)
       and -55% for NASDAQ (exchcd 3), then compound.
    3. If dlret is missing and non-performance (e.g. merger/liquidation), use 0.0.
    """
    n = len(ret)
    adjusted = np.copy(ret)

    # Performance delisting codes per Shumway (1997)
    perf_codes = {500, 520, 580, 584}
    for c in range(551, 575):
        perf_codes.add(c)

    for i in range(n):
        code = int(dlstcd[i])
        if code > 0:
            d_ret = dlret[i]
            if np.isnan(d_ret):
                if code in perf_codes:
                    exch = int(exchcd[i])
                    d_ret = default_nasdaq_ret if exch == 3 else default_nyse_ret
                else:
                    d_ret = 0.0
            # Compound return: (1 + ret) * (1 + dlret) - 1
            r_val = ret[i]
            r_base = 0.0 if np.isnan(r_val) else r_val
            adjusted[i] = (1.0 + r_base) * (1.0 + d_ret) - 1.0

    return adjusted


def winsorize_cross_section(
    values: NDArray[np.float64],
    dates: NDArray[np.int64 | np.int32],
    lower_quantile: float = 0.01,
    upper_quantile: float = 0.99,
) -> NDArray[np.float64]:
    """Winsorize values cross-sectionally for each date separately.

    Prevents look-ahead bias inherent in pooled panel winsorization.
    """
    if not 0.0 <= lower_quantile < upper_quantile <= 1.0:
        raise ValueError("Quantiles must satisfy 0 <= lower < upper <= 1")

    out = np.copy(values)
    unique_dates = np.unique(dates)

    for d in unique_dates:
        mask = dates == d
        subset = out[mask]
        valid = ~np.isnan(subset)
        if np.sum(valid) > 2:
            q_low = float(np.quantile(subset[valid], lower_quantile))
            q_high = float(np.quantile(subset[valid], upper_quantile))
            out[mask] = np.clip(subset, q_low, q_high)

    return out


def form_sorted_portfolios(
    signal: NDArray[np.float64],
    ret: NDArray[np.float64],
    me_lag: NDArray[np.float64],
    dates: NDArray[np.int64 | np.int32],
    n_portfolios: int = 5,
    weighting: str = "vw",
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Sort stocks into n_portfolios by signal each month and compute portfolio returns.

    Returns:
        (portfolio_returns, spread_return)
        where portfolio_returns is (T, n_portfolios) and spread_return is (T,)
        representing Long (Portfolio n) minus Short (Portfolio 1).
    """
    unique_dates = np.unique(dates)
    n_dates = len(unique_dates)
    port_rets = np.zeros((n_dates, n_portfolios), dtype=np.float64)

    for t_idx, d in enumerate(unique_dates):
        mask = dates == d
        d_sig = signal[mask]
        d_ret = ret[mask]
        d_me = me_lag[mask]

        valid = (~np.isnan(d_sig)) & (~np.isnan(d_ret)) & (~np.isnan(d_me)) & (d_me > 0)
        v_sig = d_sig[valid]
        v_ret = d_ret[valid]
        v_me = d_me[valid]

        if len(v_sig) < n_portfolios:
            # Fallback if insufficient stocks in date
            continue

        # Compute quantiles/breakpoints
        percentiles = np.linspace(0.0, 100.0, n_portfolios + 1)
        breakpoints = np.percentile(v_sig, percentiles)

        for p in range(n_portfolios):
            if p == n_portfolios - 1:
                p_mask = (v_sig >= breakpoints[p]) & (v_sig <= breakpoints[p + 1])
            else:
                p_mask = (v_sig >= breakpoints[p]) & (v_sig < breakpoints[p + 1])

            if np.any(p_mask):
                if weighting == "vw":
                    weights = v_me[p_mask] / np.sum(v_me[p_mask])
                    port_rets[t_idx, p] = float(np.sum(weights * v_ret[p_mask]))
                else:  # ew
                    port_rets[t_idx, p] = float(np.mean(v_ret[p_mask]))

    spread = port_rets[:, -1] - port_rets[:, 0]
    return port_rets, spread


def estimate_regression(
    y: NDArray[np.float64],
    x_mat: NDArray[np.float64],
    method: str = "ols",
    cluster_entity: NDArray[np.int64 | np.int32] | None = None,
    cluster_time: NDArray[np.int64 | np.int32] | None = None,
    nw_lags: int = 0,
) -> RegressionResult:
    """Estimate linear regression with specified covariance estimator.

    Methods:
    - 'ols': Homoskedastic OLS covariance
    - 'white': White (1980) HC0 heteroskedasticity-consistent covariance
    - 'newey_west': Newey-West (1987) HAC covariance with Bartlett kernel
    - 'cluster_entity': One-way clustered by entity (Petersen 2009)
    - 'cluster_time': One-way clustered by time (Petersen 2009)
    - 'cluster_twoway': Two-way clustered by entity and time (Cameron et al. 2011)
    """
    n, k = x_mat.shape
    if len(y) != n:
        raise ValueError(f"Shape mismatch: y has {len(y)} obs, x_mat has {n}")

    # OLS coefficient estimates: beta = (X'X)^(-1) X'y
    xtx_inv = np.linalg.pinv(x_mat.T @ x_mat)
    params = xtx_inv @ (x_mat.T @ y)
    y_pred = x_mat @ params
    resid = y - y_pred

    ss_tot = np.sum((y - np.mean(y)) ** 2)
    ss_res = np.sum(resid**2)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    if method == "ols":
        s2 = ss_res / max(1, n - k)
        cov = s2 * xtx_inv

    elif method == "white":
        # HC0: (X'X)^(-1) [sum e_i^2 x_i x_i'] (X'X)^(-1)
        meat = (x_mat.T * (resid**2)) @ x_mat
        cov = xtx_inv @ meat @ xtx_inv

    elif method == "newey_west":
        # Newey-West (1987) with Bartlett kernel: gamma_0 + sum_l (1 - l/(L+1)) (gamma_l + gamma_l')
        meat = (x_mat.T * (resid**2)) @ x_mat
        for lag in range(1, nw_lags + 1):
            weight = 1.0 - (lag / (nw_lags + 1.0))
            score_t = x_mat[lag:, :] * resid[lag:, np.newaxis]
            score_lag = x_mat[:-lag, :] * resid[:-lag, np.newaxis]
            gamma_l = score_t.T @ score_lag
            meat += weight * (gamma_l + gamma_l.T)
        cov = xtx_inv @ meat @ xtx_inv

    elif method in ("cluster_entity", "cluster_time", "cluster_twoway"):

        def _calc_cluster_cov(groups: NDArray[np.int64 | np.int32]) -> NDArray[np.float64]:
            unique_g = np.unique(groups)
            g_count = len(unique_g)
            meat_g = np.zeros((k, k), dtype=np.float64)
            for g in unique_g:
                g_idx = groups == g
                score_g = x_mat[g_idx].T @ resid[g_idx]
                meat_g += np.outer(score_g, score_g)
            # Finite-sample degrees of freedom adjustment: G/(G-1) * (N-1)/(N-K)
            df_adj = (g_count / max(1, g_count - 1)) * ((n - 1) / max(1, n - k))
            res_cov: NDArray[np.float64] = np.asarray(df_adj * (xtx_inv @ meat_g @ xtx_inv), dtype=np.float64)
            return res_cov

        if method == "cluster_entity":
            if cluster_entity is None:
                raise ValueError("cluster_entity IDs required for cluster_entity method")
            cov = _calc_cluster_cov(cluster_entity)

        elif method == "cluster_time":
            if cluster_time is None:
                raise ValueError("cluster_time IDs required for cluster_time method")
            cov = _calc_cluster_cov(cluster_time)

        else:  # cluster_twoway
            if cluster_entity is None or cluster_time is None:
                raise ValueError("Both cluster_entity and cluster_time required for twoway clustering")
            cov_e = _calc_cluster_cov(cluster_entity)
            cov_t = _calc_cluster_cov(cluster_time)
            # Intersection clustering
            # Unique pairing of entity and time
            combined = [f"{e}_{t}" for e, t in zip(cluster_entity, cluster_time, strict=False)]
            _, group_ids = np.unique(combined, return_inverse=True)
            cov_et = _calc_cluster_cov(group_ids)
            cov = cov_e + cov_t - cov_et

    else:
        raise ValueError(f"Unknown regression method: {method}")

    # Standard errors
    var_diag = np.maximum(0.0, np.diag(cov))
    bse = np.sqrt(var_diag)
    tvalues = np.zeros_like(params)
    nonzero = bse > 1e-14
    tvalues[nonzero] = params[nonzero] / bse[nonzero]

    # Two-sided normal approximation p-values using complementary error function
    import math

    _erfc_vec = np.vectorize(lambda v: float(math.erfc(abs(float(v)) / 1.4142135623730951)))
    pvalues: NDArray[np.float64] = np.asarray(_erfc_vec(tvalues), dtype=np.float64)

    return RegressionResult(
        params=params,
        bse=bse,
        tvalues=tvalues,
        pvalues=pvalues,
        resid=resid,
        cov=cov,
        n_obs=n,
        r_squared=float(r2),
    )


def decompose_replication_divergence(
    stage_estimates: dict[str, float],
) -> dict[str, float]:
    """Decompose total empirical divergence into sequential stage contributions.

    Given an ordered dict of sequential pipeline estimates:
    stage_estimates = {
        'original': val_0,
        'step1_sample_filter': val_1,
        'step2_delisting': val_2,
        'step3_winsorization': val_3,
        'step4_weighting': val_4,
        'replicated': val_k,
    }

    Computes:
    - Delta for each step: Delta_k = val_k - val_{k-1}
    - Total divergence: Delta_total = val_replicated - val_original
    - Articulation discrepancy: Delta_total - sum(Delta_k) (must equal 0.0)
    """
    keys = list(stage_estimates.keys())
    if len(keys) < 2:
        raise ValueError("At least 2 stages required for divergence decomposition")

    steps: dict[str, float] = {}
    running_sum = 0.0

    for i in range(1, len(keys)):
        prev_k = keys[i - 1]
        curr_k = keys[i]
        diff = stage_estimates[curr_k] - stage_estimates[prev_k]
        steps[f"delta_{curr_k}"] = float(diff)
        running_sum += diff

    orig_val = stage_estimates[keys[0]]
    final_val = stage_estimates[keys[-1]]
    total_delta = final_val - orig_val

    steps["total_divergence"] = float(total_delta)
    steps["articulation_gap"] = float(total_delta - running_sum)
    return steps


def verify_manifest(
    file_hashes: dict[str, str],
    actual_data: dict[str, bytes],
) -> bool:
    """Verify cryptographic integrity of replication package data and outputs."""
    for filename, expected_hash in file_hashes.items():
        if filename not in actual_data:
            return False
        content = actual_data[filename]
        actual_hash = hashlib.sha256(content).hexdigest()
        if actual_hash.lower() != expected_hash.lower():
            return False
    return True
