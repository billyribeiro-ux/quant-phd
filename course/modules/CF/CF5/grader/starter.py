"""Starter template for CF5 LBO Model project.

Students implement the required LBO modeling functions according to specifications.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def build_sources_and_uses(
    ebitda_0: float,
    entry_multiple: float,
    existing_debt: float,
    min_cash: float,
    target_cash: float,
    txn_fee_rate: float,
    financing_fee_rate: float,
    tla_leverage: float,
    tlb_leverage: float,
    rollover_equity: float = 0.0,
) -> dict[str, Any]:
    """Construct Sources and Uses of funds for the buyout transaction."""
    raise NotImplementedError("Implement build_sources_and_uses")


def forecast_operations(
    revenue_0: float,
    growth_rates: Sequence[float],
    ebitda_margins: Sequence[float],
    capex_pcts: Sequence[float],
    da_pcts: Sequence[float],
    nwc_pcts: Sequence[float],
    tax_rate: float,
) -> dict[str, list[float]]:
    """Generate multi-year operating forecast for revenues, EBITDA, EBIT, and unlevered cash flows."""
    raise NotImplementedError("Implement forecast_operations")


def run_debt_schedule(
    ebitda_forecast: Sequence[float],
    capex_forecast: Sequence[float],
    da_forecast: Sequence[float],
    delta_nwc_forecast: Sequence[float],
    tax_rate: float,
    tla_initial: float,
    tla_rate: float,
    tla_amort_rate: float,
    tlb_initial: float,
    tlb_rate: float,
    tlb_amort_rate: float,
    min_cash: float,
    initial_cash: float,
    sweep_pct: float = 1.0,
    interest_method: str = "beginning",
) -> dict[str, Any]:
    """Execute multi-tranche debt schedule with mandatory amortization and priority cash sweeps."""
    raise NotImplementedError("Implement run_debt_schedule")


def evaluate_covenants(
    total_debt: Sequence[float],
    cash: Sequence[float],
    interest: Sequence[float],
    ebitda: Sequence[float],
    max_leverage_schedule: Sequence[float],
    min_coverage: float,
) -> dict[str, Any]:
    """Evaluate financial covenants across forecast periods."""
    raise NotImplementedError("Implement evaluate_covenants")


def calculate_returns_and_attribution(
    entry_ebitda: float,
    exit_ebitda: float,
    entry_multiple: float,
    exit_multiple: float,
    sponsor_equity_0: float,
    exit_net_debt: float,
    holding_period_years: float,
    rollover_equity_0: float = 0.0,
) -> dict[str, Any]:
    """Compute exit equity value, MOIC, IRR, and Kaplan-Strömberg value creation attribution."""
    raise NotImplementedError("Implement calculate_returns_and_attribution")


def run_lbo_model(params: dict[str, Any]) -> dict[str, Any]:
    """Execute the complete end-to-end LBO model pipeline."""
    raise NotImplementedError("Implement run_lbo_model")
