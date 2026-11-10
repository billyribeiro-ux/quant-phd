"""Lab X3-L04-1: Commodity Futures Return Decomposition: Spot, Roll, and Collateral Yield.

Replicates the Erb & Harvey (2006) and Gorton & Rouwenhorst (2006) return decomposition,
demonstrating that roll yield drives the long-term divergence between backwardation and contango.
"""

from __future__ import annotations

import math
import random


def simulate_futures_decomposition(
    n_months: int = 120,
    annual_spot_drift: float = 0.02,
    annual_roll_yield: float = 0.06,
    annual_collateral_rate: float = 0.03,
    volatility: float = 0.18,
    seed: int = 42,
) -> dict[str, float]:
    """Simulate a 10-year monthly fully collateralized commodity futures investment."""
    rng = random.Random(seed)
    dt = 1.0 / 12.0
    monthly_roll = annual_roll_yield * dt
    monthly_collateral = annual_collateral_rate * dt
    monthly_spot_drift = annual_spot_drift * dt
    monthly_vol = volatility * math.sqrt(dt)

    spot_wealth = 100.0
    total_wealth = 100.0

    cumulative_spot_ret = 0.0
    cumulative_roll_ret = 0.0
    cumulative_collateral_ret = 0.0

    for _ in range(n_months):
        r_spot = monthly_spot_drift + monthly_vol * rng.gauss(0.0, 1.0)
        r_roll = monthly_roll
        r_collateral = monthly_collateral

        r_total = r_spot + r_roll + r_collateral

        spot_wealth *= 1.0 + r_spot
        total_wealth *= 1.0 + r_total

        cumulative_spot_ret += r_spot
        cumulative_roll_ret += r_roll
        cumulative_collateral_ret += r_collateral

    annualized_total_return = (total_wealth / 100.0) ** (12.0 / n_months) - 1.0
    annualized_spot_return = (spot_wealth / 100.0) ** (12.0 / n_months) - 1.0

    return {
        "final_wealth": round(total_wealth, 2),
        "spot_wealth": round(spot_wealth, 2),
        "ann_total_return": round(annualized_total_return * 100.0, 2),
        "ann_spot_return": round(annualized_spot_return * 100.0, 2),
        "cum_spot_ret": round(cumulative_spot_ret * 100.0, 2),
        "cum_roll_ret": round(cumulative_roll_ret * 100.0, 2),
        "cum_collateral_ret": round(cumulative_collateral_ret * 100.0, 2),
    }


def main() -> None:
    print("Lab X3-L04-1 | Futures Return Decomposition: Spot Return vs. Roll Yield")
    print("-" * 75)
    print("Decomposing 10-Year (120 Months) Collateralized Commodity Returns (Erb & Harvey 2006)")
    print("-" * 75)

    # Commodity A: Backwardation (positive roll yield +6.0% p.a.)
    res_a = simulate_futures_decomposition(
        n_months=120,
        annual_spot_drift=0.02,
        annual_roll_yield=0.06,
        annual_collateral_rate=0.03,
        seed=101,
    )

    # Commodity B: Contango (negative roll yield -8.0% p.a. - e.g. Natural Gas / USO decay)
    res_b = simulate_futures_decomposition(
        n_months=120,
        annual_spot_drift=0.02,
        annual_roll_yield=-0.08,
        annual_collateral_rate=0.03,
        seed=101,
    )

    w_a = f"${res_a['final_wealth']:.2f}"
    w_b = f"${res_b['final_wealth']:.2f}"
    s_a = f"${res_a['spot_wealth']:.2f}"
    s_b = f"${res_b['spot_wealth']:.2f}"
    tr_a = f"{res_a['ann_total_return']:.2f}%"
    tr_b = f"{res_b['ann_total_return']:.2f}%"
    sr_a = f"{res_a['ann_spot_return']:.2f}%"
    sr_b = f"{res_b['ann_spot_return']:.2f}%"
    cs_a = f"{res_a['cum_spot_ret']:.2f}%"
    cs_b = f"{res_b['cum_spot_ret']:.2f}%"
    cr_a = f"{res_a['cum_roll_ret']:.2f}%"
    cr_b = f"{res_b['cum_roll_ret']:.2f}%"
    cc_a = f"{res_a['cum_collateral_ret']:.2f}%"
    cc_b = f"{res_b['cum_collateral_ret']:.2f}%"

    print(f"{'Component':<28} {'Backwardated (Commodity A)':>22} {'Contango (Commodity B)':>22}")
    print("-" * 75)
    print(f"{'Initial Investment ($)':<28} {'$100.00':>22} {'$100.00':>22}")
    print(f"{'Final Collateralized Wealth':<28} {w_a:>22} {w_b:>22}")
    print(f"{'Spot Wealth (Unhedged Spot)':<28} {s_a:>22} {s_b:>22}")
    print(f"{'Annualized Total Return':<28} {tr_a:>22} {tr_b:>22}")
    print(f"{'Annualized Spot Return':<28} {sr_a:>22} {sr_b:>22}")
    print("-" * 75)
    print(f"{'Cumulative Spot Return Sum':<28} {cs_a:>22} {cs_b:>22}")
    print(f"{'Cumulative Roll Return Sum':<28} {cr_a:>22} {cr_b:>22}")
    print(f"{'Cumulative Collateral Sum':<28} {cc_a:>22} {cc_b:>22}")
    print("-" * 75)

    wealth_diff = res_a["final_wealth"] - res_b["final_wealth"]
    roll_diff = res_a["cum_roll_ret"] - res_b["cum_roll_ret"]
    ratio = res_a["final_wealth"] / res_b["final_wealth"]
    print(f"Total Wealth Spread after 10 Years: ${wealth_diff:.2f} ({ratio:.1f}x wealth multiple)")
    print(f"Cumulative Roll Yield Spread:       {roll_diff:.2f}% (14.0% p.a. spread)")
    print(f"Economic Finding: Spot prices evolved identically, yet Commodity A delivered {ratio:.1f}x wealth")
    print("over Commodity B solely due to positive roll yield from backwardation.")


main()
