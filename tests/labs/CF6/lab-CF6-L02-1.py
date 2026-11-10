"""CF6 Lesson 2 Inline Lab 1: Benveniste-Spindt Bookbuilding Allocation.

Holdings to BUILDER_RULES §6: deterministic, self-contained, standard library.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal
from typing import Any


def run_bookbuilding(
    bids: list[dict[str, Any]],
    total_shares: int,
    clearing_price: float,
    rule: str = "discretionary",
) -> dict[str, Any]:
    alloc: dict[str, int] = {b["bidder_id"]: 0 for b in bids}
    qualifying = [b for b in bids if b["bid_price"] >= clearing_price]
    total_qualifying_demand = sum(b["bid_shares"] for b in qualifying)

    if total_qualifying_demand <= total_shares:
        for b in qualifying:
            alloc[b["bidder_id"]] = b["bid_shares"]
    elif rule == "pro_rata":
        ratio = total_shares / total_qualifying_demand
        raw = {b["bidder_id"]: b["bid_shares"] * ratio for b in qualifying}
        base = {b["bidder_id"]: math.floor(raw[b["bidder_id"]]) for b in qualifying}
        rem = total_shares - sum(base.values())
        sorted_by_frac = sorted(
            qualifying,
            key=lambda b: raw[b["bidder_id"]] - base[b["bidder_id"]],
            reverse=True,
        )
        for i in range(rem):
            base[sorted_by_frac[i]["bidder_id"]] += 1
        alloc.update(base)
    elif rule == "discretionary":
        pos_bids = [b for b in qualifying if b.get("revealed_info") == "positive"]
        pos_demand = sum(b["bid_shares"] for b in pos_bids)
        if pos_demand <= total_shares:
            for b in pos_bids:
                alloc[b["bidder_id"]] = b["bid_shares"]
            rem_shares = total_shares - pos_demand
            other_bids = [b for b in qualifying if b.get("revealed_info") != "positive"]
            other_demand = sum(b["bid_shares"] for b in other_bids)
            if other_demand > 0 and rem_shares > 0:
                ratio = rem_shares / other_demand
                raw = {b["bidder_id"]: b["bid_shares"] * ratio for b in other_bids}
                base = {b["bidder_id"]: math.floor(raw[b["bidder_id"]]) for b in other_bids}
                rem = rem_shares - sum(base.values())
                sorted_others = sorted(
                    other_bids,
                    key=lambda b: raw[b["bidder_id"]] - base[b["bidder_id"]],
                    reverse=True,
                )
                for i in range(rem):
                    base[sorted_others[i]["bidder_id"]] += 1
                alloc.update(base)
        else:
            ratio = total_shares / pos_demand
            raw = {b["bidder_id"]: b["bid_shares"] * ratio for b in pos_bids}
            base = {b["bidder_id"]: math.floor(raw[b["bidder_id"]]) for b in pos_bids}
            rem = total_shares - sum(base.values())
            sorted_pos = sorted(
                pos_bids,
                key=lambda b: raw[b["bidder_id"]] - base[b["bidder_id"]],
                reverse=True,
            )
            for i in range(rem):
                base[sorted_pos[i]["bidder_id"]] += 1
            alloc.update(base)

    tot_alloc = sum(alloc.values())
    inst_shares = sum(alloc[b["bidder_id"]] for b in bids if b.get("investor_type") == "institutional")
    inst_frac = inst_shares / tot_alloc if tot_alloc > 0 else 0.0
    fulfill = {b["bidder_id"]: alloc[b["bidder_id"]] / b["bid_shares"] if b["bid_shares"] > 0 else 0.0 for b in bids}
    price_dec = Decimal(str(clearing_price))
    rev_cents = int((Decimal(tot_alloc) * price_dec * Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    return {
        "allocations": alloc,
        "total_allocated": tot_alloc,
        "total_revenue_cents": rev_cents,
        "institutional_share_fraction": inst_frac,
        "fulfillment_rates": fulfill,
    }


def main() -> None:
    # 4 syndicate book orders
    bids: list[dict[str, Any]] = [
        {
            "bidder_id": "Fidelity (Pos)",
            "bid_price": 22.0,
            "bid_shares": 1_000_000,
            "revealed_info": "positive",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "BlackRock (Pos)",
            "bid_price": 21.0,
            "bid_shares": 800_000,
            "revealed_info": "positive",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "Vanguard (Neu)",
            "bid_price": 20.0,
            "bid_shares": 1_200_000,
            "revealed_info": "neutral",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "Retail Pool",
            "bid_price": 20.0,
            "bid_shares": 1_000_000,
            "revealed_info": "neutral",
            "investor_type": "retail",
        },
    ]
    total_offering = 2_500_000
    clearing_price = 20.00

    print("=== Bookbuilding Order Book Analysis ===")
    total_demand = sum(int(b["bid_shares"]) for b in bids)
    over_sub = total_demand / total_offering
    print(f"Total Offering: {total_offering:,.0f} shares | Clearing Price: ${clearing_price:.2f}")
    print(f"Total Demand:   {total_demand:,.0f} shares | Oversubscription: {over_sub:.2f}x\n")

    # 1. Pro-Rata Allocation
    res_pr = run_bookbuilding(bids, total_offering, clearing_price, rule="pro_rata")
    print("--- Rule A: Uniform Pro-Rata Allocation ---")
    for b in bids:
        bid = b["bidder_id"]
        sh = res_pr["allocations"][bid]
        pct = res_pr["fulfillment_rates"][bid] * 100
        print(f"  {bid:<16}: {sh:,.0f} shares ({pct:.1f}% fulfillment)")
    print(f"  Institutional Allocation Fraction: {res_pr['institutional_share_fraction'] * 100:.1f}%\n")

    # 2. Benveniste-Spindt Discretionary Allocation
    res_disc = run_bookbuilding(bids, total_offering, clearing_price, rule="discretionary")
    print("--- Rule B: Benveniste-Spindt Discretionary Allocation ---")
    for b in bids:
        bid = b["bidder_id"]
        sh = res_disc["allocations"][bid]
        pct = res_disc["fulfillment_rates"][bid] * 100
        print(f"  {bid:<16}: {sh:,.0f} shares ({pct:.1f}% fulfillment)")
    print(f"  Institutional Allocation Fraction: {res_disc['institutional_share_fraction'] * 100:.1f}%")
    print(f"  Total Offering Revenue:            ${res_disc['total_revenue_cents'] / 100:,.2f}")


main()
