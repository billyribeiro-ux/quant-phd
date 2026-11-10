"""Mutant 5: Evaluates debt ceiling breach only at terminal horizon t=H instead of anytime max.

Fails anytime breach probability test when debt peaks mid-horizon and subsides.
"""

from __future__ import annotations


def debt_dynamics_step(b_prev: float, r: float, g: float, s: float) -> float:
    if g <= -1.0:
        raise ValueError(f"Real growth rate must be strictly greater than -1.0: got g={g}")
    if r <= -1.0:
        raise ValueError(f"Real interest rate must be strictly greater than -1.0: got r={r}")
    if b_prev < 0.0:
        raise ValueError(f"Debt-to-GDP ratio cannot be negative: got b_prev={b_prev}")
    return ((1.0 + r) / (1.0 + g)) * b_prev - s


def primary_gap(b_target: float, r: float, g: float, s_actual: float) -> float:
    if g <= -1.0:
        raise ValueError(f"Real growth rate must be strictly greater than -1.0: got g={g}")
    if b_target < 0.0:
        raise ValueError(f"Target debt ratio cannot be negative: got b_target={b_target}")
    s_star = ((r - g) / (1.0 + g)) * b_target
    return s_star - s_actual


def simulate_trajectory(
    b0: float,
    r_path: list[float],
    g_path: list[float],
    s_path: list[float],
) -> list[float]:
    if not r_path or len(r_path) != len(g_path) or len(r_path) != len(s_path):
        raise ValueError("Paths must be non-empty and of equal length")
    trajectory = [b0]
    b_curr = b0
    for r, g, s in zip(r_path, g_path, s_path, strict=True):
        b_curr = debt_dynamics_step(b_curr, r, g, s)
        trajectory.append(b_curr)
    return trajectory


def compute_fan_chart(
    trajectories: list[list[float]],
    percentiles: list[float],
) -> dict[float, list[float]]:
    if not trajectories:
        raise ValueError("Trajectories list must not be empty")
    h_len = len(trajectories[0])
    for p in percentiles:
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"Percentile must be in [0, 1], got {p}")
    results: dict[float, list[float]] = {p: [] for p in percentiles}
    n_paths = len(trajectories)
    for t in range(h_len):
        cross_section = sorted(path[t] for path in trajectories)
        for p in percentiles:
            idx = round(p * (n_paths - 1))
            results[p].append(cross_section[idx])
    return results


def breach_probability(trajectories: list[list[float]], debt_ceiling: float) -> float:
    if not trajectories:
        return 0.0
    # BUG: only checking terminal horizon point path[-1] instead of any(b > ceiling)
    breached_count = sum(1 for path in trajectories if path[-1] > debt_ceiling)
    return breached_count / len(trajectories)


def dsa_summary(instance_data: dict[str, object]) -> dict[str, object]:
    required_keys = ("b0", "r_path", "g_path", "s_path", "mc_paths", "debt_ceiling", "target_debt")
    for k in required_keys:
        if k not in instance_data:
            raise ValueError(f"Missing required key: {k}")
    b0 = float(str(instance_data["b0"]))
    r_path = [float(x) for x in list(instance_data["r_path"])]  # type: ignore[arg-type]
    g_path = [float(x) for x in list(instance_data["g_path"])]  # type: ignore[arg-type]
    s_path = [float(x) for x in list(instance_data["s_path"])]  # type: ignore[arg-type]
    raw_mc = instance_data["mc_paths"]
    mc_paths: list[list[float]] = [[float(v) for v in path] for path in list(raw_mc)]  # type: ignore[union-attr]
    debt_ceiling = float(str(instance_data["debt_ceiling"]))
    target_debt = float(str(instance_data["target_debt"]))

    baseline_trajectory = simulate_trajectory(b0, r_path, g_path, s_path)
    terminal_debt = baseline_trajectory[-1]
    gaps = [primary_gap(target_debt, r, g, s) for r, g, s in zip(r_path, g_path, s_path, strict=True)]
    max_gap = max(gaps)
    percentiles = [0.10, 0.25, 0.50, 0.75, 0.90]
    fan_chart = compute_fan_chart(mc_paths, percentiles)
    p_breach = breach_probability(mc_paths, debt_ceiling)
    is_sustainable = bool(terminal_debt <= b0 * 1.05 and p_breach < 0.35)

    return {
        "baseline_trajectory": baseline_trajectory,
        "terminal_debt": terminal_debt,
        "max_primary_gap": max_gap,
        "fan_chart": fan_chart,
        "breach_probability": p_breach,
        "is_sustainable": is_sustainable,
    }
