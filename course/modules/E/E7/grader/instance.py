"""Per-learner instances for the E7 Monetary-Shock Identification project.

make_instance(seed) is deterministic. It generates a synthetic macroeconomic panel with:
1. FOMC meeting announcement dates, pre- and post-announcement Fed funds futures rates,
   meeting day of month d, and days in month M.
2. Monthly macroeconomic time series:
   - Output gap / IP growth: y_t
   - CPI inflation: pi_t
   - 2-year Treasury yield: y2_t
   - 10-year Treasury yield: y10_t
   - Excess bond premium / credit spread: ebp_t
3. True underlying structural monetary shock, alongside:
   - Staff Greenbook forecast revisions for Romer-Romer narrative filtering
   - Market-based high-frequency surprises with plausible microstructure noise
"""

from __future__ import annotations

import json
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic macroeconomic time series and FOMC announcement instance."""
    rng = random.Random(f"E7-monetary-shock/{int(seed)}")

    n_months = 180  # 15 years of monthly data
    n_announcements = 120  # 8 meetings per year on average

    # 1. Generate FOMC meeting announcements
    announcements: list[dict[str, Any]] = []
    for i in range(n_announcements):
        month_idx = int(i * (n_months / n_announcements))
        day = rng.randint(6, 26)
        days_in_month = rng.choice([30, 31]) if month_idx % 2 == 0 else 30

        # Underlying true policy innovation (in basis points)
        true_innovation_bps = rng.gauss(0.0, 8.0)
        base_rate = round(rng.uniform(1.2, 4.8), 3)

        # Scale factor per Kuttner (2001): Delta f = ( (M - d) / M ) * Delta i_u
        scale = (days_in_month - day) / float(days_in_month)
        futures_jump_bps = true_innovation_bps * scale + rng.gauss(0.0, 0.3)

        f_pre = base_rate
        f_post = round(base_rate + futures_jump_bps / 100.0, 4)

        announcements.append(
            {
                "meeting_id": f"FOMC-{month_idx:03d}",
                "month_index": month_idx,
                "day": day,
                "days_in_month": days_in_month,
                "f_pre": f_pre,
                "f_post": f_post,
                "true_shock_bps": round(true_innovation_bps, 3),
            }
        )

    # 2. Simulate monthly macroeconomic series and narrative Greenbook forecasts
    shock_hf = [0.0] * n_months
    for a in announcements:
        m = a["month_index"]
        d, m_days = a["day"], a["days_in_month"]
        jump = (a["f_post"] - a["f_pre"]) * 100.0
        shock_hf[m] += jump * (m_days / float(m_days - d))

    shock_narrative = [0.0] * n_months
    for t in range(n_months):
        gb_revision = rng.gauss(0.0, 0.25)
        shock_narrative[t] = shock_hf[t] * 0.85 + rng.gauss(0.0, 2.5) - 1.2 * gb_revision

    y = [0.0] * n_months
    pi = [0.0] * n_months
    y2 = [0.0] * n_months
    ebp = [0.0] * n_months

    y[0] = rng.gauss(0.0, 0.2)
    pi[0] = rng.gauss(2.0, 0.2)
    y2[0] = rng.gauss(3.0, 0.2)
    ebp[0] = rng.gauss(0.8, 0.1)

    for t in range(1, n_months):
        m_shock = shock_hf[t - 1] / 100.0
        y[t] = 0.70 * y[t - 1] - 1.80 * m_shock + rng.gauss(0.0, 0.15)
        pi[t] = 0.80 * pi[t - 1] + 0.12 * y[t - 1] - 0.40 * m_shock + rng.gauss(0.0, 0.15)
        y2[t] = 0.85 * y2[t - 1] + 0.65 * (shock_hf[t] / 100.0) + 0.15 * pi[t] + rng.gauss(0.0, 0.10)
        ebp[t] = 0.65 * ebp[t - 1] + 0.30 * (shock_hf[t] / 100.0) - 0.10 * y[t] + rng.gauss(0.0, 0.08)

    payload = {
        "seed": int(seed),
        "n_months": n_months,
        "announcements": announcements,
        "shock_hf": shock_hf,
        "shock_narrative": shock_narrative,
        "output_gap": y,
        "inflation": pi,
        "yield_2y": y2,
        "credit_spread": ebp,
        "max_horizon": 12,
        "lags": 2,
    }

    return {
        "seed": int(seed),
        "label": f"SIMULATED monetary surprise & macro panel, seed {seed}",
        "payload": json.dumps(payload),
    }
