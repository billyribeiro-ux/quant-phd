"""Lab L02-1: Tax-advantaged accounts and asset location tax-drag analysis.

Compares terminal wealth across Taxable, Traditional TDA, and Roth accounts under flat,
rising, and falling tax rates, and quantifies the asset location premium over 30 years.
Standard library only. All inputs are SIMULATED.
"""


def terminal_wealth_single_deposit(
    pre_tax_deposit: float,
    gross_annual_return: float,
    years: int,
    tax_rate_initial: float,
    tax_rate_terminal: float,
    account_type: str,
    annual_tax_drag: float = 0.0,
) -> float:
    """Compute terminal after-tax wealth for a single lump-sum pre-tax contribution."""
    if account_type == "roth":
        # Post-tax contribution, tax-free growth and withdrawal
        after_tax_initial = pre_tax_deposit * (1.0 - tax_rate_initial)
        return after_tax_initial * ((1.0 + gross_annual_return) ** years)
    elif account_type == "tda":
        # Pre-tax contribution, tax-deferred growth, ordinary income tax on full withdrawal
        pre_tax_growth = pre_tax_deposit * ((1.0 + gross_annual_return) ** years)
        return pre_tax_growth * (1.0 - tax_rate_terminal)
    elif account_type == "taxable":
        # Post-tax contribution, annual tax drag on returns
        after_tax_initial = pre_tax_deposit * (1.0 - tax_rate_initial)
        net_return = gross_annual_return - annual_tax_drag
        return after_tax_initial * ((1.0 + net_return) ** years)
    else:
        raise ValueError(f"Unknown account_type: {account_type}")


def main() -> None:
    deposit = 10_000.0  # pre-tax dollars
    horizon = 30  # years
    equity_gross_return = 0.08  # 8.0% annual return
    bond_gross_return = 0.045  # 4.5% annual return

    # Part A: Flat tax rate (24% working, 24% retirement)
    tw_roth_flat = terminal_wealth_single_deposit(deposit, equity_gross_return, horizon, 0.24, 0.24, "roth")
    tw_tda_flat = terminal_wealth_single_deposit(deposit, equity_gross_return, horizon, 0.24, 0.24, "tda")
    print(
        f"Flat tax (24% -> 24%): Roth {round(tw_roth_flat):6d} | "
        f"TDA {round(tw_tda_flat):6d} | diff {tw_tda_flat - tw_roth_flat:6.2f}"
    )

    # Part B: Falling tax rate (32% working -> 22% retirement)
    tw_roth_fall = terminal_wealth_single_deposit(deposit, equity_gross_return, horizon, 0.32, 0.22, "roth")
    tw_tda_fall = terminal_wealth_single_deposit(deposit, equity_gross_return, horizon, 0.32, 0.22, "tda")
    print(
        f"Falling tax (32% -> 22%): Roth {round(tw_roth_fall):6d} | "
        f"TDA {round(tw_tda_fall):6d} | TDA advantage {tw_tda_fall - tw_roth_fall:6.2f}"
    )

    # Part C: Rising tax rate (22% working -> 32% retirement)
    tw_roth_rise = terminal_wealth_single_deposit(deposit, equity_gross_return, horizon, 0.22, 0.22, "roth")
    tw_tda_rise = terminal_wealth_single_deposit(deposit, equity_gross_return, horizon, 0.22, 0.32, "tda")
    print(
        f"Rising tax (22% -> 32%): Roth {round(tw_roth_rise):6d} | "
        f"TDA {round(tw_tda_rise):6d} | Roth advantage {tw_roth_rise - tw_tda_rise:6.2f}"
    )

    # Part D: Asset location evaluation on a $500,000 portfolio (50% Equities, 50% Bonds)
    # Account capacities: $250,000 Taxable (after-tax money), $250,000 TDA (pre-tax money)
    # Tax rates: Ordinary income 25%, Qualified dividend / Long-term cap gain 15%
    # Bonds: 4.5% interest -> taxed at 25% ordinary income in Taxable (tax drag = 4.5% * 0.25 = 1.125%)
    # Equities: 8.0% return (2% dividend taxed at 15% = 0.30% drag, 6% capital gain deferred with 15% final tax)
    # Optimal location: Bonds in TDA ($250k), Equities in Taxable ($250k)
    # Suboptimal location: Equities in TDA ($250k), Bonds in Taxable ($250k)
    portfolio_size = 250_000.0  # per account
    tau_ord = 0.25
    tau_cg = 0.15

    # Optimal:
    # 1. TDA holds Bonds: grows at gross 4.5%, taxed at 25% upon withdrawal after 30 years
    tda_bonds_growth = portfolio_size * ((1.0 + bond_gross_return) ** horizon) * (1.0 - tau_ord)
    # 2. Taxable holds Equities: 2% div taxed at 15% annual drag = 0.30%. Net growth = 8.0% - 0.30% = 7.70%
    # At end, capital gains tax paid on unrealized appreciation:
    equity_taxable_terminal_pre_cg = portfolio_size * ((1.0 + 0.077) ** horizon)
    gain = equity_taxable_terminal_pre_cg - portfolio_size
    taxable_equities_net = equity_taxable_terminal_pre_cg - (gain * tau_cg * 0.6)  # effective deferred cg rate
    optimal_total = tda_bonds_growth + taxable_equities_net

    # Suboptimal:
    # 1. TDA holds Equities: grows at 8.0%, taxed at 25% ordinary income upon withdrawal
    tda_equities_growth = portfolio_size * ((1.0 + equity_gross_return) ** horizon) * (1.0 - tau_ord)
    # 2. Taxable holds Bonds: 4.5% interest taxed annually at 25% ordinary income: net return = 4.5% * 0.75 = 3.375%
    taxable_bonds_net = portfolio_size * ((1.0 + (bond_gross_return * (1.0 - tau_ord))) ** horizon)
    suboptimal_total = tda_equities_growth + taxable_bonds_net

    location_alpha = optimal_total - suboptimal_total
    print(
        f"Asset location over 30y: Optimal {round(optimal_total):8d} | "
        f"Suboptimal {round(suboptimal_total):8d} | Location Alpha {round(location_alpha):7d}"
    )


main()
