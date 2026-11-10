"""Long-run abnormal return calculates arithmetic difference of sums (CAR) instead of compounding products (BHAR)."""

from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_UP
from typing import Any


def rock_equilibrium_price(
    v_low: float,
    v_high: float,
    prob_high: float,
    s_shares: int,
    informed_demand: int,
    uninformed_budget: float,
) -> tuple[float, float, float]:
    if not (v_low > 0.0 and v_high > v_low):
        raise ValueError("v_high must be strictly greater than v_low > 0")
    if not (0.0 < prob_high < 1.0):
        raise ValueError("prob_high must be in (0, 1)")
    if s_shares <= 0 or informed_demand <= 0 or uninformed_budget <= 0.0:
        raise ValueError("Shares, demand, and budget must be strictly positive")

    e_v = (1.0 - prob_high) * v_low + prob_high * v_high

    def expected_profit(p: float) -> float:
        d_u = uninformed_budget / p
        alloc_l = min(d_u, float(s_shares))
        tot_high_dem = d_u + float(informed_demand)
        if tot_high_dem > float(s_shares):
            alloc_h = (float(s_shares) / tot_high_dem) * d_u
        else:
            alloc_h = d_u
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
    if total_shares <= 0 or clearing_price <= 0.0:
        raise ValueError("total_shares and clearing_price must be positive")
    if rule not in ("discretionary", "pro_rata"):
        raise ValueError("rule must be 'discretionary' or 'pro_rata'")

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
    fulfill = {
        b["bidder_id"]: alloc[b["bidder_id"]] / b["bid_shares"] if b["bid_shares"] > 0 else 0.0
        for b in bids
    }
    price_dec = Decimal(str(clearing_price))
    rev_cents = int((Decimal(tot_alloc) * price_dec * Decimal("100")).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    return {
        "allocations": alloc,
        "total_allocated": tot_alloc,
        "total_revenue_cents": rev_cents,
        "institutional_share_fraction": inst_frac,
        "fulfillment_rates": fulfill,
    }


def seo_announcement_impact(
    v_assets_good: float,
    v_assets_bad: float,
    prob_good: float,
    project_cost: float,
    project_npv: float,
    slack_cash: float = 0.0,
) -> dict[str, Any]:
    if not (v_assets_good > v_assets_bad > 0.0):
        raise ValueError("v_assets_good must exceed v_assets_bad > 0")
    if not (0.0 < prob_good < 1.0):
        raise ValueError("prob_good must be in (0, 1)")
    if project_cost <= 0.0 or project_npv <= 0.0 or slack_cash < 0.0:
        raise ValueError("Project cost and NPV must be positive; slack must be non-negative")

    e_required = max(0.0, project_cost - slack_cash)
    if e_required == 0.0:
        return {
            "good_firm_decision": "issue",
            "dilution_cost": 0.0,
            "npv_threshold": 0.0,
            "pooling_price": v_assets_good + slack_cash + project_npv,
            "announcement_return": 0.0,
            "slack_sufficient": True,
        }

    a_bar = prob_good * v_assets_good + (1.0 - prob_good) * v_assets_bad
    v_pool = a_bar + project_cost + project_npv
    alpha = e_required / v_pool
    v_good_true = v_assets_good + project_cost + project_npv
    dilution_cost = alpha * v_good_true - e_required

    net_benefit_good = (1.0 - alpha) * v_good_true - (v_assets_good + slack_cash)
    decision = "issue" if net_benefit_good >= -1e-9 else "pass"
    npv_threshold = e_required * (1.0 - prob_good) * (v_assets_good - v_assets_bad) / v_pool

    p_pre = a_bar + slack_cash
    p_post_existing = v_pool - e_required
    ann_ret = (p_post_existing - p_pre) / p_pre if decision == "issue" else 0.0

    return {
        "good_firm_decision": decision,
        "dilution_cost": dilution_cost,
        "npv_threshold": npv_threshold,
        "pooling_price": v_pool,
        "announcement_return": ann_ret,
        "slack_sufficient": False,
    }


def long_run_bhar(firm_returns: list[float], benchmark_returns: list[float]) -> dict[str, Any]:
    n = len(firm_returns)
    if n == 0 or len(benchmark_returns) != n:
        raise ValueError("Return series must be non-empty and equal in length")

    prod_firm = 1.0
    prod_bench = 1.0
    car = 0.0
    for rf, rb in zip(firm_returns, benchmark_returns, strict=True):
        prod_firm *= (1.0 + rf)
        prod_bench *= (1.0 + rb)
        car += (rf - rb)

    # MUTANT ERROR: Sets BHAR to cumulative arithmetic return CAR
    bhar = car
    wr = prod_firm / prod_bench if prod_bench != 0.0 else 0.0
    ann_firm = (prod_firm ** (12.0 / float(n))) - 1.0 if prod_firm > 0.0 else -1.0
    ann_bench = (prod_bench ** (12.0 / float(n))) - 1.0 if prod_bench > 0.0 else -1.0

    return {
        "bhar": bhar,
        "wealth_relative": wr,
        "car": car,
        "firm_compounded": prod_firm - 1.0,
        "benchmark_compounded": prod_bench - 1.0,
        "annualized_abnormal": ann_firm - ann_bench,
    }


def syndicate_economics(
    gross_proceeds_cents: int,
    spread_bps: int = 700,
    lead_manager_share: float = 0.60,
    co_manager_share: float = 0.30,
    selling_group_share: float = 0.10,
) -> dict[str, int]:
    if gross_proceeds_cents <= 0 or spread_bps <= 0:
        raise ValueError("gross_proceeds_cents and spread_bps must be positive")
    if not (0.999 < lead_manager_share + co_manager_share + selling_group_share < 1.001):
        raise ValueError("Syndicate shares must sum to 1.0")

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
