"""CF2 project lab 2 (rung 2, completion): Capital structure unlevering, WACC, and delta error.

SIMULATED: A corporate issuer with uncertain cost-of-capital inputs.
Money is in integer cents; component rates are floats; valuations are rounded half-up in cents.
Standard library only; no external network access.
The student completes the missing lines for beta unlevering, WACC, delta variance, and valuation.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal

DEBT_CENTS = 30_000_000_00  # $30,000,000.00 in cents
EQUITY_CENTS = 70_000_000_00  # $70,000,000.00 in cents
TAU_C = 0.25

RF = 0.0400  # 4.00%
ERP = 0.0500  # 5.00%
SPREAD = 0.0150  # 1.50% (150 bps)
BETA_L = 1.20
VAR_BETA = 0.0196  # se(beta) = 0.14
VAR_ERP = 0.000100  # se(ERP) = 0.01
COV_BETA_ERP = 0.000200
VAR_SPREAD = 0.000009  # se(spread) = 0.003

CASH_FLOW_CENTS = 400_000_000  # $4,000,000.00
GROWTH = 0.0200  # 2.00%


def main() -> None:
    total_cents = DEBT_CENTS + EQUITY_CENTS
    w_e = EQUITY_CENTS / total_cents
    w_d = DEBT_CENTS / total_cents
    de_ratio = DEBT_CENTS / EQUITY_CENTS

    # Line to complete in rung 2: unlever beta
    beta_u = BETA_L / (1.0 + (1.0 - TAU_C) * de_ratio)

    re = RF + BETA_L * ERP
    rd = RF + SPREAD
    after_tax_rd = rd * (1.0 - TAU_C)

    # Line to complete in rung 2: WACC calculation
    r_wacc = w_e * re + w_d * after_tax_rd

    # Line to complete in rung 2: delta-method equity uncertainty term
    term_equity = (w_e**2) * (ERP**2 * VAR_BETA + BETA_L**2 * VAR_ERP + 2.0 * BETA_L * ERP * COV_BETA_ERP)
    term_debt = (w_d * (1.0 - TAU_C)) ** 2 * VAR_SPREAD
    wacc_var = term_equity + term_debt
    wacc_se = math.sqrt(wacc_var)

    # Line to complete in rung 2: valuation bounds
    d_mid = Decimal(str(r_wacc))
    d_se = Decimal(str(wacc_se))
    d_g = Decimal(str(GROWTH))
    d_cf = Decimal(CASH_FLOW_CENTS)

    r_low = d_mid - d_se
    r_high = d_mid + d_se

    val_low = int((d_cf / (r_high - d_g)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    val_high = int((d_cf / (r_low - d_g)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    print(f"Asset beta (beta_U):        {beta_u:.4f}")
    print(f"WACC point estimate:        {r_wacc:.4%}")
    print(f"Delta standard error:       {wacc_se:.4%}")
    print(f"Valuation Low:              ${val_low / 100:,.2f}")
    print(f"Valuation High:             ${val_high / 100:,.2f}")


main()
