"""CF2 lab L01-1: Exact weighted average cost of capital (WACC) identity.

Model: Exact closed-form capital structure valuation using fractions.Fraction.
No synthetic or simulated data is used; all parameters are exact rational numbers.
Demonstrates that market-value weights sum to unity and WACC equals the weighted
average of the cost of equity and after-tax cost of debt.
"""

from __future__ import annotations

from fractions import Fraction


def calculate_wacc(
    equity: Fraction,
    debt: Fraction,
    cost_equity: Fraction,
    cost_debt: Fraction,
    tax_rate: Fraction,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Compute (weight_equity, weight_debt, after_tax_cost_debt, wacc) exactly."""
    total_val = equity + debt
    w_e = equity / total_val
    w_d = debt / total_val
    after_tax_rd = cost_debt * (Fraction(1, 1) - tax_rate)
    r_wacc = w_e * cost_equity + w_d * after_tax_rd
    return w_e, w_d, after_tax_rd, r_wacc


def main() -> None:
    print("CF2 Lab L01-1: The WACC Identity and Market-Value Weights")
    print("-------------------------------------------------------")

    # Stated capital structure in integer dollars
    equity = Fraction(60_000_000, 1)
    debt = Fraction(40_000_000, 1)
    r_e = Fraction(10, 100)  # 10.0%
    r_d = Fraction(6, 100)  # 6.0%
    tau_c = Fraction(25, 100)  # 25.0%

    w_e, w_d, after_tax_rd, r_wacc = calculate_wacc(equity, debt, r_e, r_d, tau_c)

    print(f"Equity market value: ${equity:,.2f}")
    print(f"Debt market value:   ${debt:,.2f}")
    print(f"Total value (V):     ${(equity + debt):,.2f}")
    print(f"Equity weight (w_E): {w_e} = {float(w_e):.4f}")
    print(f"Debt weight (w_D):   {w_d} = {float(w_d):.4f}")
    print(f"Weights sum to one:  {w_e + w_d == Fraction(1, 1)}")
    print(f"Pre-tax cost of debt:       {r_d} = {float(r_d):.4%}")
    print(f"After-tax cost of debt:     {after_tax_rd} = {float(after_tax_rd):.4%}")
    print(f"Cost of equity:             {r_e} = {float(r_e):.4%}")
    print(f"Exact WACC:                 {r_wacc} = {float(r_wacc):.4%}")

    print("\nWACC sensitivity to leverage (holding component costs constant):")
    for d_pct in [0, 20, 40, 50, 60, 80]:
        d_val = Fraction(d_pct * 1_000_000, 1)
        e_val = Fraction((100 - d_pct) * 1_000_000, 1)
        _, _, _, w = calculate_wacc(e_val, d_val, r_e, r_d, tau_c)
        print(f"  Debt share {d_pct:2d}%: WACC = {float(w):.4%} ({w})")


main()
