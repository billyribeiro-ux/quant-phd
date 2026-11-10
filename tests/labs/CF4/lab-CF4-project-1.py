"""CF4 project lab 1 (rung 2 completion): Full valuation engine pipeline.

Calculates FCFF, discounts explicit cash flows and terminal value to determine
Enterprise Value, and applies the enterprise-to-equity bridge to determine
equity value and per-share price.
"""

from __future__ import annotations

import numpy as np


def calculate_fcff(
    ebit: np.ndarray,
    tax_rate: float,
    depreciation: np.ndarray,
    capex: np.ndarray,
    delta_nwc: np.ndarray,
) -> np.ndarray:
    """Calculate Free Cash Flow to the Firm (FCFF)."""
    nopat = ebit * (1.0 - tax_rate)
    return np.asarray(nopat + depreciation - capex - delta_nwc)


def dcf_enterprise_value(
    fcff_forecast: np.ndarray,
    wacc: float,
    terminal_growth: float,
    mid_year: bool = False,
) -> dict[str, float]:
    """Discount explicit FCFF forecast and terminal value to determine Enterprise Value."""
    h = len(fcff_forecast)
    periods = np.arange(1, h + 1, dtype=np.float64)
    discount_powers = periods - 0.5 if mid_year else periods
    pv_explicit = float(np.sum(fcff_forecast / np.power(1.0 + wacc, discount_powers)))

    last_cf = float(fcff_forecast[-1])
    terminal_value = (last_cf * (1.0 + terminal_growth)) / (wacc - terminal_growth)
    pv_terminal = float(terminal_value / np.power(1.0 + wacc, float(h)))
    enterprise_value = pv_explicit + pv_terminal
    tv_share = pv_terminal / enterprise_value if enterprise_value != 0.0 else 0.0

    return {
        "pv_explicit": pv_explicit,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "tv_share": tv_share,
    }


def enterprise_to_equity_bridge(
    enterprise_value: float,
    total_debt: float,
    cash: float,
    minority_interest: float = 0.0,
    preferred_stock: float = 0.0,
    non_operating_assets: float = 0.0,
    shares_outstanding: float = 1.0,
) -> dict[str, float]:
    """Reconcile enterprise value to common equity value and per-share price."""
    net_debt = total_debt - cash
    equity_value = enterprise_value - total_debt + cash - minority_interest - preferred_stock + non_operating_assets
    per_share_value = equity_value / shares_outstanding
    return {
        "net_debt": float(net_debt),
        "equity_value": float(equity_value),
        "per_share_value": float(per_share_value),
    }


def main() -> None:
    print("CF4 Project Completion: Core Valuation Pipeline")
    print("================================================")

    # 5-year operating forecast ($M)
    ebit = np.array([120.0, 135.0, 150.0, 165.0, 180.0])
    depr = np.array([25.0, 28.0, 30.0, 32.0, 35.0])
    capex = np.array([40.0, 42.0, 45.0, 48.0, 50.0])
    delta_nwc = np.array([10.0, 12.0, 14.0, 15.0, 16.0])
    tax_rate = 0.25

    fcff = calculate_fcff(ebit, tax_rate, depr, capex, delta_nwc)
    print("Projected FCFF ($M):", np.round(fcff, 2))

    wacc = 0.090  # 9.0%
    g = 0.025  # 2.5% terminal growth
    dcf = dcf_enterprise_value(fcff, wacc=wacc, terminal_growth=g, mid_year=False)

    print(f"PV of explicit FCFF:  ${dcf['pv_explicit']:.2f}M")
    print(f"Terminal Value (TV5): ${dcf['terminal_value']:.2f}M")
    print(f"PV of Terminal Value: ${dcf['pv_terminal']:.2f}M")
    print(f"Enterprise Value:     ${dcf['enterprise_value']:.2f}M")
    print(f"Terminal Value Share: {dcf['tv_share']:.2%}")

    # Capital claims ($M)
    total_debt = 350.0
    cash = 80.0
    minority_interest = 25.0
    preferred_stock = 15.0
    non_operating_assets = 30.0
    shares = 50.0  # million shares

    bridge = enterprise_to_equity_bridge(
        enterprise_value=dcf["enterprise_value"],
        total_debt=total_debt,
        cash=cash,
        minority_interest=minority_interest,
        preferred_stock=preferred_stock,
        non_operating_assets=non_operating_assets,
        shares_outstanding=shares,
    )

    print(f"Net Debt:             ${bridge['net_debt']:.2f}M")
    print(f"Equity Value:         ${bridge['equity_value']:.2f}M")
    print(f"Per-Share Fair Value: ${bridge['per_share_value']:.2f}")


main()
