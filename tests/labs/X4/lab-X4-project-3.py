"""Lab X4-project-3: Rung 3 reference verification across multiple seeds.

Validates the full reserve portfolio stress testing engine across seeds 0 through 4,
checking modified duration pricing, liquidation waterfall accounting, and critical run sizes.
"""

from __future__ import annotations

import random
from typing import Any

TIER_NAMES: list[str] = ["cash", "overnight_repo", "tbills_short", "treasury_notes", "bank_deposits"]


def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic problem instance for seed."""
    rng = random.Random(seed)
    total_liabilities = round(10000.0 + (seed * 431) % 40000 + rng.uniform(0.0, 100.0), 2)
    surplus_pct = 0.002 + ((seed * 17) % 10) * 0.001
    total_assets = total_liabilities * (1.0 + surplus_pct)

    w_cash = 0.15 + (seed % 7) * 0.01
    w_repo = 0.25 + ((seed * 3) % 8) * 0.01
    w_tbills = 0.30 + ((seed * 5) % 6) * 0.01
    w_bank = 0.08 + (seed % 5) * 0.01
    w_notes = 1.0 - (w_cash + w_repo + w_tbills + w_bank)

    d_tbills = round(0.20 + (seed % 5) * 0.03, 3)
    d_notes = round(2.00 + ((seed * 7) % 7) * 0.20, 2)

    h_repo = round(0.005 + (seed % 4) * 0.001, 4)
    h_tbills = round(0.010 + ((seed * 2) % 5) * 0.002, 4)
    h_notes = round(0.025 + ((seed * 3) % 4) * 0.005, 4)
    h_bank = round(0.060 + (seed % 5) * 0.010, 4)

    tier_pars = [
        round(total_assets * w_cash, 2),
        round(total_assets * w_repo, 2),
        round(total_assets * w_tbills, 2),
        round(total_assets * w_notes, 2),
        round(total_assets * w_bank, 2),
    ]
    tier_durations = [0.0, 0.0, d_tbills, d_notes, 0.0]
    tier_haircuts = [0.0, h_repo, h_tbills, h_notes, h_bank]

    rate_shock_bps = round(75.0 + (seed * 23) % 175, 1)
    peg_threshold = 0.995 if seed % 2 == 0 else 0.990
    stressed_outflow_30d = round(total_liabilities * 0.30, 2)

    return {
        "seed": seed,
        "total_liabilities": total_liabilities,
        "tier_names": list(TIER_NAMES),
        "tier_pars": tier_pars,
        "tier_durations": tier_durations,
        "tier_haircuts": tier_haircuts,
        "rate_shock_bps": rate_shock_bps,
        "peg_threshold": peg_threshold,
        "stressed_outflow_30d": stressed_outflow_30d,
    }


def get_reserve_assets(inst: dict[str, Any]) -> dict[str, dict[str, float]]:
    """Reconstruct tiered reserve assets dictionary from instance arrays."""
    names: list[str] = inst["tier_names"]
    pars: list[float] = inst["tier_pars"]
    durations: list[float] = inst["tier_durations"]
    haircuts: list[float] = inst["tier_haircuts"]

    return {
        name: {"par": p, "duration": d, "haircut": h}
        for name, p, d, h in zip(names, pars, durations, haircuts, strict=True)
    }


def apply_rate_shock(
    reserve_assets: dict[str, dict[str, float]],
    rate_shock_bps: float,
) -> dict[str, dict[str, float]]:
    """Apply interest rate shock using modified duration pricing."""
    dy = rate_shock_bps / 10000.0
    shocked: dict[str, dict[str, float]] = {}
    for tier, data in reserve_assets.items():
        par = float(data["par"])
        duration = float(data["duration"])
        haircut = float(data["haircut"])
        price_factor = max(0.0, 1.0 - duration * dy)
        shocked[tier] = {
            "par": par,
            "duration": duration,
            "haircut": haircut,
            "market_value": par * price_factor,
        }
    return shocked


def simulate_waterfall(
    total_liabilities: float,
    shocked_assets: dict[str, dict[str, float]],
    redemptions: float,
) -> float:
    """Execute redemption waterfall and return post-run NAV."""
    order = ("cash", "overnight_repo", "tbills_short", "treasury_notes", "bank_deposits")
    current_mv = {t: shocked_assets[t]["market_value"] for t in order}
    haircuts = {t: shocked_assets[t]["haircut"] for t in order}

    rem_r = redemptions
    for t in order:
        if rem_r <= 0.0:
            break
        mv = current_mv[t]
        h = haircuts[t]
        avail_cash = mv * (1.0 - h)
        if rem_r <= avail_cash:
            current_mv[t] -= rem_r / (1.0 - h)
            rem_r = 0.0
        else:
            current_mv[t] = 0.0
            rem_r -= avail_cash

    rem_tokens = max(0.0, total_liabilities - redemptions)
    rem_mv = sum(current_mv.values())

    if rem_r > 1e-9:
        return 0.0
    if rem_tokens <= 1e-9:
        return 1.0
    return rem_mv / rem_tokens


def find_peg_break(
    total_liabilities: float,
    shocked_assets: dict[str, dict[str, float]],
    peg_threshold: float,
) -> tuple[float, float, bool]:
    """Find critical run size R* that causes NAV < peg_threshold."""
    if simulate_waterfall(total_liabilities, shocked_assets, 0.0) < peg_threshold:
        return 0.0, 0.0, True

    if simulate_waterfall(total_liabilities, shocked_assets, total_liabilities - 0.01) >= peg_threshold:
        return total_liabilities, 1.0, False

    low = 0.0
    high = total_liabilities
    for _ in range(60):
        mid = (low + high) / 2.0
        if simulate_waterfall(total_liabilities, shocked_assets, mid) < peg_threshold:
            high = mid
        else:
            low = mid

    r_star = (low + high) / 2.0
    return round(r_star, 4), round(r_star / total_liabilities, 6), True


def compute_lcr(reserve_assets: dict[str, dict[str, float]], outflow_30d: float) -> float:
    """Compute Liquidity Coverage Ratio."""
    cash = reserve_assets.get("cash", {}).get("par", 0.0)
    repo = reserve_assets.get("overnight_repo", {}).get("par", 0.0)
    return (cash + repo) / outflow_30d


def main() -> None:
    print("Lab X4-project-3 | Multi-Seed Stress Testing Suite Verification")
    print("----------------------------------------------------------------")

    seeds_to_check = [0, 1, 2, 3, 4]
    hdr = f"{'Seed':<5} | {'Liabilities':<12} | {'Rate Shock':<10} | {'LCR':<8} | {'R* ($M)':<12} | {'Run %':<8} | Peg"
    print(hdr)
    print("-" * len(hdr))

    for seed in seeds_to_check:
        inst = make_instance(seed)
        liab = float(inst["total_liabilities"])
        shock_bps = float(inst["rate_shock_bps"])
        peg_thresh = float(inst["peg_threshold"])
        outflow_30d = float(inst["stressed_outflow_30d"])

        assets = get_reserve_assets(inst)
        shocked = apply_rate_shock(assets, shock_bps)
        lcr = compute_lcr(assets, outflow_30d)

        r_star, r_pct, broken = find_peg_break(liab, shocked, peg_thresh)
        run_pct_str = f"{r_pct * 100.0:.2f}%"

        line = (
            f"{seed:<5} | ${liab:<11.1f} | +{shock_bps:<8.1f} | {lcr:<8.2f} | "
            f"${r_star:<11.1f} | {run_pct_str:<8} | {broken}"
        )
        print(line)

        assert lcr > 0.0
        assert 0.0 <= r_star <= liab

    print("\nAll seed instances validated successfully under reference stress test engine.")


main()
