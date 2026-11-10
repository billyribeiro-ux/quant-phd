"""Lab FI4-L06-1: Treasury cash-futures basis trade P&L with haircut, margin, and unwinding dynamics.

The curriculum lab: Python simulation of Treasury cash-futures basis trade,
repo leverage, margin calls, haircut sensitivity, and unwinding dynamics during
the March 2020 dash-for-cash market dislocation.
"""

from __future__ import annotations


def main() -> None:
    # Portfolio setup: $100,000,000 face value cash-futures basis trade (SIMULATED)
    notional_usd = 100_000_000
    conversion_factor = 0.80
    haircut = 0.02  # 2.0% bilateral repo haircut
    initial_margin_rate = 0.03  # 3.0% CME futures initial margin

    # Capital requirements at trade inception (Day 0)
    p0_cash = 100.00
    f0_fut = 125.00  # Parity: 125.00 * 0.80 = 100.00

    repo_borrowed_usd = notional_usd * (p0_cash / 100.0) * (1.0 - haircut)  # $98,000,000
    repo_equity_usd = notional_usd * (p0_cash / 100.0) * haircut  # $2,000,000
    futures_equity_usd = notional_usd * (f0_fut / 100.0) * conversion_factor * initial_margin_rate  # $3,000,000
    total_equity_usd = repo_equity_usd + futures_equity_usd  # $5,000,000

    leverage = notional_usd / total_equity_usd  # 20.0x leverage

    print("Treasury Basis Trade Structure (SIMULATED, Day 0):")
    print(f"  Trade Notional:            ${notional_usd:,.0f}")
    print(f"  Cash Treasury Price:       {p0_cash:.2f}")
    print(f"  Futures Quoted Price:      {f0_fut:.2f} (CF = {conversion_factor:.2f})")
    print(f"  Repo Borrowing:            ${repo_borrowed_usd:,.0f} (Haircut = {haircut:.1%})")
    print(f"  Repo Haircut Equity:       ${repo_equity_usd:,.0f}")
    print(f"  Futures Margin Equity:     ${futures_equity_usd:,.0f} (Margin = {initial_margin_rate:.1%})")
    print(f"  Total Fund Equity Posted:  ${total_equity_usd:,.0f}")
    print(f"  Effective Balance Leverage:{leverage:.1f}x")

    # Three-day March 2020 stress simulation path
    # Day 0: Normal equilibrium
    # Day 1: Emerging dislocation (foreign central banks sell Treasuries)
    # Day 2: Dash for cash dislocation (severe basis blowout and haircut hike)
    market_path = [
        {"day": 0, "p_cash": 100.00, "f_fut": 125.00, "haircut": 0.02, "fut_margin": 0.03, "note": "Parity"},
        {"day": 1, "p_cash": 99.20, "f_fut": 124.60, "haircut": 0.02, "fut_margin": 0.03, "note": "Selling pressure"},
        {
            "day": 2,
            "p_cash": 97.00,
            "f_fut": 123.50,
            "haircut": 0.04,
            "fut_margin": 0.05,
            "note": "Dash for cash spike",
        },
    ]

    print("\nSimulation Path & Unwinding Dynamics:")
    print(
        f"  {'Day':<4s} {'Cash Px':<8s} {'Fut Px':<8s} {'Basis':<9s} "
        f"{'Cash PnL':<14s} {'Fut PnL':<14s} {'Margin Call':<14s} {'Equity Rem':<12s}"
    )

    for step in market_path:
        day = step["day"]
        p_c = float(str(step["p_cash"]))
        p_f = float(str(step["f_fut"]))
        h = float(str(step["haircut"]))
        m = float(str(step["fut_margin"]))

        # Basis = Implied futures delivery value minus cash price
        basis_points = p_f * conversion_factor - p_c

        # Cumulative P&L relative to Day 0
        cash_pnl = notional_usd * (p_c - p0_cash) / 100.0
        # Short futures position gains when futures price falls
        fut_pnl = -notional_usd * (p_f - f0_fut) * conversion_factor / 100.0
        net_market_pnl = cash_pnl + fut_pnl

        # Margin requirements under new market prices and haircuts
        new_max_repo_loan = notional_usd * (p_c / 100.0) * (1.0 - h)
        repo_margin_call = max(0.0, repo_borrowed_usd - new_max_repo_loan)

        new_futures_req = notional_usd * (p_f / 100.0) * conversion_factor * m
        # Variation margin + initial margin increase
        fut_margin_call = max(0.0, new_futures_req - (futures_equity_usd + fut_pnl))

        total_margin_call = repo_margin_call + fut_margin_call
        rem_equity = total_equity_usd + net_market_pnl

        print(
            f"  {day:<4d} {p_c:<8.2f} {p_f:<8.2f} {basis_points:>+5.2f}    "
            f"${cash_pnl / 1_000:>+9.0f}k    ${fut_pnl / 1_000:>+9.0f}k    "
            f"${total_margin_call / 1_000:>9.0f}k    ${rem_equity / 1_000:>8.0f}k"
        )

    # Deleveraging analysis on Day 2
    d2 = market_path[2]
    p_c2 = float(str(d2["p_cash"]))
    p_f2 = float(str(d2["f_fut"]))
    h2 = float(str(d2["haircut"]))
    m2 = float(str(d2["fut_margin"]))

    loan_d2 = notional_usd * (p_c2 / 100.0) * (1.0 - h2)
    repo_call_d2 = max(0.0, repo_borrowed_usd - loan_d2)
    fut_call_d2 = max(
        0.0,
        notional_usd * (p_f2 / 100.0) * conversion_factor * m2
        - (futures_equity_usd - notional_usd * (p_f2 - f0_fut) * conversion_factor / 100.0),
    )
    total_call_d2 = repo_call_d2 + fut_call_d2

    print("\nMechanism Explanation (March 2020 Dash-for-Cash Unwind):")
    print(f"  Day 2 Cash Treasury Price Collapse: -3.00 points (${notional_usd * 0.03:,.0f} loss)")
    print(f"  Futures Hedge Gain:                 +1.20 points (${notional_usd * 0.012:,.0f} gain)")
    print("  Net Market Loss from Basis Blowout: $-1,800,000")
    print(f"  Repo Margin Call (Haircut doubled to 4%): ${repo_call_d2:,.0f}")
    print(f"  Futures Margin Call (CME margin hiked to 5%): ${fut_call_d2:,.0f}")
    print(f"  Total Liquidity Required to Avoid Default:   ${total_call_d2:,.0f}")
    print(f"  Total Liquidity Demand as % of Initial Fund Equity: {total_call_d2 / total_equity_usd:.1%}")
    print("  Outcome: Margin calls exceed equity cushion; hedge funds forced to dump Treasuries,")
    print("           triggering a fire-sale spiral until Federal Reserve intervened with massive QE.")


main()
