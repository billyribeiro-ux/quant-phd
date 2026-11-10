"""Deterministic instance generator for AC3 project: PEAD replication.

Generates simulated quarterly earnings histories, current quarter earnings, and post-announcement
daily returns for pre-2000 and post-2000 regimes. Deterministic for a given seed, distinct across seeds.
"""

from __future__ import annotations

import json
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic simulated PEAD replication instance from an integer seed."""
    rng = random.Random(seed)

    # 1. Generate 30 firms for SUE calculation and decile sorting
    n_firms = 30
    firms: list[dict[str, Any]] = []

    for i in range(n_firms):
        firm_id = f"F{i + 1:02d}"
        scale = 10.0 + rng.uniform(0.0, 80.0)
        drift = rng.uniform(0.02, 0.08) * scale
        sigma = rng.uniform(0.05, 0.15) * scale

        # 8 quarters of history (quarters 0..7)
        history: list[float] = [round(scale * (1.0 + 0.05 * q), 4) for q in range(4)]
        for t in range(4, 8):
            eps = rng.gauss(0.0, sigma)
            val = round(history[t - 4] + drift + eps, 4)
            history.append(val)

        # Current quarter realization (quarter 8)
        # Random surprise: standardized surprise in [-3, +3]
        sue_draw = rng.gauss(0.0, 1.2)
        diffs = [history[t] - history[t - 4] for t in range(4, 8)]
        d_mean = sum(diffs) / len(diffs)
        errors = [d - d_mean for d in diffs]
        var = sum(e**2 for e in errors) / (len(errors) - 1)
        s_dev = max(0.01, var**0.5)

        expected = history[4] + d_mean
        current = round(expected + sue_draw * s_dev, 4)

        firms.append(
            {
                "firm_id": firm_id,
                "history": history,
                "current": current,
            }
        )

    # 2. Pre-2000 announcements (pronounced drift, lower liquidity / higher spread)
    # 50 simulated announcement events across 10 deciles (5 per decile)
    pre_announcements: list[dict[str, Any]] = []
    post_announcements: list[dict[str, Any]] = []

    # Total days = 80 (announcement at day 10, holding period days [12, 70], i.e. +2 to +60)
    total_days = 80
    announcement_day = 10

    for d in range(1, 11):
        for rep in range(5):
            firm_id = f"PRE_D{d:02d}_{rep}"
            # Pre-2000 drift slope: strong drift ~ 0.8% per decile step
            # Decile 1 has -3.6% CAR[+2, +60], Decile 10 has +3.6% CAR[+2, +60] -> ~7.2% spread
            drift_target = (d - 5.5) * 0.008 + rng.gauss(0.0, 0.001)
            # Immediate announcement jump at day 10: ~ 0.5% per decile step
            jump_target = (d - 5.5) * 0.005 + rng.gauss(0.0, 0.002)

            rets: list[float] = []
            for t in range(total_days):
                if t == announcement_day:
                    ret = jump_target + rng.gauss(0.0, 0.002)
                elif announcement_day + 2 <= t <= announcement_day + 60:
                    daily_drift = drift_target / 59.0
                    ret = daily_drift + rng.gauss(0.0, 0.001)
                else:
                    ret = rng.gauss(0.0, 0.001)
                rets.append(round(ret, 6))

            pre_announcements.append(
                {
                    "firm_id": firm_id,
                    "decile": d,
                    "daily_returns": rets,
                    "announcement_day": announcement_day,
                }
            )

    # 3. Post-2000 announcements (compressed drift, higher efficiency)
    for d in range(1, 11):
        for rep in range(5):
            firm_id = f"POST_D{d:02d}_{rep}"
            # Post-2000 drift slope: compressed drift ~ 0.22% per decile step -> ~2.0% gross spread
            drift_target = (d - 5.5) * 0.0022 + rng.gauss(0.0, 0.001)
            # Faster immediate announcement jump at day 10: ~ 0.8% per decile step
            jump_target = (d - 5.5) * 0.008 + rng.gauss(0.0, 0.002)

            rets = []
            for t in range(total_days):
                if t == announcement_day:
                    ret = jump_target + rng.gauss(0.0, 0.002)
                elif announcement_day + 2 <= t <= announcement_day + 60:
                    daily_drift = drift_target / 59.0
                    ret = daily_drift + rng.gauss(0.0, 0.001)
                else:
                    ret = rng.gauss(0.0, 0.001)
                rets.append(round(ret, 6))

            post_announcements.append(
                {
                    "firm_id": firm_id,
                    "decile": d,
                    "daily_returns": rets,
                    "announcement_day": announcement_day,
                }
            )

    cost_bps = round(15.0 + rng.uniform(0.0, 15.0), 1)

    case = {
        "firms": firms,
        "pre_2000_announcements": pre_announcements,
        "post_2000_announcements": post_announcements,
        "cost_bps": cost_bps,
        "holding_period": [2, 60],
    }

    return {
        "seed": int(seed),
        "label": f"SIMULATED PEAD replication panel, seed {int(seed)}",
        "payload": json.dumps(case, sort_keys=True),
    }
