"""Lab CR1-L03-1: Leland (1994) endogenous default boundary and optimal capital structure.

Demonstrates the smooth pasting condition, analytical endogenous bankruptcy boundary V_B,
firm value decomposition (unlevered value, tax shield, bankruptcy costs), and optimal leverage.
"""

from __future__ import annotations

import math


def leland_model(
    v: float,
    c: float,
    r: float,
    sigma: float,
    tau_c: float,
    alpha: float,
) -> dict[str, float]:
    """Calculate Leland (1994) perpetual debt, equity, and firm value."""
    # Characteristic power X = 2r / sigma^2
    x_pow = 2.0 * r / (sigma * sigma)

    # Endogenous default boundary derived from smooth pasting dE/dV = 0
    # V_B = (1 - tau_c) * C / (r + 0.5 * sigma^2)
    v_b = (1.0 - tau_c) * c / (r + 0.5 * sigma * sigma)

    if v <= v_b:
        # Already in default
        p_b = 1.0
        debt = (1.0 - alpha) * v
        equity = 0.0
        tax_shield = 0.0
        bankruptcy_costs = alpha * v
        firm_value = (1.0 - alpha) * v
    else:
        # Default probability factor (V / V_B)^{-X}
        p_b = math.pow(v / v_b, -x_pow)
        debt = (c / r) * (1.0 - p_b) + (1.0 - alpha) * v_b * p_b
        equity = v - (1.0 - tau_c) * (c / r) * (1.0 - p_b) - v_b * p_b
        tax_shield = (tau_c * c / r) * (1.0 - p_b)
        bankruptcy_costs = alpha * v_b * p_b
        firm_value = v + tax_shield - bankruptcy_costs

    # Articulation check: Equity + Debt == Total Firm Value
    assert abs(equity + debt - firm_value) < 1e-9

    leverage = debt / firm_value if firm_value > 0 else 0.0
    credit_spread_bps = ((c / debt) - r) * 10000.0 if debt > 0 else 0.0

    return {
        "v_b": v_b,
        "debt": debt,
        "equity": equity,
        "firm_value": firm_value,
        "tax_shield": tax_shield,
        "bankruptcy_costs": bankruptcy_costs,
        "leverage": leverage,
        "credit_spread_bps": credit_spread_bps,
        "p_b": p_b,
    }


def main() -> None:
    # Base parameters from Leland (1994): V = 100, r = 0.06, sigma = 0.20, tau_c = 0.35, alpha = 0.50
    v = 100.0
    r = 0.06
    sigma = 0.20
    tau_c = 0.35
    alpha = 0.50

    print("Leland (1994) Capital Structure and Firm Value Across Coupon Choices (V=100, tau_c=0.35, alpha=0.50):")
    print("  Coupon C |  Def V_B  |  Debt ($)  | Equity ($) | Total Value | TaxShield | BankruptCost | Leverage")
    print("-----------+-----------+------------+------------+-------------+-----------+--------------+---------")

    coupons = [2.0, 4.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0]
    best_c = 0.0
    max_val = 0.0

    for c in coupons:
        res = leland_model(v, c, r, sigma, tau_c, alpha)
        if res["firm_value"] > max_val:
            max_val = res["firm_value"]
            best_c = c
        print(
            f"   {c:5.1f}   |   {res['v_b']:5.2f}   |   {res['debt']:6.2f}   |   "
            f"{res['equity']:6.2f}   |   {res['firm_value']:7.2f}   |   "
            f"{res['tax_shield']:6.2f}  |    {res['bankruptcy_costs']:6.2f}    |  "
            f"{res['leverage'] * 100:5.1f}%"
        )

    print(f"\nOptimal perpetual coupon: C* = {best_c:.1f} yielding maximum firm value = ${max_val:.2f}")

    # Verify smooth-pasting boundary condition: dE/dV at V=V_B is exactly 0
    c_test = 6.0
    v_b_test = (1.0 - tau_c) * c_test / (r + 0.5 * sigma * sigma)
    # Evaluate numerical derivative of E just above V_B
    eps = 1e-5
    e_vb = leland_model(v_b_test, c_test, r, sigma, tau_c, alpha)["equity"]
    e_vb_plus = leland_model(v_b_test + eps, c_test, r, sigma, tau_c, alpha)["equity"]
    de_dv = (e_vb_plus - e_vb) / eps
    print(f"Smooth pasting check: E(V_B) = {e_vb:.6f}, dE/dV(V_B+) = {de_dv:.6f} (matches theoretical 0)")
    assert abs(e_vb) < 1e-9
    assert abs(de_dv) < 1e-3


main()
