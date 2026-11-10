"""Deterministic instance generator for AP4 Model Horse Race project."""

from __future__ import annotations

from typing import Any

import numpy as np

CC_PARAM_NAMES: tuple[str, ...] = ("g", "sigma", "phi", "gamma", "delta", "b_s", "pd_mean")

BY_PARAM_NAMES: tuple[str, ...] = (
    "mu",
    "rho",
    "phi_e",
    "sigma_bar",
    "nu",
    "sigma_w",
    "mu_d",
    "phi_d",
    "phi_u",
    "delta",
    "gamma",
    "psi",
    "kappa1",
    "a2_m",
    "pd_mean",
)

BR_PARAM_NAMES: tuple[str, ...] = ("g", "sigma", "sigma_d", "p_disaster", "b_mean", "b_div_mult", "delta", "gamma")

MOMENT_NAMES: tuple[str, ...] = (
    "mean_consumption_growth",
    "vol_consumption_growth",
    "ac1_consumption_growth",
    "mean_equity_premium",
    "vol_equity_return",
    "sharpe_ratio",
    "mean_risk_free_rate",
    "vol_risk_free_rate",
    "mean_log_pd",
    "vol_log_pd",
    "ac1_log_pd",
    "predictability_slope_1y",
)


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic calibration and target moment instance for a given seed.

    All array fields are float64 arrays ensuring strict byte-level determinism.
    """
    rng = np.random.default_rng(seed)

    t_len = 500

    # 1. Campbell-Cochrane (1999) external habit calibration
    cc_arr = np.array(
        [
            0.0189 + rng.uniform(-0.0005, 0.0005),  # g
            0.0150 + rng.uniform(-0.0004, 0.0004),  # sigma
            0.87 + rng.uniform(-0.008, 0.008),  # phi
            2.0,  # gamma
            0.89 + rng.uniform(-0.004, 0.004),  # delta
            0.48 + rng.uniform(-0.02, 0.02),  # b_s
            3.38,  # pd_mean
        ],
        dtype=np.float64,
    )

    # 2. Bansal-Yaron (2004) long-run risks calibration
    by_arr = np.array(
        [
            0.0180 + rng.uniform(-0.0005, 0.0005),  # mu
            0.979 + rng.uniform(-0.002, 0.002),  # rho
            0.044 + rng.uniform(-0.002, 0.002),  # phi_e
            0.015 + rng.uniform(-0.0005, 0.0005),  # sigma_bar
            0.987 + rng.uniform(-0.002, 0.002),  # nu
            0.0001,  # sigma_w
            0.0180 + rng.uniform(-0.0005, 0.0005),  # mu_d
            3.0 + rng.uniform(-0.05, 0.05),  # phi_d
            4.5 + rng.uniform(-0.08, 0.08),  # phi_u
            0.980 + rng.uniform(-0.002, 0.002),  # delta
            10.0,  # gamma
            1.5 + rng.uniform(-0.04, 0.04),  # psi
            0.96,  # kappa1
            -15.0,  # a2_m
            3.38,  # pd_mean
        ],
        dtype=np.float64,
    )

    # 3. Barro-Rietz (1988, 2006) rare disasters calibration
    br_arr = np.array(
        [
            0.025 + rng.uniform(-0.0005, 0.0005),  # g
            0.020 + rng.uniform(-0.0005, 0.0005),  # sigma
            0.050 + rng.uniform(-0.001, 0.001),  # sigma_d
            0.017 + rng.uniform(-0.0005, 0.0005),  # p_disaster
            0.29 + rng.uniform(-0.005, 0.005),  # b_mean
            1.5 + rng.uniform(-0.02, 0.02),  # b_div_mult
            0.970 + rng.uniform(-0.003, 0.003),  # delta
            4.0,  # gamma
        ],
        dtype=np.float64,
    )

    # 12 Target data moments
    targets_arr = np.array(
        [
            0.0189,  # mean_consumption_growth
            0.0325,  # vol_consumption_growth
            0.4500,  # ac1_consumption_growth
            0.0620,  # mean_equity_premium
            0.1940,  # vol_equity_return
            0.3200,  # sharpe_ratio
            0.0080,  # mean_risk_free_rate
            0.0540,  # vol_risk_free_rate
            3.3800,  # mean_log_pd
            0.4000,  # vol_log_pd
            0.8700,  # ac1_log_pd
            -0.1500,  # predictability_slope_1y
        ],
        dtype=np.float64,
    )

    weights_arr = np.array(
        [0.08, 0.08, 0.08, 0.12, 0.10, 0.10, 0.10, 0.08, 0.08, 0.06, 0.06, 0.06],
        dtype=np.float64,
    )

    return {
        "seed": seed,
        "t_len": t_len,
        "cc_params": cc_arr,
        "by_params": by_arr,
        "br_params": br_arr,
        "targets": targets_arr,
        "weights": weights_arr,
        "moment_names": list(MOMENT_NAMES),
    }
