"""Lab FI5-L04-1: The TIPS-Treasury puzzle: synthetic replication, basis, and arbitrage limits.

Standard library only. Constructs synthetic nominal Treasury bonds from TIPS and inflation swaps,
computes the Fleckenstein, Longstaff, and Lustig (2014) mispricing puzzle basis,
and evaluates financing and balance-sheet limits to arbitrage.
"""

from __future__ import annotations

from typing import Any


def price_synthetic_treasury(
    real_cash_flows: list[dict[str, float]],
    inflation_swap_rates: list[float],
    nominal_discount_factors: list[float],
) -> dict[str, float]:
    """Price a synthetic nominal Treasury created by bundling TIPS with inflation swaps.

    For each payment period t:
    TIPS cash flow = CF_real * (CPI_t / CPI_0)
    Inflation swap exchanges (CPI_t / CPI_0) for (1 + S_t)^t
    Synthesized nominal cash flow = CF_real * (1 + S_t)^t
    Present value = sum synthesized nominal cash flow * DF_nominal_t
    """
    if len(real_cash_flows) != len(inflation_swap_rates) or len(real_cash_flows) != len(nominal_discount_factors):
        raise ValueError("Cash flows, swap rates, and discount factors must have identical length")

    pv_synthetic = 0.0
    total_nominal_cf = 0.0

    for cf_item, s_t, df_t in zip(real_cash_flows, inflation_swap_rates, nominal_discount_factors, strict=True):
        t = cf_item["time_years"]
        cf_real = cf_item["cf_real"]
        synth_cf_nominal = cf_real * ((1.0 + s_t) ** t)
        pv_synthetic += synth_cf_nominal * df_t
        total_nominal_cf += synth_cf_nominal

    return {
        "pv_synthetic": pv_synthetic,
        "total_nominal_cf": total_nominal_cf,
    }


def compute_puzzle_basis(
    cash_treasury_price: float,
    synthetic_treasury_price: float,
    modified_duration: float,
) -> dict[str, float]:
    """Compute the Fleckenstein-Longstaff-Lustig TIPS-Treasury puzzle basis.

    Price basis (cents per $100 par): P_Treasury - P_Synthetic
    Yield basis approximation (basis points): [P_Treasury - P_Synthetic] / [P * ModDur] * 10,000
    """
    price_basis = cash_treasury_price - synthetic_treasury_price
    yield_basis_bps = (price_basis / (cash_treasury_price * modified_duration)) * 10_000.0

    return {
        "cash_treasury_price": cash_treasury_price,
        "synthetic_treasury_price": synthetic_treasury_price,
        "price_basis": price_basis,
        "yield_basis_bps": yield_basis_bps,
    }


def evaluate_arbitrage_viability(
    price_basis: float,
    cash_treasury_price: float,
    holding_period_years: float,
    repo_haircut: float,
    repo_financing_spread_bps: float,
    dealer_capital_hurdle_bps: float,
) -> dict[str, Any]:
    """Evaluate whether the TIPS-Treasury mispricing basis can be profitably exploited.

    Net arbitrage return = Yield Basis - Repo Financing Spread - Dealer Capital Hurdle
    """
    gross_annual_carry_bps = (price_basis / cash_treasury_price) / holding_period_years * 10_000.0
    net_annual_carry_bps = gross_annual_carry_bps - repo_financing_spread_bps - dealer_capital_hurdle_bps

    is_profitable = net_annual_carry_bps > 0.0

    return {
        "gross_annual_carry_bps": gross_annual_carry_bps,
        "repo_financing_spread_bps": repo_financing_spread_bps,
        "dealer_capital_hurdle_bps": dealer_capital_hurdle_bps,
        "net_annual_carry_bps": net_annual_carry_bps,
        "is_profitable": is_profitable,
    }


def main() -> None:
    # 1. Synthetic 5-Year Nominal Treasury Bond Construction (SIMULATED)
    # Real coupon = 2.0% ($1.00 semiannual), par = $100
    times = [0.5 * k for k in range(1, 11)]
    real_cfs = []
    for t in times:
        cf = 1.0 if t < 5.0 else 101.0
        real_cfs.append({"time_years": t, "cf_real": cf})

    # Flat inflation swap rate = 2.40% across tenors
    swap_rates = [0.0240 for _ in times]

    # Nominal discount factors at 4.20% flat yield
    discount_factors = [(1.0 + 0.0420 / 2.0) ** (-2.0 * t) for t in times]

    synth_res = price_synthetic_treasury(real_cfs, swap_rates, discount_factors)
    synth_price = synth_res["pv_synthetic"]

    # 2. Compare against Cash Nominal Treasury
    # Stylized market price reflecting Fleckenstein et al. (2014) overpricing of nominals
    cash_price = 102.50  # Cash Treasury trades at a premium over synthetic package ($1.51 per $100 par)
    mod_duration = 4.45

    basis_res = compute_puzzle_basis(cash_price, synth_price, mod_duration)

    print("TIPS-Treasury Puzzle Replication (SIMULATED):")
    print(f"  Cash Nominal Treasury Price:       ${basis_res['cash_treasury_price']:.3f}")
    print(f"  Synthetic Treasury Package Price:  ${basis_res['synthetic_treasury_price']:.3f}")
    print(f"  Mispricing Price Basis:            ${basis_res['price_basis']:.3f} per $100 par")
    print(f"  Implied Yield Mispricing Basis:    {basis_res['yield_basis_bps']:.1f} bps")

    # 3. Arbitrage Limits Evaluation
    # Repo financing cost (special vs GC spread) = 15 bps
    # Dealer SLR capital hurdle rate = 25 bps
    arb_res = evaluate_arbitrage_viability(
        price_basis=basis_res["price_basis"],
        cash_treasury_price=cash_price,
        holding_period_years=5.0,
        repo_haircut=0.03,
        repo_financing_spread_bps=15.0,
        dealer_capital_hurdle_bps=25.0,
    )

    print("\nLimits to Arbitrage Friction Analysis:")
    print(f"  Gross Annualized Basis Spread:     {arb_res['gross_annual_carry_bps']:.1f} bps")
    print(f"  Repo Financing Drag (Special/GC):  {arb_res['repo_financing_spread_bps']:.1f} bps")
    print(f"  Dealer Capital Charge Hurdle (SLR):{arb_res['dealer_capital_hurdle_bps']:.1f} bps")
    print(f"  Net Annualized Arbitrage Return:   {arb_res['net_annual_carry_bps']:+.1f} bps")
    print(f"  Arbitrage Viable After Frictions:  {arb_res['is_profitable']}")


main()
