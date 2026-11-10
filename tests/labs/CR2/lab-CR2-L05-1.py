"""Lab CR2-L05-1: Synthetic CDO tranche pricing across the capital structure under one-factor Gaussian copula.

Calculates tranche expected loss, risky premium duration, default protection leg,
break-even par spreads, and verifies the tranche portfolio articulation identity.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats


def calc_tranche_expected_loss(
    k1: float,
    k2: float,
    p: float,
    recovery: float,
    rho: float,
    num_points: int = 80,
) -> float:
    """Compute expected loss percentage for tranche [k1, k2] under Gaussian copula."""
    if p <= 1e-12:
        return 0.0
    nodes, weights = np.polynomial.legendre.leggauss(num_points)
    m = nodes * 5.0
    wm = weights * 5.0
    inv_p = float(stats.norm.ppf(p))
    sigma_idio = math.sqrt(max(1e-10, 1.0 - rho))
    cond_p = stats.norm.cdf((inv_p - math.sqrt(rho) * m) / sigma_idio)
    loss = (1.0 - recovery) * cond_p
    tranche_loss = np.maximum(0.0, np.minimum(loss, k2) - k1) / (k2 - k1)
    return float(np.sum(tranche_loss * stats.norm.pdf(m) * wm))


def main() -> None:
    # Portfolio and market parameters
    tenor = 5.0
    coupon_freq = 4
    dt = 1.0 / coupon_freq
    r = 0.03
    p_5y = 0.05
    recovery = 0.40
    rho = 0.20

    tranches = [
        ("Equity", 0.0, 0.03),
        ("Junior Mezz", 0.03, 0.07),
        ("Senior Mezz", 0.07, 0.10),
        ("Senior", 0.10, 0.15),
        ("Super Senior", 0.15, 0.30),
    ]

    times = [(k + 1) * dt for k in range(round(tenor * coupon_freq))]

    print("Synthetic CDO Capital Structure Valuation (5Y, p=5.0%, R=40%, rho=20%, r=3%):")
    print("  Tranche Name   | Attachment-Detachment | Expected Loss | Prot Leg PV | Prem Leg PV | Par Spread")
    print("-----------------+-----------------------+---------------+-------------+-------------+------------")

    weighted_loss_sum = 0.0

    for name, k1, k2 in tranches:
        # Time-profile of losses
        period_losses = [0.0]
        for tk in times:
            p_k = p_5y * (tk / tenor)
            period_losses.append(calc_tranche_expected_loss(k1, k2, p_k, recovery, rho))

        prem_pv = 0.0
        prot_pv = 0.0
        for k, tk in enumerate(times):
            t_prev = times[k - 1] if k > 0 else 0.0
            df_k = math.exp(-r * tk)
            df_mid = math.exp(-r * 0.5 * (t_prev + tk))
            surv_avg = 1.0 - 0.5 * (period_losses[k] + period_losses[k + 1])
            prem_pv += dt * df_k * surv_avg
            prot_pv += df_mid * (period_losses[k + 1] - period_losses[k])

        par_spread_bps = (prot_pv / max(1e-10, prem_pv)) * 10000.0
        final_loss = period_losses[-1]
        width = k2 - k1
        weighted_loss_sum += width * final_loss

        if k1 == 0.0:
            # Equity tranche market quote: 500 bp running + upfront fee
            upfront_fee_pct = (prot_pv - 0.05 * prem_pv) * 100.0
            quote_str = f"500 bp + {upfront_fee_pct:5.2f}%"
        else:
            quote_str = f"{par_spread_bps:6.1f} bp"

        print(
            f"  {name:14s} |     {k1 * 100:4.1f}% - {k2 * 100:4.1f}%     |     "
            f"{final_loss * 100:5.2f}%    |   {prot_pv:7.5f}   |   {prem_pv:7.4f}   | {quote_str}"
        )

    # Add unhedged senior tail [30%, 100%]
    final_loss_tail = calc_tranche_expected_loss(0.30, 1.00, p_5y, recovery, rho)
    weighted_loss_sum += (1.00 - 0.30) * final_loss_tail

    total_portfolio_expected_loss = (1.0 - recovery) * p_5y
    print("\nCapital Structure Articulation Identity:")
    print(f"  Sum of Tranche Losses (weighted by tranche width): {weighted_loss_sum * 100:6.4f}%")
    print(f"  Total Portfolio Expected Loss (1 - R) * p:          {total_portfolio_expected_loss * 100:6.4f}%")
    discrepancy = abs(weighted_loss_sum - total_portfolio_expected_loss)
    print(f"  Discrepancy:                                        {discrepancy:1.2e}")

    assert abs(weighted_loss_sum - total_portfolio_expected_loss) < 1e-4


main()
