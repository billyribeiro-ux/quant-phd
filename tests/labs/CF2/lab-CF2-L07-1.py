"""CF2 lab L07-1: The pecking order and financing waterfall.

Model: Deterministic financing hierarchy model under stated issue cost ordering.
Ranking assumption (A10):
  Cost(internal cash) < Cost(debt) < Cost(external equity).
Given an investment plan and operating cash flows, the firm funds deficits
first from internal cash, second from debt up to debt capacity, and third from
equity as the financing source of last resort.
"""

from __future__ import annotations


def run_financing_waterfall(
    initial_cash: float,
    initial_debt: float,
    debt_capacity: float,
    operating_cash_flows: list[float],
    capex_schedule: list[float],
) -> list[dict[str, float]]:
    """Simulate pecking order waterfall period by period."""
    n_years = len(operating_cash_flows)
    cash = initial_cash
    debt = initial_debt
    equity_issued_total = 0.0

    history: list[dict[str, float]] = []

    for t in range(n_years):
        ocf = operating_cash_flows[t]
        capex = capex_schedule[t]
        deficit = capex - ocf

        cash_used = 0.0
        debt_issued = 0.0
        equity_issued = 0.0

        if deficit <= 0.0:
            # Surplus adds to internal cash
            cash += -deficit
        else:
            # 1. Use internal cash first
            if cash > 0.0:
                cash_used = min(cash, deficit)
                cash -= cash_used
                deficit -= cash_used

            # 2. If deficit remains, issue debt up to debt capacity
            if deficit > 0.0:
                available_debt_capacity = max(0.0, debt_capacity - debt)
                debt_issued = min(available_debt_capacity, deficit)
                debt += debt_issued
                deficit -= debt_issued

            # 3. If deficit still remains, issue equity
            if deficit > 0.0:
                equity_issued = deficit
                equity_issued_total += equity_issued
                deficit = 0.0

        history.append(
            {
                "year": t + 1,
                "ocf": ocf,
                "capex": capex,
                "cash_end": cash,
                "debt_end": debt,
                "equity_issued": equity_issued,
                "cumulative_equity": equity_issued_total,
            }
        )

    return history


def main() -> None:
    print("CF2 Lab L07-1: Pecking-Order Financing Waterfall")
    print("-----------------------------------------------")

    init_cash = 20_000_000.0  # $20M
    init_debt = 30_000_000.0  # $30M
    capacity = 70_000_000.0  # $70M max debt capacity

    ocf = [25_000_000.0, 30_000_000.0, 20_000_000.0, 35_000_000.0, 40_000_000.0]
    capex_high = [40_000_000.0, 50_000_000.0, 60_000_000.0, 20_000_000.0, 25_000_000.0]

    print(f"Initial cash: ${init_cash / 1e6:.1f}M | Initial debt: ${init_debt / 1e6:.1f}M")
    print(f"Debt capacity limit: ${capacity / 1e6:.1f}M")
    print("\nYear-by-Year Financing Decisions (High Capex Expansion):")
    print(
        f"{'Yr':>3} | {'OCF ($M)':>9} | {'Capex ($M)':>11} | {'Cash ($M)':>10} | {'Debt ($M)':>10} | "
        f"{'New Eq ($M)':>12} | {'Funding Priority Applied'}"
    )
    print("-" * 88)

    results = run_financing_waterfall(init_cash, init_debt, capacity, ocf, capex_high)
    for r in results:
        yr = int(r["year"])
        o = r["ocf"] / 1e6
        c = r["capex"] / 1e6
        cash = r["cash_end"] / 1e6
        d = r["debt_end"] / 1e6
        eq = r["equity_issued"] / 1e6

        if eq > 0:
            action = "Debt capacity exhausted -> issued equity"
        elif d > results[yr - 2]["debt_end"] / 1e6 if yr > 1 else d > init_debt / 1e6:
            action = "Internal cash depleted -> issued debt"
        elif c > o:
            action = "Funded entirely by internal cash"
        else:
            action = "Surplus OCF -> cash balance grew"

        print(f"{yr:3d} | ${o:8.1f}M | ${c:10.1f}M | ${cash:9.1f}M | ${d:9.1f}M | ${eq:11.1f}M | {action}")

    print("-" * 88)
    total_eq = results[-1]["cumulative_equity"] / 1e6
    final_debt = results[-1]["debt_end"] / 1e6
    final_cash = results[-1]["cash_end"] / 1e6
    print(
        f"Summary: Final cash = ${final_cash:.1f}M, Final debt = ${final_debt:.1f}M, "
        f"Total equity issued = ${total_eq:.1f}M."
    )
    print("Demonstration: Equity is issued only in Year 3 when both internal cash and debt capacity are exhausted.")


main()
