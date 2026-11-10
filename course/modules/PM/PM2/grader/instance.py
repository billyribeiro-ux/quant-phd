"""Deterministic instance generator for PM2: Venture Capital (Term-Sheet Economics).

Generates realistic 3-round venture capital investment sequences (Series A, B, and C)
with varied valuations, option pool expansions, anti-dilution protections, liquidation
preferences, and seniority structures.
"""

from __future__ import annotations

from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic 3-round cap table and waterfall instance."""
    founders_shares = 10_000_000

    # Series A (Foundational institutional round)
    pre_a = float(12_000_000 + (seed % 7) * 1_000_000)
    inv_a = float(4_000_000 + (seed % 5) * 500_000)
    pool_a = 0.15  # Standard 15% post-money option pool requirement
    part_a_choices = ["non_participating", "participating", "capped"]
    part_a = part_a_choices[seed % 3]
    cap_a = 2.5 if part_a == "capped" else 0.0

    # Series B (Growth round; down-round occurs when seed % 4 == 1)
    is_down_b = seed % 4 == 1
    pre_b = float(pre_a * 0.75) if is_down_b else float((pre_a + inv_a) * 1.5 + (seed % 4) * 2_000_000)
    inv_b = float(8_000_000 + (seed % 6) * 1_000_000)
    pool_b = 0.05 if (seed % 2 == 0) else 0.0  # 5% top-up or 0%
    ad_choices = ["broad_based", "narrow_based", "full_ratchet"]
    ad_b = ad_choices[(seed // 3) % 3]
    part_b_choices = ["non_participating", "participating", "non_participating"]
    part_b = part_b_choices[seed % 3]
    cap_b = 3.0 if part_b == "capped" else 0.0

    # Series C (Late stage / expansion; down-round when seed % 5 == 2)
    is_down_c = seed % 5 == 2
    pre_c = float(pre_b * 0.70) if is_down_c else float((pre_b + inv_b) * 1.4 + (seed % 5) * 3_000_000)
    inv_c = float(15_000_000 + (seed % 7) * 2_000_000)
    pool_c = 0.02 if (seed % 3 == 0) else 0.0
    ad_c = ad_choices[(seed // 2) % 3]
    part_c = "non_participating"

    seniority_choice = "pari_passu" if (seed % 4 == 3) else "standard"

    total_inv = inv_a + inv_b + inv_c
    exit_values = [
        0.0,
        round(total_inv * 0.25, 2),
        round(total_inv * 0.75, 2),
        round(total_inv * 1.0, 2),
        round(total_inv * 1.5, 2),
        round(total_inv * 3.0, 2),
        round(total_inv * 6.0, 2),
        round(total_inv * 12.0, 2),
    ]

    return {
        "seed": seed,
        "founders_shares": founders_shares,
        "seniority": seniority_choice,
        "round_names": ["Series A", "Series B", "Series C"],
        "round_pre_money": [pre_a, pre_b, pre_c],
        "round_investments": [inv_a, inv_b, inv_c],
        "round_pools": [pool_a, pool_b, pool_c],
        "round_liquidation_multiples": [1.0, 1.0, 1.0],
        "round_participations": [part_a, part_b, part_c],
        "round_cap_multiples": [cap_a, cap_b, 0.0],
        "round_anti_dilutions": ["broad_based", ad_b, ad_c],
        "test_exit_values": exit_values,
    }
