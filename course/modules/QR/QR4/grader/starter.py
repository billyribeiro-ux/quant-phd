"""Starter template for QR4 project (Contamination-Safe Text Signal).

Implement each class and function according to the specification.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase alphabetic words."""
    raise NotImplementedError


def compute_sublinear_tone(
    tokens: list[str],
    pos_words: set[str],
    neg_words: set[str],
    eps: float = 1e-9,
) -> float:
    """Compute Loughran-McDonald sentiment tone with sublinear term-frequency weighting."""
    raise NotImplementedError


class PointInTimeFilingStore:
    """In-memory filing store strictly enforcing temporal causality and execution lag."""

    def __init__(self) -> None:
        raise NotImplementedError

    def add_filing(self, ticker: str, filing_date: str, content: str) -> None:
        """Register a corporate filing with date validation."""
        raise NotImplementedError

    def get_as_of_filings(
        self,
        ticker: str,
        as_of_date: str,
        execution_lag_days: int = 1,
    ) -> list[dict[str, str]]:
        """Retrieve all filings for a ticker strictly prior to as_of_date."""
        raise NotImplementedError

    def get_latest_filing(
        self,
        ticker: str,
        as_of_date: str,
        execution_lag_days: int = 1,
    ) -> dict[str, str] | None:
        """Retrieve the single most recent filing available strictly prior to as_of_date."""
        raise NotImplementedError


class CrossSectionalSignalEngine:
    """Extracts sentiment signals and normalizes cross-sectional factor z-scores."""

    def __init__(
        self,
        store: PointInTimeFilingStore,
        pos_words: set[str],
        neg_words: set[str],
    ) -> None:
        raise NotImplementedError

    def compute_ticker_tone(self, ticker: str, as_of_date: str) -> float:
        """Compute tone for a ticker from its latest available filing before as_of_date."""
        raise NotImplementedError

    def compute_cross_sectional_scores(
        self,
        tickers: list[str],
        as_of_date: str,
    ) -> dict[str, float]:
        """Compute demeaned, variance-standardized z-scores across a basket of tickers."""
        raise NotImplementedError


class ContaminationAuditor:
    """Audits return predictability across temporal boundaries to detect lookahead contamination."""

    def evaluate_split_performance(
        self,
        signals: dict[str, dict[str, float]],
        forward_returns: dict[str, dict[str, float]],
        cutoff_date: str,
    ) -> dict[str, Any]:
        """Evaluate pre-cutoff vs post-cutoff rank Information Coefficient."""
        raise NotImplementedError

    def run_time_permutation_test(
        self,
        signals: np.ndarray,
        returns: np.ndarray,
        n_permutations: int = 200,
        seed: int = 42,
    ) -> dict[str, float]:
        """Compute empirical permutation test p-value by shuffling returns across timestamps."""
        raise NotImplementedError
