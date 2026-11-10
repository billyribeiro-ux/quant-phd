"""Test suite for FI4 Plumbing Monitor autograder.

Verifies no-arbitrage basis boundaries, margin solvency equations,
and Supplementary Leverage Ratio (SLR) impacts.
"""

from __future__ import annotations

import os
from typing import Any, cast

import pytest
from instance import make_instance

# The browser autograder loads the solution module as configured in project.html.
try:
    import monitor as sol
except ImportError:
    import reference as sol


@pytest.fixture
def current_instance() -> dict[str, Any]:
    seed = int(os.environ.get("QF_SEED", "42"))
    inst = cast(dict[str, Any], make_instance(seed))
    return inst


def test_net_implied_repo_rate_exact_parity(current_instance: dict[str, Any]) -> None:
    """At theoretical no-arbitrage parity, the net implied repo rate must be exactly zero."""
    cash_price = float(current_instance["cash_price"])
    cf = float(current_instance["conversion_factor"])
    days = int(current_instance["days"])
    repo_rate = float(current_instance["repo_rate"])

    # Forward price under exact cash-and-carry no arbitrage
    forward_cash = cash_price * (1.0 + repo_rate * (float(days) / 360.0))
    parity_futures = forward_cash / cf

    net_rate = sol.net_implied_repo_rate(cash_price, parity_futures, cf, days, repo_rate)
    assert abs(net_rate) < 1e-7, (
        f"Net implied repo rate at parity must be 0.0; got {net_rate} (property: cash-futures parity)"
    )


def test_net_implied_repo_rate_spread_sign(current_instance: dict[str, Any]) -> None:
    """A rich futures contract yields a positive net carry; a cheap futures contract yields negative carry."""
    cash_price = float(current_instance["cash_price"])
    cf = float(current_instance["conversion_factor"])
    days = int(current_instance["days"])
    repo_rate = float(current_instance["repo_rate"])

    forward_cash = cash_price * (1.0 + repo_rate * (float(days) / 360.0))
    parity_futures = forward_cash / cf

    rich_futures = parity_futures * 1.01
    net_rate_rich = sol.net_implied_repo_rate(cash_price, rich_futures, cf, days, repo_rate)
    assert net_rate_rich > 0.0, "Rich futures must produce strictly positive net implied repo rate"

    cheap_futures = parity_futures * 0.99
    net_rate_cheap = sol.net_implied_repo_rate(cash_price, cheap_futures, cf, days, repo_rate)
    assert net_rate_cheap < 0.0, "Cheap futures must produce strictly negative net implied repo rate"


def test_net_implied_repo_rate_monotonicity(current_instance: dict[str, Any]) -> None:
    """Net implied repo rate is strictly increasing in futures price and strictly decreasing in cash price."""
    cash_price = float(current_instance["cash_price"])
    futures_price = float(current_instance["futures_price"])
    cf = float(current_instance["conversion_factor"])
    days = int(current_instance["days"])
    repo_rate = float(current_instance["repo_rate"])

    base_rate = sol.net_implied_repo_rate(cash_price, futures_price, cf, days, repo_rate)
    higher_fut = sol.net_implied_repo_rate(cash_price, futures_price + 0.50, cf, days, repo_rate)
    higher_cash = sol.net_implied_repo_rate(cash_price + 0.50, futures_price, cf, days, repo_rate)

    assert higher_fut > base_rate, "Implied repo rate must increase when futures price increases"
    assert higher_cash < base_rate, "Implied repo rate must decrease when cash price increases"


def test_basis_trade_zero_shock(current_instance: dict[str, Any]) -> None:
    """When prices do not change, market P&L is zero and net return equals negative repo interest cost."""
    cash_price = float(current_instance["cash_price"])
    futures_price = float(current_instance["futures_price"])
    cf = float(current_instance["conversion_factor"])
    days = int(current_instance["days"])
    repo_rate = float(current_instance["repo_rate"])
    haircut = float(current_instance["haircut"])
    initial_margin = float(current_instance["initial_margin"])

    res = sol.basis_trade_return(
        cash_price,
        futures_price,
        cf,
        days,
        repo_rate,
        haircut,
        initial_margin,
        cash_price,
        futures_price,
    )

    assert abs(res["cash_pnl"]) < 1e-9, "Zero shock must give zero cash PnL"
    assert abs(res["futures_pnl"]) < 1e-9, "Zero shock must give zero futures PnL"
    assert res["repo_interest"] > 0.0, "Repo financing interest must be positive"
    assert abs(res["total_pnl"] - (-res["repo_interest"])) < 1e-9, "Total PnL must equal negative repo interest"

    expected_roe = -res["repo_interest"] / res["initial_equity"]
    assert abs(res["return_on_equity"] - expected_roe) < 1e-9, "ROE must equal net PnL / initial equity"


def test_basis_trade_perfect_hedge(current_instance: dict[str, Any]) -> None:
    """A parallel basis-neutral price shock leaves cash and futures P&L perfectly offsetting."""
    cash_price = float(current_instance["cash_price"])
    futures_price = float(current_instance["futures_price"])
    cf = float(current_instance["conversion_factor"])
    days = int(current_instance["days"])
    repo_rate = float(current_instance["repo_rate"])
    haircut = float(current_instance["haircut"])
    initial_margin = float(current_instance["initial_margin"])

    delta_cash = 1.25
    delta_futures = delta_cash / cf  # exact DV01 hedge

    shock_cash = cash_price + delta_cash
    shock_fut = futures_price + delta_futures

    res = sol.basis_trade_return(
        cash_price,
        futures_price,
        cf,
        days,
        repo_rate,
        haircut,
        initial_margin,
        shock_cash,
        shock_fut,
    )

    pnl_spread = res["cash_pnl"] + res["futures_pnl"]
    assert abs(pnl_spread) < 1e-7, (
        f"Perfect hedge must give zero combined market PnL; got {pnl_spread} (property: basis hedging)"
    )


def test_margin_coverage_zero_shock(current_instance: dict[str, Any]) -> None:
    """Under no market shock, zero margin calls are issued and coverage ratio is exactly 1.0."""
    cash_price = float(current_instance["cash_price"])
    futures_price = float(current_instance["futures_price"])
    cf = float(current_instance["conversion_factor"])
    haircut = float(current_instance["haircut"])
    initial_margin = float(current_instance["initial_margin"])
    maintenance_margin = float(current_instance["maintenance_margin"])

    cov = sol.margin_coverage(
        cash_price,
        futures_price,
        cf,
        haircut,
        initial_margin,
        maintenance_margin,
        cash_price,
        futures_price,
    )

    assert cov["repo_margin_call"] == 0.0, "Zero shock must have zero repo margin call"
    assert cov["futures_margin_call"] == 0.0, "Zero shock must have zero futures margin call"
    assert cov["total_margin_call"] == 0.0, "Zero shock must have zero total margin call"
    assert cov["is_margin_called"] is False, "is_margin_called must be False under zero shock"
    assert abs(cov["margin_coverage_ratio"] - 1.0) < 1e-9, "Coverage ratio must be 1.0"


def test_margin_coverage_adverse_shock(current_instance: dict[str, Any]) -> None:
    """An adverse dislocation (cash bond falls and futures rises) generates repo and futures margin calls."""
    cash_price = float(current_instance["cash_price"])
    futures_price = float(current_instance["futures_price"])
    cf = float(current_instance["conversion_factor"])
    haircut = float(current_instance["haircut"])
    initial_margin = float(current_instance["initial_margin"])
    maintenance_margin = float(current_instance["maintenance_margin"])

    # Cash price plunges 2 points; futures price spikes 5%
    shock_cash = cash_price - 2.0
    shock_fut = futures_price * 1.05

    cov = sol.margin_coverage(
        cash_price,
        futures_price,
        cf,
        haircut,
        initial_margin,
        maintenance_margin,
        shock_cash,
        shock_fut,
    )

    expected_repo_call = 2.0 * (1.0 - haircut)
    assert abs(cov["repo_margin_call"] - expected_repo_call) < 1e-7, (
        f"Repo margin call mismatch: expected {expected_repo_call}, got {cov['repo_margin_call']}"
    )
    assert cov["futures_margin_call"] > 0.0, "Rising futures must trigger variation margin call on short position"
    assert cov["total_margin_call"] > 0.0, "Total margin call must be positive"
    assert cov["is_margin_called"] is True, "is_margin_called must be True"
    assert 0.0 <= cov["margin_coverage_ratio"] < 1.0, "Coverage ratio must degrade below 1.0"


def test_leverage_ratio_properties(current_instance: dict[str, Any]) -> None:
    """SLR is inversely proportional to exposure and strictly increases when Treasuries are exempt."""
    equity = float(current_instance["dealer_equity"])
    treasuries = float(current_instance["cash_treasuries"])
    repo_book = float(current_instance["repo_matched_book"])
    derivs = float(current_instance["derivatives_exposure"])

    standard = sol.leverage_ratio(equity, treasuries, repo_book, derivs, exempt_reserves_and_treasuries=False)
    exempt = sol.leverage_ratio(equity, treasuries, repo_book, derivs, exempt_reserves_and_treasuries=True)

    assert standard["total_leverage_exposure"] > exempt["total_leverage_exposure"], (
        "Exempting Treasuries must strictly reduce total leverage exposure"
    )
    assert exempt["slr"] > standard["slr"], "Exempting Treasuries must strictly increase SLR"
    assert exempt["capital_surplus"] > standard["capital_surplus"], "Exempting Treasuries must increase capital surplus"

    # Invariance and bounds
    assert standard["is_compliant"] == (standard["slr"] >= 0.05), "Compliance flag must match 5% threshold"
    assert exempt["is_compliant"] == (exempt["slr"] >= 0.05), "Exempt compliance flag must match 5% threshold"


def test_invalid_input_boundaries() -> None:
    """Functions must enforce strict parameter domains with ValueError."""
    with pytest.raises(ValueError):
        sol.net_implied_repo_rate(0.0, 100.0, 0.8, 30, 0.03)

    with pytest.raises(ValueError):
        sol.net_implied_repo_rate(100.0, 100.0, 0.8, 0, 0.03)

    with pytest.raises(ValueError):
        sol.basis_trade_return(0.0, 100.0, 0.8, 30, 0.03, 0.02, 0.03, 100.0, 100.0)

    with pytest.raises(ValueError):
        sol.basis_trade_return(100.0, 100.0, 0.8, 30, 0.03, -0.01, 0.03, 100.0, 100.0)
