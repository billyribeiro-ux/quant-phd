"""Starter template for Atlas A7: cross-sectional engine (atlas.cross_section).

Implement the required functions to pass the project test suite.
"""

from __future__ import annotations

from typing import NamedTuple

import numpy as np


class FMResult(NamedTuple):
    """Container for Fama-MacBeth cross-sectional estimation results."""

    premia: np.ndarray
    naive_se: np.ndarray
    shanken_se: np.ndarray
    t_stat_naive: np.ndarray
    t_stat_shanken: np.ndarray


class GRSResult(NamedTuple):
    """Container for Gibbons-Ross-Shanken (1989) test results."""

    stat: float
    p_value: float
    df_num: int
    df_denom: int


def apply_shumway_delisting(
    returns: np.ndarray,
    delist_codes: np.ndarray,
    delist_returns: np.ndarray,
    exchange_codes: np.ndarray,
) -> np.ndarray:
    """Adjust monthly returns for delisting events following Shumway (1997)."""
    raise NotImplementedError("apply_shumway_delisting is not implemented")


def compute_breakpoints(
    characteristics: np.ndarray,
    exchange_codes: np.ndarray,
    n_quantiles: int = 5,
    use_nyse_only: bool = True,
) -> np.ndarray:
    """Compute quantile breakpoint thresholds, optionally restricted to NYSE."""
    raise NotImplementedError("compute_breakpoints is not implemented")


def univariate_sort(
    returns: np.ndarray,
    signals: np.ndarray,
    market_caps: np.ndarray,
    exchange_codes: np.ndarray,
    n_quantiles: int = 5,
    use_nyse_only: bool = True,
    weighting: str = "value",
) -> dict[str, object]:
    """Sort cross-sectional assets into quantiles based on a single characteristic."""
    raise NotImplementedError("univariate_sort is not implemented")


def bivariate_sort(
    returns: np.ndarray,
    signal1: np.ndarray,
    signal2: np.ndarray,
    market_caps: np.ndarray,
    exchange_codes: np.ndarray,
    n_quantiles1: int = 2,
    n_quantiles2: int = 3,
    method: str = "independent",
    use_nyse_only: bool = True,
    weighting: str = "value",
) -> dict[str, object]:
    """Perform independent or conditional bivariate 2D portfolio sorts."""
    raise NotImplementedError("bivariate_sort is not implemented")


def fama_macbeth(
    excess_returns: np.ndarray,
    loadings: np.ndarray,
    factor_returns: np.ndarray | None = None,
) -> FMResult:
    """Execute two-pass Fama-MacBeth regressions with Shanken (1992) correction."""
    raise NotImplementedError("fama_macbeth is not implemented")


def grs_test(
    alphas: np.ndarray,
    residuals: np.ndarray,
    factor_returns: np.ndarray,
) -> GRSResult:
    """Compute the Gibbons-Ross-Shanken (1989) test statistic and p-value."""
    raise NotImplementedError("grs_test is not implemented")
