"""CF3 lab L03-1: Agency costs of outside equity (Jensen & Meckling 1976).

Model: Formal closed-form model of managerial perquisite consumption and agency loss:
Managerial ownership fraction alpha in (0, 1].
Firm market value V(P) = V_0 - P, where P is non-pecuniary perquisites.
Manager utility: U(P) = alpha * (V_0 - P) + b * sqrt(P).
Computes optimal perks P*(alpha), firm value, outside equity discount, and residual agency loss.
Standard library only; exact analytical solutions.
"""

from __future__ import annotations

import math


def jensen_meckling_agency_equilibrium(
    v_0: float,
    b_perk: float,
    alpha: float,
) -> dict[str, float]:
    """Solve the Jensen-Meckling (1976) perquisite consumption equilibrium for given alpha."""
    if not (0.0 < alpha <= 1.0):
        raise ValueError(f"alpha must be in (0, 1], got {alpha}")

    # Manager maximizes U_M(P) = alpha * (V_0 - P) + b * sqrt(P)
    # FOC: dU/dP = -alpha + b / (2 * sqrt(P)) = 0
    # => sqrt(P) = b / (2 * alpha) => P* = (b / (2 * alpha))^2
    # Cap perks at V_0 to ensure non-negative enterprise value
    p_opt = min(v_0 * 0.95, (b_perk / (2.0 * alpha)) ** 2)

    # Firm market value
    firm_value = v_0 - p_opt

    # Value of outside equity: rational market prices outside shares knowing manager will consume P*
    outside_share = 1.0 - alpha
    outside_equity_value = outside_share * firm_value

    # Manager's utility components
    manager_equity_value = alpha * firm_value
    manager_perk_utility = b_perk * math.sqrt(p_opt)
    manager_total_payoff = manager_equity_value + manager_perk_utility

    return {
        "alpha": alpha,
        "perks": p_opt,
        "firm_value": firm_value,
        "outside_equity": outside_equity_value,
        "manager_equity": manager_equity_value,
        "manager_perk_utility": manager_perk_utility,
        "manager_total_payoff": manager_total_payoff,
    }


def main() -> None:
    print("CF3 Lab L03-1: Jensen & Meckling (1976) Agency Costs of Outside Equity")
    print("====================================================================")

    v_0 = 100.0  # $100M uncompromised enterprise potential
    b_perk = 4.0  # Perquisite utility scaling parameter

    # First-best benchmark: 100% Owner-Manager (alpha = 1.0)
    fb = jensen_meckling_agency_equilibrium(v_0, b_perk, alpha=1.0)

    print("First-Best Benchmark (100% Owner-Manager, alpha = 1.0):")
    print(f"  Firm potential V_0:             ${v_0:.2f}M")
    print(f"  First-best perks P*(1.0):       ${fb['perks']:.4f}M")
    print(f"  First-best firm value:          ${fb['firm_value']:.4f}M")
    print(f"  Manager total utility payoff:   ${fb['manager_total_payoff']:.4f}M")

    print("\nImpact of Diluting Managerial Ownership (alpha < 1.0):")
    hdr = f"  {'alpha':>6} | {'Perks P*':>12} | {'Firm Value':>14} | {'Outside Eq':>14} | {'Agency Loss':>14}"
    print(hdr)
    print("  " + "-" * 66)

    for alpha_pct in [100, 80, 60, 50, 40, 30, 20, 10]:
        alpha_val = alpha_pct / 100.0
        res = jensen_meckling_agency_equilibrium(v_0, b_perk, alpha_val)

        # Agency cost (deadweight residual loss) = difference in total value relative to alpha = 1.0
        # Total social surplus = Firm Value + Perk Utility
        welfare_loss = (fb["firm_value"] + fb["manager_perk_utility"]) - (
            res["firm_value"] + res["manager_perk_utility"]
        )

        row = (
            f"  {alpha_val:6.2f} | {res['perks']:12.4f} | {res['firm_value']:14.4f} | "
            f"{res['outside_equity']:14.4f} | {welfare_loss:14.4f}"
        )
        print(row)


main()
