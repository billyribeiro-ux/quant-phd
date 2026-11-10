"""Lab S1-L09-1: Bayesian inference on a finite parameter grid.

Computes exact prior, likelihood, and posterior distributions across a discrete grid using fractions.Fraction.
Standard library only. No external imports.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # Parameter grid: p in {0.1, 0.2, ..., 0.9}
    grid = [Fraction(i, 10) for i in range(1, 10)]

    # Observed data: n = 10 trials, k = 7 successes
    n = 10
    k = 7
    n_minus_k = n - k

    # Likelihood proportional to p^7 * (1 - p)^3
    liks = [(p**k) * ((1 - p) ** n_minus_k) for p in grid]

    # Prior 1: Uniform (flat) prior
    prior_flat = [Fraction(1, 9) for _ in grid]
    unnorm_flat = [pri * lik for pri, lik in zip(prior_flat, liks, strict=True)]
    evidence_flat = sum(unnorm_flat)
    post_flat = [u / evidence_flat for u in unnorm_flat]
    mean_flat = sum(p * post for p, post in zip(grid, post_flat, strict=True))

    # Prior 2: Informative prior centered around p = 0.30
    raw_weights = [Fraction(w) for w in [2, 5, 8, 5, 2, 1, 1, 1, 1]]
    total_weight = sum(raw_weights)
    prior_info = [w / total_weight for w in raw_weights]
    unnorm_info = [pri * lik for pri, lik in zip(prior_info, liks, strict=True)]
    evidence_info = sum(unnorm_info)
    post_info = [u / evidence_info for u in unnorm_info]
    mean_info = sum(p * post for p, post in zip(grid, post_info, strict=True))

    print(f"data: n = {n}, successes k = {k}, sample proportion = {Fraction(k, n)}")
    print(f"flat prior evidence P(data): {evidence_flat} ({float(evidence_flat):.8e})")
    print(f"flat posterior mean E[p | data]: {mean_flat} ({float(mean_flat):.4f})")
    print(f"informative prior evidence P(data): {evidence_info} ({float(evidence_info):.8e})")
    print(f"informative posterior mean E[p | data]: {mean_info} ({float(mean_info):.4f})")

    # Find maximum a posteriori (MAP) estimate under each prior
    best_flat_idx = max(range(len(grid)), key=lambda i: post_flat[i])
    best_info_idx = max(range(len(grid)), key=lambda i: post_info[i])
    print(f"flat prior MAP estimate: {grid[best_flat_idx]} ({float(grid[best_flat_idx]):.1f})")
    print(f"informative prior MAP estimate: {grid[best_info_idx]} ({float(grid[best_info_idx]):.1f})")


main()
