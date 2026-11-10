"""Lab CR3-L01-1: Financial Accelerator Simulation and Balance-Sheet Amplification.

SIMULATED: compares macroeconomic shock propagation in a frictionless economy
against a financial accelerator economy where borrower net worth constrains borrowing
and determines the external finance premium (Bernanke, Gertler & Gilchrist 1999).
"""

from __future__ import annotations


def simulate_financial_accelerator(
    shock_size: float = -0.05,
    persistence: float = 0.70,
    amplification_factor: float = 1.80,
    n_periods: int = 8,
) -> dict[str, list[float]]:
    """Simulate dynamic path of output, capital prices, net worth, and external finance premium."""
    frictionless_output: list[float] = []
    accelerator_output: list[float] = []
    net_worth: list[float] = []
    credit_spread_bps: list[float] = []

    # Initial steady-state baseline normalized to 100
    base_y = 100.0
    base_nw = 100.0
    base_spread = 150.0  # bp

    current_shock = shock_size
    nw = base_nw

    for _t in range(n_periods):
        # Frictionless economy: output responds only to exogenous productivity shock
        y_fric = base_y * (1.0 + current_shock)
        frictionless_output.append(round(y_fric, 2))

        # Financial accelerator: balance-sheet feedback amplifies downturn
        # Net worth drop is magnified by capital price decline (asset fire-sale effect)
        nw = base_nw * (1.0 + current_shock * 2.5)
        net_worth.append(round(nw, 2))

        # External finance premium rises as borrower leverage (Asset / Net Worth) increases
        nw_gap = max(-0.8, (nw - base_nw) / base_nw)
        spread = base_spread - nw_gap * 300.0
        credit_spread_bps.append(round(spread, 1))

        # Accelerator output suffers secondary contraction from elevated cost of credit
        spread_drag = (spread - base_spread) / 10000.0 * 20.0
        y_acc = base_y * (1.0 + current_shock * amplification_factor) - spread_drag
        accelerator_output.append(round(y_acc, 2))

        current_shock *= persistence

    return {
        "frictionless_output": frictionless_output,
        "accelerator_output": accelerator_output,
        "net_worth": net_worth,
        "credit_spread_bps": credit_spread_bps,
    }


def main() -> None:
    res = simulate_financial_accelerator(shock_size=-0.04, persistence=0.65, n_periods=6)

    print("Financial Accelerator vs Frictionless Macro Dynamics:")
    print("  Period | Frictionless Y | Accelerator Y | Net Worth | Credit Spread (bp)")
    print("---------+----------------+---------------+-----------+-------------------")
    for t in range(len(res["frictionless_output"])):
        y_f = res["frictionless_output"][t]
        y_a = res["accelerator_output"][t]
        nw = res["net_worth"][t]
        spr = res["credit_spread_bps"][t]
        print(f"    {t:2d}   |     {y_f:6.2f}     |    {y_a:6.2f}     |   {nw:6.2f}  |       {spr:5.1f}")

    # Output contraction is strictly deeper under the financial accelerator
    max_fric_drop = 100.0 - min(res["frictionless_output"])
    max_acc_drop = 100.0 - min(res["accelerator_output"])
    print(f"\nTrough output drop (frictionless): {max_fric_drop:4.2f} percent")
    print(f"Trough output drop (accelerator):  {max_acc_drop:4.2f} percent")
    peak_spread = max(res["credit_spread_bps"])
    print(f"Peak external finance premium:     {peak_spread:5.1f} bp")

    assert max_acc_drop > max_fric_drop
    assert peak_spread > 150.0


main()
