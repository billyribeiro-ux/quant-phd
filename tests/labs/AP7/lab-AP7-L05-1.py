"""Lab AP7-L05-1: The Empirical Test: Risk vs Mispricing.

SIMULATED: Implements Daniel & Titman (1997) characteristic vs covariance portfolio
sorting to distinguish factor risk compensation from behavioral mispricing, and
estimates post-publication return decay (McLean & Pontiff 2016).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    seed = 42
    rng = np.random.default_rng(seed)
    n_stocks = 300
    n_months = 180

    # 1. Firm fundamental characteristic: Book-to-Market ratio (BM)
    # High BM = Value firm, Low BM = Growth firm
    bm_characteristic = rng.uniform(0.2, 1.8, size=n_stocks)

    # 2. Factor loading beta_HML
    # Under rational risk: beta_HML is strictly correlated with BM characteristic
    # In live cross-section, dispersion allows separating characteristic from loading:
    # beta_HML = a * BM + e
    beta_hml = 0.60 * bm_characteristic + rng.normal(0.0, 0.25, size=n_stocks)

    # HML factor return series: mean return +0.35% per month
    hml_returns = rng.normal(0.0035, 0.030, size=n_months)
    mkt_returns = rng.normal(0.0065, 0.045, size=n_months)

    # Data Generating Process:
    # Let true expected return depend on CHARACTERISTIC (mispricing hypothesis):
    # E[R_i] = R_f + gamma_char * BM_i
    # rather than factor loading beta_HML
    gamma_characteristic = 0.0040  # 40 bps per unit BM
    stock_returns = np.zeros((n_months, n_stocks))

    for t in range(n_months):
        idio_shocks = rng.normal(0.0, 0.05, size=n_stocks)
        stock_returns[t] = (
            0.002
            + gamma_characteristic * bm_characteristic
            + 1.0 * mkt_returns[t]
            + beta_hml * (hml_returns[t] - 0.0035)  # zero factor mean premium
            + idio_shocks
        )

    # Form 3 portfolios:
    # Portfolio A: High BM, High beta_HML
    # Portfolio B: High BM, Low beta_HML
    # Portfolio C: Low BM, Low beta_HML
    high_bm_mask = bm_characteristic > np.median(bm_characteristic)
    low_bm_mask = ~high_bm_mask

    high_bm_high_beta = high_bm_mask & (beta_hml > np.median(beta_hml[high_bm_mask]))
    high_bm_low_beta = high_bm_mask & (~high_bm_high_beta)
    low_bm_low_beta = low_bm_mask & (beta_hml < np.median(beta_hml[low_bm_mask]))

    ret_a = np.mean(stock_returns[:, high_bm_high_beta], axis=1)
    ret_b = np.mean(stock_returns[:, high_bm_low_beta], axis=1)
    ret_c = np.mean(stock_returns[:, low_bm_low_beta], axis=1)

    mean_a = float(np.mean(ret_a)) * 12.0
    mean_b = float(np.mean(ret_b)) * 12.0
    mean_c = float(np.mean(ret_c)) * 12.0

    # Test 1: Daniel-Titman Characteristic Test:
    # Does Mean(B) equal Mean(A) holding characteristic constant despite different beta?
    # Under mispricing: Mean(A) approx Mean(B)
    diff_ab = (mean_a - mean_b) * 100.0  # percentage points

    # Test 2: Does Mean(B) exceed Mean(C) holding beta constant despite different characteristic?
    # Under mispricing: Mean(B) >> Mean(C)
    diff_bc = (mean_b - mean_c) * 100.0

    # 3. McLean & Pontiff (2016) Post-Publication Anomaly Decay:
    # In-sample anomaly return: +5.5% annual
    # Post-publication return attenuation: drops by ~58%
    pre_pub_alpha = 0.055
    decay_fraction = 0.58
    post_pub_alpha = pre_pub_alpha * (1.0 - decay_fraction)

    print("Daniel & Titman (1997) Characteristic vs Covariance Test:")
    print(f"  Portfolio A (High BM, High Beta) Annual Return: {mean_a * 100:.2f}%")
    print(f"  Portfolio B (High BM, Low Beta)  Annual Return: {mean_b * 100:.2f}%")
    print(f"  Portfolio C (Low BM, Low Beta)   Annual Return: {mean_c * 100:.2f}%")
    print(f"  Diff(A - B) holding characteristic constant:    {diff_ab:+.2f} pp")
    print(f"  Diff(B - C) holding factor loading constant:    {diff_bc:+.2f} pp")
    print("McLean & Pontiff (2016) Anomaly Publication Decay:")
    print(f"  Pre-publication historical alpha:               {pre_pub_alpha * 100:.2f}%")
    print(f"  Estimated post-publication attenuation:         {decay_fraction * 100:.1f}%")
    print(f"  Post-publication persistent alpha:              {post_pub_alpha * 100:.2f}%")
    print(f"  Characteristic dominates covariance:            {bool(diff_bc > abs(diff_ab))}")


main()
