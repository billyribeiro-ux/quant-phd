"""Lab FI6-L01-1: Multi-Curve Bootstrapping and Swap Pricing.

Demonstrates dual-curve pricing: OIS discount curve vs. floating projection curve.
Compares multi-curve swap valuation with naive single-curve discounting,
quantifying the pricing discrepancy introduced by basis spreads.
"""

from __future__ import annotations

import math


def discount_factor(zero_rate: float, tenor: float) -> float:
    """Continuous compounding discount factor P(0, T) = exp(-r * T)."""
    return math.exp(-zero_rate * tenor)


def forward_rate_from_factors(df_start: float, df_end: float, tau: float) -> float:
    """Simple forward rate F(0; T_start, T_end) = (P(0, T_start)/P(0, T_end) - 1) / tau."""
    return (df_start / df_end - 1.0) / tau


def run_lab() -> None:
    print("=== Multi-Curve Discounting & Swap Valuation ===")

    # Market curves: OIS (SOFR) discounting curve vs. Forwarding curve (Term reference)
    # Tenors: 0.5y, 1.0y, 1.5y, 2.0y, 2.5y, 3.0y (semi-annual fixed leg, quarterly or semi float)
    tenors = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    tau = 0.5  # semi-annual accrual

    # OIS zero rates (discount curve) and Reference zero rates (projection curve)
    # Basis spread is ~25-35 bps across tenors
    ois_rates = [0.0380, 0.0395, 0.0405, 0.0415, 0.0422, 0.0428]
    proj_rates = [0.0410, 0.0428, 0.0440, 0.0450, 0.0457, 0.0463]

    p_ois = [discount_factor(r, t) for r, t in zip(ois_rates, tenors, strict=False)]
    p_proj = [discount_factor(r, t) for r, t in zip(proj_rates, tenors, strict=False)]

    print(
        f"{'Tenor (y)':<10} {'OIS Zero':<10} {'P_OIS(0,T)':<12} "
        f"{'Proj Zero':<10} {'P_Proj(0,T)':<12} {'Basis (bps)':<12}"
    )
    for t, ro, do, rp, dp in zip(tenors, ois_rates, p_ois, proj_rates, p_proj, strict=False):
        basis_bps = (rp - ro) * 10000.0
        print(f"{t:<10.1f} {ro:<10.4f} {do:<12.5f} {rp:<10.4f} {dp:<12.5f} {basis_bps:<12.1f}")

    # Compute forward rates on projection curve
    fwd_rates = []
    for i in range(len(tenors)):
        df_start = 1.0 if i == 0 else p_proj[i - 1]
        df_end = p_proj[i]
        f = forward_rate_from_factors(df_start, df_end, tau)
        fwd_rates.append(f)

    # Swap Annuity under OIS discounting: A(0) = sum(tau * P_OIS(0, T_k))
    annuity_multicurve = sum(tau * do for do in p_ois)

    # Floating leg PV under multi-curve: sum(tau * P_OIS(0, T_k) * F_k)
    pv_float_multicurve = sum(tau * do * f for do, f in zip(p_ois, fwd_rates, strict=False))

    # Multi-curve par swap rate: S_multi = pv_float / annuity
    s_multi = pv_float_multicurve / annuity_multicurve

    # Naive single-curve calculation (using projection curve for both discounting and forwarding)
    annuity_single = sum(tau * dp for dp in p_proj)
    # In single curve, floating leg telescopes to 1 - P(0, T_n)
    pv_float_single = 1.0 - p_proj[-1]
    s_single = pv_float_single / annuity_single

    # Also compute single curve when using OIS for both:
    annuity_ois_single = sum(tau * do for do in p_ois)
    pv_float_ois_single = 1.0 - p_ois[-1]
    s_ois_single = pv_float_ois_single / annuity_ois_single

    print("\n--- 3-Year Par Swap Rate Analysis ---")
    print(f"Multi-Curve Par Swap Rate  : {s_multi * 100.0:.4f}% ({s_multi * 10000.0:.1f} bps)")
    print(f"Single-Curve (Proj only)   : {s_single * 100.0:.4f}% ({s_single * 10000.0:.1f} bps)")
    print(f"Single-Curve (OIS only)    : {s_ois_single * 100.0:.4f}% ({s_ois_single * 10000.0:.1f} bps)")
    print(f"Dual-Curve Annuity A(0)    : {annuity_multicurve:.5f}")

    # Valuation of fixed-rate receiver swap with fixed coupon K = 4.50% on $100M notional
    notional = 100_000_000.0
    k_fixed = 0.0450
    pv_swap_multicurve = notional * (k_fixed * annuity_multicurve - pv_float_multicurve)
    pv_swap_single = notional * (k_fixed * annuity_single - pv_float_single)

    pricing_diff = pv_swap_multicurve - pv_swap_single
    print("\nReceiver Swap PV (Fixed = 4.50%, Notional = $100M):")
    print(f"Multi-Curve PV             : ${pv_swap_multicurve:,.2f}")
    print(f"Single-Curve PV            : ${pv_swap_single:,.2f}")
    print(
        f"Pricing Error (Naive - Dual): ${-pricing_diff:,.2f} "
        f"({(-pricing_diff / notional) * 10000.0:.2f} bps of notional)"
    )


run_lab()
