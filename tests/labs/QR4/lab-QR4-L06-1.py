"""Lab QR4-L06-1: Detecting Look-Ahead Contamination in LLM Return Predictability.

Replicates the core methodology of Glasserman & Lin (2024) and Lopez-Lira & Tang (2026):
evaluates apparent sentiment predictability across the pretraining temporal boundary,
computes Rank Information Coefficients before and after the training cutoff, and runs
synthetic perturbation probes to detect temporal memorization leakage.
"""

from __future__ import annotations

import numpy as np


def spearman_rank_ic(x: np.ndarray, y: np.ndarray) -> float:
    """Computes Spearman rank correlation between two vectors."""
    n = len(x)
    if n < 2:
        return 0.0
    rank_x = np.argsort(np.argsort(x)).astype(np.float64)
    rank_y = np.argsort(np.argsort(y)).astype(np.float64)

    # Pearson correlation of ranks
    rank_x_dev = rank_x - np.mean(rank_x)
    rank_y_dev = rank_y - np.mean(rank_y)
    denom = float(np.sqrt(np.sum(rank_x_dev**2) * np.sum(rank_y_dev**2)))
    if denom == 0.0:
        return 0.0
    return float(np.sum(rank_x_dev * rank_y_dev) / denom)


def main() -> None:
    rng = np.random.default_rng(2024)

    # 200 temporal cross-sectional time steps:
    # Periods 1 to 120: In-corpus pretraining period (pre-September 2021 cutoff)
    # Periods 121 to 200: Strictly out-of-sample post-cutoff period
    n_pre = 120
    n_post = 80
    n_assets = 30

    # True latent alpha signal: modest predictability (IC ~ 0.03)
    true_alpha_pre = rng.normal(0.0, 1.0, size=(n_pre, n_assets))
    true_alpha_post = rng.normal(0.0, 1.0, size=(n_post, n_assets))

    noise_pre = rng.normal(0.0, 5.0, size=(n_pre, n_assets))
    noise_post = rng.normal(0.0, 5.0, size=(n_post, n_assets))

    # Realized forward returns
    fwd_ret_pre = 0.03 * true_alpha_pre + noise_pre
    fwd_ret_post = 0.03 * true_alpha_post + noise_post

    # Contaminated LLM sentiment signal:
    # In pre-cutoff period, pretraining corpus leaked future return news into LLM weights (leakage = 0.15)
    # Post-cutoff period has zero contamination leakage
    llm_sentiment_pre = true_alpha_pre + 0.15 * fwd_ret_pre + rng.normal(0.0, 1.0, size=(n_pre, n_assets))
    llm_sentiment_post = true_alpha_post + rng.normal(0.0, 1.0, size=(n_post, n_assets))

    # Calculate average cross-sectional rank IC for pre- and post-cutoff periods
    ic_pre_list = [spearman_rank_ic(llm_sentiment_pre[t], fwd_ret_pre[t]) for t in range(n_pre)]
    ic_post_list = [spearman_rank_ic(llm_sentiment_post[t], fwd_ret_post[t]) for t in range(n_post)]

    mean_ic_pre = float(np.mean(ic_pre_list))
    mean_ic_post = float(np.mean(ic_post_list))
    ic_tstat_pre = mean_ic_pre / (float(np.std(ic_pre_list, ddof=1)) / np.sqrt(n_pre))
    ic_tstat_post = mean_ic_post / (float(np.std(ic_post_list, ddof=1)) / np.sqrt(n_post))

    print(f"Pretraining Cutoff Evaluation (Pre-cutoff: {n_pre} bars, Post-cutoff: {n_post} bars):")
    print(f"  Pre-Cutoff In-Corpus Rank IC : {mean_ic_pre:+.4f} (t-statistic = {ic_tstat_pre:+.2f})")
    print(f"  Post-Cutoff Out-of-Sample IC : {mean_ic_post:+.4f} (t-statistic = {ic_tstat_post:+.2f})")
    print(f"  Contamination Decay Ratio    : {(mean_ic_post / mean_ic_pre):.2f}")

    # Synthetic entity perturbation probe:
    # Scramble company tickers in pre-cutoff headlines.
    # Contaminated weights lose memorized entity link, causing IC to drop to true alpha level.
    perm_sentiment_pre = true_alpha_pre + rng.normal(0.0, 1.0, size=(n_pre, n_assets))
    ic_perturbed_pre = float(np.mean([spearman_rank_ic(perm_sentiment_pre[t], fwd_ret_pre[t]) for t in range(n_pre)]))
    print("\nSynthetic Perturbation Probe (Pre-Cutoff with Scrambled Entity Names):")
    print(f"  Unperturbed Pre-Cutoff IC    : {mean_ic_pre:+.4f}")
    print(f"  Perturbed Pre-Cutoff IC      : {ic_perturbed_pre:+.4f}")
    print(f"  Memorization Wedge           : {mean_ic_pre - ic_perturbed_pre:+.4f}")
    print("Verification Invariant: Contamination wedge vanishes on genuinely un-memorized text.")


main()
