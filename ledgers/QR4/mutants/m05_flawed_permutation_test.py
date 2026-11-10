"""Mutant 5: Does not shuffle returns in permutation test, reporting identical observed correlation."""

from __future__ import annotations

import math
import re
from typing import Any

import numpy as np


def tokenize(text: str) -> list[str]:
    if not isinstance(text, str):
        raise ValueError("Text must be a string.")
    return re.findall(r"\b[a-z]{2,}\b", text.lower())


def compute_sublinear_tone(
    tokens: list[str],
    pos_words: set[str],
    neg_words: set[str],
    eps: float = 1e-9,
) -> float:
    if not isinstance(tokens, list):
        raise ValueError("Tokens must be a list of strings.")
    if not isinstance(pos_words, set) or not isinstance(neg_words, set):
        raise ValueError("Sentiment lexicons must be sets of strings.")

    pos_counts: dict[str, int] = {}
    neg_counts: dict[str, int] = {}

    for t in tokens:
        if t in pos_words:
            pos_counts[t] = pos_counts.get(t, 0) + 1
        elif t in neg_words:
            neg_counts[t] = neg_counts.get(t, 0) + 1

    if not pos_counts and not neg_counts:
        return 0.0

    w_pos = sum(1.0 + math.log(c) for c in pos_counts.values())
    w_neg = sum(1.0 + math.log(c) for c in neg_counts.values())

    return float((w_pos - w_neg) / (w_pos + w_neg + eps))


class PointInTimeFilingStore:
    def __init__(self) -> None:
        self._filings: list[dict[str, str]] = []

    def add_filing(self, ticker: str, filing_date: str, content: str) -> None:
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker must be a non-empty string.")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", filing_date):
            raise ValueError("filing_date must match YYYY-MM-DD format.")
        if not content or not isinstance(content, str):
            raise ValueError("Filing content must be non-empty string.")

        self._filings.append(
            {
                "ticker": ticker.upper(),
                "filing_date": filing_date,
                "content": content,
            }
        )

    def get_as_of_filings(
        self,
        ticker: str,
        as_of_date: str,
        execution_lag_days: int = 1,
    ) -> list[dict[str, str]]:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of_date):
            raise ValueError("as_of_date must match YYYY-MM-DD format.")
        if execution_lag_days < 1:
            raise ValueError("execution_lag_days must be >= 1.")

        ticker_upper = ticker.upper()
        accessible = [f for f in self._filings if f["ticker"] == ticker_upper and f["filing_date"] < as_of_date]
        accessible.sort(key=lambda x: x["filing_date"])
        return accessible

    def get_latest_filing(
        self,
        ticker: str,
        as_of_date: str,
        execution_lag_days: int = 1,
    ) -> dict[str, str] | None:
        filings = self.get_as_of_filings(ticker, as_of_date, execution_lag_days)
        if not filings:
            return None
        return filings[-1]


class CrossSectionalSignalEngine:
    def __init__(
        self,
        store: PointInTimeFilingStore,
        pos_words: set[str],
        neg_words: set[str],
    ) -> None:
        self.store = store
        self.pos_words = set(pos_words)
        self.neg_words = set(neg_words)

    def compute_ticker_tone(self, ticker: str, as_of_date: str) -> float:
        latest = self.store.get_latest_filing(ticker, as_of_date)
        if latest is None:
            raise ValueError(f"No point-in-time filing found for {ticker} prior to {as_of_date}.")
        tokens = tokenize(latest["content"])
        return compute_sublinear_tone(tokens, self.pos_words, self.neg_words)

    def compute_cross_sectional_scores(
        self,
        tickers: list[str],
        as_of_date: str,
    ) -> dict[str, float]:
        if not tickers:
            raise ValueError("Tickers list cannot be empty.")

        raw_scores: dict[str, float] = {}
        for t in tickers:
            raw_scores[t] = self.compute_ticker_tone(t, as_of_date)

        values = np.array([raw_scores[t] for t in tickers], dtype=np.float64)
        mean_val = float(np.mean(values))
        std_val = float(np.std(values))

        z_scores: dict[str, float] = {}
        denom = std_val if std_val > 1e-8 else 1.0
        for t in tickers:
            z_scores[t] = float((raw_scores[t] - mean_val) / denom)

        return z_scores


class ContaminationAuditor:
    @staticmethod
    def _rank_ic(x: np.ndarray, y: np.ndarray) -> float:
        if len(x) < 2:
            return 0.0
        rx = np.argsort(np.argsort(x)).astype(np.float64)
        ry = np.argsort(np.argsort(y)).astype(np.float64)
        rx_dev = rx - np.mean(rx)
        ry_dev = ry - np.mean(ry)
        denom = float(np.sqrt(np.sum(rx_dev**2) * np.sum(ry_dev**2)))
        return float(np.sum(rx_dev * ry_dev) / denom) if denom > 1e-12 else 0.0

    def evaluate_split_performance(
        self,
        signals: dict[str, dict[str, float]],
        forward_returns: dict[str, dict[str, float]],
        cutoff_date: str,
    ) -> dict[str, Any]:
        dates = sorted(set(signals.keys()) & set(forward_returns.keys()))
        if not dates:
            raise ValueError("No overlapping dates between signals and returns.")

        pre_ics: list[float] = []
        post_ics: list[float] = []

        for d in dates:
            tickers = sorted(set(signals[d].keys()) & set(forward_returns[d].keys()))
            if len(tickers) < 2:
                continue
            sig_arr = np.array([signals[d][t] for t in tickers], dtype=np.float64)
            ret_arr = np.array([forward_returns[d][t] for t in tickers], dtype=np.float64)
            ic = self._rank_ic(sig_arr, ret_arr)

            if d < cutoff_date:
                pre_ics.append(ic)
            else:
                post_ics.append(ic)

        pre_ic = float(np.mean(pre_ics)) if pre_ics else 0.0
        post_ic = float(np.mean(post_ics)) if post_ics else 0.0

        decay_ratio = float(max(0.0, 1.0 - post_ic / pre_ic)) if pre_ic > 0.0001 else 0.0

        is_contaminated = bool(pre_ic > 0.15 and decay_ratio > 0.50)

        return {
            "pre_ic": pre_ic,
            "post_ic": post_ic,
            "ic_decay": decay_ratio,
            "is_contaminated": is_contaminated,
        }

    def run_time_permutation_test(
        self,
        signals: np.ndarray,
        returns: np.ndarray,
        n_permutations: int = 200,
        seed: int = 42,
    ) -> dict[str, float]:
        sig = np.asarray(signals, dtype=np.float64).flatten()
        ret = np.asarray(returns, dtype=np.float64).flatten()
        if len(sig) != len(ret):
            raise ValueError("Signals and returns must have identical lengths.")
        if len(sig) < 3:
            raise ValueError("At least 3 observations required for permutation test.")

        s_dev = sig - np.mean(sig)
        r_dev = ret - np.mean(ret)
        denom_obs = float(np.sqrt(np.sum(s_dev**2) * np.sum(r_dev**2)))
        obs_corr = float(np.sum(s_dev * r_dev) / denom_obs) if denom_obs > 1e-12 else 0.0

        perm_corrs = np.zeros(n_permutations, dtype=np.float64)
        for i in range(n_permutations):
            # BUG: does not shuffle returns, returns unpermuted array
            shuff_ret = ret
            shuff_dev = shuff_ret - np.mean(shuff_ret)
            denom_perm = float(np.sqrt(np.sum(s_dev**2) * np.sum(shuff_dev**2)))
            perm_corrs[i] = float(np.sum(s_dev * shuff_dev) / denom_perm) if denom_perm > 1e-12 else 0.0

        p_value = float(np.mean(np.abs(perm_corrs) >= abs(obs_corr)))

        return {
            "observed_corr": obs_corr,
            "perm_pvalue": p_value,
            "null_mean": float(np.mean(perm_corrs)),
            "null_std": float(np.std(perm_corrs)),
        }
