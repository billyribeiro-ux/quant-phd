"""Instance generator for the CR3 credit cycle & macro-credit autograder.

SIMULATED: generates synthetic micro-level bond panels, credit market sentiment series,
macroeconomic recession indicators, and leveraged loan balance sheets for testing
the CR3 quantitative credit engine. Labelled SIMULATED per BLUEPRINT §5.3.

Deterministic per seed; valid by construction.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given integer seed."""
    rng = np.random.default_rng(seed)

    # 1. Micro-level corporate bond panel for GZ spread & EBP decomposition
    n_bonds = int(rng.integers(35, 55))
    durations: list[float] = []
    coupons: list[float] = []
    amounts: list[float] = []
    edfs: list[float] = []
    industries: list[int] = []
    spreads_bps: list[float] = []

    # Latent macro credit conditions for this seed
    macro_ebp_shock = float(rng.normal(25.0, 15.0))  # bps of excess bond premium
    true_beta_dur = 0.04
    true_beta_coup = 2.5
    true_beta_amt = -0.08
    true_beta_edf = 0.45

    for _ in range(n_bonds):
        dur = float(round(rng.uniform(1.5, 12.0), 2))
        coup = float(round(rng.uniform(0.025, 0.085), 4))
        amt = float(round(rng.uniform(150.0, 1200.0), 1))
        # Merton EDF between 0.001 (10 bp) and 0.06 (600 bp)
        edf = float(round(rng.uniform(0.0015, 0.045), 5))
        ind = int(rng.integers(0, 4))
        ind_effect = [0.0, 0.08, -0.05, 0.12][ind]

        # Log spread model + idiosyncratic noise
        log_pred = (
            3.8
            + true_beta_dur * (dur - 5.0)
            + true_beta_coup * (coup - 0.05)
            + true_beta_amt * (math.log(amt) - 6.0)
            + true_beta_edf * (math.log(edf) - math.log(0.01))
            + ind_effect
        )
        idio_noise = float(rng.normal(0.0, 0.15))
        # Spread with macro EBP premium added
        spread = float(math.exp(log_pred + idio_noise) + macro_ebp_shock)
        spread = max(25.0, round(spread, 2))

        durations.append(dur)
        coupons.append(coup)
        amounts.append(amt)
        edfs.append(edf)
        industries.append(ind)
        spreads_bps.append(spread)

    # 2. Time series for Credit Market Sentiment & Reversals (T = 48 quarters)
    t_quarters = 48
    # High yield issuance share: mean 0.22, range ~0.08 to 0.40
    hy_raw = np.zeros(t_quarters, dtype=np.float64)
    spread_raw = np.zeros(t_quarters, dtype=np.float64)
    ebp_raw = np.zeros(t_quarters, dtype=np.float64)

    # Autoregressive credit cycle state
    state = float(rng.normal(0.0, 1.0))
    for t in range(t_quarters):
        state = 0.75 * state + float(rng.normal(0.0, 0.65))
        hy_val = 0.22 + 0.08 * state + float(rng.normal(0.0, 0.03))
        hy_raw[t] = max(0.05, min(0.50, hy_val))

        # When sentiment is high (state > 0), spreads compress and EBP is negative
        spr_val = 180.0 - 55.0 * state + float(rng.normal(0.0, 18.0))
        spread_raw[t] = max(50.0, spr_val)

        ebp_val = -30.0 * state + float(rng.normal(0.0, 12.0))
        ebp_raw[t] = ebp_val

    weights = [0.35, 0.35, 0.30]

    # 3. Macro recession time series (T = 64 quarters)
    t_macro = 64
    term_spreads = np.zeros(t_macro, dtype=np.float64)
    credit_indicators = np.zeros(t_macro, dtype=np.float64)
    recessions = np.zeros(t_macro, dtype=np.int64)

    macro_cycle = float(rng.normal(0.0, 1.0))
    for t in range(t_macro):
        macro_cycle = 0.80 * macro_cycle + float(rng.normal(0.0, 0.60))
        # Inverted term spread precedes recession
        ts_val = 1.4 - 1.1 * macro_cycle + float(rng.normal(0.0, 0.40))
        term_spreads[t] = round(float(ts_val), 3)

        # Elevated EBP / credit distress
        ci_val = 0.8 * macro_cycle + float(rng.normal(0.0, 0.45))
        credit_indicators[t] = round(float(ci_val), 3)

        # Recession probability driven by inverted TS and high credit distress
        prob_rec = 1.0 / (1.0 + math.exp(-(-2.2 + 1.2 * ci_val - 1.4 * ts_val)))
        recessions[t] = 1 if rng.uniform(0.0, 1.0) < prob_rec else 0

    # Ensure at least 5 recessions and 10 non-recessions for identification
    if np.sum(recessions) < 5:
        recessions[rng.choice(np.where(recessions == 0)[0], size=5, replace=False)] = 1
    if np.sum(recessions == 0) < 10:
        recessions[rng.choice(np.where(recessions == 1)[0], size=10, replace=False)] = 0

    # Out-of-sample evaluation data
    eval_n = 40
    eval_true = [int(rng.choice([0, 1], p=[0.75, 0.25])) for _ in range(eval_n)]
    eval_prob = [
        float(
            max(
                0.01,
                min(
                    0.99,
                    0.65 * y + rng.normal(0.20, 0.15) if y == 1 else 0.15 * y + rng.normal(0.18, 0.12),
                ),
            )
        )
        for y in eval_true
    ]

    # 4. Leveraged loan balance sheet parameters
    loan_debt = float(round(rng.uniform(300.0, 800.0), 1))
    loan_ebitda = float(round(rng.uniform(50.0, 120.0), 1))
    loan_addback = float(round(rng.choice([0.15, 0.25, 0.35, 0.45]), 2))
    loan_senior_share = float(round(rng.uniform(0.65, 0.85), 2))
    loan_cov_lite = bool(rng.choice([True, False]))
    loan_distress = float(round(rng.uniform(0.25, 0.60), 2))

    return {
        "bond_spread_bps": spreads_bps,
        "bond_duration": durations,
        "bond_coupon": coupons,
        "bond_amount_outstanding": amounts,
        "bond_merton_edf": edfs,
        "bond_industry_id": industries,
        "hy_issuance_share": [round(float(x), 4) for x in hy_raw],
        "credit_spreads": [round(float(x), 2) for x in spread_raw],
        "ebp": [round(float(x), 2) for x in ebp_raw],
        "weights": weights,
        "horizon_steps": int(rng.choice([2, 4, 6])),
        "term_spreads": [float(x) for x in term_spreads],
        "credit_indicators": [float(x) for x in credit_indicators],
        "recession_flags": [int(x) for x in recessions],
        "eval_true": eval_true,
        "eval_prob": eval_prob,
        "loan_debt": loan_debt,
        "loan_ebitda": loan_ebitda,
        "loan_addback": loan_addback,
        "loan_senior_share": loan_senior_share,
        "loan_cov_lite": loan_cov_lite,
        "loan_distress": loan_distress,
    }
