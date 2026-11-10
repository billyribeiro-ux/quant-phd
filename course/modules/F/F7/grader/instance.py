"""Deterministic instance generator for F7: Performance Evaluation & Skill.

Exposes make_instance(seed: int) -> dict[str, object] generating realistic multi-manager
institutional universes with systematic factors, return smoothing, nonlinear option payoffs,
and varying skill levels.
"""

from __future__ import annotations

import numpy as np


def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic 5-manager due-diligence dataset from a seed."""
    rng = np.random.default_rng(seed)
    n_months = 180  # 15 years of monthly track records
    burn = 2

    # 4 Systematic benchmark factors: Mkt-RF, SMB, HML, MOM
    mkt_all = rng.normal(0.0065, 0.045, size=n_months + burn)
    smb_all = rng.normal(0.0020, 0.030, size=n_months + burn)
    hml_all = rng.normal(0.0025, 0.032, size=n_months + burn)
    mom_all = rng.normal(0.0050, 0.040, size=n_months + burn)

    mkt = mkt_all[burn:]
    smb = smb_all[burn:]
    hml = hml_all[burn:]
    mom = mom_all[burn:]
    factors = np.column_stack([mkt, smb, hml, mom])

    mkt_demeaned_sq = (mkt - np.mean(mkt)) ** 2

    # Manager 1: AlphaStar Equity (Genuine skill, liquid equity long/short)
    # Positive alpha, moderate systematic betas, homoskedastic noise
    r1 = 0.0035 + 0.80 * mkt + 0.20 * smb - 0.10 * hml + 0.15 * mom + rng.normal(0.0, 0.018, size=n_months)

    # Manager 2: Harbor DirectLending (Illiquid private debt with return smoothing)
    # Stale valuations generate MA(2) smoothed returns
    r2_star = 0.0010 + 0.25 * mkt_all + rng.normal(0.0, 0.038, size=n_months + burn)
    th_harbor = np.array([0.55, 0.30, 0.15])
    r2 = np.zeros(n_months)
    for t in range(n_months):
        r2[t] = th_harbor[0] * r2_star[t + 2] + th_harbor[1] * r2_star[t + 1] + th_harbor[2] * r2_star[t]

    # Manager 3: Apex VolCarry (Short volatility / naked put seller; hidden tail risk)
    # Collects regular option premium but exhibits severe negative quadratic curvature
    r3 = 0.0090 + 0.40 * mkt - 6.0 * mkt_demeaned_sq + rng.normal(0.0, 0.014, size=n_months)

    # Manager 4: Beacon TrendCTA (Trend following / long straddle; convex payoff)
    # Generates convex positive gamma during large market swings
    r4 = 0.0015 + 0.05 * mkt + 4.5 * mkt_demeaned_sq + rng.normal(0.0, 0.022, size=n_months)

    # Manager 5: Crestline BetaChaser (Zero true alpha, disguised high market beta)
    r5 = 0.0000 + 1.15 * mkt + rng.normal(0.0, 0.012, size=n_months)

    manager_returns = np.column_stack([r1, r2, r3, r4, r5])
    manager_names = [
        "AlphaStar_Equity",
        "Harbor_DirectLending",
        "Apex_VolCarry",
        "Beacon_TrendCTA",
        "Crestline_BetaChaser",
    ]

    return {
        "seed": int(seed),
        "n_months": int(n_months),
        "factor_names": ["Mkt-RF", "SMB", "HML", "MOM"],
        "factors": factors,
        "mkt_excess": mkt,
        "manager_names": manager_names,
        "manager_returns": manager_returns,
    }
