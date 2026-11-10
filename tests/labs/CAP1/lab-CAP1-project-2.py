"""Lab Project 2 (Completion Problem Solution): Clustered SE df correction and divergence articulation."""

from __future__ import annotations


def compute_cluster_df_factor(n_obs: int, n_params: int, n_clusters: int) -> float:
    """Compute the finite-sample degrees-of-freedom adjustment for clustered standard errors."""
    cluster_adjustment = float(n_clusters) / float(max(1, n_clusters - 1))
    sample_adjustment = float(n_obs - 1) / float(max(1, n_obs - n_params))
    return cluster_adjustment * sample_adjustment


def check_articulation_identity(
    published_val: float,
    replicated_val: float,
    step_deltas: list[float],
) -> tuple[float, float, bool]:
    """Check that sum of incremental step deltas articulates exactly to total divergence."""
    total_divergence = replicated_val - published_val
    sum_deltas = sum(step_deltas)
    articulation_gap = total_divergence - sum_deltas
    is_articulated = abs(articulation_gap) < 1e-10
    return total_divergence, articulation_gap, is_articulated


def main() -> None:
    # 1. Degrees of freedom factor check
    n_obs = 1200
    n_params = 4
    n_clusters = 50

    df_factor = compute_cluster_df_factor(n_obs, n_params, n_clusters)
    print(f"Degrees of freedom multiplier for G = {n_clusters}, N = {n_obs}, K = {n_params}: {df_factor:.6f}")

    # 2. Articulation check
    published = 0.850
    replicated = 0.420
    deltas = [-0.070, -0.110, -0.120, -0.010, -0.120]  # sample, shrcd, delist, winsor, vw

    tot_div, gap, ok = check_articulation_identity(published, replicated, deltas)
    print(f"Total empirical divergence: {tot_div:+.3f}")
    print(f"Sum of step deltas:        {sum(deltas):+.3f}")
    print(f"Articulation gap:          {gap:.12f}")
    print(f"Identity holds exactly:    {ok}")


main()
