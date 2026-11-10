"""CF3 lab L05-1: Board composition, monitoring intensity, and optimal independence.

Model: Economic model of internal board governance:
Fraction of independent directors gamma in [0, 1] balances external monitoring
benefits (reducing managerial extraction D(gamma) = D_0 * (1 - gamma))
against the informational and advisory cost of outside directors (C(gamma) = kappa * gamma^2).
Board size coordination frictions modeled following Yermack (1996).
Standard library only; closed-form analytical optimization and discrete grid analysis.
"""

from __future__ import annotations


def board_governance_value(
    v_base: float,
    d_0: float,
    kappa: float,
    gamma: float,
    board_size: int,
    optimal_size: int = 9,
    size_penalty_coeff: float = 0.25,
) -> dict[str, float]:
    """Calculate net firm value as a function of board independence and board size."""
    if not (0.0 <= gamma <= 1.0):
        raise ValueError(f"Board independence gamma must be in [0, 1], got {gamma}")
    if board_size < 3:
        raise ValueError(f"Board size must be at least 3, got {board_size}")

    # 1. Monitoring benefit: independent directors reduce managerial extraction
    diversion_cost = d_0 * (1.0 - gamma)

    # 2. Advisory / information cost of outside directors
    advisory_cost = kappa * (gamma**2)

    # 3. Yermack (1996) board size coordination and free-rider penalty
    size_friction = size_penalty_coeff * ((board_size - optimal_size) ** 2)

    net_firm_value = v_base - diversion_cost - advisory_cost - size_friction

    return {
        "gamma": gamma,
        "board_size": float(board_size),
        "diversion_cost": diversion_cost,
        "advisory_cost": advisory_cost,
        "size_friction": size_friction,
        "net_firm_value": net_firm_value,
    }


def find_optimal_independence(d_0: float, kappa: float) -> float:
    """Analytical optimal independence fraction: dV/d_gamma = d_0 - 2 * kappa * gamma = 0."""
    if kappa <= 0.0:
        return 1.0
    gamma_star = d_0 / (2.0 * kappa)
    return max(0.0, min(1.0, gamma_star))


def main() -> None:
    print("CF3 Lab L05-1: Optimal Board Independence and Governance Trade-Offs")
    print("=================================================================")

    v_base = 100.0  # $100M base potential enterprise value
    d_0 = 24.0  # Max managerial diversion under zero monitoring ($24M)
    kappa = 16.0  # Information friction parameter ($16M)
    optimal_size = 8

    # Analytical optimum
    gamma_opt = find_optimal_independence(d_0, kappa)
    opt_res = board_governance_value(v_base, d_0, kappa, gamma_opt, board_size=optimal_size)

    print("Theoretical Parameters:")
    print(f"  Base enterprise potential (V_base): ${v_base:.2f}M")
    print(f"  Unmonitored agency diversion (D_0): ${d_0:.2f}M")
    print(f"  Advisory information cost (kappa):  ${kappa:.2f}M")
    print(f"  Optimal board independence (gamma*): {gamma_opt:.2%} ({gamma_opt:.4f})")
    print(f"  Maximum enterprise value:           ${opt_res['net_firm_value']:.4f}M")

    print("\nIndependence Grid (Board Size = 8 directors):")
    hdr = f"  {'gamma':>7} | {'Diversion':>12} | {'Advisory':>12} | {'Net Value':>12} | {'Indep Dirs':>10}"
    print(hdr)
    print("  " + "-" * 57)

    for g_pct in range(0, 101, 10):
        g = g_pct / 100.0
        res = board_governance_value(v_base, d_0, kappa, g, board_size=8)
        n_indep = round(g * 8)
        row = (
            f"  {g:7.2f} | {res['diversion_cost']:12.2f} | {res['advisory_cost']:12.2f} | "
            f"{res['net_firm_value']:12.2f} | {n_indep:6d} / 8"
        )
        print(row)

    print("\nBoard Size Coordination Friction (Holding gamma = 0.75):")
    print(f"  {'Board Size':>10} | {'Size Friction ($M)':>18} | {'Net Value ($M)':>15}")
    print("  " + "-" * 48)
    for n_board in [5, 7, 8, 9, 12, 16, 20]:
        res_size = board_governance_value(v_base, d_0, kappa, gamma=0.75, board_size=n_board, optimal_size=8)
        print(f"  {n_board:10d} | {res_size['size_friction']:18.2f} | {res_size['net_firm_value']:15.2f}")


main()
