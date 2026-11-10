"""CF2 lab L06-1: MM with taxes and distress costs: the optimal-leverage curve.

Curriculum Lab (curriculum/02-economics-finance-core.yaml:725).
Model: Static trade-off theory with corporate taxes and expected financial distress costs.
Firm value: V(D) = V_U + tau_c * D - PV(distress costs).
Distress function: PV(distress) = alpha * V_U * (D / V_U)^3, representing convex expected
direct and indirect costs of distress.
Enumerates over a stated finite grid to identify the optimal leverage ratio.
"""

from __future__ import annotations

import math

V_U = 100_000_000.0  # $100M unlevered enterprise value
TAU_C = 0.25  # 25% corporate tax rate
ALPHA = 0.30  # Distress cost intensity (30% of V_U lost upon severe distress)
GRID_STEP = 1_000_000.0  # $1M grid step


def pv_tax_shield(debt: float) -> float:
    return TAU_C * debt


def pv_distress(debt: float) -> float:
    debt_ratio = debt / V_U
    return ALPHA * V_U * (debt_ratio**3)


def total_firm_value(debt: float) -> float:
    return V_U + pv_tax_shield(debt) - pv_distress(debt)


def main() -> None:
    print("CF2 Lab L06-1: Trade-Off Theory Optimal Leverage Curve")
    print("-----------------------------------------------------")
    print(f"Unlevered firm value (V_U): ${V_U:,.2f}")
    print(f"Corporate tax rate (tau_c):  {TAU_C:.1%}")
    print(f"Distress severity factor:    {ALPHA:.1%}")
    print(f"Grid search step:            ${GRID_STEP:,.2f}")

    # Exact analytical first-order condition:
    # dV/dD = tau_c - 3 * ALPHA * (D / V_U)^2 = 0
    # D* / V_U = sqrt(tau_c / (3 * ALPHA))
    analytical_ratio = math.sqrt(TAU_C / (3.0 * ALPHA))
    analytical_opt_d = analytical_ratio * V_U

    # Discrete grid evaluation
    max_d = 100_000_000.0
    n_points = int(max_d / GRID_STEP) + 1
    grid_d = [i * GRID_STEP for i in range(n_points)]

    best_d = 0.0
    best_val = -math.inf
    curve: list[tuple[float, float, float, float]] = []

    for d in grid_d:
        shield = pv_tax_shield(d)
        distress = pv_distress(d)
        val = total_firm_value(d)
        curve.append((d, shield, distress, val))
        if val > best_val:
            best_val = val
            best_d = d

    print("\nOptimal Leverage Curve (Selected Grid Points):")
    print(f"{'Debt ($M)':>10} | {'PV(Shield)':>11} | {'PV(Distress)':>12} | {'Value ($M)':>11} | {'Marginal Net':>12}")
    print("-" * 66)

    sample_points = [0.0, 20.0, 40.0, 50.0, 52.0, 53.0, 60.0, 80.0, 100.0]
    for d_mil in sample_points:
        d = d_mil * 1_000_000.0
        sh = pv_tax_shield(d)
        dis = pv_distress(d)
        v = total_firm_value(d)
        # Marginal net benefit: tau_c - 3 * alpha * (D/V_U)^2
        marginal = TAU_C - 3.0 * ALPHA * ((d / V_U) ** 2)
        print(f"{d_mil:10.1f} | ${sh / 1e6:9.2f}M | ${dis / 1e6:10.2f}M | ${v / 1e6:9.2f}M | {marginal:12.4f}")

    print("-" * 66)
    print(f"Analytical optimal debt:    ${analytical_opt_d / 1e6:.4f}M (leverage {analytical_ratio:.2%})")
    opt_summary = f"${best_d / 1e6:.2f}M (value = ${best_val / 1e6:.4f}M, step = ${GRID_STEP / 1e6:.1f}M)"
    print(f"Grid search optimal debt:   {opt_summary}")
    print(f"Interior optimum confirmed: {0.0 < best_d < V_U}")
    print(f"Difference from analytical: ${abs(best_d - analytical_opt_d):,.2f}")


main()
