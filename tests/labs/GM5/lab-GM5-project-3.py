"""Lab GM5-project-3: Rung 3 Independent Project — Crisis Mechanism Dossier Simulator.

Runs full mechanism dossier simulations for two canonical historical episodes:
1. 1998 Long-Term Capital Management (LTCM) Fixed Income Relative-Value Margin Spiral.
2. August 2024 Yen-Carry Trade Deleveraging & Cross-Asset Volatility Spiral.
"""

from __future__ import annotations

from typing import Any


def simulate_spiral(
    p0: float,
    q0: float,
    cash0: float,
    debt0: float,
    haircut0: float,
    shocks: list[float],
    lambda_impact: float,
    haircut_sens: float,
    price_floor: float | None = None,
) -> dict[str, Any]:
    """Self-contained liquidity spiral engine for project dossier verification."""
    prices = [p0]
    positions = [q0]
    haircuts = [haircut0]
    forced_sales = [0.0]
    insolvent = False

    curr_p = p0
    curr_q = q0
    curr_cash = cash0
    curr_debt = debt0
    curr_h = haircut0
    cum_exo = 0.0

    for s in shocks:
        delta_exo = curr_p * s
        if delta_exo < 0.0:
            cum_exo += abs(delta_exo)
        p_shock = max(0.01, curr_p + delta_exo)

        if haircut_sens > 0.0:
            curr_h = min(0.60, curr_h + haircut_sens * abs(s))

        equity_before = curr_q * p_shock + curr_cash - curr_debt
        if equity_before <= 0.0:
            insolvent = True
            forced_qty = curr_q
            p_final = max(0.01, p_shock - lambda_impact * forced_qty)
            if price_floor is not None and p_final < price_floor:
                p_final = price_floor
            prices.append(p_final)
            positions.append(0.0)
            haircuts.append(curr_h)
            forced_sales.append(forced_qty)
            break

        required_margin = curr_h * curr_q * p_shock
        deficit = max(0.0, required_margin - equity_before)

        cash_used = min(curr_cash, deficit)
        rem_def = deficit - cash_used

        denom = curr_h * p_shock
        forced_qty = min(curr_q, rem_def / denom) if (rem_def > 1e-12 and denom > 0) else 0.0

        p_impact = max(0.01, p_shock - lambda_impact * forced_qty)
        if price_floor is not None and p_impact < price_floor:
            p_impact = price_floor

        curr_p = p_impact
        curr_q = max(0.0, curr_q - forced_qty)
        proceeds = forced_qty * p_shock
        curr_debt = max(0.0, curr_debt - cash_used - proceeds)
        curr_cash = max(0.0, curr_cash - cash_used)

        prices.append(curr_p)
        positions.append(curr_q)
        haircuts.append(curr_h)
        forced_sales.append(forced_qty)

    total_drop = p0 - prices[-1]
    mult = (total_drop / cum_exo) if cum_exo > 1e-9 else 1.0

    return {
        "prices": prices,
        "positions": positions,
        "haircuts": haircuts,
        "forced_sales": forced_sales,
        "insolvent": insolvent,
        "total_forced": sum(forced_sales),
        "spiral_multiplier": mult,
    }


def main() -> None:
    # -------------------------------------------------------------
    # Episode 1: 1998 LTCM Relative-Value Fixed Income Spiral
    # -------------------------------------------------------------
    p0_ltcm = 100.0
    q0_ltcm = 1250000.0  # scaled units ($125M nominal)
    equity0_ltcm = 5000000.0  # $5.0M equity (25x leverage)
    debt0_ltcm = p0_ltcm * q0_ltcm - equity0_ltcm
    cash0_ltcm = 500000.0
    h0_ltcm = 0.04

    shocks_ltcm = [-0.015, -0.025, -0.035, -0.040, -0.020]
    lambda_ltcm = 0.000025
    haircut_sens_ltcm = 0.40

    sim_ltcm_base = simulate_spiral(
        p0_ltcm,
        q0_ltcm,
        cash0_ltcm,
        debt0_ltcm,
        h0_ltcm,
        shocks_ltcm,
        lambda_ltcm,
        haircut_sens_ltcm,
        price_floor=None,
    )
    sim_ltcm_back = simulate_spiral(
        p0_ltcm,
        q0_ltcm,
        cash0_ltcm,
        debt0_ltcm,
        h0_ltcm,
        shocks_ltcm,
        lambda_ltcm,
        haircut_sens_ltcm,
        price_floor=88.0,
    )

    print("=== EPISODE 1: 1998 LTCM MECHANISM DOSSIER ===")
    print(f"Initial Gross Assets: ${p0_ltcm * q0_ltcm:,.0f}")
    print(f"Initial Leverage: {(p0_ltcm * q0_ltcm) / equity0_ltcm:.1f}x")
    print(f"Baseline Terminal Price: ${sim_ltcm_base['prices'][-1]:.2f}")
    print(f"Baseline Insolvent: {sim_ltcm_base['insolvent']}")
    print(f"Baseline Spiral Multiplier: {sim_ltcm_base['spiral_multiplier']:.4f}x")
    print(f"Backstopped Terminal Price: ${sim_ltcm_back['prices'][-1]:.2f}")
    print(f"Backstopped Insolvent: {sim_ltcm_back['insolvent']}")

    # -------------------------------------------------------------
    # Episode 2: August 2024 Yen-Carry Trade & Nikkei Plunge
    # -------------------------------------------------------------
    p0_yen = 160.0
    q0_yen = 100000.0
    equity0_yen = 2000000.0  # 8x leverage
    debt0_yen = p0_yen * q0_yen - equity0_yen
    cash0_yen = 100000.0
    h0_yen = 0.12

    shocks_yen = [-0.020, -0.045, -0.060, 0.015, 0.020]
    lambda_yen = 0.00010
    haircut_sens_yen = 0.25

    sim_yen_base = simulate_spiral(
        p0_yen,
        q0_yen,
        cash0_yen,
        debt0_yen,
        h0_yen,
        shocks_yen,
        lambda_yen,
        haircut_sens_yen,
        price_floor=None,
    )
    sim_yen_back = simulate_spiral(
        p0_yen,
        q0_yen,
        cash0_yen,
        debt0_yen,
        h0_yen,
        shocks_yen,
        lambda_yen,
        haircut_sens_yen,
        price_floor=142.0,
    )

    print("\n=== EPISODE 2: AUGUST 2024 YEN CARRY UNWIND ===")
    print(f"Initial USD/JPY Spot: {p0_yen:.2f}")
    print(f"Baseline Trough Spot: {min(sim_yen_base['prices']):.2f}")
    print(f"Baseline Spiral Multiplier: {sim_yen_base['spiral_multiplier']:.4f}x")
    print(f"Backstopped Trough Spot: {min(sim_yen_back['prices']):.2f}")
    print(f"Multiplier Attenuation: {sim_yen_base['spiral_multiplier'] - sim_yen_back['spiral_multiplier']:.4f}x")


main()
