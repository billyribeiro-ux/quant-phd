"""Reference solution for FI4 Plumbing Monitor autograder.

Computes net implied repo rates, basis trade returns, margin coverage,
and dealer Supplementary Leverage Ratio (SLR) impacts.
"""

from __future__ import annotations

from typing import Any


def net_implied_repo_rate(
    cash_price: float,
    futures_price: float,
    conversion_factor: float,
    days: int,
    repo_rate: float,
) -> float:
    """Compute the net implied repo rate (basis carry spread) for a cash-futures basis trade.

    Parameters
    ----------
    cash_price : float
        Dirty/clean cash price of the Treasury bond per 100 face value.
    futures_price : float
        Quoted price of the Treasury futures contract per 100 face value.
    conversion_factor : float
        Conversion factor of the cash bond for the futures contract.
    days : int
        Actual days to futures delivery date (ACT/360 convention).
    repo_rate : float
        Secured financing rate (decimal, e.g. 0.035 for 3.50%).

    Returns
    -------
    float
        Net implied repo rate = gross implied repo rate minus repo financing rate.
    """
    if cash_price <= 0.0:
        raise ValueError("Cash price must be strictly positive.")
    if days <= 0:
        raise ValueError("Days to delivery must be strictly positive.")

    gross_implied = ((futures_price * conversion_factor) / cash_price - 1.0) * (360.0 / float(days))
    return float(gross_implied - repo_rate)


def basis_trade_return(
    cash_price: float,
    futures_price: float,
    conversion_factor: float,
    days: int,
    repo_rate: float,
    haircut: float,
    initial_margin: float,
    shock_cash_price: float,
    shock_futures_price: float,
) -> dict[str, float]:
    """Compute P&L, financing costs, and return on equity for a leveraged basis trade.

    Parameters
    ----------
    cash_price : float
        Initial purchase price of cash Treasury bond per 100 face value.
    futures_price : float
        Initial futures contract price per 100 face value.
    conversion_factor : float
        Conversion factor for the cash bond.
    days : int
        Holding period in days (ACT/360 day-count basis).
    repo_rate : float
        Annual repo borrowing rate (decimal).
    haircut : float
        Bilateral repo haircut fraction (e.g. 0.02 for 2%).
    initial_margin : float
        Futures initial margin fraction (e.g. 0.03 for 3%).
    shock_cash_price : float
        Post-shock cash Treasury price.
    shock_futures_price : float
        Post-shock futures price.

    Returns
    -------
    dict[str, float]
        Dictionary with cash_pnl, futures_pnl, repo_interest, total_pnl,
        initial_equity, and return_on_equity.
    """
    if cash_price <= 0.0 or initial_margin < 0.0 or haircut < 0.0:
        raise ValueError("Invalid trade pricing or margin parameters.")

    repo_borrowed = cash_price * (1.0 - haircut)
    cash_equity = cash_price * haircut
    futures_equity = (futures_price * conversion_factor) * initial_margin
    initial_equity = cash_equity + futures_equity

    if initial_equity <= 0.0:
        raise ValueError("Initial equity requirement must be strictly positive.")

    repo_interest = repo_borrowed * repo_rate * (float(days) / 360.0)

    cash_pnl = shock_cash_price - cash_price
    futures_pnl = -(shock_futures_price - futures_price) * conversion_factor
    total_pnl = cash_pnl + futures_pnl - repo_interest
    return_on_equity = total_pnl / initial_equity

    return {
        "cash_pnl": cash_pnl,
        "futures_pnl": futures_pnl,
        "repo_interest": repo_interest,
        "total_pnl": total_pnl,
        "initial_equity": initial_equity,
        "return_on_equity": return_on_equity,
    }


def margin_coverage(
    cash_price: float,
    futures_price: float,
    conversion_factor: float,
    haircut: float,
    initial_margin: float,
    maintenance_margin: float,
    shock_cash_price: float,
    shock_futures_price: float,
) -> dict[str, Any]:
    """Evaluate margin calls and solvency under adverse market price shocks.

    Parameters
    ----------
    cash_price : float
        Initial cash Treasury price.
    futures_price : float
        Initial futures price.
    conversion_factor : float
        Conversion factor for the cash bond.
    haircut : float
        Repo haircut fraction.
    initial_margin : float
        Futures initial margin fraction.
    maintenance_margin : float
        Futures maintenance margin fraction threshold.
    shock_cash_price : float
        Post-shock cash Treasury price.
    shock_futures_price : float
        Post-shock futures price.

    Returns
    -------
    dict[str, Any]
        Dictionary with repo_margin_call, futures_margin_call, total_margin_call,
        is_margin_called, and margin_coverage_ratio.
    """
    # Repo margin call: lender marks collateral to market
    initial_loan = cash_price * (1.0 - haircut)
    max_loan_post_shock = shock_cash_price * (1.0 - haircut)
    repo_margin_call = max(0.0, initial_loan - max_loan_post_shock)

    # Futures margin call: loss on short position triggers call if equity < maintenance
    futures_initial_equity = (futures_price * conversion_factor) * initial_margin
    futures_maint_threshold = (futures_price * conversion_factor) * maintenance_margin
    futures_loss = (shock_futures_price - futures_price) * conversion_factor
    futures_rem_equity = futures_initial_equity - futures_loss

    if futures_rem_equity < futures_maint_threshold:
        futures_margin_call = max(0.0, futures_initial_equity - futures_rem_equity)
    else:
        futures_margin_call = 0.0

    total_margin_call = repo_margin_call + futures_margin_call
    is_margin_called = total_margin_call > 0.0

    total_initial_equity = cash_price * haircut + futures_initial_equity
    remaining_equity = max(
        0.0,
        total_initial_equity + (shock_cash_price - cash_price) - futures_loss,
    )
    margin_coverage_ratio = remaining_equity / total_initial_equity

    return {
        "repo_margin_call": repo_margin_call,
        "futures_margin_call": futures_margin_call,
        "total_margin_call": total_margin_call,
        "is_margin_called": is_margin_called,
        "margin_coverage_ratio": margin_coverage_ratio,
    }


def leverage_ratio(
    dealer_equity: float,
    cash_treasuries: float,
    repo_matched_book: float,
    derivatives_exposure: float,
    exempt_reserves_and_treasuries: bool = False,
) -> dict[str, Any]:
    """Compute primary dealer Supplementary Leverage Ratio (SLR) and regulatory capital surplus.

    Parameters
    ----------
    dealer_equity : float
        Tier 1 capital of the dealer bank.
    cash_treasuries : float
        On-balance-sheet Treasury bond holdings.
    repo_matched_book : float
        Gross repo financing assets.
    derivatives_exposure : float
        Potential future exposure and mark-to-market derivatives exposure.
    exempt_reserves_and_treasuries : bool
        Whether Treasuries and central bank deposits are excluded from Total
        Leverage Exposure (e.g. temporary Federal Reserve COVID rule).

    Returns
    -------
    dict[str, Any]
        Dictionary with total_leverage_exposure, slr, is_compliant, and capital_surplus.
    """
    treasuries_in_exposure = 0.0 if exempt_reserves_and_treasuries else cash_treasuries
    total_leverage_exposure = treasuries_in_exposure + repo_matched_book + derivatives_exposure

    slr = float("inf") if total_leverage_exposure <= 0.0 else dealer_equity / total_leverage_exposure

    # US G-SIB minimum SLR requirement is 5.0% (3% minimum + 2% enhanced buffer)
    minimum_ratio = 0.05
    is_compliant = slr >= minimum_ratio
    capital_surplus = dealer_equity - minimum_ratio * total_leverage_exposure

    return {
        "total_leverage_exposure": total_leverage_exposure,
        "slr": slr,
        "is_compliant": is_compliant,
        "capital_surplus": capital_surplus,
    }
