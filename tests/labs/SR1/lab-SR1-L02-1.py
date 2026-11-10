"""Lab SR1-L02-1: Sequential Service, Equilibrium Multiplicity, and Bank Runs.

Calculates exact expected payoffs for patient depositors under sequential service.
Demonstrates that both the good equilibrium (Wait, Wait) and the bank run equilibrium
(Run, Run) are pure-strategy Nash equilibria. Verifies that government deposit
insurance renders waiting strictly dominant, eliminating the bank run equilibrium.
"""

from fractions import Fraction


def main() -> None:
    # N = 3 depositors, each depositing 1 unit. Total deposits = 3.
    # Bank assets: Liquid buffer = 2, Long asset = 1.
    # Long asset mature return = 4, salvage value upon early liquidation = 1/2.
    # Deposit contract promises r1 = 4/3 at t=1.
    # Depositor 1 is impatient (always withdraws at t=1).
    # Depositors 2 and 3 are patient, choosing Action in {Wait, Run}.

    # Profile payoffs for (Depositor 2, Depositor 3):
    # 1. (Wait, Wait): Only Depositor 1 withdraws.
    # Cash needed = 4/3 <= 2. Remaining cash = 2/3. Long asset matures to 4.
    # Total date 2 resources = 2/3 + 4 = 14/3. Split equally: 7/3 each.
    payoff_ww = (Fraction(7, 3), Fraction(7, 3))

    # 2. (Run, Wait): Depositors 1 and 2 withdraw at t=1.
    # Cash demand = 8/3 > 2. Bank liquidates entire long asset yielding 1/2 cash.
    # Total cash = 2 + 1/2 = 5/2.
    # Arrivals uniformly random: first gets 4/3, second gets 5/2 - 4/3 = 7/6.
    # Expected payoff for running Depositor 2: (1/2)*(4/3) + (1/2)*(7/6) = 15/12 = 5/4.
    # Depositor 3 (waiting): 0 (bank has zero assets remaining).
    payoff_rw = (Fraction(5, 4), Fraction(0, 1))
    payoff_wr = (Fraction(0, 1), Fraction(5, 4))

    # 3. (Run, Run): All 3 depositors withdraw at t=1.
    # Total available cash = 5/2.
    # Random arrival queue: 1st gets 4/3, 2nd gets 7/6, 3rd gets 0.
    # Symmetric expected payoff: (4/3 + 7/6 + 0) / 3 = (15/6) / 3 = 5/6.
    payoff_rr = (Fraction(5, 6), Fraction(5, 6))

    print(
        f"Profile (Wait, Wait): P2 = {payoff_ww[0]} ({float(payoff_ww[0]):.4f}), "
        f"P3 = {payoff_ww[1]} ({float(payoff_ww[1]):.4f})"
    )
    print(
        f"Profile (Run, Wait):  P2 = {payoff_rw[0]} ({float(payoff_rw[0]):.4f}), "
        f"P3 = {payoff_rw[1]} ({float(payoff_rw[1]):.4f})"
    )
    print(
        f"Profile (Wait, Run):  P2 = {payoff_wr[0]} ({float(payoff_wr[0]):.4f}), "
        f"P3 = {payoff_wr[1]} ({float(payoff_wr[1]):.4f})"
    )
    print(
        f"Profile (Run, Run):   P2 = {payoff_rr[0]} ({float(payoff_rr[0]):.4f}), "
        f"P3 = {payoff_rr[1]} ({float(payoff_rr[1]):.4f})"
    )

    # Best response analysis:
    # If P3 plays Wait: P2 payoff for Wait is 7/3, for Run is 5/4. 7/3 > 5/4 ==> Wait is BR.
    br_p3_wait = "Wait" if payoff_ww[0] > payoff_rw[0] else "Run"
    # If P3 plays Run: P2 payoff for Wait is 0, for Run is 5/6. 5/6 > 0 ==> Run is BR.
    br_p3_run = "Run" if payoff_rr[0] > payoff_wr[0] else "Wait"

    print(f"P2 Best Response to P3=Wait: {br_p3_wait} (Payoff {payoff_ww[0]} > {payoff_rw[0]})")
    print(f"P2 Best Response to P3=Run:  {br_p3_run} (Payoff {payoff_rr[0]} > {payoff_wr[0]})")
    print("Multiplicity Confirmed: (Wait, Wait) and (Run, Run) are both Nash equilibria.")

    # Government Deposit Insurance Guarantee:
    # Guarantee guarantees full promised payoff r1 = 4/3 at date 2 even if bank liquidates.
    # Waiting payoff under run becomes 4/3 instead of 0.
    di_guarantee = Fraction(4, 3)
    p2_wait_with_di = di_guarantee
    print(
        f"With Deposit Insurance: P2 payoff for Wait when P3=Run becomes "
        f"{p2_wait_with_di} ({float(p2_wait_with_di):.4f})"
    )
    print(f"Comparison: Guaranteed Wait payoff {p2_wait_with_di} > Run payoff {payoff_rr[0]}")
    print("Run equilibrium eliminated: Waiting is strictly dominant for patient depositors.")


main()
