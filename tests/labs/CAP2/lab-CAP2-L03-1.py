"""Lab CAP2-L03-1: Empirical tests for QE transmission channels and UIP failure.

Implements Krishnamurthy-Vissing-Jorgensen (2011) event-study yield response
decomposition across safe and credit assets, and Fama (1984) forward premium
regressions for uncovered interest parity.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def evaluate_qe_announcement_effects(
    event_yield_changes: dict[str, np.ndarray],
) -> dict[str, tuple[float, float, float]]:
    """Compute mean 2-day announcement yield changes, t-statistics, and p-values."""
    results = {}
    for asset, changes in event_yield_changes.items():
        m = float(np.mean(changes))
        se = float(np.std(changes, ddof=1) / np.sqrt(len(changes)))
        t_stat = m / se if se > 1e-12 else 0.0
        p_val = float(2.0 * (1.0 - stats.norm.cdf(abs(t_stat))))
        results[asset] = (m, t_stat, p_val)
    return results


def fama_uip_regression(
    spot_depreciation: np.ndarray,
    forward_premium: np.ndarray,
) -> tuple[float, float, float, float, float]:
    """Estimate Fama (1984) forward discount regression: Delta s_{t+1} = alpha + beta (f_t - s_t) + e."""
    x = forward_premium
    y = spot_depreciation
    n = len(x)

    x_mean = float(np.mean(x))
    y_mean = float(np.mean(y))

    ss_xx = float(np.sum((x - x_mean) ** 2))
    ss_xy = float(np.sum((x - x_mean) * (y - y_mean)))

    beta = ss_xy / ss_xx
    alpha = y_mean - beta * x_mean

    resid = y - (alpha + beta * x)
    s_sq = float(np.sum(resid**2) / (n - 2))
    se_beta = float(np.sqrt(s_sq / ss_xx))
    t_beta_zero = float(beta / se_beta)

    # Test H0: beta == 1 (Uncovered Interest Parity)
    t_beta_one = float((beta - 1.0) / se_beta)
    p_uip = float(2.0 * (1.0 - stats.norm.cdf(abs(t_beta_one))))

    return alpha, beta, se_beta, t_beta_zero, p_uip


def main() -> None:
    rng = np.random.default_rng(2011)

    # 1. Resolution 5: QE Announcement Window Yield Responses (bps)
    # 5 major QE1 announcements (Nov 2008 - Mar 2009)
    # Long Treasury, Agency MBS, Baa Corporate
    qe_events = {
        "10Y_Treasury": np.array([-38.0, -18.0, -14.0, -47.0, -11.0]),
        "Agency_MBS": np.array([-44.0, -29.0, -20.0, -52.0, -15.0]),
        "Baa_Corporate": np.array([-15.0, -8.0, -12.0, -28.0, -7.0]),
    }

    qe_res = evaluate_qe_announcement_effects(qe_events)

    print("--- Resolution 5: QE Transmission & Portfolio Balance ---")
    print(f"{'Asset Class':<16} | {'Mean Change (bps)':<18} | {'t-stat':<10} | {'p-value'}")
    print("-" * 56)
    for asset, (mean_chg, t_val, p_val) in qe_res.items():
        print(f"{asset:<16} | {mean_chg:<18.1f} | {t_val:<10.2f} | {p_val:.4f}")

    # 2. Resolution 6: UIP Failure and Forward Discount Puzzle
    # Simulate 120 monthly currency observations
    fp = rng.normal(0.002, 0.006, size=120)  # interest rate differential (f - s)
    # Under empirical puzzle: beta is negative (~ -0.80), carry currency appreciates
    noise = rng.normal(0.0, 0.025, size=120)
    delta_s = 0.001 - 0.85 * fp + noise

    alpha, beta, se_beta, t_zero, p_uip = fama_uip_regression(delta_s, fp)

    print("\n--- Resolution 6: UIP Failure & Currency Risk Premia ---")
    print(f"Fama Regression Intercept (alpha): {alpha:.5f}")
    print(f"Fama Regression Slope (beta):     {beta:.3f} (SE: {se_beta:.3f})")
    print(f"t-statistic against zero (beta=0): {t_zero:.3f}")
    print(f"UIP Hypothesis Test (H0: beta=1):  p-value = {p_uip:.5f}")
    print(f"UIP Rejection Status:              {'REJECTED' if p_uip < 0.05 else 'ACCEPTED'}")


main()
