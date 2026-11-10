"""CF2 project lab 3 (rung 3 check): Reference numbers for independent memo evaluation.

Real data: 10-year Treasury constant-maturity yield (cmt_10y) from ust_daily.csv.
SIMULATED / BYOD: Corporate returns, equity risk premium, and debt spreads.
Money is in integer cents; component rates are decimals; valuations are rounded half-up in cents.
Standard library only; reads data/ust_daily.csv.
Computes and prints the exact baseline table that the student's project memo must reproduce.
"""

from __future__ import annotations

import csv
import math
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

VALUATION_DATE = "2026-09-30"


def read_risk_free_rate(csv_path: Path, target_date: str) -> float:
    """Read 10-year Treasury constant-maturity yield on or before target date from ust_daily.csv."""
    latest_yield = None
    with csv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["date"] <= target_date and row["cmt_10y"]:
                latest_yield = float(row["cmt_10y"])
    if latest_yield is None:
        raise ValueError(f"No Treasury yield found on or before {target_date}")
    # Published by H.15 in percent per year; convert to decimal
    return latest_yield / 100.0


def main() -> None:
    print("CF2 Project Rung 3: Sanity Check and Memo Benchmark")
    print("==================================================")

    # Locate ust_daily.csv
    csv_path = Path("data") / "ust_daily.csv"
    if not csv_path.exists():
        csv_path = Path("course/assets/data/market/ust_daily.csv")

    rf = read_risk_free_rate(csv_path, VALUATION_DATE)

    # Stated firm parameters (from project specification)
    debt_cents = 4_500_000_000  # $45,000,000.00
    equity_cents = 5_500_000_000  # $55,000,000.00
    total_cents = debt_cents + equity_cents  # $100,000,000.00
    tau_c = 0.25

    erp = 0.0500  # 5.00%
    spread = 0.0180  # 1.80% (180 bps)
    beta_l = 1.15
    var_beta = 0.0196  # se = 0.14
    var_erp = 0.000100  # se = 0.01
    cov_beta_erp = 0.000200
    var_spread = 0.000016  # se = 0.004

    cash_flow_cents = 600_000_000  # $6,000,000.00
    growth = 0.0200  # 2.00%

    # Pipeline calculations
    we = equity_cents / total_cents
    wd = debt_cents / total_cents
    de = debt_cents / equity_cents

    bu = beta_l / (1.0 + (1.0 - tau_c) * de)
    re = rf + beta_l * erp
    rd = rf + spread
    after_tax_rd = rd * (1.0 - tau_c)
    wacc_val = we * re + wd * after_tax_rd

    term_eq = (we**2) * (erp**2 * var_beta + beta_l**2 * var_erp + 2.0 * beta_l * erp * cov_beta_erp)
    term_d = (wd * (1.0 - tau_c)) ** 2 * var_spread
    wacc_var = term_eq + term_d
    wacc_se = math.sqrt(wacc_var)

    # Valuation range at k = 1.0
    d_mid = Decimal(str(wacc_val))
    d_se = Decimal(str(wacc_se))
    d_g = Decimal(str(growth))
    d_cf = Decimal(cash_flow_cents)

    r_low = d_mid - d_se
    r_high = d_mid + d_se

    val_low = int((d_cf / (r_high - d_g)).quantize(Decimal("1"), ROUND_HALF_UP))
    val_base = int((d_cf / (d_mid - d_g)).quantize(Decimal("1"), ROUND_HALF_UP))
    val_high = int((d_cf / (r_low - d_g)).quantize(Decimal("1"), ROUND_HALF_UP))

    print(f"Valuation Date:                   {VALUATION_DATE}")
    print(f"10-Year Treasury Yield (r_f):     {rf:.4%} (real data: H.15 cmt_10y)")
    print(f"Asset beta (beta_U):              {bu:.4f}")
    print(f"Cost of equity (r_E):             {re:.4%}")
    print(f"Pre-tax cost of debt (r_D):       {rd:.4%}")
    print(f"After-tax cost of debt:           {after_tax_rd:.4%}")
    print(f"WACC point estimate:              {wacc_val:.4%}")
    print(f"Delta-method variance:            {wacc_var:.8f}")
    print(f"Delta-method standard error:      {wacc_se:.4%} ({wacc_se * 10000:.1f} bps)")
    print(f"\nTerminal growth rate (g):         {growth:.2%}")
    print(f"Base enterprise valuation:        ${val_base / 100:,.2f} ({val_base} cents)")
    print("Valuation range (k = 1.0 SE):")
    print(f"  Low valuation (at {float(r_high):.4%}):       ${val_low / 100:,.2f} ({val_low} cents)")
    print(f"  High valuation (at {float(r_low):.4%}):      ${val_high / 100:,.2f} ({val_high} cents)")
    print(f"  Uncertainty spread:             ${(val_high - val_low) / 100:,.2f}")


main()
