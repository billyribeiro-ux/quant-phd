"""Lab FC4-L01-1: Residual claim waterfall on an illustrative capital structure."""

from fractions import Fraction


def main() -> None:
    # Illustrative capital structure (SIMULATED)
    # Senior debt: $40M face value, senior priority
    # Subordinated debt: $30M face value, subordinated priority
    # Preferred equity: $20M liquidation preference, junior to debt, senior to common
    # Common equity: residual claim max(V - S, 0)
    senior_debt = Fraction(40)
    sub_debt = Fraction(30)
    pref_equity = Fraction(20)
    total_senior_claims = senior_debt + sub_debt + pref_equity  # $90M

    firm_values = [Fraction(v) for v in (20, 50, 80, 90, 120, 160)]

    print("SIMULATED Capital Structure Waterfall (Million USD)")
    print(f"Senior Debt: ${senior_debt}M | Sub Debt: ${sub_debt}M")
    print(f"Preferred: ${pref_equity}M | Total Prior Claims: ${total_senior_claims}M")
    print("-" * 72)
    print(f"{'Firm V':>8} {'Senior Debt':>12} {'Sub Debt':>10} {'Preferred':>10} {'Common Eq':>12} {'Eq Payoff':>14}")
    print("-" * 72)

    for v in firm_values:
        pay_senior = min(v, senior_debt)
        rem1 = v - pay_senior

        pay_sub = min(rem1, sub_debt)
        rem2 = rem1 - pay_sub

        pay_pref = min(rem2, pref_equity)
        rem3 = rem2 - pay_pref

        pay_common = max(rem3, Fraction(0))
        formula_common = max(v - total_senior_claims, Fraction(0))
        assert pay_common == formula_common

        print(
            f"{float(v):8.2f} {float(pay_senior):12.2f} {float(pay_sub):10.2f} "
            f"{float(pay_pref):10.2f} {float(pay_common):12.2f} {pay_common!s:>14}"
        )

    print("-" * 72)
    print("Waterfall identity verified: common equity equals max(V - S, 0) in all states.")


main()
