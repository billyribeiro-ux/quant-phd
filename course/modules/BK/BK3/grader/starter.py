"""Starter for the BK3 project: LDI collateral-spiral model (ldi_model.py).

Implement each class and function to the specification on the project page (section "Rung 3"),
then run the autograder locally with:

    QF_SEED=<your seed> pytest -q -p no:cacheprovider --assert=plain -W error test_project.py

Conventions:
- All monetary amounts are integer cents (int).
- Durations are in hundredths of a year (int, e.g. 1500 = 15.00y).
- Shocks and impacts are in basis points (int).
- Use standard library only (dataclasses, fractions, math).
- Validate arguments and raise ValueError for invalid inputs as specified.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fund:
    """An LDI pension fund with assets and an interest-rate swap overlay."""

    assets_cents: int
    asset_duration_cy: int
    overlay_notional_cents: int
    overlay_duration_cy: int
    buffer_cents: int
    impact_bps_per_gcent: int
    backstop_trigger_bps: int
    backstop_capacity_cents: int


@dataclass(frozen=True)
class Step:
    """One iteration of the LDI collateral spiral."""

    step: int
    cumulative_bps: int
    margin_call_cents: int
    buffer_paid_cents: int
    forced_sale_cents: int
    backstop_absorbed_cents: int
    price_impact_bps: int


def margin_call_cents(fund: Fund, cumulative_bps: int) -> int:
    """Cumulative variation margin due for cumulative_bps increase in yield."""
    raise NotImplementedError("margin_call_cents")


def threshold_bps(fund: Fund) -> int | None:
    """Smallest integer yield shock s >= 0 causing forced selling."""
    raise NotImplementedError("threshold_bps")


def run_steps(fund: Fund, shock_bps: int, backstop: bool) -> list[Step]:
    """Simulate the spiral iteration until termination or 50 steps."""
    raise NotImplementedError("run_steps")
