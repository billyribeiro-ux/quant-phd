"""Deterministic instance generator for QR4 project (Contamination-Safe Text Signal).

Generates synthetic EDGAR-style corporate filing archives, point-in-time filing timelines,
domain sentiment lexicons, and cross-sectional forward return panels across seeds.
"""

from __future__ import annotations

import functools
from typing import Any

import numpy as np


@functools.lru_cache(maxsize=128)
def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic filing and return dataset for the given seed."""
    rng = np.random.default_rng(seed)

    tickers = ["ALPHA", "BETA", "GAMMA", "DELTA", "EPSILON"]

    # Domain sentiment lexicons
    pos_words = {"profitable", "growth", "exceeded", "strong", "improved", "expansion", "gain", "efficiency"}
    neg_words = {
        "loss",
        "default",
        "restructuring",
        "impairment",
        "litigation",
        "adverse",
        "recession",
        "breach",
        "decline",
        "deterioration",
    }
    neutral_words = [
        "operating",
        "revenue",
        "capital",
        "balance",
        "sheet",
        "segment",
        "quarterly",
        "report",
        "management",
        "accounting",
        "inventory",
        "equipment",
        "expenditure",
        "commercial",
        "infrastructure",
    ]

    # Generate quarterly filing dates from 2021 to 2024 (16 quarters)
    years = [2021, 2022, 2023, 2024]
    quarters = [("02", "15"), ("05", "15"), ("08", "15"), ("11", "15")]
    filing_dates: list[str] = []
    for y in years:
        for m, d in quarters:
            filing_dates.append(f"{y}-{m}-{d}")

    # Generate filings for each ticker
    filings: list[dict[str, str]] = []
    for ticker in tickers:
        base_bias = float(rng.uniform(-0.5, 0.5))
        for f_date in filing_dates:
            # Deterministic number of sentiment words
            n_pos = int(rng.integers(1, 6)) + (1 if base_bias > 0 else 0)
            n_neg = int(rng.integers(1, 6)) + (1 if base_bias < 0 else 0)
            n_neu = int(rng.integers(10, 20))

            chosen_pos = list(rng.choice(sorted(pos_words), size=n_pos, replace=True))
            chosen_neg = list(rng.choice(sorted(neg_words), size=n_neg, replace=True))
            chosen_neu = list(rng.choice(neutral_words, size=n_neu, replace=True))

            all_words = chosen_pos + chosen_neg + chosen_neu
            rng.shuffle(all_words)
            content = " ".join(all_words) + "."

            filings.append(
                {
                    "ticker": ticker,
                    "filing_date": f_date,
                    "content": content,
                }
            )

    # Cutoff date separating pre-cutoff from post-cutoff
    cutoff_date = "2023-01-01"

    # Forward returns and signals per quarter
    # For dates before cutoff: contaminated signal has high correlation to returns
    # For dates after cutoff: correlation is near zero (null)
    dates_pre = [d for d in filing_dates if d < cutoff_date]
    dates_post = [d for d in filing_dates if d >= cutoff_date]

    signals_history: dict[str, dict[str, float]] = {}
    returns_history: dict[str, dict[str, float]] = {}

    for d in filing_dates:
        signals_history[d] = {}
        returns_history[d] = {}
        is_pre = d < cutoff_date

        for ticker in tickers:
            true_sentiment = float(rng.normal(0.0, 1.0))
            if is_pre:
                # Strong return predictability in pretraining corpus (contaminated)
                fwd_ret = 0.08 * true_sentiment + float(rng.normal(0.0, 0.01))
                signal_val = true_sentiment + float(rng.normal(0.0, 0.05))
            else:
                # Pure noise / zero predictability post-cutoff (clean OOS)
                fwd_ret = float(rng.normal(0.0, 0.05))
                signal_val = float(rng.normal(0.0, 1.0))

            signals_history[d][ticker] = signal_val
            returns_history[d][ticker] = fwd_ret

    # 1D paired arrays for permutation test verification
    n_perm_samples = 50
    sig_1d = rng.normal(0.0, 1.0, size=n_perm_samples)
    sig_1d = sig_1d - np.mean(sig_1d)

    # Strong correlation: r > 0.90
    noise_1d = rng.normal(0.0, 0.15, size=n_perm_samples)
    ret_1d_strong = 1.5 * sig_1d + noise_1d

    # Exact null: orthogonal to sig_1d (r == 0.0)
    raw_null = rng.normal(0.0, 1.0, size=n_perm_samples)
    raw_null = raw_null - np.mean(raw_null)
    proj = float(np.dot(raw_null, sig_1d) / np.dot(sig_1d, sig_1d))
    ret_1d_null = raw_null - proj * sig_1d

    return {
        "seed": seed,
        "tickers": tickers,
        "pos_words": sorted(pos_words),
        "neg_words": sorted(neg_words),
        "filings": filings,
        "filing_dates": filing_dates,
        "cutoff_date": cutoff_date,
        "dates_pre": dates_pre,
        "dates_post": dates_post,
        "signals_history": signals_history,
        "returns_history": returns_history,
        "query_date": "2023-06-01",
        "boundary_date": "2022-05-15",
        "sig_1d": sig_1d,
        "ret_1d_strong": ret_1d_strong,
        "ret_1d_null": ret_1d_null,
    }
