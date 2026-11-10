"""CF6 Project Lab 2 (Rung 2 Completion Problem): Solved Twin.

Holdings to BUILDER_RULES §6: deterministic, self-contained, standard library.
Completion problem: fill in Rock underpricing calculation and discretionary bookbuilding allocation.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal


def complete_rock_pricing(
    v_l: float,
    v_h: float,
    p: float,
    s_shares: int,
    informed_dem: int,
    uninformed_b: float,
) -> tuple[float, float, float]:
    e_v = (1.0 - p) * v_l + p * v_h

    def expected_profit(p_test: float) -> float:
        d_u = uninformed_b / p_test
        alloc_l = min(d_u, float(s_shares))
        tot_dem_h = d_u + float(informed_dem)
        alloc_h = float(s_shares) / tot_dem_h * d_u if tot_dem_h > float(s_shares) else d_u
        return (1.0 - p) * alloc_l * (v_l - p_test) + p * alloc_h * (v_h - p_test)

    lo, hi = v_l, e_v
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if expected_profit(mid) > 0.0:
            lo = mid
        else:
            hi = mid

    p_star = 0.5 * (lo + hi)
    d_u_star = uninformed_b / p_star
    alpha_h = min(1.0, float(s_shares) / (d_u_star + float(informed_dem)))
    underpricing = (e_v - p_star) / p_star
    return p_star, alpha_h, underpricing


def complete_discretionary_allocation(
    bids: list[dict[str, object]],
    total_shares: int,
    clearing_price: float,
) -> dict[str, int]:
    alloc: dict[str, int] = {str(b["bidder_id"]): 0 for b in bids}
    qualifying = [b for b in bids if float(str(b["bid_price"])) >= clearing_price]

    pos_bids = [b for b in qualifying if str(b.get("revealed_info")) == "positive"]
    pos_demand = sum(int(str(b["bid_shares"])) for b in pos_bids)

    if pos_demand <= total_shares:
        for b in pos_bids:
            alloc[str(b["bidder_id"])] = int(str(b["bid_shares"]))
        rem_shares = total_shares - pos_demand
        other_bids = [b for b in qualifying if str(b.get("revealed_info")) != "positive"]
        other_demand = sum(int(str(b["bid_shares"])) for b in other_bids)
        if other_demand > 0 and rem_shares > 0:
            ratio = rem_shares / other_demand
            raw = {str(b["bidder_id"]): int(str(b["bid_shares"])) * ratio for b in other_bids}
            base = {str(b["bidder_id"]): math.floor(raw[str(b["bidder_id"])]) for b in other_bids}
            rem = rem_shares - sum(base.values())
            sorted_others = sorted(
                other_bids,
                key=lambda b: raw[str(b["bidder_id"])] - base[str(b["bidder_id"])],
                reverse=True,
            )
            for i in range(rem):
                base[str(sorted_others[i]["bidder_id"])] += 1
            alloc.update(base)
    else:
        ratio = total_shares / pos_demand
        raw = {str(b["bidder_id"]): int(str(b["bid_shares"])) * ratio for b in pos_bids}
        base = {str(b["bidder_id"]): math.floor(raw[str(b["bidder_id"])]) for b in pos_bids}
        rem = total_shares - sum(base.values())
        sorted_pos = sorted(
            pos_bids,
            key=lambda b: raw[str(b["bidder_id"])] - base[str(b["bidder_id"])],
            reverse=True,
        )
        for i in range(rem):
            base[str(sorted_pos[i]["bidder_id"])] += 1
        alloc.update(base)

    return alloc


def main() -> None:
    print("=== CF6 Project Rung 2: Completion Verification ===")

    # Test Rock pricing completion
    p_star, alpha_h, up = complete_rock_pricing(
        v_l=11.0, v_h=25.0, p=0.60, s_shares=1_500_000, informed_dem=1_800_000, uninformed_b=36_000_000.0
    )
    print(f"Calculated Offer Price:       ${p_star:.2f}")
    print(f"Calculated Underpricing:       {up * 100:.2f}%")
    print(f"High-State Allocation alpha_H: {alpha_h:.4f}")

    # Test Discretionary Allocation completion
    bids: list[dict[str, object]] = [
        {"bidder_id": "Inst_1", "bid_price": 20.0, "bid_shares": 600_000, "revealed_info": "positive"},
        {"bidder_id": "Inst_2", "bid_price": 19.5, "bid_shares": 500_000, "revealed_info": "neutral"},
        {"bidder_id": "Ret_1", "bid_price": 19.5, "bid_shares": 400_000, "revealed_info": "neutral"},
    ]
    allocs = complete_discretionary_allocation(bids, total_shares=1_000_000, clearing_price=19.5)
    print("Allocations:")
    for k in sorted(allocs):
        print(f"  {k}: {allocs[k]:,d} shares")

    # Articulation check
    tot_sh = sum(allocs.values())
    tot_rev = int((Decimal(tot_sh) * Decimal("19.5") * Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    print(f"Total Shares Allocated: {tot_sh:,d} (Conserved: {tot_sh == 1_000_000})")
    print(f"Total Gross Revenue:   ${tot_rev / 100:,.2f}")


main()
