"""Reference solution for Atlas A7: cross-sectional engine (atlas.cross_section).

Delivers:
- apply_shumway_delisting
- compute_breakpoints
- univariate_sort
- bivariate_sort
- fama_macbeth
- grs_test
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np
import scipy.stats


class FMResult(NamedTuple):
    """Container for Fama-MacBeth cross-sectional estimation results."""

    premia: np.ndarray
    naive_se: np.ndarray
    shanken_se: np.ndarray
    t_stat_naive: np.ndarray
    t_stat_shanken: np.ndarray


class GRSResult(NamedTuple):
    """Container for Gibbons-Ross-Shanken (1989) test results."""

    stat: float
    p_value: float
    df_num: int
    df_denom: int


def _validate_numeric_1d(arr: np.ndarray, name: str) -> np.ndarray:
    """Validate that input is a 1D finite numeric numpy array."""
    out = np.asarray(arr, dtype=np.float64)
    if out.ndim != 1:
        raise ValueError(f"{name} must be a 1D array")
    if not np.all(np.isfinite(out)):
        raise ValueError(f"{name} contains non-finite values (NaN or Inf)")
    return out


def apply_shumway_delisting(
    returns: np.ndarray,
    delist_codes: np.ndarray,
    delist_returns: np.ndarray,
    exchange_codes: np.ndarray,
) -> np.ndarray:
    """Adjust monthly returns for delisting events following Shumway (1997).

    Parameters:
        returns: (N,) float64 ndarray of standard monthly returns before delisting.
        delist_codes: (N,) int32 ndarray of CRSP delisting codes (100 = active).
        delist_returns: (N,) float64 ndarray of recorded delisting returns (may contain NaN).
        exchange_codes: (N,) int32 ndarray of exchange codes (1=NYSE, 2=AMEX, 3=NASDAQ).

    Returns:
        (N,) float64 ndarray of total compounded returns: (1 + r) * (1 + r_dl) - 1.
    """
    ret = np.asarray(returns, dtype=np.float64)
    dl_codes = np.asarray(delist_codes, dtype=np.int32)
    dl_ret = np.asarray(delist_returns, dtype=np.float64)
    ex_codes = np.asarray(exchange_codes, dtype=np.int32)

    n = len(ret)
    if len(dl_codes) != n or len(dl_ret) != n or len(ex_codes) != n:
        raise ValueError("all inputs to apply_shumway_delisting must have identical length")
    if not np.all(np.isfinite(ret)):
        raise ValueError("raw returns must contain only finite numbers")

    adj_returns = np.empty(n, dtype=np.float64)

    for i in range(n):
        code = dl_codes[i]
        r_base = ret[i]
        r_dl = dl_ret[i]
        ex = ex_codes[i]

        if np.isfinite(r_dl):
            # Explicit delisting return is available in CRSP
            adj_returns[i] = (1.0 + r_base) * (1.0 + r_dl) - 1.0
        elif code >= 200:
            # Delisting occurred with missing return
            is_performance = code == 500 or (520 <= code <= 584)
            replacement = (-0.55 if ex == 3 else -0.30) if is_performance else 0.0
            adj_returns[i] = (1.0 + r_base) * (1.0 + replacement) - 1.0
        else:
            # Normal active stock
            adj_returns[i] = r_base

    return adj_returns


def compute_breakpoints(
    characteristics: np.ndarray,
    exchange_codes: np.ndarray,
    n_quantiles: int = 5,
    use_nyse_only: bool = True,
) -> np.ndarray:
    """Compute quantile breakpoint thresholds, optionally restricted to NYSE.

    Parameters:
        characteristics: (N,) float64 ndarray of sorting signals.
        exchange_codes: (N,) int32 ndarray of exchange identifiers (1=NYSE).
        n_quantiles: integer number of quantile bins (must be >= 2).
        use_nyse_only: if True, breakpoints are evaluated on NYSE stocks (code 1) only.

    Returns:
        (n_quantiles - 1,) float64 ndarray of strictly ascending breakpoint thresholds.
    """
    chars = _validate_numeric_1d(characteristics, "characteristics")
    ex = np.asarray(exchange_codes, dtype=np.int32)
    if len(chars) != len(ex):
        raise ValueError("characteristics and exchange_codes must have identical length")
    if n_quantiles < 2:
        raise ValueError("n_quantiles must be at least 2")

    if use_nyse_only:
        nyse_mask = ex == 1
        sub_chars = chars[nyse_mask]
        if len(sub_chars) == 0:
            raise ValueError("no valid NYSE securities found for breakpoint computation")
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
    """Sort cross-sectional assets into quantiles based on a single characteristic.

    Parameters:
        returns: (N,) float64 ndarray of asset returns.
        signals: (N,) float64 ndarray of sorting signals.
        market_caps: (N,) float64 ndarray of firm market capitalizations.
        exchange_codes: (N,) int32 ndarray of exchange identifiers (1=NYSE).
        n_quantiles: number of portfolios (e.g. 5 for quintiles, 10 for deciles).
        use_nyse_only: whether to calculate breakpoints using NYSE stocks only.
        weighting: "value" for market-cap weighting or "equal" for equal weighting.

    Returns:
        dict containing:
            - portfolio_returns: (n_quantiles,) float64 ndarray
            - spread_return: float (high minus low, port[n_quantiles-1] - port[0])
            - counts: (n_quantiles,) int32 ndarray of stock counts per bin
            - breakpoints: (n_quantiles - 1,) float64 ndarray of applied thresholds
            - assignments: (N,) int32 ndarray of portfolio indices (0 to n_quantiles-1)
    """
    ret = _validate_numeric_1d(returns, "returns")
    sig = _validate_numeric_1d(signals, "signals")
    caps = _validate_numeric_1d(market_caps, "market_caps")
    ex = np.asarray(exchange_codes, dtype=np.int32)

    n = len(ret)
    if len(sig) != n or len(caps) != n or len(ex) != n:
        raise ValueError("all array inputs to univariate_sort must have identical length")
    if np.any(caps <= 0.0):
        raise ValueError("market_caps must be strictly positive")
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


def bivariate_sort(
    returns: np.ndarray,
    signal1: np.ndarray,
    signal2: np.ndarray,
    market_caps: np.ndarray,
    exchange_codes: np.ndarray,
    n_quantiles1: int = 2,
    n_quantiles2: int = 3,
    method: str = "independent",
    use_nyse_only: bool = True,
    weighting: str = "value",
) -> dict[str, object]:
    """Perform independent or conditional bivariate 2D portfolio sorts.

    Parameters:
        returns: (N,) float64 ndarray of asset returns.
        signal1: (N,) float64 ndarray of first characteristic (e.g. Size).
        signal2: (N,) float64 ndarray of second characteristic (e.g. Value).
        market_caps: (N,) float64 ndarray of firm market capitalizations.
        exchange_codes: (N,) int32 ndarray of exchange identifiers.
        n_quantiles1: bins along signal 1 (e.g. 2 for Small/Big).
        n_quantiles2: bins along signal 2 (e.g. 3 for Low/Neutral/High).
        method: "independent" or "conditional".
        use_nyse_only: whether breakpoints for signal1 (and signal2 if independent) use NYSE only.
        weighting: "value" or "equal".

    Returns:
        dict containing:
            - grid_returns: (n_quantiles1, n_quantiles2) float64 ndarray
            - counts: (n_quantiles1, n_quantiles2) int32 ndarray
            - factor_hml: float (average high minus low across signal1 rows)
            - factor_smb: float (average small minus big across signal2 columns)
    """
    ret = _validate_numeric_1d(returns, "returns")
    s1 = _validate_numeric_1d(signal1, "signal1")
    s2 = _validate_numeric_1d(signal2, "signal2")
    caps = _validate_numeric_1d(market_caps, "market_caps")
    ex = np.asarray(exchange_codes, dtype=np.int32)

    n = len(ret)
    if len(s1) != n or len(s2) != n or len(caps) != n or len(ex) != n:
        raise ValueError("all array inputs to bivariate_sort must have identical length")
    if np.any(caps <= 0.0):
        raise ValueError("market_caps must be strictly positive")
    if method not in ("independent", "conditional"):
        raise ValueError("method must be 'independent' or 'conditional'")
    if weighting not in ("value", "equal"):
        raise ValueError("weighting must be 'value' or 'equal'")

    cuts1 = compute_breakpoints(s1, ex, n_quantiles=n_quantiles1, use_nyse_only=use_nyse_only)
    assign1 = np.digitize(s1, cuts1).astype(np.int32)
    assign2 = np.empty(n, dtype=np.int32)

    if method == "independent":
        cuts2 = compute_breakpoints(s2, ex, n_quantiles=n_quantiles2, use_nyse_only=use_nyse_only)
        assign2 = np.digitize(s2, cuts2).astype(np.int32)
    else:  # conditional: sort signal2 conditionally within each signal1 bucket
        for q1 in range(n_quantiles1):
            mask_q1 = assign1 == q1
            sub_s2 = s2[mask_q1]
            sub_ex = ex[mask_q1]
            if len(sub_s2) < n_quantiles2:
                raise ValueError(f"insufficient assets in bucket {q1} for conditional sort")
            # In conditional sorts within size buckets, breakpoints are computed on bucket members
            cuts2_cond = compute_breakpoints(sub_s2, sub_ex, n_quantiles=n_quantiles2, use_nyse_only=False)
            assign2[mask_q1] = np.digitize(sub_s2, cuts2_cond).astype(np.int32)

    grid_returns = np.zeros((n_quantiles1, n_quantiles2), dtype=np.float64)
    counts = np.zeros((n_quantiles1, n_quantiles2), dtype=np.int32)

    for i in range(n_quantiles1):
        for j in range(n_quantiles2):
            idx = np.where((assign1 == i) & (assign2 == j))[0]
            counts[i, j] = len(idx)
            if len(idx) > 0:
                if weighting == "value":
                    w = caps[idx] / np.sum(caps[idx])
                    grid_returns[i, j] = float(np.sum(w * ret[idx]))
                else:
                    grid_returns[i, j] = float(np.mean(ret[idx]))

    # Standard Fama-French style factor spreads:
    # HML (signal2 high minus low averaged across signal1):
    hml_spreads = [grid_returns[i, -1] - grid_returns[i, 0] for i in range(n_quantiles1)]
    factor_hml = float(np.mean(hml_spreads))

    # SMB (signal1 low minus high averaged across signal2):
    smb_spreads = [grid_returns[0, j] - grid_returns[-1, j] for j in range(n_quantiles2)]
    factor_smb = float(np.mean(smb_spreads))

    return {
        "grid_returns": grid_returns,
        "counts": counts,
        "factor_hml": factor_hml,
        "factor_smb": factor_smb,
    }


def fama_macbeth(
    excess_returns: np.ndarray,
    loadings: np.ndarray,
    factor_returns: np.ndarray | None = None,
) -> FMResult:
    """Execute two-pass Fama-MacBeth regressions with Shanken (1992) correction.

    Parameters:
        excess_returns: (T, N) float64 ndarray of asset excess returns.
        loadings: (N, K) float64 ndarray of estimated factor loadings (betas).
        factor_returns: (T, K) float64 ndarray of factor returns (for Shanken correction).

    Returns:
        FMResult containing:
            - premia: (K + 1,) array [intercept, lambda_1, ..., lambda_K]
            - naive_se: (K + 1,) naive sample standard errors of the mean slopes
            - shanken_se: (K + 1,) Shanken (1992) corrected standard errors
            - t_stat_naive: (K + 1,) naive t-statistics
            - t_stat_shanken: (K + 1,) Shanken t-statistics
    """
    excess = np.asarray(excess_returns, dtype=np.float64)
    betas = np.asarray(loadings, dtype=np.float64)

    if excess.ndim != 2 or betas.ndim != 2:
        raise ValueError("excess_returns and loadings must be 2D arrays")
    if not (np.all(np.isfinite(excess)) and np.all(np.isfinite(betas))):
        raise ValueError("inputs must contain only finite numbers")

    t_months, n_assets = excess.shape
    n_betas, k_factors = betas.shape

    if n_assets != n_betas:
        raise ValueError("columns of excess_returns (N) must match rows of loadings")
    if n_assets <= k_factors + 1:
        raise ValueError("insufficient assets for cross-sectional regression (N <= K + 1)")
    if t_months < 3:
        raise ValueError("insufficient time periods (T < 3)")

    # Cross-sectional design matrix: [1, betas] of shape (N, K + 1)
    x_cs = np.column_stack([np.ones(n_assets, dtype=np.float64), betas])
    x_t_x = x_cs.T @ x_cs
    x_t_x_inv = np.linalg.inv(x_t_x)

    # Monthly cross-sectional slopes: gammas of shape (T, K + 1)
    gammas = np.empty((t_months, k_factors + 1), dtype=np.float64)
    for t in range(t_months):
        r_t = excess[t]
        gammas[t] = x_t_x_inv @ (x_cs.T @ r_t)

    # Time series average risk premia
    premia = np.asarray(np.mean(gammas, axis=0), dtype=np.float64)

    # Naive covariance of slopes: (1 / (T - 1)) sum (gamma_t - mean_gamma)^2
    sample_cov = np.cov(gammas, rowvar=False, ddof=1)
    if k_factors == 0:
        sample_cov = np.array([[sample_cov]])
    naive_se = np.sqrt(np.diag(sample_cov) / float(t_months))

    # Shanken (1992) errors-in-variables correction
    if factor_returns is not None:
        f_ret = np.asarray(factor_returns, dtype=np.float64)
        if f_ret.shape != (t_months, k_factors):
            raise ValueError("factor_returns must have shape (T, K)")
        if not np.all(np.isfinite(f_ret)):
            raise ValueError("factor_returns must contain only finite values")

        sigma_f = np.cov(f_ret, rowvar=False, ddof=1)
        if k_factors == 1:
            sigma_f = np.array([[sigma_f]])

        # Factor premia vector lambda_f (excluding intercept)
        lambda_f = premia[1:]
        shanken_quad = float(lambda_f.T @ np.linalg.solve(sigma_f, lambda_f))
        c_shanken = 1.0 + shanken_quad

        # Shanken asymptotic variance: c * sample_cov + (1/T) * [0 0; 0 Sigma_f]
        shanken_cov = c_shanken * sample_cov
        shanken_cov[1:, 1:] += (1.0 / float(t_months)) * sigma_f
        shanken_se = np.sqrt(np.diag(shanken_cov) / float(t_months))
    else:
        shanken_se = np.copy(naive_se)

    t_stat_naive = premia / naive_se
    t_stat_shanken = premia / shanken_se

    return FMResult(
        premia=premia,
        naive_se=naive_se,
        shanken_se=shanken_se,
        t_stat_naive=t_stat_naive,
        t_stat_shanken=t_stat_shanken,
    )


def grs_test(
    alphas: np.ndarray,
    residuals: np.ndarray,
    factor_returns: np.ndarray,
) -> GRSResult:
    """Compute the Gibbons-Ross-Shanken (1989) test statistic and p-value.

    Parameters:
        alphas: (N,) float64 ndarray of estimated pricing errors.
        residuals: (T, N) float64 ndarray of regression residuals.
        factor_returns: (T, K) float64 ndarray of benchmark factor returns.

    Returns:
        GRSResult containing:
            - stat: float GRS F-statistic
            - p_value: float upper tail p-value from F(N, T - N - K)
            - df_num: int degrees of freedom numerator (N)
            - df_denom: int degrees of freedom denominator (T - N - K)
    """
    a = _validate_numeric_1d(alphas, "alphas")
    res = np.asarray(residuals, dtype=np.float64)
    factors = np.asarray(factor_returns, dtype=np.float64)

    if res.ndim != 2 or factors.ndim != 2:
        raise ValueError("residuals and factor_returns must be 2D arrays")
    if not (np.all(np.isfinite(res)) and np.all(np.isfinite(factors))):
        raise ValueError("residuals and factor_returns must contain only finite numbers")

    t_obs, n_assets = res.shape
    t_f, k_factors = factors.shape

    if len(a) != n_assets:
        raise ValueError("length of alphas must match columns of residuals (N)")
    if t_obs != t_f:
        raise ValueError("rows of residuals and factor_returns must match (T)")

    df_num = n_assets
    df_denom = t_obs - n_assets - k_factors

    if df_denom <= 0:
        raise ValueError(f"degrees of freedom non-positive: T ({t_obs}) <= N ({n_assets}) + K ({k_factors})")

    # 1. Factor mean and sample covariance matrix
    mu_f = np.mean(factors, axis=0)
    sigma_f = np.cov(factors, rowvar=False, ddof=1)
    if k_factors == 1:
        sigma_f = np.array([[sigma_f]])

    # 2. Unbiased residual covariance matrix: E' E / (T - K - 1)
    sigma_e = (res.T @ res) / float(t_obs - k_factors - 1)

    # 3. Quadratic forms
    sh2_f = float(mu_f.T @ np.linalg.solve(sigma_f, mu_f))
    a_inv_a = float(a.T @ np.linalg.solve(sigma_e, a))

    # 4. GRS F-statistic
    scale = float(t_obs - n_assets - k_factors) / float(n_assets)
    sh_adj = 1.0 / (1.0 + sh2_f)
    grs_stat = scale * sh_adj * a_inv_a

    # 5. Upper-tail p-value from F(N, T - N - K)
    p_val = float(scipy.stats.f.sf(grs_stat, dfn=df_num, dfd=df_denom))

    return GRSResult(
        stat=float(grs_stat),
        p_value=p_val,
        df_num=df_num,
        df_denom=df_denom,
    )
