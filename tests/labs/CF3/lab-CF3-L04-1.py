"""CF3 lab L04-1: Free cash flow agency problem and debt as a bonding device (Jensen 1986).

Model: Michael Jensen (1986) free cash flow hypothesis:
Operating cash flow C exceeds funding needs of positive-NPV projects I* (FCF = C - I* > 0).
Compares:
1. Unconstrained equity governance: manager undertakes negative-NPV empire-building projects.
2. Debt bonding mechanism: hard debt service commits cash flow to payout, eliminating overinvestment.
Standard library only; exact closed-form comparative statics.
"""

from __future__ import annotations


def evaluate_fcf_governance(
    operating_cash: float,
    positive_npv_investment: float,
    positive_npv_return: float,
    pet_project_return: float,
    manager_empire_utility_weight: float,
    debt_service_commitment: float,
) -> dict[str, float]:
    """Evaluate free cash flow allocation under unconstrained governance vs debt bonding."""
    # Free cash flow after positive-NPV project
    npv_positive_project = positive_npv_investment * (positive_npv_return - 1.0)
    fcf = operating_cash - positive_npv_investment

    # Policy 1: No debt commitment (D = 0)
    # Manager has unconstrained discretion over FCF.
    # If manager derives private utility from empire building, manager invests FCF into pet project
    pet_investment_unconstrained = fcf
    npv_pet_unconstrained = pet_investment_unconstrained * (pet_project_return - 1.0)  # Negative
    total_wealth_unconstrained = operating_cash + npv_positive_project + npv_pet_unconstrained

    # Policy 2: Debt commitment (D = debt_service_commitment)
    # Cash remaining after debt service and positive-NPV investment
    cash_after_debt = max(0.0, operating_cash - debt_service_commitment)
    # Positive NPV project is prioritized
    invested_in_good = min(cash_after_debt, positive_npv_investment)
    remaining_fcf_bonded = max(0.0, cash_after_debt - invested_in_good)

    # Pet project funded only if cash remains after debt and positive-NPV project
    pet_investment_bonded = remaining_fcf_bonded
    npv_pet_bonded = pet_investment_bonded * (pet_project_return - 1.0)

    # Total shareholder wealth under debt commitment
    # (Debt receives debt_service_commitment, equity receives remaining cash flows)
    total_wealth_bonded = operating_cash + npv_positive_project + npv_pet_bonded

    agency_cost_of_fcf = total_wealth_bonded - total_wealth_unconstrained

    return {
        "operating_cash": operating_cash,
        "fcf": fcf,
        "npv_good_project": npv_positive_project,
        "pet_investment_unconstrained": pet_investment_unconstrained,
        "npv_pet_unconstrained": npv_pet_unconstrained,
        "total_wealth_unconstrained": total_wealth_unconstrained,
        "debt_service": debt_service_commitment,
        "pet_investment_bonded": pet_investment_bonded,
        "npv_pet_bonded": npv_pet_bonded,
        "total_wealth_bonded": total_wealth_bonded,
        "agency_cost_eliminated": agency_cost_of_fcf,
    }


def main() -> None:
    print("CF3 Lab L04-1: Free Cash Flow Agency Problem & Debt Bonding (Jensen 1986)")
    print("=====================================================================")

    operating_cash = 100.0  # $100M internal operating cash flow
    good_project_inv = 40.0  # $40M optimal positive-NPV investment
    good_return = 1.30  # 30% gross return (NPV = +$12M)
    pet_return = 0.65  # 65% gross return (severe negative NPV: -35% loss)
    empire_weight = 0.10

    # Case 1: Unconstrained equity governance (D = $0)
    res_zero = evaluate_fcf_governance(
        operating_cash,
        good_project_inv,
        good_return,
        pet_return,
        empire_weight,
        debt_service_commitment=0.0,
    )

    print("Baseline Corporate Cash Flow & Opportunities:")
    print(f"  Operating cash flow (C):          ${operating_cash:.2f}M")
    print(f"  Optimal positive-NPV capex (I*):  ${good_project_inv:.2f}M")
    print(f"  Positive-NPV project value:       +${res_zero['npv_good_project']:.2f}M")
    print(f"  Free Cash Flow (FCF = C - I*):    ${res_zero['fcf']:.2f}M")

    print("\nCase 1: Unconstrained Governance (Zero Debt, D = $0M):")
    print(f"  FCF absorbed by pet projects:     ${res_zero['pet_investment_unconstrained']:.2f}M")
    print(f"  Net wealth destroyed by pet capex:${res_zero['npv_pet_unconstrained']:.2f}M (-35% return)")
    print(f"  Total Enterprise Value created:   ${res_zero['total_wealth_unconstrained']:.2f}M")

    # Case 2: Optimal Debt Bonding (D = $60M, matching FCF)
    res_bonded = evaluate_fcf_governance(
        operating_cash,
        good_project_inv,
        good_return,
        pet_return,
        empire_weight,
        debt_service_commitment=60.0,
    )

    print("\nCase 2: Disciplinary Debt Commitment (D = $60M):")
    print(f"  Hard debt service paid to bondholders: ${res_bonded['debt_service']:.2f}M")
    print(f"  Remaining FCF in firm:                 ${res_bonded['pet_investment_bonded']:.2f}M")
    print(f"  Pet project overinvestment:            ${res_bonded['pet_investment_bonded']:.2f}M")
    print(f"  Total Enterprise Value created:        ${res_bonded['total_wealth_bonded']:.2f}M")
    print(f"  Value created by debt bonding:        +${res_bonded['agency_cost_eliminated']:.2f}M")

    print("\nSensitivity: Debt Commitment vs Enterprise Value Created:")
    print(f"  {'Debt Service ($M)':>18} | {'Pet Capex ($M)':>16} | {'Enterprise Value ($M)':>22}")
    print("  " + "-" * 62)
    for d_val in [0.0, 15.0, 30.0, 45.0, 60.0]:
        s = evaluate_fcf_governance(
            operating_cash,
            good_project_inv,
            good_return,
            pet_return,
            empire_weight,
            debt_service_commitment=d_val,
        )
        print(f"  {d_val:18.1f} | {s['pet_investment_bonded']:16.1f} | {s['total_wealth_bonded']:22.2f}")


main()
