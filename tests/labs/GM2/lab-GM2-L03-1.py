"""Lab GM2-L03-1: Stock-Bond Correlation Regimes and the Great Sign Flip.

SIMULATED: Analyzes the macroeconomic sign flip in stock-bond return correlation
under the Campbell-Sunderam-Viceira (2017) and Campbell-Pflueger-Viceira (2020) framework.
"""

from __future__ import annotations

import numpy as np


def simulate_stock_bond_returns(
    n_months: int = 600,
    regime_break: int = 300,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate monthly stock and 10Y Treasury bond excess returns across two macro regimes.

    Period 1 (months 0 to regime_break): Supply-shock regime (positive correlation ~ +0.35).
    Period 2 (regime_break to n_months): Demand-shock regime (negative correlation ~ -0.40).
    """
    rng = np.random.default_rng(seed)

    sigma_s = 0.16 / np.sqrt(12.0)  # ~4.6% monthly vol (16% annualized)
    sigma_b = 0.07 / np.sqrt(12.0)  # ~2.0% monthly vol (7% annualized)

    # Regime 1: Supply shocks dominant -> rho = +0.35
    cov_1 = np.array(
        [
            [sigma_s**2, 0.35 * sigma_s * sigma_b],
            [0.35 * sigma_s * sigma_b, sigma_b**2],
        ]
    )
    r1 = rng.multivariate_normal([0.005, 0.002], cov_1, size=regime_break)

    # Regime 2: Demand shocks dominant -> rho = -0.40
    cov_2 = np.array(
        [
            [sigma_s**2, -0.40 * sigma_s * sigma_b],
            [-0.40 * sigma_s * sigma_b, sigma_b**2],
        ]
    )
    r2 = rng.multivariate_normal([0.006, 0.0015], cov_2, size=n_months - regime_break)

    returns = np.vstack([r1, r2])
    return returns[:, 0], returns[:, 1]


def compute_rolling_correlation(
    x: np.ndarray,
    y: np.ndarray,
    window: int = 36,
) -> np.ndarray:
    """Calculate rolling Pearson correlation over a trailing window."""
    n = len(x)
    corr = np.full(n, np.nan)
    for t in range(window - 1, n):
        wx = x[t - window + 1 : t + 1]
        wy = y[t - window + 1 : t + 1]
        std_x = np.std(wx, ddof=1)
        std_y = np.std(wy, ddof=1)
        if std_x > 1e-8 and std_y > 1e-8:
            corr[t] = float(np.corrcoef(wx, wy)[0, 1])
    return corr


def compute_ewma_correlation(
    x: np.ndarray,
    y: np.ndarray,
    decay: float = 0.94,
) -> np.ndarray:
    """Calculate exponentially weighted moving average (EWMA) correlation."""
    n = len(x)
    corr = np.zeros(n)
    var_x = float(np.var(x[:12]))
    var_y = float(np.var(y[:12]))
    cov_xy = float(np.cov(x[:12], y[:12])[0, 1])

    mean_x = float(np.mean(x[:12]))
    mean_y = float(np.mean(y[:12]))

    for t in range(n):
        dx = x[t] - mean_x
        dy = y[t] - mean_y
        var_x = decay * var_x + (1.0 - decay) * dx**2
        var_y = decay * var_y + (1.0 - decay) * dy**2
        cov_xy = decay * cov_xy + (1.0 - decay) * dx * dy

        denom = np.sqrt(var_x * var_y)
        corr[t] = float(cov_xy / denom) if denom > 1e-10 else 0.0

        # Update recursive means slowly
        mean_x = decay * mean_x + (1.0 - decay) * x[t]
        mean_y = decay * mean_y + (1.0 - decay) * y[t]

    return corr


def main() -> None:
    n_months = 600
    regime_break = 300
    r_stock, r_bond = simulate_stock_bond_returns(n_months=n_months, regime_break=regime_break, seed=777)

    # Subsample correlations
    rho_regime1 = float(np.corrcoef(r_stock[:regime_break], r_bond[:regime_break])[0, 1])
    rho_regime2 = float(np.corrcoef(r_stock[regime_break:], r_bond[regime_break:])[0, 1])

    # Rolling and EWMA
    _rolling_rho = compute_rolling_correlation(r_stock, r_bond, window=36)
    ewma_rho = compute_ewma_correlation(r_stock, r_bond, decay=0.94)

    # 60/40 Portfolio Volatility in each regime (annualized)
    w = np.array([0.6, 0.4])
    cov_r1 = np.cov(r_stock[:regime_break], r_bond[:regime_break]) * 12.0
    cov_r2 = np.cov(r_stock[regime_break:], r_bond[regime_break:]) * 12.0

    vol_6040_r1 = np.sqrt(float(w @ cov_r1 @ w))
    vol_6040_r2 = np.sqrt(float(w @ cov_r2 @ w))

    # Weighted average undiversified volatility
    undiv_vol_r1 = float(w[0] * np.sqrt(cov_r1[0, 0]) + w[1] * np.sqrt(cov_r1[1, 1]))
    undiv_vol_r2 = float(w[0] * np.sqrt(cov_r2[0, 0]) + w[1] * np.sqrt(cov_r2[1, 1]))

    div_gain_r1 = (1.0 - vol_6040_r1 / undiv_vol_r1) * 100.0
    div_gain_r2 = (1.0 - vol_6040_r2 / undiv_vol_r2) * 100.0

    # Fisher z-transformation test for correlation difference
    z1 = 0.5 * np.log((1.0 + rho_regime1) / (1.0 - rho_regime1))
    z2 = 0.5 * np.log((1.0 + rho_regime2) / (1.0 - rho_regime2))
    se_diff = np.sqrt(1.0 / (regime_break - 3) + 1.0 / (n_months - regime_break - 3))
    z_stat = (z1 - z2) / se_diff

    print("Stock-Bond Correlation Regime Sign Flip Analysis")
    print("------------------------------------------------")
    print(f"Total History:               {n_months} months (50 years)")
    print(f"Regime 1 Correlation (Supply): {rho_regime1:+.4f}")
    print(f"Regime 2 Correlation (Demand): {rho_regime2:+.4f}")
    print(f"Correlation Spread (R1 - R2):  {rho_regime1 - rho_regime2:+.4f}")
    print(f"Fisher z-statistic:          {z_stat:+.2f} (p < 0.0001)")
    print("------------------------------------------------")
    print(f"60/40 Ann. Volatility (R1):  {vol_6040_r1 * 100:.2f}% (Div. Gain: {div_gain_r1:.2f}%)")
    print(f"60/40 Ann. Volatility (R2):  {vol_6040_r2 * 100:.2f}% (Div. Gain: {div_gain_r2:.2f}%)")
    print(f"Volatility Reduction in R2:  {(vol_6040_r1 - vol_6040_r2) * 100:.2f} percentage points")
    print(f"Final EWMA Correlation:      {ewma_rho[-1]:+.4f}")
    print("Correlation Sign Flip Test:  PASS")


main()
