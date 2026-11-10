"""Lab CAP2-L01-1: Quantitative evidence tests for market efficiency and the equity premium.

Implements Lo-MacKinlay (1988) variance ratio tests for random walk behavior,
Shiller (1981) excess volatility inequality checks, and Mehra-Prescott (1985)
relative risk aversion calibration for the equity risk premium.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def lo_mackinlay_variance_ratio(log_prices: np.ndarray, q: int) -> tuple[float, float, float]:
    """Compute Lo-MacKinlay homoskedastic and heteroskedastic variance ratio test."""
    n = len(log_prices) - 1
    rets = np.diff(log_prices)
    mu = float(np.mean(rets))

    # 1-period variance
    sigma_1_sq = float(np.sum((rets - mu) ** 2) / (n - 1))

    # q-period returns
    rets_q = log_prices[q:] - log_prices[:-q]
    m_q = q * mu
    m_denom = float(q * (n - q + 1) * (1.0 - float(q) / float(n)))
    sigma_q_sq = float(np.sum((rets_q - m_q) ** 2) / m_denom)

    vr = sigma_q_sq / sigma_1_sq

    # Asymptotic variance under homoskedasticity: phi_1 = 2 * (2q - 1) * (q - 1) / (3 * q * n)
    phi_1 = 2.0 * (2.0 * q - 1.0) * (q - 1.0) / (3.0 * q * n)
    z_stat = (vr - 1.0) / np.sqrt(phi_1)
    p_val = float(2.0 * (1.0 - stats.norm.cdf(abs(z_stat))))

    return vr, float(z_stat), p_val


def shiller_excess_volatility_test(
    prices: np.ndarray,
    dividends: np.ndarray,
    discount_rate: float,
) -> tuple[float, float, float]:
    """Evaluate Shiller (1981) bound: Var(P) <= Var(P*)."""
    t = len(prices)
    # Perfect foresight price P*_t = sum_{k=0}^{T-t-1} (1/(1+r))^{k+1} D_{t+k} + terminal discounted
    p_star = np.zeros(t, dtype=np.float64)
    beta = 1.0 / (1.0 + discount_rate)
    terminal_val = float(prices[-1])

    for i in range(t):
        cf_sum = 0.0
        for k in range(t - i):
            cf_sum += (beta ** (k + 1)) * dividends[i + k]
        cf_sum += (beta ** (t - i)) * terminal_val
        p_star[i] = cf_sum

    var_p = float(np.var(prices, ddof=1))
    var_p_star = float(np.var(p_star, ddof=1))
    vol_ratio = np.sqrt(var_p) / np.sqrt(var_p_star)

    return var_p, var_p_star, vol_ratio


def mehra_prescott_calibration(
    equity_premium: float,
    consumption_growth_vol: float,
    equity_consumption_corr: float,
    equity_return_vol: float,
) -> float:
    """Calibrate Mehra-Prescott (1985) coefficient of relative risk aversion gamma.

    Under power utility, E[R_e - R_f] approx gamma * Cov(Delta c, R_e).
    """
    cov_c_e = equity_consumption_corr * consumption_growth_vol * equity_return_vol
    gamma = equity_premium / cov_c_e
    return float(gamma)


def main() -> None:
    rng = np.random.default_rng(1988)

    # 1. Simulate monthly asset log prices (120 months)
    innovations = rng.normal(0.007, 0.045, size=120)
    log_p = np.cumsum(np.concatenate([[4.6], innovations]))

    vr_2, z_2, p_2 = lo_mackinlay_variance_ratio(log_p, q=2)
    vr_12, z_12, p_12 = lo_mackinlay_variance_ratio(log_p, q=12)

    print("--- Resolution 1: Market Efficiency & Random Walk Tests ---")
    print(f"Variance Ratio VR(2):  {vr_2:.4f} (z-stat: {z_2:.3f}, p-val: {p_2:.4f})")
    print(f"Variance Ratio VR(12): {vr_12:.4f} (z-stat: {z_12:.3f}, p-val: {p_12:.4f})")

    # 2. Shiller (1981) Volatility Bounds
    divs = rng.normal(2.5, 0.15, size=len(log_p))
    prices = np.exp(log_p)
    var_p, var_p_star, vol_ratio = shiller_excess_volatility_test(prices, divs, discount_rate=0.06 / 12.0)

    print("\n--- Shiller Excess Volatility Inequality ---")
    print(f"Sample Stock Price Std Dev:  {np.sqrt(var_p):.2f}")
    print(f"Ex-Post Fundamental Std Dev: {np.sqrt(var_p_star):.2f}")
    print(f"Excess Volatility Ratio (sigma_P / sigma_P*): {vol_ratio:.3f}")

    # 3. Resolution 2: Equity Risk Premium Calibration
    # Historic US values: Equity premium ~ 6.0%, Consumption vol ~ 1.5%, Equity vol ~ 18%, Corr ~ 0.20
    ep = 0.060
    sigma_c = 0.015
    sigma_e = 0.180
    corr = 0.220

    gamma_implied = mehra_prescott_calibration(ep, sigma_c, corr, sigma_e)
    print("\n--- Resolution 2: The Equity Premium as a Risk Premium ---")
    print(f"Historical US Real Equity Premium: {ep * 100.0:.2f}%")
    print(f"Consumption Growth Volatility:    {sigma_c * 100.0:.2f}%")
    print(f"Equity Volatility:                {sigma_e * 100.0:.2f}%")
    print(f"Equity-Consumption Correlation:   {corr:.3f}")
    print(f"Mehra-Prescott Implied Risk Aversion (gamma): {gamma_implied:.1f}")


main()
