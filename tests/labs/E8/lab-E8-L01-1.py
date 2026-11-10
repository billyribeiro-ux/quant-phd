"""Lab 1: Balance of payments accounting identity and quote convention inversion.

SIMULATED numbers. Standard library only.
Verifies CA + KA + FA + EO == 0 exact arithmetic and direct/indirect quote reciprocal.
"""

from fractions import Fraction


def verify_balance_of_payments(
    ca: Fraction,
    ka: Fraction,
    fa: Fraction,
) -> tuple[Fraction, Fraction]:
    """Compute net errors and omissions and verify identity.

    Convention:
    CA: Current account balance (trade balance + net primary income + net secondary income).
    KA: Capital account balance (capital transfers + non-produced non-financial assets).
    FA: Financial account net balance. Under BPM6 presentation:
        Net lending (+) / net borrowing (-) = CA + KA.
        Financial account measures net acquisition of financial assets minus net incurrence of liabilities.
        Identity: CA + KA - FA + EO = 0, or with FA defined as net capital outflow: CA + KA + FA + EO = 0.
        Here we follow the analytic presentation where all sources and uses sum to zero:
        Total balance = CA + KA + FA + EO = 0.
    """
    # Net errors and omissions balances the observed accounts
    net_recorded = ca + ka + fa
    eo = -net_recorded
    identity_sum = ca + ka + fa + eo
    return eo, identity_sum


def invert_quote(direct_quote: Fraction) -> Fraction:
    """Return indirect quote (foreign currency per USD) from direct quote (USD per foreign currency)."""
    if direct_quote <= 0:
        msg = f"Exchange rate must be positive, got {direct_quote}"
        raise ValueError(msg)
    return Fraction(1, 1) / direct_quote


def main() -> None:
    # Scenario 1: Trade deficit offset by financial account inflows
    ca_1 = Fraction(-450, 1)  # -450 billion USD current account deficit
    ka_1 = Fraction(10, 1)  # +10 billion USD capital account surplus
    fa_1 = Fraction(440, 1)  # +440 billion USD net financial inflow
    eo_1, sum_1 = verify_balance_of_payments(ca_1, ka_1, fa_1)

    # Scenario 2: Unbalanced records requiring statistical discrepancy (Errors & Omissions)
    ca_2 = Fraction(-520, 1)
    ka_2 = Fraction(15, 1)
    fa_2 = Fraction(485, 1)
    eo_2, sum_2 = verify_balance_of_payments(ca_2, ka_2, fa_2)

    # Quote convention check
    # Spot rate: EUR/USD quote convention is direct (USD per 1 EUR) = 1.25 = 5/4
    s_direct = Fraction(5, 4)
    s_indirect = invert_quote(s_direct)
    reciprocal_product = s_direct * s_indirect

    print("=== Balance of Payments Verification ===")
    print(f"Scenario 1: CA={float(ca_1):.1f}B, KA={float(ka_1):.1f}B, FA={float(fa_1):.1f}B")
    print(f"Scenario 1: Errors & Omissions = {float(eo_1):.1f}B, Total Sum = {float(sum_1):.1f}B")
    print(f"Scenario 2: CA={float(ca_2):.1f}B, KA={float(ka_2):.1f}B, FA={float(fa_2):.1f}B")
    print(f"Scenario 2: Errors & Omissions = {float(eo_2):.1f}B, Total Sum = {float(sum_2):.1f}B")
    print("\n=== Quote Convention Verification ===")
    print(f"Direct quote (USD per EUR): {float(s_direct):.4f} ({s_direct})")
    print(f"Indirect quote (EUR per USD): {float(s_indirect):.4f} ({s_indirect})")
    print(f"Product (S * 1/S): {reciprocal_product} (Exact)")

    assert sum_1 == Fraction(0, 1), "Scenario 1 BoP sum must be 0"
    assert sum_2 == Fraction(0, 1), "Scenario 2 BoP sum must be 0"
    assert reciprocal_product == Fraction(1, 1), "Quote inversion product must be 1"


main()
