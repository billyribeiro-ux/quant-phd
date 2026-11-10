"""CF6 Project Lab 1 (Rung 1 Worked Example): Full IPO Pricing and Syndicate Model.

Holdings to BUILDER_RULES §6: deterministic, self-contained, standard library.
Demonstrates end-to-end execution of the investment banking capital raising model.
"""

from __future__ import annotations

import math
from decimal import ROUND_HALF_UP, Decimal
from typing import Any


def rock_equilibrium_price(
    v_low: float,
    v_high: float,
    prob_high: float,
    s_shares: int,
    informed_demand: int,
    uninformed_budget: float,
) -> tuple[float, float, float]:
    e_v = (1.0 - prob_high) * v_low + prob_high * v_high

    def expected_profit(p: float) -> float:
        d_u = uninformed_budget / p
        alloc_l = min(d_u, float(s_shares))
        tot_high_dem = d_u + float(informed_demand)
        alloc_h = float(s_shares) / tot_high_dem * d_u if tot_high_dem > float(s_shares) else d_u
        return (1.0 - prob_high) * alloc_l * (v_low - p) + prob_high * alloc_h * (v_high - p)

    lo, hi = v_low, e_v
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if expected_profit(mid) > 0.0:
            lo = mid
        else:
            hi = mid

    p_star = 0.5 * (lo + hi)
    d_u_star = uninformed_budget / p_star
    total_demand_high = d_u_star + float(informed_demand)
    alpha_h = min(1.0, float(s_shares) / total_demand_high)
    underpricing = (e_v - p_star) / p_star
    return p_star, alpha_h, underpricing


def bookbuilding_allocation(
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


def syndicate_economics(
    gross_proceeds_cents: int,
    spread_bps: int = 700,
    lead_manager_share: float = 0.60,
    co_manager_share: float = 0.30,
    selling_group_share: float = 0.10,
) -> dict[str, int]:
    spread_dec = Decimal(spread_bps) / Decimal(10000)
    total_spread = int((Decimal(gross_proceeds_cents) * spread_dec).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    net_proceeds = gross_proceeds_cents - total_spread

    lead_dec = Decimal(str(lead_manager_share))
    co_dec = Decimal(str(co_manager_share))
    lead_cents = int((Decimal(total_spread) * lead_dec).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    co_cents = int((Decimal(total_spread) * co_dec).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    selling_cents = total_spread - lead_cents - co_cents

    mgmt_fee = int((Decimal(total_spread) * Decimal("0.20")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    uw_fee = int((Decimal(total_spread) * Decimal("0.20")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    selling_concession = total_spread - mgmt_fee - uw_fee

    return {
        "gross_proceeds_cents": gross_proceeds_cents,
        "total_spread_cents": total_spread,
        "net_proceeds_cents": net_proceeds,
        "lead_manager_cents": lead_cents,
        "co_manager_cents": co_cents,
        "selling_group_cents": selling_cents,
        "management_fee_cents": mgmt_fee,
        "underwriting_fee_cents": uw_fee,
        "selling_concession_cents": selling_concession,
    }


def main() -> None:
    print("=== CF6 Project Rung 1: Benchmark IPO Pricing and Allocation ===")

    # 1. Rock Winner's Curse Pricing
    v_l, v_h, prob_h = 13.50, 31.20, 0.58
    s_shares, i_dem, b_u = 2_000_000, 2_400_000, 48_000_000.0
    p_star, alpha_h, up = rock_equilibrium_price(v_l, v_h, prob_h, s_shares, i_dem, b_u)

    print(f"Rock Equilibrium Offer Price:   ${p_star:.2f}")
    print(f"Equilibrium Expected Underpricing:{up * 100:.2f}%")
    print(f"High State Rationing alpha_H:   {alpha_h:.4f}\n")

    # 2. Bookbuilding Allocation
    bids: list[dict[str, Any]] = [
        {
            "bidder_id": "Inst_Alpha",
            "bid_price": 25.0,
            "bid_shares": 800_000,
            "revealed_info": "positive",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "Inst_Beta",
            "bid_price": 24.0,
            "bid_shares": 600_000,
            "revealed_info": "positive",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "Inst_Gamma",
            "bid_price": 23.5,
            "bid_shares": 900_000,
            "revealed_info": "neutral",
            "investor_type": "institutional",
        },
        {
            "bidder_id": "Retail_Synd",
            "bid_price": 23.5,
            "bid_shares": 500_000,
            "revealed_info": "neutral",
            "investor_type": "retail",
        },
    ]
    res_bb = bookbuilding_allocation(bids, total_shares=2_000_000, clearing_price=23.50, rule="discretionary")
    print(f"Total Shares Allocated:         {res_bb['total_allocated']:,.0f}")
    print(f"Total Offering Proceeds:        ${res_bb['total_revenue_cents'] / 100:,.2f}")
    print(f"Institutional Allocation Share: {res_bb['institutional_share_fraction'] * 100:.1f}%\n")

    # 3. Syndicate Economics (7% gross spread)
    gross_cents = res_bb["total_revenue_cents"]
    res_syn = syndicate_economics(gross_cents, spread_bps=700)
    print("--- Syndicate Proceeds Breakdown (700 bps Spread) ---")
    print(f"Gross Offering Proceeds:        ${res_syn['gross_proceeds_cents'] / 100:,.2f}")
    print(f"Total Syndicate Spread (7.0%):  ${res_syn['total_spread_cents'] / 100:,.2f}")
    print(f"Net Proceeds to Issuing Firm:   ${res_syn['net_proceeds_cents'] / 100:,.2f}")
    print(f"Lead Manager Compensation:      ${res_syn['lead_manager_cents'] / 100:,.2f}")
    print(f"Co-Managers Compensation:       ${res_syn['co_manager_cents'] / 100:,.2f}")
    print(f"Selling Group Compensation:     ${res_syn['selling_group_cents'] / 100:,.2f}")


main()
