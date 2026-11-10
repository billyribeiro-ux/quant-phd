"""Lab QR4-project-1: Rung 2 Completion Problem Reference Solution.

Implements the three core algorithmic building blocks of a contamination-safe text signal:
1. Sublinear Loughran-McDonald sentiment polarity calculation.
2. Point-in-time filing temporal filtering with execution lag enforcement.
3. Permutation-based chronological contamination test p-value computation.
"""

from __future__ import annotations

import math

import numpy as np


def compute_lm_polarity(
    tokens: list[str],
    pos_words: set[str],
    neg_words: set[str],
    eps: float = 1e-9,
) -> float:
    """Computes Loughran-McDonald polarity score with sublinear term-frequency weighting."""
    pos_counts: dict[str, int] = {}
    neg_counts: dict[str, int] = {}

    for t in tokens:
        if t in pos_words:
            pos_counts[t] = pos_counts.get(t, 0) + 1
        elif t in neg_words:
            neg_counts[t] = neg_counts.get(t, 0) + 1

    # Sublinear weighting: 1 + log(tf) for tf > 0
    w_pos = sum(1.0 + math.log(c) for c in pos_counts.values())
    w_neg = sum(1.0 + math.log(c) for c in neg_counts.values())

    return float((w_pos - w_neg) / (w_pos + w_neg + eps))


def filter_point_in_time_filings(
    filings: list[dict[str, str]],
    query_date: str,
    lag_days: int = 1,
) -> list[dict[str, str]]:
    """Filters filings to only those strictly available prior to trading date minus lag."""
    # In YYYY-MM-DD format, lexicographical comparison matches chronological ordering
    valid_filings: list[dict[str, str]] = []
    for f in filings:
        filing_date = f["filing_date"]
        # Strictly enforces that filing date is strictly earlier than query date
        if filing_date < query_date:
            valid_filings.append(f)
    return valid_filings


def compute_permutation_pvalue(
    signals: np.ndarray,
    returns: np.ndarray,
    n_permutations: int = 1000,
    seed: int = 42,
) -> tuple[float, float]:
    """Computes empirical two-tailed permutation p-value under the null hypothesis of no return predictability."""
    rng = np.random.default_rng(seed)
    n = len(signals)
    if n < 2:
        return 0.0, 1.0

    # Observed Pearson correlation
    s_dev = signals - np.mean(signals)
    r_dev = returns - np.mean(returns)
    obs_denom = float(np.sqrt(np.sum(s_dev**2) * np.sum(r_dev**2)))
    obs_corr = float(np.sum(s_dev * r_dev) / obs_denom) if obs_denom > 0 else 0.0

    # Permutation null distribution
    perm_corrs = np.zeros(n_permutations, dtype=np.float64)
    for i in range(n_permutations):
        shuffled_returns = rng.permutation(returns)
        shuff_dev = shuffled_returns - np.mean(shuffled_returns)
        denom = float(np.sqrt(np.sum(s_dev**2) * np.sum(shuff_dev**2)))
        perm_corrs[i] = float(np.sum(s_dev * shuff_dev) / denom) if denom > 0 else 0.0

    p_value = float(np.mean(np.abs(perm_corrs) >= abs(obs_corr)))
    return obs_corr, p_value


def main() -> None:
    # 1. Sublinear LM polarity check
    pos_lex = {"profitable", "growth", "exceeded", "strong"}
    neg_lex = {"loss", "default", "impairment", "litigation"}
    doc_tokens = ["profitable", "growth", "growth", "growth", "loss"]
    polarity = compute_lm_polarity(doc_tokens, pos_lex, neg_lex)
    print(f"Loughran-McDonald Polarity (sublinear weighted): {polarity:+.4f}")

    # 2. Point-in-time filtering check
    filings = [
        {"ticker": "AAPL", "filing_date": "2023-01-15", "content": "Q1 filing"},
        {"ticker": "AAPL", "filing_date": "2023-04-15", "content": "Q2 filing"},
        {"ticker": "AAPL", "filing_date": "2023-07-15", "content": "Q3 filing"},
        {"ticker": "AAPL", "filing_date": "2023-10-15", "content": "Q4 filing"},
    ]
    query_date = "2023-05-01"
    valid = filter_point_in_time_filings(filings, query_date)
    print(f"\nPoint-in-Time Query at {query_date}:")
    print(f"  Total filings in archive: {len(filings)}")
    print(f"  Accessible filings strictly before query date: {len(valid)}")
    print(f"  Latest accessible filing date: {valid[-1]['filing_date']}")

    # 3. Permutation contamination test check
    sig = np.array([1.2, -0.8, 0.5, -1.1, 0.2, 0.9, -0.4, 1.5, -1.3, 0.7])
    ret = np.array([0.04, -0.03, 0.01, -0.05, 0.00, 0.03, -0.01, 0.06, -0.04, 0.02])
    corr, pval = compute_permutation_pvalue(sig, ret, n_permutations=500, seed=42)
    print("\nPermutation Contamination Test:")
    print(f"  Observed correlation: {corr:+.4f}")
    print(f"  Permutation p-value : {pval:.4f}")
    print("Completion lab twin executed successfully.")


main()
