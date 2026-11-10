"""Lab CF7-L04-1: Scenario and Sensitivity Analysis.

Computes discrete macroeconomic scenario valuations (Base, Bull, Bear) and
constructs a two-dimensional sensitivity grid of equity value per share
varying WACC and terminal growth rate ceteris paribus.
"""

from __future__ import annotations


def compute_dcf_value(
    base_fcff: float,
    fcff_growth: list[float],
    wacc: float,
    terminal_g: float,
    net_debt: float,
    shares: float,
) -> float:
    """Compute equity value per share from a DCF projection."""
    fcffs: list[float] = []
    curr = base_fcff
    for g in fcff_growth:
        curr *= 1.0 + g
        fcffs.append(curr)

    pv_fcff = sum(f / ((1.0 + wacc) ** (t + 1)) for t, f in enumerate(fcffs))
    horizon = len(fcffs)
    terminal_fcff = fcffs[-1] * (1.0 + terminal_g)
    terminal_val = terminal_fcff / (wacc - terminal_g)
    pv_tv = terminal_val / ((1.0 + wacc) ** horizon)

    enterprise_val = pv_fcff + pv_tv
    equity_val = enterprise_val - net_debt
    return equity_val / shares


def main() -> None:
    base_fcff = 45.0
    net_debt = 80.0
    shares = 10.0

    # Scenarios: Joint parameter variations
    scenarios = {
        "Bear": {"growth": [0.02, 0.01, 0.01], "wacc": 0.11, "g": 0.015},
        "Base": {"growth": [0.06, 0.05, 0.04], "wacc": 0.09, "g": 0.025},
        "Bull": {"growth": [0.10, 0.09, 0.08], "wacc": 0.08, "g": 0.030},
    }

    scenario_values: dict[str, float] = {}
    for name, params in scenarios.items():
        val = compute_dcf_value(
            base_fcff=base_fcff,
            fcff_growth=params["growth"],  # type: ignore[arg-type]
            wacc=params["wacc"],  # type: ignore[arg-type]
            terminal_g=params["g"],  # type: ignore[arg-type]
            net_debt=net_debt,
            shares=shares,
        )
        scenario_values[name] = val

    print("Bear Scenario Per Share:", f"{scenario_values['Bear']:.4f}")
    print("Base Scenario Per Share:", f"{scenario_values['Base']:.4f}")
    print("Bull Scenario Per Share:", f"{scenario_values['Bull']:.4f}")

    # 2D Sensitivity Grid: WACC vs Terminal g (Base case cash flows)
    base_growth = [0.06, 0.05, 0.04]
    wacc_grid = [0.08, 0.09, 0.10]
    g_grid = [0.020, 0.025, 0.030]

    low_wacc_low_g = compute_dcf_value(base_fcff, base_growth, wacc_grid[0], g_grid[0], net_debt, shares)
    mid_wacc_mid_g = compute_dcf_value(base_fcff, base_growth, wacc_grid[1], g_grid[1], net_debt, shares)
    high_wacc_high_g = compute_dcf_value(base_fcff, base_growth, wacc_grid[2], g_grid[2], net_debt, shares)

    print("Sensitivity WACC 8% g 2.0%:", f"{low_wacc_low_g:.4f}")
    print("Sensitivity WACC 9% g 2.5%:", f"{mid_wacc_mid_g:.4f}")
    print("Sensitivity WACC 10% g 3.0%:", f"{high_wacc_high_g:.4f}")


main()
