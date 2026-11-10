"""Lab PR5-L04-1: Multi-Strategy Capital Allocation under Drawdown Budgets.

SIMULATED: Comparative evaluation of Equal Weight, Risk Parity, and Drawdown-Budgeted allocation.
"""

from __future__ import annotations

import math

import numpy as np


def simulate_multi_strategy_platform(
    n_pods: int = 8,
    t_years: float = 1.0,
    n_steps: int = 252,
    n_sims: int = 1000,
    seed: int = 42,
) -> dict[str, dict[str, float]]:
    """Simulate platform capital allocation under Equal Weight, Risk Parity, and Drawdown Cushioning."""
    rng = np.random.default_rng(seed)
    dt = t_years / float(n_steps)
    sqrt_dt = math.sqrt(dt)

    # 5 skilled pods (mu in [0.08, 0.16]), 3 noise pods (mu in [-0.02, 0.03])
    mus = np.array([0.16, 0.14, 0.12, 0.10, 0.08, 0.03, 0.00, -0.02])
    sigmas = np.array([0.18, 0.15, 0.20, 0.12, 0.14, 0.16, 0.15, 0.22])
    hard_stops = np.full(n_pods, 0.07)  # 7% hard stop per pod

    # Generate correlation matrix (average pairwise rho = 0.15)
    rho = 0.15
    corr = np.full((n_pods, n_pods), rho)
    np.fill_diagonal(corr, 1.0)
    l_chol = np.linalg.cholesky(corr)

    policies = ["Equal Weight", "Risk Parity", "Drawdown Cushion"]
    platform_returns: dict[str, list[float]] = {p: [] for p in policies}
    platform_vols: dict[str, list[float]] = {p: [] for p in policies}
    platform_sharpes: dict[str, list[float]] = {p: [] for p in policies}
    platform_mdds: dict[str, list[float]] = {p: [] for p in policies}

    for _sim in range(n_sims):
        # Generate correlated daily returns for all pods
        z_uncorr = rng.standard_normal((n_steps, n_pods))
        z_corr = z_uncorr @ l_chol.T
        daily_pod_rets = (mus - 0.5 * sigmas**2) * dt + sigmas * sqrt_dt * z_corr

        for policy in policies:
            # Track pod wealth, peaks, and active status
            pod_wealth = np.ones(n_pods)
            pod_peaks = np.ones(n_pods)
            pod_active = np.ones(n_pods, dtype=bool)

            plat_wealth = 1.0
            plat_peak = 1.0
            plat_mdd = 0.0
            plat_daily_rets = []

            for t in range(n_steps):
                current_dds = (pod_peaks - pod_wealth) / pod_peaks
                # Update stop-outs
                newly_stopped = (current_dds >= hard_stops) & pod_active
                pod_active[newly_stopped] = False

                if not np.any(pod_active):
                    plat_daily_rets.append(0.0)
                    continue

                # Compute portfolio weights according to policy
                if policy == "Equal Weight":
                    w = np.zeros(n_pods)
                    w[pod_active] = 1.0 / np.sum(pod_active)
                elif policy == "Risk Parity":
                    w = np.zeros(n_pods)
                    inv_vols = 1.0 / sigmas[pod_active]
                    w[pod_active] = inv_vols / np.sum(inv_vols)
                elif policy == "Drawdown Cushion":
                    w = np.zeros(n_pods)
                    cushions = np.maximum(0.0, hard_stops[pod_active] - current_dds[pod_active])
                    denom = np.sum(cushions / sigmas[pod_active])
                    if denom > 1e-8:
                        w[pod_active] = (cushions / sigmas[pod_active]) / denom
                    else:
                        w[pod_active] = 1.0 / np.sum(pod_active)

                # Realized daily returns
                r_step = np.sum(w * daily_pod_rets[t])
                plat_daily_rets.append(r_step)

                # Update pod wealth
                pod_wealth[pod_active] *= 1.0 + daily_pod_rets[t, pod_active]
                pod_peaks = np.maximum(pod_peaks, pod_wealth)

                # Update platform tracking
                plat_wealth *= 1.0 + r_step
                plat_peak = max(plat_peak, plat_wealth)
                plat_mdd = max(plat_mdd, (plat_peak - plat_wealth) / plat_peak)

            # Performance stats
            arr_rets = np.array(plat_daily_rets)
            mean_ann_ret = float(np.mean(arr_rets) * 252.0)
            ann_vol = float(np.std(arr_rets) * math.sqrt(252.0))
            sr = mean_ann_ret / ann_vol if ann_vol > 1e-6 else 0.0

            platform_returns[policy].append(mean_ann_ret)
            platform_vols[policy].append(ann_vol)
            platform_sharpes[policy].append(sr)
            platform_mdds[policy].append(plat_mdd)

    results: dict[str, dict[str, float]] = {}
    for policy in policies:
        mean_ret = float(np.mean(platform_returns[policy]))
        mean_vol = float(np.mean(platform_vols[policy]))
        mean_sr = float(np.mean(platform_sharpes[policy]))
        mean_mdd = float(np.mean(platform_mdds[policy]))
        calmar = mean_ret / mean_mdd if mean_mdd > 1e-6 else 0.0

        results[policy] = {
            "mean_return": mean_ret,
            "mean_vol": mean_vol,
            "mean_sharpe": mean_sr,
            "mean_mdd": mean_mdd,
            "calmar": calmar,
        }

    return results


def main() -> None:
    sim = simulate_multi_strategy_platform(n_pods=8, n_sims=500, seed=42)

    print("Multi-Strategy Capital Allocation under Drawdown Budgets (8 Pods, T=1.0 yr):")
    print("=" * 72)
    print(f"{'Allocation Policy':<20} {'Return':<10} {'Vol':<10} {'Sharpe':<10} {'Mean MDD':<12} {'Calmar':<10}")
    print("-" * 72)

    for policy, r in sim.items():
        print(
            f"{policy:<20} {r['mean_return'] * 100:<9.2f}% {r['mean_vol'] * 100:<9.2f}% "
            f"{r['mean_sharpe']:<10.3f} {r['mean_mdd'] * 100:<11.2f}% {r['calmar']:<10.2f}"
        )


main()
