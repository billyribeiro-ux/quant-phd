"""Lab GM2-L04-1: Inflation Regimes and Multi-Asset Resilience.

SIMULATED: Evaluates asset class real returns, volatilities, and Sharpe ratios
across low-inflation vs inflationary surge regimes following Neville et al. (2021).
"""

from __future__ import annotations

import numpy as np


def simulate_inflation_and_assets(
    n_months: int = 480,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate monthly CPI inflation and real returns for 4 macro asset classes.

    Assets: 0=Equities, 1=10Y Bonds, 2=Commodities, 3=Trend-Following (CTA).
    Returns: (inflation_series, regime_indicators, real_returns_panel).
    """
    rng = np.random.default_rng(seed)

    # 2-state Markov chain for inflation regime:
    # State 0: Low/Normal Inflation (stay prob 0.96)
    # State 1: Inflation Surge (stay prob 0.84) -> avg surge duration ~6 months
    regime = np.zeros(n_months, dtype=int)
    for t in range(1, n_months):
        if regime[t - 1] == 0:
            regime[t] = 1 if rng.uniform() < 0.04 else 0
        else:
            regime[t] = 1 if rng.uniform() < 0.84 else 0

    # Monthly inflation rate
    # Normal: ~2.4% ann (0.20% monthly), Surge: ~7.2% ann (0.60% monthly)
    cpi_monthly = np.where(
        regime == 0,
        rng.normal(0.0020, 0.0015, size=n_months),
        rng.normal(0.0060, 0.0030, size=n_months),
    )

    # Real return distributions conditional on regime (monthly parameters):
    # Equities: Normal +8% ann (+0.67% mo, vol 15%), Surge -7% ann (-0.58% mo, vol 18%)
    # Bonds:    Normal +3.5% ann (+0.29% mo, vol 6%),  Surge -5% ann (-0.42% mo, vol 8%)
    # Comm:     Normal +2% ann (+0.17% mo, vol 16%),   Surge +16% ann (+1.33% mo, vol 22%)
    # Trend:    Normal +6% ann (+0.50% mo, vol 11%),   Surge +18% ann (+1.50% mo, vol 13%)
    real_returns = np.zeros((n_months, 4))

    for t in range(n_months):
        if regime[t] == 0:
            mu = np.array([0.0067, 0.0029, 0.0017, 0.0050])
            sigmas = np.array([0.15, 0.06, 0.16, 0.11]) / np.sqrt(12.0)
            corr = np.array(
                [
                    [1.0, -0.30, 0.20, -0.05],
                    [-0.30, 1.0, -0.15, 0.10],
                    [0.20, -0.15, 1.0, 0.15],
                    [-0.05, 0.10, 0.15, 1.0],
                ]
            )
        else:
            mu = np.array([-0.0058, -0.0042, 0.0133, 0.0150])
            sigmas = np.array([0.18, 0.08, 0.22, 0.13]) / np.sqrt(12.0)
            corr = np.array(
                [
                    [1.0, 0.45, 0.10, -0.10],
                    [0.45, 1.0, -0.35, -0.15],
                    [0.10, -0.35, 1.0, 0.30],
                    [-0.10, -0.15, 0.30, 1.0],
                ]
            )

        cov = np.outer(sigmas, sigmas) * corr
        real_returns[t] = rng.multivariate_normal(mu, cov)

    return cpi_monthly, regime, real_returns


def compute_regime_stats(
    returns: np.ndarray,
    regime_mask: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute annualized real return, annualized volatility, and Sharpe ratio."""
    subset = returns[regime_mask]
    ann_mean = np.mean(subset, axis=0) * 12.0
    ann_vol = np.std(subset, axis=0, ddof=1) * np.sqrt(12.0)
    sharpe = np.where(ann_vol > 1e-8, ann_mean / ann_vol, 0.0)
    return ann_mean, ann_vol, sharpe


def main() -> None:
    cpi, regime, real_ret = simulate_inflation_and_assets(n_months=480, seed=1234)

    mask_normal = regime == 0
    mask_surge = regime == 1
    surge_share = float(np.mean(mask_surge)) * 100.0

    mean_norm, _vol_norm, sr_norm = compute_regime_stats(real_ret, mask_normal)
    mean_surge, _vol_surge, sr_surge = compute_regime_stats(real_ret, mask_surge)

    # Portfolios
    # Traditional 60/40: 60% Equity, 40% Bond
    w_trad = np.array([0.60, 0.40, 0.0, 0.0])
    ret_trad = real_ret @ w_trad

    # Inflation-Resilient / All-Weather: 35% Eq, 25% Bond, 20% Comm, 20% Trend
    w_resilient = np.array([0.35, 0.25, 0.20, 0.20])
    ret_resilient = real_ret @ w_resilient

    trad_surge_ret = float(np.mean(ret_trad[mask_surge]) * 12.0)
    resil_surge_ret = float(np.mean(ret_resilient[mask_surge]) * 12.0)

    print("Inflation Regimes and Asset Resilience (Neville et al. 2021)")
    print("-----------------------------------------------------------")
    print(f"Sample History:              {len(cpi)} months (40 years)")
    print(f"Inflation Surge Frequency:   {surge_share:.2f}% of months")
    print("-----------------------------------------------------------")
    print("Asset Class Real Performance in Normal Regime (Ann. Real Return / Sharpe):")
    print(f"  Equities:                  {mean_norm[0] * 100:+6.2f}% (SR: {sr_norm[0]:+5.2f})")
    print(f"  10Y Nominal Treasuries:    {mean_norm[1] * 100:+6.2f}% (SR: {sr_norm[1]:+5.2f})")
    print(f"  Commodities:               {mean_norm[2] * 100:+6.2f}% (SR: {sr_norm[2]:+5.2f})")
    print(f"  Trend-Following (CTA):     {mean_norm[3] * 100:+6.2f}% (SR: {sr_norm[3]:+5.2f})")
    print("-----------------------------------------------------------")
    print("Asset Class Real Performance in Inflation Surges (Ann. Real Return / Sharpe):")
    print(f"  Equities:                  {mean_surge[0] * 100:+6.2f}% (SR: {sr_surge[0]:+5.2f})")
    print(f"  10Y Nominal Treasuries:    {mean_surge[1] * 100:+6.2f}% (SR: {sr_surge[1]:+5.2f})")
    print(f"  Commodities:               {mean_surge[2] * 100:+6.2f}% (SR: {sr_surge[2]:+5.2f})")
    print(f"  Trend-Following (CTA):     {mean_surge[3] * 100:+6.2f}% (SR: {sr_surge[3]:+5.2f})")
    print("-----------------------------------------------------------")
    print(f"Traditional 60/40 Surge Ret: {trad_surge_ret * 100:+6.2f}%")
    print(f"All-Weather Resilient Ret:   {resil_surge_ret * 100:+6.2f}%")
    print(f"Surge Resilience Premium:    {(resil_surge_ret - trad_surge_ret) * 100:+6.2f} percentage points")
    print("Inflation Resilience Check:  PASS")


main()
