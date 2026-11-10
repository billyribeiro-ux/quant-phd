"""Lab Project 2 (Completion Problem Solution): WACC and Sloan Accruals calculation."""

from __future__ import annotations


def compute_wacc(we: float, re: float, wd: float, rd: float, tax_rate: float) -> float:
    """Compute weighted average cost of capital under corporate taxation."""
    equity_component = we * re
    debt_component = wd * rd * (1.0 - tax_rate)
    return equity_component + debt_component


def compute_sloan_accruals(
    delta_ca: float,
    delta_cash: float,
    delta_cl: float,
    delta_std: float,
    depr: float,
) -> float:
    """Compute operating accruals following Sloan (1996) balance sheet identity."""
    delta_working_assets = delta_ca - delta_cash
    delta_operating_liabilities = delta_cl - delta_std
    return delta_working_assets - delta_operating_liabilities - depr


def main() -> None:
    # 1. WACC computation check
    we = 0.70
    re = 0.095
    wd = 0.30
    rd = 0.050
    tax_rate = 0.25

    wacc = compute_wacc(we, re, wd, rd, tax_rate)
    print(f"Weighted Average Cost of Capital (WACC): {wacc * 100:.3f}%")

    # 2. Sloan Accruals check
    d_ca = 85.0
    d_cash = 15.0
    d_cl = 40.0
    d_std = 5.0
    depr = 50.0

    accruals = compute_sloan_accruals(d_ca, d_cash, d_cl, d_std, depr)
    print(f"Operating Accruals (Sloan 1996): {accruals:+.2f}")


main()
