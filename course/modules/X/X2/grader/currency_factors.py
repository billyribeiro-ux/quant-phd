"""Reference solution for X2 project: Currency factor replication (currency_factors.py).

Implements:
- Currency excess return calculations
- Forward discount sorting into carry portfolios
- Lustig, Roussanov & Verdelhan (2011) Dollar and HML-FX factors
- Menkhoff, Sarno, Schmeling & Schrimpf (2012) global FX volatility innovations
- Two-pass Fama-MacBeth cross-sectional asset pricing regressions
"""

from __future__ import annotations

import math
from typing import Any


def _solve_linear_system(a_matrix: list[list[float]], b_vector: list[float]) -> list[float]:
    """Solve A x = b using Gaussian elimination with partial pivoting."""
    n = len(b_vector)
    # Make augmented matrix [A | b]
    aug = [[*row[:], b_vector[i]] for i, row in enumerate(a_matrix)]

    for col in range(n):
        # Pivot selection
        max_row = col
        max_val = abs(aug[col][col])
        for row in range(col + 1, n):
            if abs(aug[row][col]) > max_val:
                max_val = abs(aug[row][col])
                max_row = row
        if max_val < 1e-12:
            raise ValueError("Matrix is singular or near-singular in linear system solver")
        aug[col], aug[max_row] = aug[max_row], aug[col]

        pivot = aug[col][col]
        for c in range(col, n + 1):
            aug[col][c] /= pivot

        for row in range(n):
            if row != col:
                factor = aug[row][col]
                for c in range(col, n + 1):
                    aug[row][c] -= factor * aug[col][c]

    return [aug[i][n] for i in range(n)]


def _multivariate_ols(
    x_matrix: list[list[float]],
    y_vector: list[float],
    fit_intercept: bool = True,
) -> tuple[list[float], list[float], float]:
    """Run multivariate OLS of y on X.

    Returns:
        tuple of (coefficients, fitted_values, r_squared)
    """
    t_obs = len(y_vector)
    p_vars = len(x_matrix[0]) if x_matrix else 0

    if fit_intercept:
        design = [[1.0, *row] for row in x_matrix]
        num_params = p_vars + 1
    else:
        design = [row[:] for row in x_matrix]
        num_params = p_vars

    # Compute X'X (num_params x num_params) and X'y (num_params)
    xt_x = [[0.0] * num_params for _ in range(num_params)]
    xt_y = [0.0] * num_params

    for t in range(t_obs):
        row = design[t]
        y_val = y_vector[t]
        for i in range(num_params):
            xt_y[i] += row[i] * y_val
            for j in range(num_params):
                xt_x[i][j] += row[i] * row[j]

    coeffs = _solve_linear_system(xt_x, xt_y)

    fitted: list[float] = []
    for t in range(t_obs):
        pred = sum(design[t][i] * coeffs[i] for i in range(num_params))
        fitted.append(pred)

    y_mean = sum(y_vector) / t_obs
    ss_tot = sum((y - y_mean) ** 2 for y in y_vector)
    ss_res = sum((y - fitted[t]) ** 2 for t, y in enumerate(y_vector))

    r_squared = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-12 else 0.0
    return coeffs, fitted, r_squared


def compute_excess_returns(
    spot_rates: list[list[float]],
    forward_rates: list[list[float]],
) -> list[list[float]]:
    """Compute log currency excess returns: rx_{t+1, j} = ln(S_{t+1, j}) - ln(F_{t, j}).

    Args:
        spot_rates: List of shape (T, N) where spot_rates[t][j] is USD per unit of foreign currency j.
        forward_rates: List of shape (T, N) where forward_rates[t][j] is 1-month forward rate.

    Returns:
        List of shape (T-1, N) containing monthly log excess returns.
    """
    if not spot_rates or not forward_rates:
        raise ValueError("spot_rates and forward_rates must be non-empty")
    t_obs = len(spot_rates)
    if t_obs < 2:
        raise ValueError("At least 2 periods required to compute excess returns")
    if len(forward_rates) != t_obs:
        raise ValueError("spot_rates and forward_rates must have identical length")

    n_cur = len(spot_rates[0])
    if n_cur < 2:
        raise ValueError("At least 2 currencies required")
    if any(len(row) != n_cur for row in spot_rates) or any(len(row) != n_cur for row in forward_rates):
        raise ValueError("spot_rates and forward_rates must have consistent columns")

    excess_returns: list[list[float]] = []
    for t in range(t_obs - 1):
        month_rx: list[float] = []
        for j in range(n_cur):
            s_next = spot_rates[t + 1][j]
            f_curr = forward_rates[t][j]
            if s_next <= 0.0 or f_curr <= 0.0:
                raise ValueError("Spot and forward rates must be strictly positive")
            rx = math.log(s_next) - math.log(f_curr)
            month_rx.append(round(rx, 6))
        excess_returns.append(month_rx)

    return excess_returns


def compute_forward_discounts(
    spot_rates: list[list[float]],
    forward_rates: list[list[float]],
) -> list[list[float]]:
    """Compute log forward discounts: fd_{t, j} = ln(F_{t, j}) - ln(S_{t, j}).

    Under covered interest parity, fd_{t, j} approx i_{t, USD} - i_{t, j}^*.
    Currencies with lower fd have higher foreign interest rates.

    Args:
        spot_rates: List of shape (T, N).
        forward_rates: List of shape (T, N).

    Returns:
        List of shape (T-1, N) containing forward discounts at start of each return period.
    """
    if not spot_rates or not forward_rates:
        raise ValueError("spot_rates and forward_rates must be non-empty")
    t_obs = len(spot_rates)
    n_cur = len(spot_rates[0])

    forward_discounts: list[list[float]] = []
    for t in range(t_obs - 1):
        month_fd: list[float] = []
        for j in range(n_cur):
            s_curr = spot_rates[t][j]
            f_curr = forward_rates[t][j]
            if s_curr <= 0.0 or f_curr <= 0.0:
                raise ValueError("Spot and forward rates must be strictly positive")
            fd = math.log(f_curr) - math.log(s_curr)
            month_fd.append(round(fd, 6))
        forward_discounts.append(month_fd)

    return forward_discounts


def sort_carry_portfolios(
    excess_returns: list[list[float]],
    forward_discounts: list[list[float]],
    n_portfolios: int = 5,
) -> dict[str, Any]:
    """Sort currencies into carry portfolios based on forward discounts at time t.

    Following Lustig et al. (2011):
    - Currencies are sorted in descending order of forward discount (ascending order of foreign interest rate).
    - Portfolio 1 contains currencies with highest fd (lowest foreign interest rate, funding currencies).
    - Portfolio K contains currencies with lowest fd (highest foreign interest rate, target currencies).

    Args:
        excess_returns: List of shape (T-1, N).
        forward_discounts: List of shape (T-1, N).
        n_portfolios: Number of sorted portfolios (e.g. 5 quintiles).

    Returns:
        dict containing:
            portfolio_returns: List of shape (T-1, K) of monthly portfolio excess returns
            mean_returns: List of length K of annualized mean returns
            std_returns: List of length K of annualized standard deviations
            sharpe_ratios: List of length K of annualized Sharpe ratios
    """
    if n_portfolios < 2:
        raise ValueError("n_portfolios must be at least 2")
    if not excess_returns or not forward_discounts:
        raise ValueError("excess_returns and forward_discounts must be non-empty")
    t_ret = len(excess_returns)
    if len(forward_discounts) != t_ret:
        raise ValueError("excess_returns and forward_discounts dimensions must match")

    n_cur = len(excess_returns[0])
    if n_portfolios > n_cur:
        raise ValueError("n_portfolios cannot exceed number of currencies")

    portfolio_returns: list[list[float]] = []

    for t in range(t_ret):
        fds = forward_discounts[t]
        rxs = excess_returns[t]

        # Rank currencies:
        # Highest forward discount (lowest interest rate) -> Portfolio 0 (P1)
        # Lowest forward discount (highest interest rate) -> Portfolio K-1 (PK)
        # Sort indices by fd in descending order
        ranked_indices = sorted(range(n_cur), key=lambda j: fds[j], reverse=True)

        # Split into n_portfolios groups
        p_rets: list[float] = [0.0] * n_portfolios
        p_counts: list[int] = [0] * n_portfolios

        for rank_pos, cur_idx in enumerate(ranked_indices):
            # Bucket: 0 to n_portfolios - 1
            bucket = min(int(rank_pos * n_portfolios / n_cur), n_portfolios - 1)
            p_rets[bucket] += rxs[cur_idx]
            p_counts[bucket] += 1

        month_p = [round(p_rets[k] / p_counts[k], 6) for k in range(n_portfolios)]
        portfolio_returns.append(month_p)

    # Compute annualized statistics
    mean_returns: list[float] = []
    std_returns: list[float] = []
    sharpe_ratios: list[float] = []

    for k in range(n_portfolios):
        k_rets = [portfolio_returns[t][k] for t in range(t_ret)]
        m_ret = sum(k_rets) / t_ret
        var_ret = sum((r - m_ret) ** 2 for r in k_rets) / (t_ret - 1) if t_ret > 1 else 0.0
        s_ret = math.sqrt(max(0.0, var_ret))

        # Annualization: 12 months per year
        ann_mean = m_ret * 12.0
        ann_std = s_ret * math.sqrt(12.0)
        ann_sr = (ann_mean / ann_std) if ann_std > 1e-8 else 0.0

        mean_returns.append(round(ann_mean, 5))
        std_returns.append(round(ann_std, 5))
        sharpe_ratios.append(round(ann_sr, 4))

    return {
        "portfolio_returns": portfolio_returns,
        "mean_returns": mean_returns,
        "std_returns": std_returns,
        "sharpe_ratios": sharpe_ratios,
    }


def build_factors(portfolio_returns: list[list[float]]) -> dict[str, list[float]]:
    """Construct the Dollar factor (DOL) and High-Minus-Low FX carry factor (HML-FX).

    - Dollar factor: Unweighted mean return of all currency portfolios.
    - HML-FX factor: Portfolio K (highest carry) minus Portfolio 1 (lowest carry).

    Args:
        portfolio_returns: List of shape (T, K).

    Returns:
        dict containing "dollar_factor" and "hml_fx" time series.
    """
    if not portfolio_returns:
        raise ValueError("portfolio_returns must be non-empty")
    t_obs = len(portfolio_returns)
    k_ports = len(portfolio_returns[0])
    if k_ports < 2:
        raise ValueError("At least 2 portfolios required to build HML factor")

    dollar_factor: list[float] = []
    hml_fx: list[float] = []

    for t in range(t_obs):
        p_row = portfolio_returns[t]
        dol_val = sum(p_row) / k_ports
        # Long highest interest rate portfolio (index K-1), short lowest interest rate (index 0)
        hml_val = p_row[-1] - p_row[0]
        dollar_factor.append(round(dol_val, 6))
        hml_fx.append(round(hml_val, 6))

    return {
        "dollar_factor": dollar_factor,
        "hml_fx": hml_fx,
    }


def estimate_volatility_innovations(
    daily_returns: list[list[float]],
    days_per_month: int = 21,
) -> dict[str, Any]:
    """Estimate monthly global FX volatility and AR(1) innovations (Menkhoff et al. 2012).

    Daily global volatility is the cross-sectional mean absolute return across currencies:
        v_tau = (1 / N) * sum_{j=1}^N |r_{tau, j}|
    Monthly volatility Vol_m is the mean of daily volatility within month m.
    Innovations Delta Vol_m are residuals from AR(1):
        Vol_m = c + rho * Vol_{m-1} + u_m

    Args:
        daily_returns: List of shape (N_days, N_cur).
        days_per_month: Number of trading days per month (default 21).

    Returns:
        dict containing "monthly_vol", "ar1_rho", "ar1_const", and "vol_innovations".
    """
    if not daily_returns:
        raise ValueError("daily_returns must be non-empty")
    if days_per_month < 5:
        raise ValueError("days_per_month must be at least 5")

    total_days = len(daily_returns)
    n_cur = len(daily_returns[0])
    m_months = total_days // days_per_month

    if m_months < 3:
        raise ValueError("At least 3 months of daily data required for AR(1) estimation")

    # Compute daily global volatility: mean absolute return across currencies
    daily_vol: list[float] = []
    for day_row in daily_returns:
        mean_abs = sum(abs(r) for r in day_row) / n_cur
        daily_vol.append(mean_abs)

    # Aggregate to monthly volatility
    monthly_vol: list[float] = []
    for m in range(m_months):
        start_d = m * days_per_month
        end_d = start_d + days_per_month
        m_vol = sum(daily_vol[start_d:end_d]) / days_per_month
        monthly_vol.append(round(m_vol, 6))

    # Fit AR(1) regression: Vol_m = c + rho * Vol_{m-1}
    # y = monthly_vol[1:], x = monthly_vol[:-1]
    y_vec = monthly_vol[1:]
    x_mat = [[monthly_vol[i]] for i in range(m_months - 1)]

    coeffs, fitted, _ = _multivariate_ols(x_mat, y_vec, fit_intercept=True)
    ar1_const = round(coeffs[0], 6)
    ar1_rho = round(coeffs[1], 5)

    vol_innovations: list[float] = []
    for i in range(len(y_vec)):
        innov = y_vec[i] - fitted[i]
        vol_innovations.append(round(innov, 6))

    return {
        "monthly_vol": monthly_vol,
        "ar1_rho": ar1_rho,
        "ar1_const": ar1_const,
        "vol_innovations": vol_innovations,
    }


def fama_macbeth_twostep(
    portfolio_returns: list[list[float]],
    factor_matrix: list[list[float]],
    factor_names: list[str],
) -> dict[str, Any]:
    """Perform two-pass Fama-MacBeth cross-sectional asset pricing regressions.

    Stage 1: For each portfolio k, estimate time-series factor betas:
        R_{k, t} = a_k + sum_p beta_{k, p} * F_{p, t} + eps_{k, t}
    Stage 2: Cross-sectional regression of portfolio mean returns on betas:
        bar{R}_k = sum_p lambda_p * beta_{k, p} + alpha_k

    Args:
        portfolio_returns: List of shape (T, K) of test asset excess returns.
        factor_matrix: List of shape (T, P) of factor realizations.
        factor_names: Names of the P factors.

    Returns:
        dict containing betas, lambda_premia, pricing_errors, r_squared, and mape.
    """
    if not portfolio_returns or not factor_matrix:
        raise ValueError("portfolio_returns and factor_matrix must be non-empty")
    t_obs = len(portfolio_returns)
    if len(factor_matrix) != t_obs:
        raise ValueError("portfolio_returns and factor_matrix must have equal length")

    k_ports = len(portfolio_returns[0])
    p_factors = len(factor_matrix[0])
    if len(factor_names) != p_factors:
        raise ValueError("factor_names length must match factor_matrix columns")

    # Stage 1: Time-series OLS for each portfolio k
    betas: list[list[float]] = []
    mean_excess_returns: list[float] = []

    for k in range(k_ports):
        y_k = [portfolio_returns[t][k] for t in range(t_obs)]
        mean_excess_returns.append(sum(y_k) / t_obs)

        # Regress on constant and factors
        coeffs, _, _ = _multivariate_ols(factor_matrix, y_k, fit_intercept=True)
        # Factor betas are coeffs[1:] (coeffs[0] is intercept)
        k_betas = [round(c, 5) for c in coeffs[1:]]
        betas.append(k_betas)

    # Stage 2: Cross-sectional OLS of mean returns on betas (through the origin for traded factors)
    # y = mean_excess_returns, X = betas (K x P)
    cs_coeffs, fitted_mean, r_squared = _multivariate_ols(betas, mean_excess_returns, fit_intercept=False)

    lambda_premia = [round(c, 6) for c in cs_coeffs]

    pricing_errors: list[float] = []
    for k in range(k_ports):
        alpha_k = mean_excess_returns[k] - fitted_mean[k]
        pricing_errors.append(round(alpha_k, 6))

    mape = round(sum(abs(a) for a in pricing_errors) / k_ports, 6)

    return {
        "factor_names": factor_names,
        "betas": betas,
        "lambda_premia": lambda_premia,
        "pricing_errors": pricing_errors,
        "r_squared": round(r_squared, 4),
        "mape": mape,
    }


def run_currency_factor_replication(instance: dict[str, Any]) -> dict[str, Any]:
    """Execute complete currency factor replication and pricing evaluation.

    Args:
        instance: Problem instance dictionary from make_instance(seed).

    Returns:
        Comprehensive results dictionary containing carry portfolios, factors,
        and Fama-MacBeth pricing models.
    """
    spot_rates = instance.get("spot_rates")
    forward_rates = instance.get("forward_rates")
    daily_returns = instance.get("daily_returns")
    n_portfolios = instance.get("n_portfolios", 5)

    if spot_rates is None or forward_rates is None or daily_returns is None:
        raise ValueError("instance must contain spot_rates, forward_rates, and daily_returns")

    # Step 1: Compute currency excess returns and forward discounts
    rx = compute_excess_returns(spot_rates, forward_rates)
    fd = compute_forward_discounts(spot_rates, forward_rates)

    # Step 2: Form carry portfolios
    carry_info = sort_carry_portfolios(rx, fd, n_portfolios=n_portfolios)
    port_rets = carry_info["portfolio_returns"]

    # Step 3: Construct Dollar and HML-FX factors
    factors = build_factors(port_rets)
    dol = factors["dollar_factor"]
    hml = factors["hml_fx"]

    # Step 4: Estimate global FX volatility innovations
    vol_info = estimate_volatility_innovations(daily_returns, days_per_month=21)
    vol_innov = vol_info["vol_innovations"]

    # Align sample lengths for pricing regressions
    # Ensure factor series and portfolio returns have matching length
    t_eval = min(len(port_rets), len(vol_innov))
    eval_port_rets = port_rets[:t_eval]
    eval_dol = dol[:t_eval]
    eval_hml = hml[:t_eval]
    eval_vol_innov = vol_innov[:t_eval]

    # Model 1: Lustig, Roussanov & Verdelhan (2011) 2-factor model (DOL, HML-FX)
    x_lustig = [[eval_dol[t], eval_hml[t]] for t in range(t_eval)]
    lustig_pricing = fama_macbeth_twostep(
        eval_port_rets,
        x_lustig,
        factor_names=["DOL", "HML_FX"],
    )

    # Model 2: Menkhoff, Sarno, Schmeling & Schrimpf (2012) 2-factor model (DOL, VOL_INNOV)
    x_menkhoff = [[eval_dol[t], eval_vol_innov[t]] for t in range(t_eval)]
    menkhoff_pricing = fama_macbeth_twostep(
        eval_port_rets,
        x_menkhoff,
        factor_names=["DOL", "VOL_INNOV"],
    )

    return {
        "n_periods": len(spot_rates),
        "n_currencies": len(spot_rates[0]),
        "n_portfolios": n_portfolios,
        "carry_portfolios": carry_info,
        "factors": {
            "dollar_factor": dol,
            "hml_fx": hml,
            "monthly_vol": vol_info["monthly_vol"],
            "vol_innovations": vol_innov,
            "ar1_rho": vol_info["ar1_rho"],
            "ar1_const": vol_info["ar1_const"],
        },
        "lustig_model": lustig_pricing,
        "menkhoff_model": menkhoff_pricing,
    }
