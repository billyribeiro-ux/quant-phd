"""Lab X4-project-1: Rung 1 worked example for Stablecoin Reserve Stress Test.

SIMULATED reserve portfolio on seed 42. Traces rate shock duration adjustment,
liquidation waterfall accounting, and binary search for critical peg-break run size R*.
"""

from __future__ import annotations

from typing import Any

ORDERED_TIERS = ("cash", "overnight_repo", "tbills_short", "treasury_notes", "bank_deposits")


def make_sample_instance() -> dict[str, Any]:
    """Generate fixed worked example instance (seed 42)."""
    liabilities = 20000.0  # $20 Billion
    assets = {
        "cash": {"par": 3600.0, "duration": 0.0, "haircut": 0.0},
        "overnight_repo": {"par": 5400.0, "duration": 0.0, "haircut": 0.005},
        "tbills_short": {"par": 6800.0, "duration": 0.25, "haircut": 0.010},
        "treasury_notes": {"par": 3000.0, "duration": 2.50, "haircut": 0.035},
        "bank_deposits": {"par": 1400.0, "duration": 0.0, "haircut": 0.080},
    }
    return {
        "liabilities": liabilities,
        "assets": assets,
        "rate_shock_bps": 125.0,  # 125 bps
        "peg_threshold": 0.995,
    }


def apply_rate_shock(assets: dict[str, dict[str, float]], rate_shock_bps: float) -> dict[str, dict[str, float]]:
    dy = rate_shock_bps / 10000.0
    shocked = {}
    for tier, data in assets.items():
        par = data["par"]
        dur = data["duration"]
        h = data["haircut"]
        mv = par * max(0.0, 1.0 - dur * dy)
        shocked[tier] = {"par": par, "duration": dur, "haircut": h, "market_value": mv}
    return shocked


def simulate_waterfall(liabilities: float, shocked: dict[str, dict[str, float]], redemptions: float) -> dict[str, Any]:
    rem_r = redemptions
    current_mv = {t: shocked[t]["market_value"] for t in ORDERED_TIERS}
    haircut_losses = {t: 0.0 for t in ORDERED_TIERS}

    for t in ORDERED_TIERS:
        if rem_r <= 0:
            break
        mv = current_mv[t]
        h = shocked[t]["haircut"]
        avail_cash = mv * (1.0 - h)

        if rem_r <= avail_cash:
            mv_used = rem_r / (1.0 - h)
            loss = mv_used - rem_r
            current_mv[t] -= mv_used
            haircut_losses[t] = loss
            rem_r = 0.0
        else:
            current_mv[t] = 0.0
            haircut_losses[t] = mv * h
            rem_r -= avail_cash

    rem_tokens = max(0.0, liabilities - redemptions)
    rem_mv = sum(current_mv.values())
    total_loss = sum(haircut_losses.values())

    nav = rem_mv / rem_tokens if rem_tokens > 1e-9 else 1.0
    return {
        "nav": nav,
        "remaining_tokens": rem_tokens,
        "remaining_mv": rem_mv,
        "haircut_losses": haircut_losses,
        "total_haircut_loss": total_loss,
        "unfulfilled": rem_r,
    }


def main() -> None:
    print("Lab X4-project-1 | Rung 1 Worked Example: Reserve Stress Waterfall")
    print("-------------------------------------------------------------------")

    inst = make_sample_instance()
    liab = inst["liabilities"]
    shocked = apply_rate_shock(inst["assets"], inst["rate_shock_bps"])

    total_par = sum(v["par"] for v in inst["assets"].values())
    total_shocked_mv = sum(v["market_value"] for v in shocked.values())

    print(f"Total Liabilities:             ${liab:,.1f}M")
    print(f"Initial Reserve Par Value:     ${total_par:,.1f}M")
    print(f"Rate Shock:                    +{inst['rate_shock_bps']:.1f} bps")
    print(f"Post-Shock Market Value:       ${total_shocked_mv:,.2f}M")
    print(f"Duration Mark-to-Market Loss:  ${total_par - total_shocked_mv:,.2f}M")
    print(f"Initial Backing Ratio:         ${total_shocked_mv / liab:.5f}")

    # Stress test under a 40% redemption run ($8,000M)
    run_amount = 8000.0
    res_run = simulate_waterfall(liab, shocked, run_amount)
    print(f"\nStress Scenario: 40% Run (${run_amount:,.1f}M Redemptions):")
    print(f"  Remaining Tokens:            ${res_run['remaining_tokens']:,.1f}M")
    print(f"  Remaining Asset Market Val:  ${res_run['remaining_mv']:,.2f}M")
    print(f"  Total Liquidation Haircuts:  ${res_run['total_haircut_loss']:,.2f}M")
    print(f"  Post-Run Secondary NAV:      ${res_run['nav']:.5f}")

    # Binary search for R*
    peg_threshold = inst["peg_threshold"]
    low = 0.0
    high = liab
    for _ in range(50):
        mid = (low + high) / 2.0
        nav_mid = simulate_waterfall(liab, shocked, mid)["nav"]
        if nav_mid < peg_threshold:
            high = mid
        else:
            low = mid

    r_star = (low + high) / 2.0
    res_star = simulate_waterfall(liab, shocked, r_star)
    print(f"\nCritical Peg-Break Run Analysis (NAV < ${peg_threshold:.3f}):")
    print(f"  Critical Run Size R*:        ${r_star:,.2f}M")
    print(f"  Run Percentage of Supply:    {r_star / liab * 100.0:.2f}%")
    print(f"  NAV at Critical Point:       ${res_star['nav']:.5f}")


main()
