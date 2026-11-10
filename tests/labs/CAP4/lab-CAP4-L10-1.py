"""Lab CAP4-L10-1: Dissertation Defense Adversarial Attack Resilience Diagnostic.

Evaluates oral defense committee examination readiness by simulating five hostile attack vectors:
look-ahead restatement bias, weak instrument inflation, microcap leverage contamination,
turnover transaction drag, and post-sample structural break decay.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    np.random.seed(42)

    # 1. Baseline reported thesis findings
    reported_alpha_annual = 0.0480  # 4.80% annual long-short alpha
    reported_t_stat = 3.65
    annual_turnover = 3.20  # 320% one-way turnover per year

    # 2. Defense Committee Attack Vector 1: Look-ahead bias in accounting restatements
    # Compustat point-in-time vs restated data removes ~35 bps
    look_ahead_penalty = 0.0035

    # 3. Defense Committee Attack Vector 2: Microcap concentration & liquidity
    # Excluding bottom 20% NYSE size percentile reduces spread by ~65 bps
    microcap_penalty = 0.0065

    # 4. Defense Committee Attack Vector 3: Transaction costs & price impact
    # Novy-Marx & Velikov (2015) effective trading costs: ~15 bps per turn
    effective_tcost_per_turn = 0.0015
    turnover_drag = annual_turnover * effective_tcost_per_turn  # 48 bps

    # 5. Defense Committee Attack Vector 4: Post-publication / Out-of-sample decay
    # McLean & Pontiff (2016) find ~50% decay out of sample
    # Stress-test under 35% exogenous structural decay
    oos_decay_rate = 0.35

    # 3. Compute Net Economic Alpha under Cumulative Hostile Committee Attacks
    pre_decay_net_alpha = reported_alpha_annual - look_ahead_penalty - microcap_penalty - turnover_drag
    stressed_net_alpha = pre_decay_net_alpha * (1.0 - oos_decay_rate)

    # 4. Break-even transaction cost (cost per turn where net alpha hits zero)
    # 0 = (reported_alpha - look_ahead - microcap) * (1 - decay) - turnover * tcost
    unhedged_margin = reported_alpha_annual - look_ahead_penalty - microcap_penalty
    breakeven_cost_bps = (unhedged_margin / annual_turnover) * 10000.0

    # 5. Committee Defense Resilience Index (0 to 100)
    # Scaled by surviving alpha and t-statistic resilience
    t_stat_stressed = reported_t_stat * (stressed_net_alpha / reported_alpha_annual)
    resilience_index = float(np.clip(100.0 * (stressed_net_alpha / 0.0200) * (t_stat_stressed / 2.0), 0.0, 100.0))
    defense_pass = bool(resilience_index >= 50.0 and stressed_net_alpha > 0.015)

    print(f"Reported Gross Alpha: {reported_alpha_annual * 100:.2f}% (t={reported_t_stat:.2f})")
    print(f"Look-Ahead Bias Drag: {look_ahead_penalty * 10000:.1f} bps")
    print(f"Microcap Exclusion Drag: {microcap_penalty * 10000:.1f} bps")
    print(f"Annual Turnover Drag: {turnover_drag * 10000:.1f} bps")
    print(f"Stressed Net Alpha: {stressed_net_alpha * 100:.2f}%")
    print(f"Break-Even Trading Cost: {breakeven_cost_bps:.1f} bps/turn")
    print(f"Stressed Defense t-Stat: {t_stat_stressed:.2f}")
    print(f"Defense Resilience Index: {resilience_index:.1f}")
    print(f"Dissertation Defense Passed: {defense_pass}")


main()
