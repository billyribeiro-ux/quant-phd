"""Grader instance generator for E9 Sovereign DSA and Fan Chart project.

Generates deterministic synthetic sovereign debt profiles and Monte Carlo trajectory panels.
Different seeds generate materially different debt levels, growth regimes, and risk distributions.
"""

from __future__ import annotations

import functools
import random

SOVEREIGN_NAMES = [
    "Republic of Meridiana",
    "Federation of Borealis",
    "Commonwealth of Pacifica",
    "Kingdom of Hesperia",
    "State of Eldoria",
    "Union of Austrasia",
    "Duchy of Valoria",
    "Republic of Solaria",
]


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic test instance for seed.

    Returns sovereign debt parameters, deterministic baseline paths,
    and a panel of simulated trajectories for fan chart testing.
    """
    rng = random.Random(seed)

    country = SOVEREIGN_NAMES[seed % len(SOVEREIGN_NAMES)]
    horizon = 10

    # Macroeconomic initial state
    b0 = round(0.65 + 0.50 * rng.random(), 4)  # 0.65 to 1.15
    debt_ceiling = round(b0 + 0.15 + 0.15 * rng.random(), 4)  # 15-30% above b0
    target_debt = round(b0 * (0.90 + 0.10 * rng.random()), 4)

    # Baseline paths across horizon
    base_r = 0.020 + 0.025 * rng.random()  # 2.0% to 4.5%
    base_g = 0.010 + 0.025 * rng.random()  # 1.0% to 3.5%
    base_s = -0.020 + 0.030 * rng.random()  # -2.0% to +1.0%

    r_path: list[float] = []
    g_path: list[float] = []
    s_path: list[float] = []

    r_curr = base_r
    g_curr = base_g
    s_curr = base_s

    for _ in range(horizon):
        r_curr = max(-0.01, r_curr + rng.gauss(0.0, 0.003))
        g_curr = max(-0.03, g_curr + rng.gauss(0.0, 0.004))
        s_curr = max(-0.05, min(0.05, s_curr + rng.gauss(0.0, 0.003)))

        r_path.append(round(r_curr, 6))
        g_path.append(round(g_curr, 6))
        s_path.append(round(s_curr, 6))

    # Monte Carlo trajectories (50 paths, horizon = 10 periods => 11 points each)
    n_mc_paths = 50
    mc_paths: list[list[float]] = []

    for _ in range(n_mc_paths):
        path = [b0]
        b_sim = b0
        for t in range(horizon):
            r_t = r_path[t] + rng.gauss(0.0, 0.015)
            g_t = g_path[t] + rng.gauss(0.0, 0.020)
            s_t = s_path[t] + rng.gauss(0.0, 0.010)

            # Exact step
            b_sim = ((1.0 + r_t) / (1.0 + g_t)) * b_sim - s_t
            path.append(round(b_sim, 6))
        mc_paths.append(path)

    return {
        "seed": seed,
        "country": country,
        "b0": b0,
        "horizon": horizon,
        "target_debt": target_debt,
        "debt_ceiling": debt_ceiling,
        "r_path": r_path,
        "g_path": g_path,
        "s_path": s_path,
        "mc_paths": mc_paths,
    }
