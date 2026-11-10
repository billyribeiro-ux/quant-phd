"""Mutant 2: Broad-based weighted average anti-dilution uses new round issued shares
instead of hypothetical shares in the numerator."""

from __future__ import annotations

import itertools
from typing import Any


def compute_anti_dilution_price(
    old_conv_price: float,
    new_issue_price: float,
    investment: float,
    fully_diluted_pre: float,
    common_preferred_pre: float,
    method: str,
) -> float:
    if new_issue_price >= old_conv_price - 1e-9:
        return old_conv_price
    if method == "full_ratchet":
        return new_issue_price
    if method == "broad_based":
        new_shares = investment / new_issue_price
        # ERROR: Uses new_shares instead of hypothetical_shares in numerator
        adjusted_price = old_conv_price * (fully_diluted_pre + new_shares) / (fully_diluted_pre + new_shares)
        return float(adjusted_price)
    if method == "narrow_based":
        new_shares = investment / new_issue_price
        hypothetical_shares = investment / old_conv_price
        numerator = common_preferred_pre + hypothetical_shares
        denominator = common_preferred_pre + new_shares
        return float(old_conv_price * numerator / denominator)
    raise ValueError(f"Unknown anti-dilution method: {method}")


def build_cap_table(instance: dict[str, Any]) -> dict[str, Any]:
    founders_shares = float(instance["founders_shares"])
    pre_moneys = [float(x) for x in instance["round_pre_money"]]
    investments = [float(x) for x in instance["round_investments"]]
    pool_targets = [float(x) for x in instance["round_pools"]]
    multiples = [float(x) for x in instance["round_liquidation_multiples"]]
    participations = list(instance["round_participations"])
    caps = [float(x) for x in instance["round_cap_multiples"]]
    anti_dilutions = list(instance["round_anti_dilutions"])

    # Round 1: Series A
    pre_a = pre_moneys[0]
    inv_a = investments[0]
    post_a = pre_a + inv_a
    pool_pct_a = pool_targets[0]

    denom_a = 1.0 - (inv_a / post_a) - pool_pct_a
    total_shares_post_a = founders_shares / denom_a
    pool_shares_a = pool_pct_a * total_shares_post_a
    pre_shares_a = founders_shares + pool_shares_a
    price_a = pre_a / pre_shares_a
    shares_a = inv_a / price_a

    cp_a = price_a
    cr_a = 1.0

    # Round 2: Series B
    pre_b = pre_moneys[1]
    inv_b = investments[1]
    post_b = pre_b + inv_b
    pool_topup_pct_b = pool_targets[1]

    prior_shares_b = founders_shares + pool_shares_a + shares_a
    if pool_topup_pct_b > 0.0:
        denom_b = 1.0 - (inv_b / post_b) - pool_topup_pct_b
        total_shares_post_b = prior_shares_b / denom_b
        delta_pool_b = pool_topup_pct_b * total_shares_post_b
    else:
        delta_pool_b = 0.0

    pool_shares_b = pool_shares_a + delta_pool_b
    pre_shares_b = prior_shares_b + delta_pool_b
    price_b = pre_b / pre_shares_b
    shares_b = inv_b / price_b

    if price_b < cp_a - 1e-9:
        cp_a = compute_anti_dilution_price(
            cp_a, price_b, inv_b, pre_shares_b, founders_shares + shares_a, anti_dilutions[1]
        )
        cr_a = price_a / cp_a

    cp_b = price_b
    cr_b = 1.0

    # Round 3: Series C
    pre_c = pre_moneys[2]
    inv_c = investments[2]
    post_c = pre_c + inv_c
    pool_topup_pct_c = pool_targets[2]

    prior_shares_c = founders_shares + pool_shares_b + shares_a + shares_b
    if pool_topup_pct_c > 0.0:
        denom_c = 1.0 - (inv_c / post_c) - pool_topup_pct_c
        total_shares_post_c = prior_shares_c / denom_c
        delta_pool_c = pool_topup_pct_c * total_shares_post_c
    else:
        delta_pool_c = 0.0

    pool_shares_c = pool_shares_b + delta_pool_c
    pre_shares_c = prior_shares_c + delta_pool_c
    price_c = pre_c / pre_shares_c
    shares_c = inv_c / price_c

    if price_c < cp_a - 1e-9:
        cp_a = compute_anti_dilution_price(
            cp_a, price_c, inv_c, pre_shares_c, founders_shares + shares_a + shares_b, anti_dilutions[2]
        )
        cr_a = price_a / cp_a

    if price_c < cp_b - 1e-9:
        cp_b = compute_anti_dilution_price(
            cp_b, price_c, inv_c, pre_shares_c, founders_shares + shares_a + shares_b, anti_dilutions[2]
        )
        cr_b = price_b / cp_b

    cp_c = price_c
    cr_c = 1.0

    total_shares_final = founders_shares + pool_shares_c + shares_a + shares_b + shares_c

    return {
        "founders_shares": founders_shares,
        "options_shares": pool_shares_c,
        "series_a": {
            "shares": shares_a,
            "issue_price": price_a,
            "conversion_price": cp_a,
            "conversion_ratio": cr_a,
            "investment": inv_a,
            "liquidation_multiple": multiples[0],
            "participation": participations[0],
            "cap_multiple": caps[0],
        },
        "series_b": {
            "shares": shares_b,
            "issue_price": price_b,
            "conversion_price": cp_b,
            "conversion_ratio": cr_b,
            "investment": inv_b,
            "liquidation_multiple": multiples[1],
            "participation": participations[1],
            "cap_multiple": caps[1],
        },
        "series_c": {
            "shares": shares_c,
            "issue_price": price_c,
            "conversion_price": cp_c,
            "conversion_ratio": cr_c,
            "investment": inv_c,
            "liquidation_multiple": multiples[2],
            "participation": participations[2],
            "cap_multiple": caps[2],
        },
        "total_shares": total_shares_final,
    }


def _evaluate_candidate_payoff(
    exit_value: float,
    cap_table: dict[str, Any],
    seniority: str,
    converts: dict[str, bool],
) -> dict[str, float]:
    if exit_value <= 1e-12:
        return {"founders": 0.0, "options": 0.0, "series_a": 0.0, "series_b": 0.0, "series_c": 0.0}

    series_keys = ["series_c", "series_b", "series_a"]
    pref_needed: dict[str, float] = {}
    for key in series_keys:
        info = cap_table[key]
        pref_needed[key] = info["liquidation_multiple"] * info["investment"] if not converts[key] else 0.0

    total_pref = sum(pref_needed.values())
    pref_paid = {k: 0.0 for k in series_keys}

    if seniority == "pari_passu":
        if total_pref > 0.0:
            pref_pool = min(exit_value, total_pref)
            for key in series_keys:
                pref_paid[key] = pref_pool * (pref_needed[key] / total_pref)
            rem_val = max(0.0, exit_value - pref_pool)
        else:
            rem_val = exit_value
    else:
        rem_val = exit_value
        for key in series_keys:
            if pref_needed[key] > 0.0:
                p = min(rem_val, pref_needed[key])
                pref_paid[key] = p
                rem_val = max(0.0, rem_val - p)

    founders_sh = float(cap_table["founders_shares"])
    options_sh = float(cap_table["options_shares"])
    cap_limits: dict[str, float] = {}
    effective_shares: dict[str, float] = {
        "founders": founders_sh,
        "options": options_sh,
    }

    for key in series_keys:
        info = cap_table[key]
        if converts[key] or info["participation"] == "participating":
            effective_shares[key] = float(info["shares"]) * float(info["conversion_ratio"])
            cap_limits[key] = float("inf")
        elif info["participation"] == "capped":
            effective_shares[key] = float(info["shares"]) * float(info["conversion_ratio"])
            cap_max = info["cap_multiple"] * info["investment"]
            cap_limits[key] = max(0.0, cap_max - pref_paid[key])

    residual_paid: dict[str, float] = {k: 0.0 for k in effective_shares}
    unallocated = rem_val
    active_keys = set(effective_shares.keys())

    while unallocated > 1e-9 and active_keys:
        active_shares = sum(effective_shares[k] for k in active_keys)
        if active_shares <= 1e-12:
            break
        pro_rata = {k: unallocated * (effective_shares[k] / active_shares) for k in active_keys}
        hits = [k for k in active_keys if residual_paid[k] + pro_rata[k] >= cap_limits.get(k, float("inf")) - 1e-9]

        if not hits:
            for k in active_keys:
                residual_paid[k] += pro_rata[k]
            unallocated = 0.0
            break
        else:
            fraction_to_cap = {}
            for k in hits:
                needed = max(0.0, cap_limits[k] - residual_paid[k])
                fraction_to_cap[k] = needed / pro_rata[k] if pro_rata[k] > 0 else 0.0
            min_frac = min(fraction_to_cap.values())
            min_frac = max(0.0, min(1.0, min_frac))

            allocated_step = 0.0
            for k in active_keys:
                step = pro_rata[k] * min_frac
                residual_paid[k] += step
                allocated_step += step
            unallocated = max(0.0, unallocated - allocated_step)
            for k in list(active_keys):
                if residual_paid[k] >= cap_limits.get(k, float("inf")) - 1e-8:
                    active_keys.remove(k)

    if unallocated > 1e-9:
        base_keys = [k for k in ["founders", "options"] if k in effective_shares]
        base_shares = sum(effective_shares[k] for k in base_keys)
        if base_shares > 0.0:
            for k in base_keys:
                residual_paid[k] += unallocated * (effective_shares[k] / base_shares)

    return {
        "founders": residual_paid.get("founders", 0.0),
        "options": residual_paid.get("options", 0.0),
        "series_a": pref_paid["series_a"] + residual_paid.get("series_a", 0.0),
        "series_b": pref_paid["series_b"] + residual_paid.get("series_b", 0.0),
        "series_c": pref_paid["series_c"] + residual_paid.get("series_c", 0.0),
    }


def calculate_exit_waterfall(
    exit_value: float,
    cap_table: dict[str, Any],
    seniority: str = "standard",
) -> dict[str, float]:
    if exit_value <= 1e-12:
        return {"founders": 0.0, "options": 0.0, "series_a": 0.0, "series_b": 0.0, "series_c": 0.0}

    series_keys = ["series_a", "series_b", "series_c"]
    stable_configs = []
    for choices in itertools.product([False, True], repeat=3):
        config = {k: c for k, c in zip(series_keys, choices, strict=False)}
        pay = _evaluate_candidate_payoff(exit_value, cap_table, seniority, config)
        is_stable = True
        for key in series_keys:
            dev_config = dict(config)
            dev_config[key] = not config[key]
            dev_pay = _evaluate_candidate_payoff(exit_value, cap_table, seniority, dev_config)
            if dev_pay[key] > pay[key] + 1e-6:
                is_stable = False
                break
        if is_stable:
            stable_configs.append((config, pay))

    if stable_configs:
        _best_config, best_payoffs = max(stable_configs, key=lambda item: sum(item[1][k] for k in series_keys))
    else:
        all_evals = []
        for choices in itertools.product([False, True], repeat=3):
            config = {k: c for k, c in zip(series_keys, choices, strict=False)}
            pay = _evaluate_candidate_payoff(exit_value, cap_table, seniority, config)
            all_evals.append((config, pay))
        _best_config, best_payoffs = max(all_evals, key=lambda item: sum(item[1][k] for k in series_keys))

    tot = sum(best_payoffs.values())
    if abs(tot - exit_value) > 1e-6 and tot > 0:
        factor = exit_value / tot
        best_payoffs = {k: v * factor for k, v in best_payoffs.items()}

    return best_payoffs


def evaluate_term_sheet(instance: dict[str, Any]) -> dict[str, Any]:
    cap_table = build_cap_table(instance)
    seniority = instance.get("seniority", "standard")
    exit_values = instance.get("test_exit_values", [])
    waterfall_results = []
    for ev in exit_values:
        payoffs = calculate_exit_waterfall(float(ev), cap_table, seniority=seniority)
        waterfall_results.append({"exit_value": float(ev), "payoffs": payoffs})
    return {"cap_table": cap_table, "waterfalls": waterfall_results}
