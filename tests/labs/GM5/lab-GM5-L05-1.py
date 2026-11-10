"""Lab GM5-L05-1: Bank Runs, Dash for Cash & Policy Backstop Interventions.

Simulates depositor runs on duration-mismatched banks (Diamond & Dybvig 1983 / FRB 2023 SVB Review),
comparing fire-sale insolvency against a central bank emergency liquidity facility (BTFP / Discount Window).
"""

from __future__ import annotations

from typing import Any


def simulate_bank_run_with_backstop(
    total_deposits: float,
    uninsured_deposit_share: float,
    cash_reserves: float,
    securities_par_value: float,
    securities_market_value: float,
    daily_run_withdrawal_rate: float,
    fire_sale_haircut_slope: float,
    central_bank_facility_active: bool = False,
    n_days: int = 5,
) -> dict[str, Any]:
    """Simulate depositor withdrawals, asset liquidations, and lender-of-last-resort support.

    Parameters
    ----------
    total_deposits : float
        Initial bank deposits in millions USD.
    uninsured_deposit_share : float
        Proportion of deposits above deposit insurance limit (e.g. 0.90 for SVB).
    cash_reserves : float
        Liquid cash held at central bank.
    securities_par_value : float
        Face value of held-to-maturity (HTM) / available-for-sale (AFS) bond portfolio.
    securities_market_value : float
        Mark-to-market value of securities portfolio reflecting interest-rate duration losses.
    daily_run_withdrawal_rate : float
        Fraction of uninsured deposits attempting withdrawal per day.
    fire_sale_haircut_slope : float
        Secondary fire-sale discount parameter as liquidation volume increases.
    central_bank_facility_active : bool
        If True, central bank advances cash against collateral valued at par (e.g. Fed BTFP).
    n_days : int
        Days simulated.

    Returns
    -------
    dict[str, float | bool | list[float]]
        Solvency status, cumulative withdrawals, fire-sale losses, and terminal equity.
    """
    cash = cash_reserves
    securities_m2m = securities_market_value
    deposits = total_deposits
    uninsured_deposits = total_deposits * uninsured_deposit_share

    bank_failed = False
    failure_day = -1
    total_fire_sale_loss = 0.0
    cash_history = [cash]
    deposits_history = [deposits]

    for day in range(1, n_days + 1):
        # Withdrawals demanded by panicking uninsured depositors
        withdrawal_demand = uninsured_deposits * daily_run_withdrawal_rate

        if central_bank_facility_active:
            # Policy backstop: bank pledges securities at PAR to receive discount window/BTFP cash
            borrowed_from_cb = min(securities_par_value, withdrawal_demand)
            cash += borrowed_from_cb
            securities_par_value -= borrowed_from_cb

        # Fulfill withdrawals using cash
        if cash >= withdrawal_demand:
            cash -= withdrawal_demand
            deposits -= withdrawal_demand
            uninsured_deposits -= withdrawal_demand
        else:
            # Cash exhausted: must fire-sale securities in open market
            deficit = withdrawal_demand - cash
            deposits -= cash
            uninsured_deposits -= cash
            cash = 0.0

            # Fire sale discount: market value drops as selling pressure mounts
            discount = min(0.35, fire_sale_haircut_slope * (deficit / securities_market_value))
            effective_price_ratio = 1.0 - discount
            securities_needed = deficit / effective_price_ratio

            fire_sale_loss = securities_needed * discount
            total_fire_sale_loss += fire_sale_loss

            if securities_m2m >= securities_needed:
                securities_m2m -= securities_needed
                deposits -= deficit
                uninsured_deposits -= deficit
            else:
                # Bank runs out of liquidatable assets: failure
                bank_failed = True
                failure_day = day
                break

        cash_history.append(cash)
        deposits_history.append(deposits)

    terminal_equity = cash + securities_m2m - deposits if not bank_failed else -total_fire_sale_loss

    return {
        "bank_failed": bank_failed,
        "failure_day": failure_day,
        "terminal_deposits": deposits_history[-1],
        "total_fire_sale_loss": total_fire_sale_loss,
        "terminal_equity": terminal_equity,
    }


def main() -> None:
    # Stylized parameters resembling Silicon Valley Bank (March 2023)
    deposits_0 = 175000.0  # $175B total deposits
    uninsured_share = 0.88  # 88% uninsured deposits
    cash_0 = 15000.0  # $15B cash
    sec_par = 120000.0  # $120B par securities
    sec_m2m = 99000.0  # $99B market value ($21B unrealized duration loss)

    # Without central bank backstop
    run_no_backstop = simulate_bank_run_with_backstop(
        total_deposits=deposits_0,
        uninsured_deposit_share=uninsured_share,
        cash_reserves=cash_0,
        securities_par_value=sec_par,
        securities_market_value=sec_m2m,
        daily_run_withdrawal_rate=0.28,  # 28% run per day ($42B/day)
        fire_sale_haircut_slope=0.25,
        central_bank_facility_active=False,
        n_days=3,
    )

    # With central bank policy backstop (lending at par against eligible securities)
    run_with_backstop = simulate_bank_run_with_backstop(
        total_deposits=deposits_0,
        uninsured_deposit_share=uninsured_share,
        cash_reserves=cash_0,
        securities_par_value=sec_par,
        securities_market_value=sec_m2m,
        daily_run_withdrawal_rate=0.28,
        fire_sale_haircut_slope=0.25,
        central_bank_facility_active=True,
        n_days=3,
    )

    print("Initial Deposits ($M):", round(deposits_0, 1))
    print("Without Backstop - Bank Failed:", run_no_backstop["bank_failed"])
    print("Without Backstop - Failure Day:", run_no_backstop["failure_day"])
    print("Without Backstop - Fire Sale Loss ($M):", round(float(run_no_backstop["total_fire_sale_loss"]), 1))
    print("With Backstop - Bank Failed:", run_with_backstop["bank_failed"])
    print("With Backstop - Fire Sale Loss ($M):", round(float(run_with_backstop["total_fire_sale_loss"]), 1))
    print("With Backstop - Terminal Deposits ($M):", round(float(run_with_backstop["terminal_deposits"]), 1))


main()
