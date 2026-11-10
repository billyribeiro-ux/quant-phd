"""Lab CR1-L04-1: Reduced-form credit models and Duffie-Singleton intensity pricing.

Demonstrates defaultable zero-coupon bond pricing under constant hazard rates,
compares Recovery of Market Value (RMV) vs Recovery of Face Value (RFV),
and prices affine term structures under Cox-Ingersoll-Ross (CIR) stochastic default intensity.
"""

from __future__ import annotations

import math


def reduced_form_pricing(
    maturity: float,
    r: float,
    lam: float,
    rec: float,
    convention: str = "rmv",
) -> dict[str, float]:
    """Price defaultable bond under constant intensity."""
    t = maturity
    if convention == "rmv":
        disc_rate = r + lam * (1.0 - rec)
        price = math.exp(-disc_rate * t)
    else:  # 'rfv'
        tot = r + lam
        p_surv = math.exp(-tot * t)
        p_rec = (rec * lam / tot) * (1.0 - p_surv)
        price = p_surv + p_rec

    bond_yield = -math.log(price) / t
    spread_bps = (bond_yield - r) * 10000.0
    survival_prob = math.exp(-lam * t)

    return {
        "price": price,
        "yield": bond_yield,
        "spread_bps": spread_bps,
        "survival_prob": survival_prob,
    }


def cir_intensity_bond_price(
    t: float,
    r: float,
    lam0: float,
    kappa: float,
    theta: float,
    sigma_lam: float,
    rec: float = 0.4,
) -> tuple[float, float]:
    """Price defaultable bond under CIR stochastic default intensity with RMV.

    dlambda_t = kappa * (theta - lambda_t) dt + sigma_lam * sqrt(lambda_t) dW_t
    Effective loss rate L = 1 - R.
    Discount rate R_t = r + L * lambda_t.
    """
    loss = 1.0 - rec
    # Rescaled CIR parameters for effective discount factor
    # S_t = loss * lambda_t
    # Alternatively solve standard Riccati ODE for E[exp(-L int lambda_s ds)]:
    # gamma = sqrt(kappa^2 + 2 * sigma_lam^2 * L)
    gamma = math.sqrt(kappa * kappa + 2.0 * sigma_lam * sigma_lam * loss)
    exp_gt = math.exp(gamma * t)
    denom = (gamma + kappa) * (exp_gt - 1.0) + 2.0 * gamma

    b_t = 2.0 * loss * (exp_gt - 1.0) / denom
    a_t = math.pow(2.0 * gamma * math.exp(0.5 * (kappa + gamma) * t) / denom, 2.0 * kappa * theta / (sigma_lam**2))

    credit_discount = a_t * math.exp(-b_t * lam0)
    riskfree_discount = math.exp(-r * t)
    total_price = riskfree_discount * credit_discount

    bond_yield = -math.log(total_price) / t
    spread_bps = (bond_yield - r) * 10000.0
    return total_price, spread_bps


def main() -> None:
    # Baseline parameters: r = 0.03, lambda = 0.02 (200 bp hazard), R = 0.40
    r = 0.03
    lam_const = 0.02
    rec = 0.40
    maturities = [1.0, 2.0, 3.0, 5.0, 7.0, 10.0]

    print("Reduced-Form Pricing: RMV vs RFV Recovery Conventions (r=3%, lambda=200bp, R=40%):")
    print("  T (yr) | RMV Price | RMV Spread | RFV Price | RFV Spread | Survival Prob")
    print("---------+-----------+------------+-----------+------------+--------------")

    for t in maturities:
        rmv = reduced_form_pricing(t, r, lam_const, rec, convention="rmv")
        rfv = reduced_form_pricing(t, r, lam_const, rec, convention="rfv")
        # Under constant intensity RMV, spread is constant = lambda * (1 - R) = 0.02 * 0.60 = 120 bps
        assert abs(rmv["spread_bps"] - 120.0) < 1e-9
        print(
            f"  {t:5.1f}  |  {rmv['price']:8.4f} |  {rmv['spread_bps']:6.1f} bp |  "
            f"{rfv['price']:8.4f} |  {rfv['spread_bps']:6.1f} bp |   {rmv['survival_prob']:8.4f}"
        )

    # CIR stochastic intensity: kappa = 0.3, theta = 0.03, sigma_lam = 0.08, lambda_0 = 0.01 (100 bp)
    kappa = 0.3
    theta = 0.03
    sigma_lam = 0.08
    lam0 = 0.01

    print("\nAffine Term Structure under CIR Default Intensity (lam0=100bp, theta=300bp):")
    print("  T (yr) | Total Bond Price | Yield (%) | Credit Spread (bp)")
    print("---------+------------------+-----------+-------------------")

    cir_spreads: list[float] = []
    for t in maturities:
        p_cir, s_cir = cir_intensity_bond_price(t, r, lam0, kappa, theta, sigma_lam, rec)
        cir_spreads.append(s_cir)
        print(f"  {t:5.1f}  |      {p_cir:8.4f}    |   {-math.log(p_cir) / t * 100:5.2f}%  |      {s_cir:6.1f}")

    # Because lam0 < theta, mean reversion causes credit spread to slope upward over time
    is_upward = all(cir_spreads[i] <= cir_spreads[i + 1] for i in range(len(cir_spreads) - 1))
    print(f"\nCIR credit spread curve is upward-sloping from mean reversion: {is_upward}")
    assert is_upward


main()
