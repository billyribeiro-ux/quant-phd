"""Lab F1-project-2: Rung 2 completion problem twin for Atlas A7.

Fully implements the core cross-sectional sorting and econometric functions
for verification and autograding.
"""

from __future__ import annotations

import numpy as np


def apply_shumway_delisting(
    returns: np.ndarray,
    delist_codes: np.ndarray,
    delist_returns: np.ndarray,
    exchange_codes: np.ndarray,
) -> np.ndarray:
    """Adjust monthly returns for delisting events following Shumway (1997)."""
    ret = np.asarray(returns, dtype=np.float64)
    dl_codes = np.asarray(delist_codes, dtype=np.int32)
    dl_ret = np.asarray(delist_returns, dtype=np.float64)
    ex_codes = np.asarray(exchange_codes, dtype=np.int32)

    n = len(ret)
    if len(dl_codes) != n or len(dl_ret) != n or len(ex_codes) != n:
        raise ValueError("inputs must have identical length")

    adj_returns = np.empty(n, dtype=np.float64)
    for i in range(n):
        code = dl_codes[i]
        r_base = ret[i]
        r_dl = dl_ret[i]
        ex = ex_codes[i]

        if np.isfinite(r_dl):
            adj_returns[i] = (1.0 + r_base) * (1.0 + r_dl) - 1.0
        elif code >= 200:
            is_perf = code == 500 or (520 <= code <= 584)
            penalty = (-0.55 if ex == 3 else -0.30) if is_perf else 0.0
            adj_returns[i] = (1.0 + r_base) * (1.0 + penalty) - 1.0
        else:
            adj_returns[i] = r_base

    return adj_returns


def compute_breakpoints(
    characteristics: np.ndarray,
    exchange_codes: np.ndarray,
    n_quantiles: int = 5,
    use_nyse_only: bool = True,
) -> np.ndarray:
    """Compute quantile breakpoint thresholds, optionally restricted to NYSE."""
    chars = np.asarray(characteristics, dtype=np.float64)
    ex = np.asarray(exchange_codes, dtype=np.int32)
    if n_quantiles < 2:
        raise ValueError("n_quantiles must be at least 2")

    if use_nyse_only:
        nyse_mask = ex == 1
        sub_chars = chars[nyse_mask]
        if len(sub_chars) == 0:
            raise ValueError("no NYSE stocks found")
    else:
        sub_chars = chars

    percentiles = np.linspace(0.0, 100.0, n_quantiles + 1)[1:-1]
    return np.asarray(np.percentile(sub_chars, percentiles), dtype=np.float64)


def univariate_sort(
    returns: np.ndarray,
    signals: np.ndarray,
    market_caps: np.ndarray,
    exchange_codes: np.ndarray,
    n_quantiles: int = 5,
    use_nyse_only: bool = True,
    weighting: str = "value",
) -> dict[str, object]:
    """Sort cross-sectional assets into quantiles and compute portfolio returns."""
    ret = np.asarray(returns, dtype=np.float64)
    sig = np.asarray(signals, dtype=np.float64)
    caps = np.asarray(market_caps, dtype=np.float64)
    ex = np.asarray(exchange_codes, dtype=np.int32)

    if weighting not in ("value", "equal"):
        raise ValueError("weighting must be 'value' or 'equal'")

    cuts = compute_breakpoints(sig, ex, n_quantiles=n_quantiles, use_nyse_only=use_nyse_only)
    assignments = np.digitize(sig, cuts).astype(np.int32)

    port_returns = np.zeros(n_quantiles, dtype=np.float64)
    counts = np.zeros(n_quantiles, dtype=np.int32)

    for q in range(n_quantiles):
        idx = np.where(assignments == q)[0]
        counts[q] = len(idx)
        if len(idx) > 0:
            if weighting == "value":
                w = caps[idx] / np.sum(caps[idx])
                port_returns[q] = float(np.sum(w * ret[idx]))
            else:
                port_returns[q] = float(np.mean(ret[idx]))

    spread_return = float(port_returns[-1] - port_returns[0])
    return {
        "portfolio_returns": port_returns,
        "spread_return": spread_return,
        "counts": counts,
        "breakpoints": cuts,
        "assignments": assignments,
    }


def compute_shanken_se(
    gammas: np.ndarray,
    factor_returns: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Calculate naive and Shanken (1992) corrected standard errors for FM slopes."""
    gam = np.asarray(gammas, dtype=np.float64)
    f_ret = np.asarray(factor_returns, dtype=np.float64)
    t_obs, k_plus_1 = gam.shape
    k_factors = k_plus_1 - 1

    premia = np.mean(gam, axis=0)
    sample_cov = np.cov(gam, rowvar=False, ddof=1)
    naive_se = np.sqrt(np.diag(sample_cov) / float(t_obs))

    sigma_f = np.cov(f_ret, rowvar=False, ddof=1)
    if k_factors == 1:
        sigma_f = np.array([[sigma_f]])

    lambda_f = premia[1:]
    shanken_quad = float(lambda_f.T @ np.linalg.solve(sigma_f, lambda_f))
    c_shanken = 1.0 + shanken_quad

    shanken_cov = c_shanken * sample_cov
    shanken_cov[1:, 1:] += (1.0 / float(t_obs)) * sigma_f
    shanken_se = np.sqrt(np.diag(shanken_cov) / float(t_obs))

    return naive_se, shanken_se, c_shanken


def main() -> None:
    print("Lab F1-project-2 | Completion Problem Verification Twin")
    print("-------------------------------------------------------")
    rng = np.random.default_rng(123)
    n = 60
    ret = rng.normal(0.01, 0.05, size=n)
    dl_codes = np.full(n, 100, dtype=np.int32)
    dl_codes[5] = 500
    dl_ret = np.full(n, np.nan)
    ex = np.array([1 if i < 20 else 3 for i in range(n)], dtype=np.int32)
    caps = rng.uniform(50.0, 500.0, size=n)
    bm = rng.uniform(0.2, 2.0, size=n)

    adj = apply_shumway_delisting(ret, dl_codes, dl_ret, ex)
    cuts = compute_breakpoints(bm, ex, n_quantiles=3, use_nyse_only=True)
    res = univariate_sort(adj, bm, caps, ex, n_quantiles=3, use_nyse_only=True, weighting="value")

    gammas = rng.normal(0.005, 0.02, size=(72, 4))
    factors = rng.normal(0.006, 0.04, size=(72, 3))
    naive_se, shanken_se, c = compute_shanken_se(gammas, factors)

    print(f"Shumway delisted stock 5 return:        {adj[5]:.4f}")
    print(f"Tercile NYSE breakpoints:               {cuts[0]:.4f}, {cuts[1]:.4f}")
    print(f"Value-weighted Q3 - Q1 Spread:          {res['spread_return']:.4f}")
    print(f"Shanken multiplier c:                   {c:.4f}")
    print(f"Naive factor 1 SE:                      {naive_se[1]:.4f}")
    print(f"Shanken factor 1 SE:                    {shanken_se[1]:.4f}")


main()
