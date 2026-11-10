"""Lab SR3-L02-1: Marginal Expected Shortfall (MES) and Long-Run MES (LRMES).

SIMULATED: generates heavy-tailed market returns and cross-sectional institutional
returns to compute non-parametric MES and multi-month projected LRMES following
Acharya, Pedersen, Philippon, and Richardson (2017).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(202)
    t_obs = 600  # 600 trading days (~2.4 years)
    alpha = 0.05  # 5% tail crisis threshold
    crisis_drop = 0.40  # 40% aggregate market crash horizon

    # Leptokurtic market returns R_m via Student-t(4) innovations
    scale = np.sqrt(rng.chisquare(df=4, size=t_obs) / 4.0)
    market_noise = rng.normal(0.0, 0.012, size=t_obs) / np.maximum(scale, 1e-4)
    r_market = 0.0003 + market_noise

    # Three financial institution return series:
    # Firm A: High Beta Dealer (beta ~ 1.6)
    # Firm B: Unit Beta Commercial Bank (beta ~ 1.0)
    # Firm C: Low Beta Insurer (beta ~ 0.5)
    betas = [1.60, 1.00, 0.50]
    names = ["Dealer Bank A", "Commercial Bank B", "Insurer C"]
    idio_vols = [0.015, 0.010, 0.008]

    r_firms: list[np.ndarray] = []
    for b, iv in zip(betas, idio_vols, strict=True):
        idio = rng.normal(0.0, iv, size=t_obs)
        r_firms.append(b * r_market + idio)

    # 1. Empirical Market VaR at alpha = 0.05
    var_market = float(np.quantile(r_market, alpha))
    crisis_days = r_market <= var_market
    n_crisis = int(np.sum(crisis_days))

    print("=== Marginal Expected Shortfall (Acharya et al. 2017) ===")
    print(f"Sample periods (T): {t_obs}")
    print(f"Market VaR(0.05):   {var_market:.4f} (-{abs(var_market) * 100:.2f}%)")
    print(f"Crisis observations: {n_crisis} days ({n_crisis / t_obs * 100:.1f}%)")
    print("-" * 65)
    print(f"{'Institution':<20} {'Sample Beta':<12} {'MES (5%)':<12} {'LRMES (40%)':<12}")
    print("-" * 65)

    var_m_sample = float(np.var(r_market, ddof=1))

    for name, r_i in zip(names, r_firms, strict=True):
        # Sample beta
        cov_im = float(np.cov(r_i, r_market, ddof=1)[0, 1])
        b_est = cov_im / var_m_sample

        # Non-parametric MES: average loss on market crisis days
        mes_val = float(-np.mean(r_i[crisis_days]))

        # Dynamic LRMES: 1 - (1 - d)^beta
        lrmes_val = float(1.0 - (1.0 - crisis_drop) ** b_est)

        print(f"{name:<20} {b_est:<12.3f} {mes_val * 100:<11.2f}% {lrmes_val * 100:<11.2f}%")

    print("-" * 65)
    print("Interpretation: High-beta dealer equity suffers over 55% loss in a 40% crisis,")
    print("generating severe capital shortfall externalities under systemic market strain.")


main()
