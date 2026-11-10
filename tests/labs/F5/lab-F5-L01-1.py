"""Lab F5-L01-1: Multiple Testing Haircuts in the Factor Zoo.

Evaluates multiple-testing adjustments across candidate equity factors, comparing
unadjusted t-statistics with Bonferroni, Holm step-down, Benjamini-Hochberg FDR,
and Harvey, Liu & Zhu (2016) raised hurdles.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def evaluate_factor_hypotheses(seed: int = 42) -> dict[str, float | int]:
    """Simulate candidate factor returns and compute multiple-testing metrics."""
    rng = np.random.default_rng(seed)
    n_factors = 200
    n_true = 25
    n_noise = n_factors - n_true
    n_months = 240

    # True factors have positive annualized alpha: mean 3.6% (0.3% / mo), vol 12% (3.46% / mo)
    true_alpha_mo = 0.0030
    vol_mo = 0.0346

    true_returns = rng.normal(true_alpha_mo, vol_mo, size=(n_true, n_months))
    # Noise factors have zero alpha: mean 0.0%, vol 12%
    noise_returns = rng.normal(0.0, vol_mo, size=(n_noise, n_months))

    all_returns = np.vstack([true_returns, noise_returns])
    is_true = np.zeros(n_factors, dtype=bool)
    is_true[:n_true] = True

    # Compute sample mean, sample standard error, t-statistic, and two-sided p-value
    sample_means = np.mean(all_returns, axis=1)
    sample_stds = np.std(all_returns, axis=1, ddof=1)
    se = sample_stds / np.sqrt(n_months)
    t_stats = sample_means / se
    p_values = 2.0 * (1.0 - stats.norm.cdf(np.abs(t_stats)))

    # 1. Classical unadjusted test at alpha = 0.05 (|t| >= 1.96)
    crit_classical = 1.96
    disc_classical = np.abs(t_stats) >= crit_classical
    n_disc_classical = int(np.sum(disc_classical))
    n_false_classical = int(np.sum(disc_classical & ~is_true))
    fdr_classical = float(n_false_classical / max(n_disc_classical, 1))

    # 2. Bonferroni correction: FWER <= 0.05 -> alpha_bonf = 0.05 / M
    alpha_bonf = 0.05 / n_factors
    crit_bonf = float(stats.norm.ppf(1.0 - alpha_bonf / 2.0))
    disc_bonf = p_values <= alpha_bonf
    n_disc_bonf = int(np.sum(disc_bonf))
    n_false_bonf = int(np.sum(disc_bonf & ~is_true))

    # 3. Holm step-down procedure (FWER <= 0.05)
    sort_idx = np.argsort(p_values)
    sorted_p = p_values[sort_idx]
    holm_thresholds = 0.05 / (n_factors - np.arange(n_factors))
    holm_passed = sorted_p <= holm_thresholds
    first_fail = np.argmin(holm_passed) if not np.all(holm_passed) else n_factors
    disc_holm = np.zeros(n_factors, dtype=bool)
    if np.any(holm_passed):
        disc_holm[sort_idx[:first_fail]] = True
    n_disc_holm = int(np.sum(disc_holm))
    n_false_holm = int(np.sum(disc_holm & ~is_true))

    # 4. Benjamini-Hochberg (1995) FDR control at q = 0.05
    q_fdr = 0.05
    bh_thresholds = (np.arange(1, n_factors + 1) / n_factors) * q_fdr
    bh_passed = sorted_p <= bh_thresholds
    disc_bh = np.zeros(n_factors, dtype=bool)
    if np.any(bh_passed):
        max_idx = int(np.max(np.where(bh_passed)[0]))
        disc_bh[sort_idx[: max_idx + 1]] = True
    n_disc_bh = int(np.sum(disc_bh))
    n_false_bh = int(np.sum(disc_bh & ~is_true))
    fdr_bh = float(n_false_bh / max(n_disc_bh, 1))

    # 5. Harvey, Liu & Zhu (2016) raised hurdle: |t| >= 3.00
    crit_hlz = 3.00
    disc_hlz = np.abs(t_stats) >= crit_hlz
    n_disc_hlz = int(np.sum(disc_hlz))
    n_false_hlz = int(np.sum(disc_hlz & ~is_true))
    fdr_hlz = float(n_false_hlz / max(n_disc_hlz, 1))

    return {
        "n_factors": n_factors,
        "n_true": n_true,
        "n_noise": n_noise,
        "n_disc_classical": n_disc_classical,
        "n_false_classical": n_false_classical,
        "fdr_classical": round(fdr_classical, 4),
        "crit_bonf": round(crit_bonf, 3),
        "n_disc_bonf": n_disc_bonf,
        "n_false_bonf": n_false_bonf,
        "n_disc_holm": n_disc_holm,
        "n_false_holm": n_false_holm,
        "n_disc_bh": n_disc_bh,
        "n_false_bh": n_false_bh,
        "fdr_bh": round(fdr_bh, 4),
        "n_disc_hlz": n_disc_hlz,
        "n_false_hlz": n_false_hlz,
        "fdr_hlz": round(fdr_hlz, 4),
    }


def main() -> None:
    print("Lab F5-L01-1 | Multiple Testing Haircuts in the Factor Zoo")
    print("---------------------------------------------------------")
    res = evaluate_factor_hypotheses(seed=42)
    print(f"Total candidate factors: {res['n_factors']} ({res['n_true']} true, {res['n_noise']} noise)")
    print(
        f"Classical unadjusted (|t| >= 1.96): {res['n_disc_classical']} discoveries "
        f"({res['n_false_classical']} false, FDR {res['fdr_classical']:.2%})"
    )
    print(
        f"Bonferroni FWER (|t| >= {res['crit_bonf']}): {res['n_disc_bonf']} discoveries ({res['n_false_bonf']} false)"
    )
    print(f"Holm step-down FWER:                {res['n_disc_holm']} discoveries ({res['n_false_holm']} false)")
    print(
        f"Benjamini-Hochberg FDR (q = 5%):    {res['n_disc_bh']} discoveries "
        f"({res['n_false_bh']} false, FDR {res['fdr_bh']:.2%})"
    )
    print(
        f"Harvey-Liu-Zhu hurdle (|t| >= 3.00): {res['n_disc_hlz']} discoveries "
        f"({res['n_false_hlz']} false, FDR {res['fdr_hlz']:.2%})"
    )


main()
