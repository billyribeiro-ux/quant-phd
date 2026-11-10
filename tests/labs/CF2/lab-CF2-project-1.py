"""CF2 project lab 1 (rung 1, worked example): Full cost of capital pipeline under uncertainty.

SIMULATED: Firm data and market assumptions are generated for a simulated corporate issuer.
Money is in integer cents; component rates are floats; valuations are rounded half-up in cents.
Standard library only; no external network access.
Demonstrates the full end-to-end valuation pipeline with delta-method error propagation.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal


def main() -> None:
    print("CF2 Project Rung 1: Cost-of-Capital Estimation Pipeline (Worked Example)")
    print("======================================================================")

    # 1. Stated Inputs
    debt_cents = 4_000_000_000  # $40,000,000.00
    equity_cents = 6_000_000_000  # $60,000,000.00
    total_cents = debt_cents + equity_cents  # $100,000,000.00
    tau_c = 0.25

    rf = 0.0425  # 4.25% 10-year Treasury constant-maturity rate
    erp = 0.0550  # 5.50% Equity risk premium
    spread = 0.0175  # 1.75% (175 bps) debt credit spread

    beta_l = 1.30  # Estimated levered equity beta
    var_beta = 0.0225  # se(beta) = 0.150
    var_erp = 0.000100  # se(ERP) = 0.010 (100 bps)
    cov_beta_erp = 0.000300  # Positive estimation covariance
    var_spread = 0.000016  # se(spread) = 0.004 (40 bps)

    cash_flow_cents = 500_000_000  # $5,000,000.00 next-period operating cash flow
    growth = 0.0200  # 2.00% terminal growth

    # 2. Capital Structure Weights and Unlevering
    w_e = equity_cents / total_cents
    w_d = debt_cents / total_cents
    de_ratio = debt_cents / equity_cents
    beta_u = beta_l / (1.0 + (1.0 - tau_c) * de_ratio)

    # 3. Cost of Capital Components
    re = rf + beta_l * erp
    rd = rf + spread
    after_tax_rd = rd * (1.0 - tau_c)
    r_wacc = w_e * re + w_d * after_tax_rd

    # 4. Delta-Method Variance of WACC
    # Gradient: [w_E * ERP, w_E * beta, w_D * (1 - tau_c)]
    term_equity = (w_e**2) * (erp**2 * var_beta + beta_l**2 * var_erp + 2.0 * beta_l * erp * cov_beta_erp)
    term_debt = (w_d * (1.0 - tau_c)) ** 2 * var_spread
    wacc_var = term_equity + term_debt
    wacc_se = math.sqrt(wacc_var)

    # 5. Valuation Range using Decimal half-up rounding
    k = 1.0
    d_mid = Decimal(str(r_wacc))
    d_se = Decimal(str(wacc_se))
    d_g = Decimal(str(growth))
    d_cf = Decimal(cash_flow_cents)

    r_low = d_mid - Decimal(str(k)) * d_se
    r_high = d_mid + Decimal(str(k)) * d_se

    val_low = (d_cf / (r_high - d_g)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    val_base = (d_cf / (d_mid - d_g)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    val_high = (d_cf / (r_low - d_g)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

    cap_str = (
        f"Capital: Debt = ${debt_cents / 100:,.2f} | Equity = ${equity_cents / 100:,.2f} | "
        f"Total = ${total_cents / 100:,.2f}"
    )
    print(cap_str)
    print(f"Weights: w_E = {w_e:.4f}, w_D = {w_d:.4f}, D/E = {de_ratio:.4f}")
    print(f"Asset beta (beta_U):        {beta_u:.4f} (from equity beta {beta_l:.4f})")
    print(f"Cost of equity (r_E):       {re:.4%}")
    print(f"Pre-tax cost of debt (r_D): {rd:.4%}")
    print(f"After-tax cost of debt:     {after_tax_rd:.4%}")
    print(f"WACC point estimate:        {r_wacc:.4%}")
    print(f"Delta-method variance:      {wacc_var:.8f}")
    print(f"Delta-method standard error:{wacc_se:.4%} ({wacc_se * 10000:.1f} bps)")
    print(f"\nTerminal growth rate (g):   {growth:.2%}")
    print(f"Base Enterprise Valuation:  ${int(val_base) / 100:,.2f}")
    print("Valuation Band (k = 1.0 SE):")
    print(f"  Low valuation (at {float(r_high):.4%}):  ${int(val_low) / 100:,.2f}")
    print(f"  High valuation (at {float(r_low):.4%}): ${int(val_high) / 100:,.2f}")
    print(f"  Valuation Uncertainty Span:   ${(int(val_high) - int(val_low)) / 100:,.2f}")


main()
