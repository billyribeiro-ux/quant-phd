"""Debt interest expense computed on opening debt balance instead of average debt balance.

Student error: uses opening debt balance rather than average debt balance across the period,
understating interest expense when debt increases or overstating it when debt is amortized.
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
    # Tamper with interest calculation: compute interest on beginning debt instead of average
    term_rate = float(inputs["debt_assumptions"]["term_debt_interest_rate"])
    float(inputs["historical_data"]["term_debt"])
    term_beg = res["debt_schedule"]["term_debt_opening"]
    # Corrupt term interest on income statement
    corrupt_int = [b * term_rate for b in term_beg]
    res["income_statement"]["interest_expense"] = corrupt_int
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
