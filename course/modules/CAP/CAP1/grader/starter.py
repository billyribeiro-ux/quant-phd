"""Starter stub for CAP1 autograded replication package.

Implement each function according to the specification and replication methodology.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class RegressionResult:
    """Stores estimation results for linear factor regressions."""

    params: NDArray[np.float64]
    bse: NDArray[np.float64]
    tvalues: NDArray[np.float64]
    pvalues: NDArray[np.float64]
    resid: NDArray[np.float64]
    cov: NDArray[np.float64]
    n_obs: int
    r_squared: float


def apply_share_code_filter(
    permnos: NDArray[np.int64 | np.int32],
    shrcd: NDArray[np.int64 | np.int32],
    exchcd: NDArray[np.int64 | np.int32],
    valid_shrcd: Sequence[int] = (10, 11),
    valid_exchcd: Sequence[int] = (1, 2, 3),
) -> NDArray[np.bool_]:
    """Filter stocks for ordinary US common shares on major exchanges."""
    raise NotImplementedError("Implement apply_share_code_filter")


def apply_delisting_adjustment(
    ret: NDArray[np.float64],
    dlret: NDArray[np.float64],
    dlstcd: NDArray[np.int64 | np.int32],
    exchcd: NDArray[np.int64 | np.int32],
    default_nyse_ret: float = -0.30,
    default_nasdaq_ret: float = -0.55,
) -> NDArray[np.float64]:
    """Apply Shumway (1997) delisting return adjustments."""
    raise NotImplementedError("Implement apply_delisting_adjustment")


def winsorize_cross_section(
    values: NDArray[np.float64],
    dates: NDArray[np.int64 | np.int32],
    lower_quantile: float = 0.01,
    upper_quantile: float = 0.99,
) -> NDArray[np.float64]:
    """Winsorize values cross-sectionally for each date separately."""
    raise NotImplementedError("Implement winsorize_cross_section")


def form_sorted_portfolios(
    signal: NDArray[np.float64],
    ret: NDArray[np.float64],
    me_lag: NDArray[np.float64],
    dates: NDArray[np.int64 | np.int32],
    n_portfolios: int = 5,
    weighting: str = "vw",
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Sort stocks into n_portfolios by signal each month and compute portfolio returns."""
    raise NotImplementedError("Implement form_sorted_portfolios")


def estimate_regression(
    y: NDArray[np.float64],
    x_mat: NDArray[np.float64],
    method: str = "ols",
    cluster_entity: NDArray[np.int64 | np.int32] | None = None,
    cluster_time: NDArray[np.int64 | np.int32] | None = None,
    nw_lags: int = 0,
) -> RegressionResult:
    """Estimate linear regression with specified covariance estimator."""
    raise NotImplementedError("Implement estimate_regression")


def decompose_replication_divergence(
    stage_estimates: dict[str, float],
) -> dict[str, float]:
    """Decompose total empirical divergence into sequential stage contributions."""
    raise NotImplementedError("Implement decompose_replication_divergence")


def verify_manifest(
    file_hashes: dict[str, str],
    actual_data: dict[str, bytes],
) -> bool:
    """Verify cryptographic integrity of replication package data and outputs."""
    raise NotImplementedError("Implement verify_manifest")
