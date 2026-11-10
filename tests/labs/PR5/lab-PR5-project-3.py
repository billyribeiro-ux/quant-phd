"""Lab PR5-project-3: Project Rung 3 Full Platform Simulator Twin.

SIMULATED: Full multi-manager platform execution and policy comparison on seed 0.
"""

from __future__ import annotations

import math
import random
from typing import Any

import numpy as np


def make_instance(seed: int) -> dict[str, Any]:
    """Generate deterministic parameters for a multi-manager pod platform."""
    rng = random.Random(seed)

    n_pods = 10
    n_skilled = 6
    n_unskilled = 4

    mus: list[float] = []
    sigmas: list[float] = []
    skills: list[int] = []
    soft_stops: list[float] = []
    hard_stops: list[float] = []

    for _ in range(n_skilled):
        mu = round(0.08 + 0.10 * rng.random(), 4)
        sigma = round(0.12 + 0.10 * rng.random(), 4)
        soft_stop = round(0.04 + 0.02 * rng.random(), 4)
        hard_stop = round(soft_stop + 0.03 + 0.03 * rng.random(), 4)
        mus.append(mu)
        sigmas.append(sigma)
        skills.append(1)
        soft_stops.append(soft_stop)
        hard_stops.append(hard_stop)

    for _ in range(n_unskilled):
        mu = round(-0.04 + 0.07 * rng.random(), 4)
        sigma = round(0.14 + 0.11 * rng.random(), 4)
        soft_stop = round(0.04 + 0.02 * rng.random(), 4)
        hard_stop = round(soft_stop + 0.03 + 0.03 * rng.random(), 4)
        mus.append(mu)
        sigmas.append(sigma)
        skills.append(0)
        soft_stops.append(soft_stop)
        hard_stops.append(hard_stop)

    corr_rho = round(0.08 + 0.16 * rng.random(), 4)
    risk_free_rate = round(0.02 + 0.02 * rng.random(), 4)
    platform_budget_mdd = round(0.08 + 0.04 * rng.random(), 4)

    return {
        "seed": seed,
        "n_pods": n_pods,
        "mus": mus,
        "sigmas": sigmas,
        "skills": skills,
        "soft_stops": soft_stops,
        "hard_stops": hard_stops,
        "corr_rho": corr_rho,
        "n_days": 252,
        "t_years": 1.0,
        "risk_free_rate": risk_free_rate,
        "platform_budget_mdd": platform_budget_mdd,
    }


def compute_allocation_weights(
    policy: str,
    active_mask: np.ndarray,
    current_drawdowns: np.ndarray,
    hard_stops: np.ndarray,
    sigmas: np.ndarray,
) -> np.ndarray:
    """Compute platform portfolio weights across pods for a given risk policy."""
    n_pods = len(active_mask)
    weights = np.zeros(n_pods, dtype=float)
    n_active = int(np.sum(active_mask))

    if n_active == 0:
        return weights

    if policy == "equal":
        weights[active_mask] = 1.0 / float(n_active)
        return weights

    if policy == "risk_parity":
        inv_vols = 1.0 / np.maximum(sigmas[active_mask], 1e-4)
        total_inv_vol = float(np.sum(inv_vols))
        if total_inv_vol > 0.0:
            weights[active_mask] = inv_vols / total_inv_vol
        else:
            weights[active_mask] = 1.0 / float(n_active)
        return weights

    if policy == "cushion":
        cushions = np.maximum(0.0, hard_stops[active_mask] - current_drawdowns[active_mask])
        vols = np.maximum(sigmas[active_mask], 1e-4)
        raw_scores = cushions / vols
        total_score = float(np.sum(raw_scores))
        if total_score > 1e-7:
            weights[active_mask] = raw_scores / total_score
        else:
            weights[active_mask] = 1.0 / float(n_active)
        return weights

    msg = f"Unknown allocation policy: {policy!r}."
    raise ValueError(msg)


def simulate_platform(
    instance: dict[str, Any],
    policy: str = "cushion",
    seed: int | None = None,
) -> dict[str, Any]:
    """Execute dynamic multi-pod simulation under drawdown stops and capital allocation."""
    use_seed = instance["seed"] if seed is None else seed
    rng = np.random.default_rng(use_seed)

    n_pods = instance["n_pods"]
    n_days = instance.get("n_days", 252)
    t_years = instance.get("t_years", 1.0)
    dt = t_years / float(n_days)
    sqrt_dt = math.sqrt(dt)

    mus = np.array(instance["mus"], dtype=float)
    sigmas = np.array(instance["sigmas"], dtype=float)
    soft_stops = np.array(instance["soft_stops"], dtype=float)
    hard_stops = np.array(instance["hard_stops"], dtype=float)
    skill_flags = np.array(instance["skills"], dtype=bool)

    rho = float(instance.get("corr_rho", 0.15))
    corr = np.full((n_pods, n_pods), rho)
    np.fill_diagonal(corr, 1.0)
    l_chol = np.linalg.cholesky(corr)

    z_uncorr = rng.standard_normal((n_days, n_pods))
    z_corr = z_uncorr @ l_chol.T

    daily_returns_raw = (mus - 0.5 * sigmas**2) * dt + sigmas * sqrt_dt * z_corr

    pod_wealth = np.ones(n_pods, dtype=float)
    pod_peaks = np.ones(n_pods, dtype=float)
    pod_active = np.ones(n_pods, dtype=bool)

    platform_wealth = np.ones(n_days + 1, dtype=float)
    platform_peaks = np.ones(n_days + 1, dtype=float)
    platform_drawdowns = np.zeros(n_days + 1, dtype=float)
    platform_daily_returns: list[float] = []

    stopped_out = np.zeros(n_pods, dtype=bool)

    for t in range(n_days):
        current_dds = (pod_peaks - pod_wealth) / pod_peaks

        new_hard_stops = (current_dds >= hard_stops) & pod_active
        pod_active[new_hard_stops] = False
        stopped_out[new_hard_stops] = True

        if not np.any(pod_active):
            platform_daily_returns.append(0.0)
            platform_wealth[t + 1] = platform_wealth[t]
            platform_peaks[t + 1] = platform_peaks[t]
            platform_drawdowns[t + 1] = (platform_peaks[t + 1] - platform_wealth[t + 1]) / platform_peaks[t + 1]
            continue

        leverage_multipliers = np.ones(n_pods, dtype=float)
        in_soft_zone = (current_dds >= soft_stops) & (current_dds < hard_stops) & pod_active
        leverage_multipliers[in_soft_zone] = 0.5

        weights = compute_allocation_weights(
            policy=policy,
            active_mask=pod_active,
            current_drawdowns=current_dds,
            hard_stops=hard_stops,
            sigmas=sigmas,
        )

        scaled_pod_returns = leverage_multipliers * daily_returns_raw[t]
        r_plat = float(np.sum(weights * scaled_pod_returns))
        platform_daily_returns.append(r_plat)

        pod_wealth[pod_active] *= 1.0 + scaled_pod_returns[pod_active]
        pod_peaks = np.maximum(pod_peaks, pod_wealth)

        platform_wealth[t + 1] = platform_wealth[t] * (1.0 + r_plat)
        platform_peaks[t + 1] = max(platform_peaks[t], platform_wealth[t + 1])
        platform_drawdowns[t + 1] = (platform_peaks[t + 1] - platform_wealth[t + 1]) / platform_peaks[t + 1]

    plat_rets_arr = np.array(platform_daily_returns)
    mean_daily = float(np.mean(plat_rets_arr)) if len(plat_rets_arr) > 0 else 0.0
    std_daily = float(np.std(plat_rets_arr, ddof=1)) if len(plat_rets_arr) > 1 else 0.0

    ann_return = mean_daily * 252.0
    ann_vol = std_daily * math.sqrt(252.0)
    sharpe = ann_return / ann_vol if ann_vol > 1e-6 else 0.0

    platform_mdd = float(np.max(platform_drawdowns))
    calmar = ann_return / platform_mdd if platform_mdd > 1e-6 else 0.0

    n_skilled = int(np.sum(skill_flags))
    n_unskilled = int(np.sum(~skill_flags))

    skilled_stopped = int(np.sum(stopped_out & skill_flags))
    unskilled_stopped = int(np.sum(stopped_out & (~skill_flags)))

    skilled_churn_rate = float(skilled_stopped / n_skilled) if n_skilled > 0 else 0.0
    unskilled_stopped_rate = float(unskilled_stopped / n_unskilled) if n_unskilled > 0 else 0.0
    overall_survival_rate = float(np.sum(pod_active) / n_pods)

    return {
        "platform_annualized_return": ann_return,
        "platform_annualized_volatility": ann_vol,
        "platform_sharpe": sharpe,
        "platform_mdd": platform_mdd,
        "calmar_ratio": calmar,
        "skilled_churn_rate": skilled_churn_rate,
        "unskilled_stopped_rate": unskilled_stopped_rate,
        "overall_survival_rate": overall_survival_rate,
        "platform_wealth_path": platform_wealth,
        "platform_drawdown_path": platform_drawdowns,
    }


def main() -> None:
    seed = 0
    inst = make_instance(seed)

    print("Project Rung 3 · Full Platform Simulation (Seed 0)")
    print("=" * 72)
    print(f"Platform Setup: N={inst['n_pods']} pods (6 skilled, 4 unskilled), T=252 days")
    print(f"Average Pod Correlation rho={inst['corr_rho']:.4f}, Risk-free rate={inst['risk_free_rate']:.4f}")
    print("-" * 72)

    policies = ["equal", "risk_parity", "cushion"]

    print(f"{'Metric':<30} {'Equal Weight':<15} {'Risk Parity':<15} {'Drawdown Cushion':<15}")
    print("-" * 72)

    results = {p: simulate_platform(inst, policy=p, seed=seed) for p in policies}

    def fmt_pct(val: float) -> str:
        return f"{val * 100:.2f}%"

    def fmt_pct1(val: float) -> str:
        return f"{val * 100:.1f}%"

    def fmt_num(val: float) -> str:
        return f"{val:.4f}"

    rows = [
        ("Annualized Return", [fmt_pct(float(results[p]["platform_annualized_return"])) for p in policies]),
        ("Annualized Volatility", [fmt_pct(float(results[p]["platform_annualized_volatility"])) for p in policies]),
        ("Platform Sharpe Ratio", [fmt_num(float(results[p]["platform_sharpe"])) for p in policies]),
        ("Platform Maximum Drawdown", [fmt_pct(float(results[p]["platform_mdd"])) for p in policies]),
        ("Calmar Ratio", [fmt_num(float(results[p]["calmar_ratio"])) for p in policies]),
        ("Skilled Pod Churn Rate", [fmt_pct1(float(results[p]["skilled_churn_rate"])) for p in policies]),
        ("Unskilled Stopped Rate", [fmt_pct1(float(results[p]["unskilled_stopped_rate"])) for p in policies]),
        ("Overall Pod Survival Rate", [fmt_pct1(float(results[p]["overall_survival_rate"])) for p in policies]),
    ]

    for label, vals in rows:
        print(f"{label:<30} {vals[0]:<15} {vals[1]:<15} {vals[2]:<15}")


main()
