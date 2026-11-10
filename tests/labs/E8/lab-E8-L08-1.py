"""Lab 8: Global Financial Cycle (GFC) Common Factor Decomposition.

SIMULATED panel. Standard library only.
Models cross-border capital flows and asset returns across 5 economies (Miranda-Agrippino & Rey 2020).
Extracts the global factor using power iteration and computes the variance share of the first principal component.
"""

import math
import random

SEED = 101
N_COUNTRIES = 5
T_PERIODS = 150


def simulate_gfc_panel(seed: int = SEED) -> list[list[float]]:
    """Simulate asset returns across 5 economies driven by a common global financial cycle factor."""
    rng = random.Random(seed)

    # Factor loadings (sensitivities to global financial conditions)
    loadings = [0.85, 0.92, 0.78, 0.65, 0.80]

    # Latent global factor AR(1) process (driven by US monetary conditions & global risk aversion)
    f = 0.0
    panel: list[list[float]] = [[] for _ in range(N_COUNTRIES)]

    for _ in range(T_PERIODS):
        # Global shock
        u_f = rng.gauss(0.0, 1.0)
        f = 0.6 * f + u_f

        for i in range(N_COUNTRIES):
            # Idiosyncratic national noise
            e_i = rng.gauss(0.0, 0.5)
            x_it = loadings[i] * f + e_i
            panel[i].append(x_it)

    return panel


def power_iteration(cov_matrix: list[list[float]], num_simulations: int = 50) -> tuple[float, list[float]]:
    """Extract top eigenvalue and eigenvector from covariance matrix using power iteration."""
    n = len(cov_matrix)
    # Start with unit vector
    b_k = [1.0 / math.sqrt(n)] * n

    for _ in range(num_simulations):
        # Matrix-vector multiply
        b_k1 = [sum(cov_matrix[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        # Norm
        norm = math.sqrt(sum(x**2 for x in b_k1))
        b_k = [x / norm for x in b_k1]

    # Rayleigh quotient for eigenvalue
    ab_k = [sum(cov_matrix[i][j] * b_k[j] for j in range(n)) for i in range(n)]
    eigenval = sum(b_k[i] * ab_k[i] for i in range(n))
    return eigenval, b_k


def analyze_global_factor(panel: list[list[float]]) -> tuple[float, float, float, list[float]]:
    """Compute sample covariance matrix, trace, top eigenvalue, and variance share."""
    n = len(panel)
    t = len(panel[0])

    # De-mean each series
    means = [sum(panel[i]) / t for i in range(n)]
    demeaned = [[panel[i][time_idx] - means[i] for time_idx in range(t)] for i in range(n)]

    # Compute covariance matrix
    cov = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov[i][j] = sum(demeaned[i][k] * demeaned[j][k] for k in range(t)) / (t - 1)

    # Trace of covariance matrix = total variance
    total_variance = sum(cov[i][i] for i in range(n))

    # Top eigenvalue
    top_eigenval, top_vector = power_iteration(cov)
    variance_share = top_eigenval / total_variance

    return top_eigenval, total_variance, variance_share, top_vector


def main() -> None:
    panel = simulate_gfc_panel(SEED)
    top_eval, tot_var, var_share, top_vec = analyze_global_factor(panel)

    print("=== Global Financial Cycle Factor Analysis (SIMULATED) ===")
    print(f"Sample: {N_COUNTRIES} economies, {T_PERIODS} monthly periods")
    print(f"Total System Variance (Trace of Cov): {tot_var:.4f}")
    print(f"Top Eigenvalue (First Principal Component): {top_eval:.4f}")
    print(f"Variance Explained by Global Factor:        {var_share * 100:.2f}%\n")

    print("Global Factor Loadings (Normalized Eigenvector):")
    for idx, weight in enumerate(top_vec):
        print(f"  Country {idx + 1}: {weight:+.4f}")

    print("\nInterpretation (Miranda-Agrippino & Rey 2020):")
    print(f"A single common global factor explains {var_share * 100:.1f}% of cross-border financial variation.")
    print("National capital flows and risky asset returns are heavily synchronized across borders.")

    assert var_share > 0.65, f"Global factor variance share {var_share} should exceed 65%"
    assert all(w > 0 for w in top_vec) or all(w < 0 for w in top_vec), "Loadings must have uniform sign"


main()
