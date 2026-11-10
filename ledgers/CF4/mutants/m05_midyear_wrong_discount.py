"""Mutant m05: Student error: fails to adjust discounting power by 0.5 when
mid_year is True, applying full year-end powers.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np


def calculate_fcff(
    ebit: float | np.ndarray,
    tax_rate: float,
    depreciation: float | np.ndarray,
    capex: float | np.ndarray,
    delta_nwc: float | np.ndarray,
) -> float | np.ndarray:
    """Calculate Free Cash Flow to the Firm (FCFF)."""
    if tax_rate < 0.0 or tax_rate >= 1.0:
        raise ValueError(f"tax_rate must be in [0, 1), got {tax_rate}")

    ebit_arr = np.asarray(ebit, dtype=np.float64)
    depr_arr = np.asarray(depreciation, dtype=np.float64)
    capex_arr = np.asarray(capex, dtype=np.float64)
    nwc_arr = np.asarray(delta_nwc, dtype=np.float64)

    if np.any(depr_arr < 0.0):
        raise ValueError("depreciation cannot be negative")
    if np.any(capex_arr < 0.0):
        raise ValueError("capex cannot be negative")

    if not (ebit_arr.shape == depr_arr.shape == capex_arr.shape == nwc_arr.shape):
        raise ValueError("All inputs must have identical shapes")

    nopat = ebit_arr * (1.0 - tax_rate)
    fcff = nopat + depr_arr - capex_arr - nwc_arr

    if np.ndim(ebit) == 0:
        return float(fcff)
    return fcff


def dcf_enterprise_value(
    fcff_forecast: Sequence[float] | np.ndarray,
    wacc: float,
    terminal_method: str = "gordon",
    terminal_growth: float | None = None,
    exit_multiple: float | None = None,
    terminal_metric: float | None = None,
    mid_year: bool = False,
) -> dict[str, Any]:
    """Discount explicit FCFF forecast and terminal value to determine Enterprise Value."""
    if wacc <= 0.0:
        raise ValueError(f"WACC must be strictly positive, got {wacc}")

    cfs = np.asarray(fcff_forecast, dtype=np.float64)
    h = len(cfs)
    if h == 0:
        raise ValueError("fcff_forecast cannot be empty")

    periods = np.arange(1, h + 1, dtype=np.float64)
    # MUTATION: ignores mid_year and applies year-end powers
    discount_powers = periods
    discount_factors = 1.0 / np.power(1.0 + wacc, discount_powers)
    pv_explicit_arr = cfs * discount_factors
    pv_explicit = float(np.sum(pv_explicit_arr))

    if terminal_method == "gordon":
        if terminal_growth is None:
            raise ValueError("terminal_growth is required for Gordon growth method")
        if terminal_growth >= wacc:
            raise ValueError(f"terminal_growth ({terminal_growth}) must be strictly less than WACC ({wacc})")
        base_cf = float(cfs[-1]) if terminal_metric is None else float(terminal_metric)
        terminal_value = (base_cf * (1.0 + terminal_growth)) / (wacc - terminal_growth)
    elif terminal_method == "exit_multiple":
        if exit_multiple is None or exit_multiple <= 0.0:
            raise ValueError("exit_multiple must be positive for exit_multiple method")
        if terminal_metric is None or terminal_metric <= 0.0:
            raise ValueError("terminal_metric must be positive for exit_multiple method")
        terminal_value = float(terminal_metric * exit_multiple)
    else:
        raise ValueError(f"Unknown terminal_method: {terminal_method}")

    pv_terminal = float(terminal_value / np.power(1.0 + wacc, float(h)))
    enterprise_value = pv_explicit + pv_terminal
    tv_share = pv_terminal / enterprise_value if enterprise_value != 0.0 else 0.0

    return {
        "pv_explicit": pv_explicit,
        "terminal_value": float(terminal_value),
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
    if total_debt < 0.0 or cash < 0.0 or minority_interest < 0.0 or preferred_stock < 0.0 or non_operating_assets < 0.0:
        raise ValueError("Balance sheet claims and assets cannot be negative")
    if shares_outstanding <= 0.0:
        raise ValueError(f"shares_outstanding must be strictly positive, got {shares_outstanding}")

    net_debt = total_debt - cash
    equity_value = enterprise_value - total_debt + cash - minority_interest - preferred_stock + non_operating_assets
    per_share_value = equity_value / shares_outstanding

    return {
        "net_debt": float(net_debt),
        "equity_value": float(equity_value),
        "per_share_value": float(per_share_value),
    }


def residual_income_valuation(
    initial_book_equity: float,
    net_income_forecast: Sequence[float] | np.ndarray,
    dividends_forecast: Sequence[float] | np.ndarray,
    cost_of_equity: float,
    omega: float = 0.0,
) -> dict[str, Any]:
    """Compute equity value via Ohlson residual income model with clean surplus dynamics."""
    if initial_book_equity <= 0.0:
        raise ValueError("initial_book_equity must be strictly positive")
    if cost_of_equity <= 0.0:
        raise ValueError("cost_of_equity must be strictly positive")
    if omega < 0.0 or omega >= 1.0:
        raise ValueError(f"omega must be in [0, 1), got {omega}")

    nis = np.asarray(net_income_forecast, dtype=np.float64)
    divs = np.asarray(dividends_forecast, dtype=np.float64)
    if len(nis) != len(divs) or len(nis) == 0:
        raise ValueError("net_income_forecast and dividends_forecast must have same non-zero length")

    h = len(nis)
    book_values: list[float] = [float(initial_book_equity)]
    residual_income: list[float] = []
    pv_ri_list: list[float] = []

    curr_b = float(initial_book_equity)
    for t in range(h):
        ni = float(nis[t])
        div = float(divs[t])
        ri = ni - cost_of_equity * curr_b
        residual_income.append(ri)
        pv_ri = ri / ((1.0 + cost_of_equity) ** (t + 1))
        pv_ri_list.append(pv_ri)
        curr_b = curr_b + ni - div
        book_values.append(curr_b)

    pv_explicit_ri = float(sum(pv_ri_list))

    last_ri = residual_income[-1]
    denom = 1.0 + cost_of_equity - omega
    terminal_ri = (omega * last_ri) / denom if denom > 0.0 else 0.0
    pv_terminal_ri = float(terminal_ri / ((1.0 + cost_of_equity) ** h))

    total_equity_value = float(initial_book_equity + pv_explicit_ri + pv_terminal_ri)

    return {
        "book_values": book_values,
        "residual_income": residual_income,
        "pv_residual_income": pv_explicit_ri,
        "terminal_residual_income": float(terminal_ri),
        "pv_terminal_residual_income": pv_terminal_ri,
        "equity_value": total_equity_value,
    }


def multiples_valuation(
    metric_value: float,
    multiple: float,
    multiple_type: str = "ev_ebitda",
    net_debt: float = 0.0,
    shares_outstanding: float = 1.0,
) -> dict[str, float]:
    """Calculate implied enterprise and equity values from peer multiples."""
    if multiple <= 0.0:
        raise ValueError("multiple must be positive")
    if shares_outstanding <= 0.0:
        raise ValueError("shares_outstanding must be strictly positive")

    m_type = multiple_type.lower()
    if m_type in ("ev_ebitda", "ev_ebit", "ev_sales"):
        implied_ev = float(metric_value * multiple)
        implied_equity = float(implied_ev - net_debt)
    elif m_type in ("pe", "pb"):
        implied_equity = float(metric_value * multiple)
        implied_ev = float(implied_equity + net_debt)
    else:
        raise ValueError(f"Unknown multiple_type: {multiple_type}")

    implied_per_share = float(implied_equity / shares_outstanding)

    return {
        "implied_enterprise_value": implied_ev,
        "implied_equity_value": implied_equity,
        "implied_per_share_value": implied_per_share,
    }


def sensitivity_grid_2d(
    fcff_forecast: Sequence[float] | np.ndarray,
    wacc_range: Sequence[float],
    growth_range: Sequence[float],
    total_debt: float = 0.0,
    cash: float = 0.0,
    shares_outstanding: float = 1.0,
) -> dict[str, Any]:
    """Compute 2D grid of per-share equity values across WACC and terminal growth rates."""
    grid: list[list[float]] = []
    for w in wacc_range:
        row: list[float] = []
        for g in growth_range:
            if g >= w:
                row.append(float("nan"))
            else:
                dcf = dcf_enterprise_value(fcff_forecast, wacc=w, terminal_method="gordon", terminal_growth=g)
                bridge = enterprise_to_equity_bridge(
                    dcf["enterprise_value"],
                    total_debt=total_debt,
                    cash=cash,
                    shares_outstanding=shares_outstanding,
                )
                row.append(bridge["per_share_value"])
        grid.append(row)

    return {
        "wacc_values": [float(w) for w in wacc_range],
        "growth_values": [float(g) for g in growth_range],
        "grid": grid,
    }


def scenario_valuation(
    scenarios: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Compute probability-weighted expected enterprise and equity values across scenarios."""
    total_weight = sum(sc["weight"] for sc in scenarios.values())
    if abs(total_weight - 1.0) > 1e-4:
        raise ValueError(f"Scenario weights must sum to 1.0, got {total_weight}")

    results: dict[str, dict[str, float]] = {}
    exp_ev = 0.0
    exp_eq = 0.0
    exp_ps = 0.0

    for name, sc in scenarios.items():
        weight = float(sc["weight"])
        dcf = dcf_enterprise_value(
            sc["fcff_forecast"],
            wacc=float(sc["wacc"]),
            terminal_method="gordon",
            terminal_growth=float(sc["terminal_growth"]),
        )
        ev = float(dcf["enterprise_value"])
        net_d = float(sc.get("net_debt", 0.0))
        shares = float(sc.get("shares_outstanding", 1.0))
        eq = ev - net_d
        ps = eq / shares

        results[name] = {
            "enterprise_value": ev,
            "equity_value": eq,
            "per_share_value": ps,
        }
        exp_ev += weight * ev
        exp_eq += weight * eq
        exp_ps += weight * ps

    return {
        "scenario_results": results,
        "expected_enterprise_value": exp_ev,
        "expected_equity_value": exp_eq,
        "expected_per_share_value": exp_ps,
    }
