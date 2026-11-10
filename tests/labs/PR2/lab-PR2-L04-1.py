"""Lab 4: Volatility targeting and tail-risk compression.

Demonstrates Harvey et al. (2018) empirical mechanics:
Scaling portfolio weight inversely with conditional volatility forecast:
w_t = sigma_target / sigma_hat_t
compresses return kurtosis, thins fat tails, and mitigates maximum drawdown.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # SIMULATED: Volatility clustering with crisis tail events over 2,000 trading days (~8 years)
    rng = np.random.default_rng(101)
    n_days = 2000
    target_vol_ann = 0.12
    dt = 1.0 / 252.0
    target_vol_daily = target_vol_ann * np.sqrt(dt)

    omega = 0.000005
    alpha = 0.12
    beta = 0.85
    mu_daily = 0.08 * dt  # 8% annualized drift

    daily_returns = np.zeros(n_days)
    sigma2_t = np.zeros(n_days)
    sigma2_t[0] = omega / (1.0 - alpha - beta)

    for t in range(n_days):
        eps = rng.standard_normal()
        if rng.random() < 0.01:
            eps *= 3.0  # tail shock
        sigma_t = np.sqrt(sigma2_t[t])
        daily_returns[t] = mu_daily + sigma_t * eps
        if t + 1 < n_days:
            sigma2_t[t + 1] = omega + alpha * (daily_returns[t] - mu_daily) ** 2 + beta * sigma2_t[t]

    # Forecast conditional volatility using trailing 21-day realized volatility
    trailing_vol = np.zeros(n_days)
    for t in range(21, n_days):
        trailing_vol[t] = float(np.std(daily_returns[t - 21 : t], ddof=1))
    trailing_vol[:21] = np.sqrt(sigma2_t[0])

    # Volatility targeted portfolio weights: w_t = target_vol_daily / trailing_vol_t
    w_target = np.clip(target_vol_daily / trailing_vol, 0.2, 3.0)

    # Strategy returns (lagged by 1 day to prevent lookahead)
    strat_returns = w_target[21:-1] * daily_returns[22:]
    unmanaged_returns = daily_returns[22:]

    def stats(r: np.ndarray) -> tuple[float, float, float, float]:
        ann_ret = float(np.mean(r) * 252.0)
        ann_vol = float(np.std(r, ddof=1) * np.sqrt(252.0))
        sr = ann_ret / ann_vol
        centered = r - np.mean(r)
        kurt = float(np.mean(centered**4) / (np.var(r) ** 2) - 3.0)
        cum = np.cumprod(1.0 + r)
        peak = np.maximum.accumulate(cum)
        mdd = float(np.max((peak - cum) / peak))
        return ann_vol, sr, kurt, mdd

    u_vol, u_sr, u_kurt, u_mdd = stats(unmanaged_returns)
    m_vol, m_sr, m_kurt, m_mdd = stats(strat_returns)

    print(f"Unmanaged Realized Vol: {u_vol * 100:.2f}%, Vol-Targeted Realized Vol: {m_vol * 100:.2f}%")
    print(f"Unmanaged Sharpe Ratio: {u_sr:.4f}, Vol-Targeted Sharpe Ratio: {m_sr:.4f}")
    print(f"Unmanaged Excess Kurtosis: {u_kurt:.2f}, Vol-Targeted Excess Kurtosis: {m_kurt:.2f}")
    print(f"Unmanaged Max Drawdown: {u_mdd * 100:.2f}%, Vol-Targeted Max Drawdown: {m_mdd * 100:.2f}%")
    print(f"Kurtosis Reduction: {(1.0 - m_kurt / u_kurt) * 100:.1f}%")
    print(f"Drawdown Reduction: {(u_mdd - m_mdd) * 100:.2f}% percentage points")


main()
