"""Starter template for AP7 Sentiment-Index Replication.

Students implement proxy standardization, macroeconomic orthogonalization,
principal component extraction with anchor sign normalization, Newey-West HAC
inference, and cross-sectional sentiment asymmetry testing.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def standardize_proxies(raw_proxies: np.ndarray) -> np.ndarray:
    """Standardize each sentiment proxy column to mean zero and unit variance."""
    raise NotImplementedError("Standardize proxies to mean zero and unit variance.")


def orthogonalize_proxies(proxies_std: np.ndarray, macro_controls: np.ndarray) -> np.ndarray:
    """Orthogonalize standardized proxies with respect to macroeconomic controls."""
    raise NotImplementedError("Orthogonalize proxies against macroeconomic controls using OLS.")


def extract_sentiment_index(ortho_proxies: np.ndarray, sign_anchor_idx: int = 2) -> dict[str, Any]:
    """Extract first principal component sentiment index with sign anchor normalization."""
    raise NotImplementedError("Extract leading principal component and normalize anchor sign.")


def newey_west_hac(x_matrix: np.ndarray, y_vector: np.ndarray, lags: int = 3) -> dict[str, Any]:
    """Compute OLS coefficients and Newey-West HAC standard errors with Bartlett kernel."""
    raise NotImplementedError("Compute OLS coefficients and Newey-West HAC covariance matrix.")


def estimate_predictive_regression(
    returns: np.ndarray, sentiment: np.ndarray, horizon: int = 1, lags: int = 1
) -> dict[str, Any]:
    """Estimate multi-period predictive regression of returns on lagged sentiment."""
    raise NotImplementedError("Estimate multi-period predictive regression with HAC standard errors.")


def test_cross_sectional_asymmetry(test_assets_returns: np.ndarray, sentiment: np.ndarray) -> dict[str, Any]:
    """Test Baker & Wurgler (2006) cross-sectional sentiment asymmetry hypothesis."""
    raise NotImplementedError("Test cross-sectional asymmetry between speculative and safe portfolios.")
