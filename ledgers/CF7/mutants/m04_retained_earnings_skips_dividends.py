"""Retained earnings roll-forward fails to deduct cash dividends paid from net income.

Student error: rolls forward retained earnings as opening RE plus Net Income, failing to deduct
cash dividends distributed to shareholders.
"""

from __future__ import annotations

from typing import Any

import reference


def validate_inputs(inputs: dict[str, Any]) -> None:
    reference.validate_inputs(inputs)


def solve_revolver_circularity(
    c_min: float,
    c_prev: float,
    r_prev: float,
    cf_core: float,
    r_rate: float,
    c_rate: float,
    tax_rate: float,
    max_revolver: float,
    div_rate: float = 0.0,
) -> tuple[float, float, float]:
    return reference.solve_revolver_circularity(
        c_min, c_prev, r_prev, cf_core, r_rate, c_rate, tax_rate, max_revolver, div_rate
    )


def build_model(inputs: dict[str, Any]) -> dict[str, Any]:
    res = reference.build_model(inputs)
    # Corrupt retained earnings by adding back dividends
    divs = res["cash_flow_statement"]["dividends"]
    re_corrupt = []
    cum_div = 0.0
    for r, d in zip(res["balance_sheet"]["retained_earnings"], divs, strict=False):
        cum_div += d
        re_corrupt.append(r + cum_div)
    res["balance_sheet"]["retained_earnings"] = re_corrupt
    return res


def compute_sensitivity_table(
    fcff_list: list[float],
    horizon: int,
    net_debt: float,
    shares: float,
    wacc_range: list[float],
    g_range: list[float],
) -> list[list[float]]:
    return reference.compute_sensitivity_table(fcff_list, horizon, net_debt, shares, wacc_range, g_range)


def reconcile_sheets(sheet_data: dict[str, Any], model_data: dict[str, Any], tolerance: float = 1e-4) -> dict[str, Any]:
    return reference.reconcile_sheets(sheet_data, model_data, tolerance)


def check_hardcodes(formulas: dict[str, str]) -> list[str]:
    return reference.check_hardcodes(formulas)
