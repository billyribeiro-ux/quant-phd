"""Reference solution for E9 Sovereign DSA and Fan Chart project.

Implements exact debt dynamics step, primary gap calculation,
deterministic trajectory projection, fan chart percentile extraction,
and debt ceiling breach probability estimation.
Standard library only. Fully typed.
"""

from __future__ import annotations


def debt_dynamics_step(b_prev: float, r: float, g: float, s: float) -> float:
    """Compute one-period exact discrete-time debt-to-GDP ratio.

    Formula:
    b_t = [(1 + r) / (1 + g)] * b_{t-1} - s

    Raises:
    ValueError if g <= -1.0, r <= -1.0, or b_prev < 0.0.
    """
    if g <= -1.0:
        msg = f"Real growth rate must be strictly greater than -1.0: got g={g}"
        raise ValueError(msg)
    if r <= -1.0:
        msg = f"Real interest rate must be strictly greater than -1.0: got r={r}"
        raise ValueError(msg)
    if b_prev < 0.0:
        msg = f"Debt-to-GDP ratio cannot be negative: got b_prev={b_prev}"
        raise ValueError(msg)

    return ((1.0 + r) / (1.0 + g)) * b_prev - s


def primary_gap(b_target: float, r: float, g: float, s_actual: float) -> float:
    """Compute primary balance gap s* - s required to stabilize debt at b_target.

    Formula:
    s* = [(r - g) / (1 + g)] * b_target
    gap = s* - s_actual
    A positive gap indicates that fiscal tightening is required to prevent debt expansion.
    """
    if g <= -1.0:
        msg = f"Real growth rate must be strictly greater than -1.0: got g={g}"
        raise ValueError(msg)
    if b_target < 0.0:
        msg = f"Target debt ratio cannot be negative: got b_target={b_target}"
        raise ValueError(msg)

    s_star = ((r - g) / (1.0 + g)) * b_target
    return s_star - s_actual


def simulate_trajectory(
    b0: float,
    r_path: list[float],
    g_path: list[float],
    s_path: list[float],
) -> list[float]:
    """Deterministically simulate debt-to-GDP trajectory from t=0 to t=H.

    Returns a list of length H + 1 starting with b0.
    Raises ValueError if paths have unequal length or are empty.
    """
    if not r_path or len(r_path) != len(g_path) or len(r_path) != len(s_path):
        msg = (
            f"Paths must be non-empty and of equal length: "
            f"len(r)={len(r_path)}, len(g)={len(g_path)}, len(s)={len(s_path)}"
        )
        raise ValueError(msg)

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
    """Compute percentile curves across simulated paths for each period t in 0..H.

    Returns a dictionary mapping each percentile p to a list of length H + 1.
    Raises ValueError if trajectories are empty, inconsistent in length, or percentiles invalid.
    """
    if not trajectories:
        msg = "Trajectories list must not be empty"
        raise ValueError(msg)

    h_len = len(trajectories[0])
    for idx, path in enumerate(trajectories):
        if len(path) != h_len:
            msg = f"Path {idx} has length {len(path)}, expected {h_len}"
            raise ValueError(msg)

    for p in percentiles:
        if not 0.0 <= p <= 1.0:
            msg = f"Percentile must be in [0, 1], got {p}"
            raise ValueError(msg)

    results: dict[float, list[float]] = {p: [] for p in percentiles}
    n_paths = len(trajectories)

    for t in range(h_len):
        cross_section = sorted(path[t] for path in trajectories)
        for p in percentiles:
            idx = round(p * (n_paths - 1))
            results[p].append(cross_section[idx])

    return results


def breach_probability(trajectories: list[list[float]], debt_ceiling: float) -> float:
    """Compute empirical probability of exceeding debt_ceiling at any point across horizon.

    Returns fraction of paths where max_t(b_t) > debt_ceiling.
    """
    if not trajectories:
        return 0.0
    breached_count = sum(1 for path in trajectories if any(b > debt_ceiling for b in path))
    return breached_count / len(trajectories)


def dsa_summary(instance_data: dict[str, object]) -> dict[str, object]:
    """Execute complete DSA pipeline on instance dictionary.

    Required keys: 'b0', 'r_path', 'g_path', 's_path', 'mc_paths', 'debt_ceiling', 'target_debt'.
    Returns enriched dictionary with baseline trajectory, fan chart, breach risk, and sustainability.
    """
    required_keys = ("b0", "r_path", "g_path", "s_path", "mc_paths", "debt_ceiling", "target_debt")
    for k in required_keys:
        if k not in instance_data:
            msg = f"Missing required instance key: {k}"
            raise ValueError(msg)

    raw_b0 = instance_data["b0"]
    assert isinstance(raw_b0, (int, float))
    b0 = float(raw_b0)

    raw_r = instance_data["r_path"]
    assert isinstance(raw_r, list)
    r_path = [float(x) for x in raw_r]

    raw_g = instance_data["g_path"]
    assert isinstance(raw_g, list)
    g_path = [float(x) for x in raw_g]

    raw_s = instance_data["s_path"]
    assert isinstance(raw_s, list)
    s_path = [float(x) for x in raw_s]

    raw_mc = instance_data["mc_paths"]
    assert isinstance(raw_mc, list)
    mc_paths: list[list[float]] = [[float(v) for v in path] for path in raw_mc]

    raw_ceiling = instance_data["debt_ceiling"]
    assert isinstance(raw_ceiling, (int, float))
    debt_ceiling = float(raw_ceiling)

    raw_target = instance_data["target_debt"]
    assert isinstance(raw_target, (int, float))
    target_debt = float(raw_target)

    baseline_trajectory = simulate_trajectory(b0, r_path, g_path, s_path)
    terminal_debt = baseline_trajectory[-1]

    gaps = [primary_gap(target_debt, r, g, s) for r, g, s in zip(r_path, g_path, s_path, strict=True)]
    max_gap = max(gaps)

    percentiles = [0.10, 0.25, 0.50, 0.75, 0.90]
    fan_chart = compute_fan_chart(mc_paths, percentiles)
    p_breach = breach_probability(mc_paths, debt_ceiling)

    # Debt is sustainable if terminal debt does not exceed initial debt by more than 5%
    # and breach probability is below 35%
    is_sustainable = bool(terminal_debt <= b0 * 1.05 and p_breach < 0.35)

    return {
        "baseline_trajectory": baseline_trajectory,
        "terminal_debt": terminal_debt,
        "max_primary_gap": max_gap,
        "fan_chart": fan_chart,
        "breach_probability": p_breach,
        "is_sustainable": is_sustainable,
    }
