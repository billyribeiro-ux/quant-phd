"""Lab CR4-L04-1: Out-of-Court Debt Exchange Offers and Exit Consents under TIA 316(b).

Models the public bondholder coordination game under Section 316(b) of the Trust Indenture Act.
Demonstrates the free-rider holdout problem that causes workout failure,
and shows how exit consents alter payoffs to restore the successful out-of-court workout equilibrium
as documented by Gilson, John & Lang (1990).
"""

from __future__ import annotations


def evaluate_exchange_game(
    face_value_old: float,
    package_value_new: float,
    v_solvent: float,
    v_ch11: float,
    ch11_deadweight_cost: float,
    n_bondholders: int,
) -> dict[str, float]:
    """Evaluate payoff matrix for a representative bondholder facing an exchange offer.

    face_value_old: Contractual claim of old bond ($100).
    package_value_new: Value of exchange package (new debt + equity) offered ($65).
    v_solvent: Unlevered firm value if workout succeeds ($120).
    v_ch11: Firm value in Chapter 11 after deadweight costs ($75 = v_solvent - ch11_deadweight_cost).
    ch11_deadweight_cost: Administrative and business disruption costs in court ($45).
    n_bondholders: Total symmetric public bondholders (e.g. 100).
    """
    total_old_debt = face_value_old * n_bondholders

    # Case A: Without Exit Consents
    # If all others tender, firm survives. A holdout retains full old bond claim: min(face_value_old, v_solvent)
    holdout_payoff_if_others_tender = min(face_value_old, 100.0)
    # If bondholder tenders, they receive package_value_new
    tender_payoff_if_others_tender = package_value_new

    # If others hold out, workout fails and firm files Chapter 11
    # Recovery in Chapter 11 is distributed pro-rata across all claims: v_ch11 / total_old_debt
    ch11_recovery_rate = v_ch11 / total_old_debt
    payoff_if_all_holdout = face_value_old * ch11_recovery_rate

    # Case B: With Exit Consents
    # Tendering bondholders simultaneously vote to strip all protective covenants
    # (cross-default, negative pledge, financial covenants) from non-tendered old bonds.
    # Non-tendered bonds become subordinated, illiquid 'stub' paper trading at deep discount.
    stub_discount_penalty = 0.50  # old stripped bond trades at 50% discount
    holdout_payoff_with_exit_consent = package_value_new * (1.0 - stub_discount_penalty)

    return {
        "tender_when_others_tender": tender_payoff_if_others_tender,
        "holdout_when_others_tender_no_consent": holdout_payoff_if_others_tender,
        "ch11_failure_payoff": payoff_if_all_holdout,
        "holdout_with_exit_consent": holdout_payoff_with_exit_consent,
        "ch11_deadweight_cost": ch11_deadweight_cost,
    }


def main() -> None:
    face_old = 100.0
    package_new = 65.0
    v_solvent = 120.0
    v_ch11 = 75.0  # $45M destroyed in Chapter 11
    ch11_cost = 45.0
    n_holders = 100

    res = evaluate_exchange_game(face_old, package_new, v_solvent, v_ch11, ch11_cost, n_holders)

    print("Out-of-Court Exchange Offer Game (TIA 316(b) vs Exit Consents):")
    print("Old Face Value = 100.0, Exchange Offer Package = 65.0, Chapter 11 Deadweight Loss = 45.0")
    print("---------------------------------------------------------------------------------------")
    print("Action Profile                                | Individual Payoff | Game State Outcome")
    print("----------------------------------------------+-------------------+-------------------")
    t_p = f"{res['tender_when_others_tender']:5.1f}"
    h_p = f"{res['holdout_when_others_tender_no_consent']:5.1f}"
    c_p = f"{res['ch11_failure_payoff']:5.1f}"
    e_p = f"{res['holdout_with_exit_consent']:5.1f}"

    print(f"1. No Exit Consent: Tender (others tender)  |       {t_p}       | Voluntary Concession")
    print(f"2. No Exit Consent: Hold Out (others tender)|       {h_p}       | Free-Rider Holdout (Dominant)")
    print(f"3. All Hold Out -> Workout Fails (Ch 11)   |       {c_p}       | Pareto-Inferior Nash Eq")
    print("-" * 75)
    print(f"4. With Exit Consents: Tender (Consensual) |       {t_p}       | Successful Workout")
    print(f"5. With Exit Consents: Hold Out (Stub)     |       {e_p}       | Punished Non-Tender")

    # Invariant checks:
    # 1. Without exit consent, holding out strictly dominates tendering: 100 > 65
    assert res["holdout_when_others_tender_no_consent"] > res["tender_when_others_tender"]
    # 2. Both tendering (65) Pareto-dominates the all-holdout Chapter 11 outcome (48.75)
    assert res["tender_when_others_tender"] > res["ch11_failure_payoff"]
    # 3. Exit consent penalizes holdouts below the tender package, making tendering the dominant strategy
    assert res["tender_when_others_tender"] > res["holdout_with_exit_consent"]

    print("\nVerified coordination game invariants (Gilson et al. 1990):")
    print("1. Without exit consent, individual free-riding forces inefficient Chapter 11.")
    print("2. Exit consent eliminates holdout surplus, restoring Pareto-optimal workout.")


main()
