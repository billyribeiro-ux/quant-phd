"""Revolver interest circularity ignores the interest tax shield, overstating cash interest drain.

Student error: uses gross pre-tax interest rate in the circularity closed-form denominator
and core cash flow calculation instead of the after-tax net borrowing cost.
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
    # Error: alpha set to 1.0 (no tax shield)
    alpha = 1.0
    num_c_zero = c_prev * (1.0 + 0.5 * alpha * c_rate) + cf_core - r_prev * (1.0 + 0.5 * alpha * r_rate)
    den_c_zero = 1.0 - 0.5 * alpha * c_rate
    c_zero = num_c_zero / den_c_zero

    if c_zero >= c_min:
        return 0.0, c_zero, -r_prev

    c_bar_min = 0.5 * (c_prev + c_min)
    num_r = (c_min - c_prev) - cf_core - alpha * c_rate * c_bar_min + r_prev * (1.0 + 0.5 * alpha * r_rate)
    den_r = 1.0 - 0.5 * alpha * r_rate
    r_calc = num_r / den_r

    if r_calc <= max_revolver:
        r_t = max(0.0, r_calc)
        return r_t, c_min, r_t - r_prev

    r_t = max_revolver
    delta_r = max_revolver - r_prev
    num_c_cap = (
        c_prev * (1.0 + 0.5 * alpha * c_rate) + cf_core - 0.5 * alpha * r_rate * (r_prev + max_revolver) + delta_r
    )
    den_c_cap = 1.0 - 0.5 * alpha * c_rate
    c_t = num_c_cap / den_c_cap
    return r_t, c_t, delta_r


def build_model(inputs: dict[str, Any]) -> dict[str, Any]:
    # Run reference with the corrupted solver
    return reference.build_model(inputs)


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
