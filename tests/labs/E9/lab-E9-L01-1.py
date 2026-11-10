"""Lab 1: Public-debt dynamics, r minus g, and interest-rate-growth differentials.

SIMULATED 20-year debt trajectories. Standard library only.
Verifies exact discrete-time debt-to-GDP accumulation versus the linear approximation,
evaluating debt stability under r < g and explosive dynamics under r > g.
"""

from __future__ import annotations


def debt_step_exact(b_prev: float, r: float, g: float, s: float) -> float:
    """Compute exact discrete-time debt-to-GDP ratio for next period.

    Identity:
    b_t = [(1 + r) / (1 + g)] * b_{t-1} - s
    where:
    b is debt-to-GDP ratio,
    r is real interest rate,
    g is real GDP growth rate,
    s is primary balance as share of GDP (positive for surplus, negative for deficit).
    """
    if g <= -1.0:
        msg = f"Real GDP growth rate must be strictly greater than -1.0, got {g}"
        raise ValueError(msg)
    return ((1.0 + r) / (1.0 + g)) * b_prev - s


def debt_step_approx(b_prev: float, r: float, g: float, s: float) -> float:
    """Compute first-order linear approximation of debt-to-GDP ratio.

    Approximation:
    b_t = (1 + r - g) * b_{t-1} - s
    """
    return (1.0 + r - g) * b_prev - s


def steady_state_debt(r: float, g: float, s: float) -> float:
    """Compute stationary debt ratio b* when (1 + r) / (1 + g) < 1.

    At steady state:
    b* = -s / [ (r - g) / (1 + g) ]
    """
    growth_factor = (1.0 + r) / (1.0 + g)
    if growth_factor >= 1.0:
        msg = f"No stable steady state exists when (1 + r) / (1 + g) >= 1.0: factor={growth_factor:.4f}"
        raise ValueError(msg)
    return -s / (1.0 - growth_factor)


def main() -> None:
    # Baseline parameters (Blanchard 2019 regime: r < g)
    b0 = 0.80  # 80% initial debt-to-GDP
    r_low = 0.01  # 1.0% real rate
    g_normal = 0.03  # 3.0% real growth
    s_deficit = -0.015  # 1.5% primary deficit

    # 1. Verify steady state under r < g
    b_star = steady_state_debt(r_low, g_normal, s_deficit)

    # 2. Simulate 20 years under regime transition at t = 10
    # Years 1-10: r < g (r = 1.0%, g = 3.0%, s = -1.5%)
    # Years 11-20: r > g (r = 0.045, g = 0.015, s = -1.5% - sign flip shock)
    exact_path: list[float] = [b0]
    approx_path: list[float] = [b0]

    b_curr_exact = b0
    b_curr_approx = b0

    for t in range(1, 21):
        if t <= 10:
            r = r_low
            g = g_normal
        else:
            r = 0.045
            g = 0.015
        s = s_deficit

        b_curr_exact = debt_step_exact(b_curr_exact, r, g, s)
        b_curr_approx = debt_step_approx(b_curr_approx, r, g, s)

        exact_path.append(b_curr_exact)
        approx_path.append(b_curr_approx)

    print("=== Public Debt Dynamics: Exact vs Linear Approximation ===")
    print(f"Initial Debt Ratio b0:           {b0:.4f}")
    print(f"Regime 1 (r < g): r={r_low:.4f}, g={g_normal:.4f}, r-g={r_low - g_normal:.4f}, s={s_deficit:.4f}")
    print(f"Steady-State Debt Ratio b*:      {b_star:.4f}")
    print(f"Year 5 Debt Ratio (Exact):       {exact_path[5]:.4f}")
    print(f"Year 5 Debt Ratio (Approx):      {approx_path[5]:.4f}")
    print(f"Year 10 Debt Ratio (Exact):      {exact_path[10]:.4f}")
    print(f"Year 10 Debt Ratio (Approx):     {approx_path[10]:.4f}")
    print("\n=== Regime 2 Shock (t=11..20: r=0.045, g=0.015, r-g=+0.030) ===")
    print(f"Year 15 Debt Ratio (Exact):      {exact_path[15]:.4f}")
    print(f"Year 15 Debt Ratio (Approx):     {approx_path[15]:.4f}")
    print(f"Year 20 Debt Ratio (Exact):      {exact_path[20]:.4f}")
    print(f"Year 20 Debt Ratio (Approx):     {approx_path[20]:.4f}")
    print(f"Approximation Error at Year 20:  {abs(exact_path[20] - approx_path[20]):.4f}")

    assert 0.77 <= b_star <= 0.78, "Steady state debt ratio must be approximately 77.25%"
    assert exact_path[10] < b0, "Debt ratio must decline under r < g despite running primary deficit"
    assert exact_path[20] > 1.0, "Debt ratio must explode above 100% after r > g reversal"


main()
