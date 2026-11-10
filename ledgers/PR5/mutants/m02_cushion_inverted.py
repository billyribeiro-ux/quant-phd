"""Mutant 2: Cushion allocation uses current drawdown instead of distance to stop-loss (inverting cushion).
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np


def expected_mdd_brownian(mu: float, sigma: float, t: float) -> float:
    """Calculate expected maximum drawdown of a Brownian motion path under Magdon-Ismail et al. (2004).

    Args:
        mu: Annualized drift of arithmetic process.
        sigma: Annualized volatility (diffusion parameter).
        t: Time horizon in years.

    Returns:
        Theoretical expected maximum drawdown E[MDD(t)].
    """
    if t <= 0.0 or sigma <= 0.0:
        return 0.0

    # Dimensionless time / Sharpe scaling variable x = mu * sqrt(t) / sigma
    x = mu * math.sqrt(t) / sigma
    z0 = math.sqrt(math.pi / 2.0)

    if abs(x) < 1e-6:
        # Zero-drift analytic formula: sigma * sqrt(pi * t / 2)
        return float(sigma * math.sqrt(t) * z0)

    if x > 0:
        # Positive drift: logarithmic scaling regime Q(x)
        # Smooth interpolation to asymptotic decay
        q_val = z0 / (1.0 + 0.36 * x + 0.08 * (x**2))
    else:
        # Negative drift: linear scaling regime Q(x) ~ |x| + ...
        abs_x = abs(x)
        q_val = z0 + 0.45 * abs_x + 0.08 * (abs_x**2)

    return float(sigma * math.sqrt(t) * q_val)


def grossman_zhou_cushion_allocation(
    wealth: float,
    peak: float,
    alpha: float,
    m_multiplier: float,
) -> float:
    """Calculate optimal risky dollar allocation under Grossman-Zhou (1993) floor protection.

    Allocation pi = m * (W - alpha * M)^+.

    Args:
        wealth: Current portfolio wealth W_t.
        peak: Running historical maximum wealth M_t = max_{s <= t} W_s.
        alpha: Floor protection fraction in (0, 1), such that W_t >= alpha * M_t.
        m_multiplier: Multiplier m* derived from risk aversion and asset Sharpe.

    Returns:
        Dollar amount allocated to risky asset (strictly non-negative).
    """
    if peak <= 0.0 or wealth <= 0.0:
        return 0.0
    floor = alpha * peak
    cushion = max(0.0, wealth - floor)
    return float(m_multiplier * cushion)


def compute_pod_drawdowns(wealth_paths: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute running maximums, current drawdowns, and maximum drawdowns for asset paths.

    Args:
        wealth_paths: Array of shape (n_pods, n_steps + 1) of cumulative wealth.

    Returns:
        Tuple of (running_peaks, current_drawdowns, max_drawdowns).
        running_peaks: shape (n_pods, n_steps + 1)
        current_drawdowns: shape (n_pods, n_steps + 1) with values in [0, 1]
        max_drawdowns: shape (n_pods,) peak-to-trough maximum drawdown
    """
    running_peaks = np.maximum.accumulate(wealth_paths, axis=1)
    current_drawdowns = np.clip((running_peaks - wealth_paths) / running_peaks, 0.0, 1.0)
    max_drawdowns = np.max(current_drawdowns, axis=1)
    return running_peaks, current_drawdowns, max_drawdowns


def compute_allocation_weights(
    policy: str,
    active_mask: np.ndarray,
    current_drawdowns: np.ndarray,
    hard_stops: np.ndarray,
    sigmas: np.ndarray,
) -> np.ndarray:
    """Compute platform portfolio weights across pods for a given risk policy.

    Args:
        policy: One of 'equal', 'risk_parity', 'cushion'.
        active_mask: Boolean array of shape (n_pods,) where True means pod is active.
        current_drawdowns: Float array of shape (n_pods,) of current drawdowns.
        hard_stops: Float array of shape (n_pods,) of hard stop loss levels.
        sigmas: Float array of shape (n_pods,) of annualized volatilities.

    Returns:
        Normalized weights array of shape (n_pods,) summing to 1.0 (or all 0 if none active).
    """
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
        # Grossman-Zhou inspired cushion: distance to hard stop C_i = max(0, hard_stop_i - D_i)
        cushions = np.maximum(0.001, current_drawdowns[active_mask])
        vols = np.maximum(sigmas[active_mask], 1e-4)
        raw_scores = cushions / vols
        total_score = float(np.sum(raw_scores))
        if total_score > 1e-7:
            weights[active_mask] = raw_scores / total_score
        else:
            # Fall back to equal weight if all active cushions are near zero
            weights[active_mask] = 1.0 / float(n_active)
        return weights

    msg = f"Unknown allocation policy: {policy!r}. Must be 'equal', 'risk_parity', or 'cushion'."
    raise ValueError(msg)


def simulate_platform(
    instance: dict[str, Any],
    policy: str = "cushion",
    seed: int | None = None,
) -> dict[str, Any]:
    """Execute dynamic multi-pod simulation under drawdown stops and capital allocation.

    Args:
        instance: Problem instance dictionary from make_instance.
        policy: Capital allocation policy ('equal', 'risk_parity', or 'cushion').
        seed: Optional RNG override seed. If None, uses instance['seed'].

    Returns:
        Dictionary of platform performance metrics, survival statistics, and paths.
    """
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

    # Equi-correlation matrix with rho
    rho = float(instance.get("corr_rho", 0.15))
    corr = np.full((n_pods, n_pods), rho)
    np.fill_diagonal(corr, 1.0)
    l_chol = np.linalg.cholesky(corr)

    # Pre-generate correlated daily return innovations
    z_uncorr = rng.standard_normal((n_days, n_pods))
    z_corr = z_uncorr @ l_chol.T

    # Base unconstrained log-returns
    daily_returns_raw = (mus - 0.5 * sigmas**2) * dt + sigmas * sqrt_dt * z_corr

    # State tracking arrays
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

        # Evaluate stop-outs
        # Hard stop: permanently halts pod
        new_hard_stops = (current_dds >= hard_stops) & pod_active
        pod_active[new_hard_stops] = False
        stopped_out[new_hard_stops] = True

        if not np.any(pod_active):
            # All pods liquidated; platform is cash only
            platform_daily_returns.append(0.0)
            platform_wealth[t + 1] = platform_wealth[t]
            platform_peaks[t + 1] = platform_peaks[t]
            platform_drawdowns[t + 1] = (platform_peaks[t + 1] - platform_wealth[t + 1]) / platform_peaks[t + 1]
            continue

        # Soft stop: halves exposure / leverage if between soft and hard stop
        leverage_multipliers = np.ones(n_pods, dtype=float)
        in_soft_zone = (current_dds >= soft_stops) & (current_dds < hard_stops) & pod_active
        leverage_multipliers[in_soft_zone] = 0.5

        # Allocation weights
        weights = compute_allocation_weights(
            policy=policy,
            active_mask=pod_active,
            current_drawdowns=current_dds,
            hard_stops=hard_stops,
            sigmas=sigmas,
        )

        # Scaled pod returns for day t
        scaled_pod_returns = leverage_multipliers * daily_returns_raw[t]

        # Platform daily portfolio return
        r_plat = float(np.sum(weights * scaled_pod_returns))
        platform_daily_returns.append(r_plat)

        # Update pod wealth and peaks
        pod_wealth[pod_active] *= 1.0 + scaled_pod_returns[pod_active]
        pod_peaks = np.maximum(pod_peaks, pod_wealth)

        # Update platform wealth and peak
        platform_wealth[t + 1] = platform_wealth[t] * (1.0 + r_plat)
        platform_peaks[t + 1] = max(platform_peaks[t], platform_wealth[t + 1])
        platform_drawdowns[t + 1] = (platform_peaks[t + 1] - platform_wealth[t + 1]) / platform_peaks[t + 1]

    # Performance metrics
    plat_rets_arr = np.array(platform_daily_returns)
    mean_daily = float(np.mean(plat_rets_arr)) if len(plat_rets_arr) > 0 else 0.0
    std_daily = float(np.std(plat_rets_arr, ddof=1)) if len(plat_rets_arr) > 1 else 0.0

    ann_return = mean_daily * 252.0
    ann_vol = std_daily * math.sqrt(252.0)
    sharpe = ann_return / ann_vol if ann_vol > 1e-6 else 0.0

    platform_mdd = float(np.max(platform_drawdowns))
    calmar = ann_return / platform_mdd if platform_mdd > 1e-6 else 0.0

    # Churn metrics
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
