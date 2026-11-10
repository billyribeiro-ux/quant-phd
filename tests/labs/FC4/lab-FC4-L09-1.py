"""Lab FC4-L09-1: Scenario-weighted price target and half-up cent rounding."""

from fractions import Fraction


def compute_target_cents(scenarios: list[tuple[Fraction, int]]) -> tuple[Fraction, int, int]:
    """Compute exact expected value in cents, half-up rounded integer cents, and round-to-even cents."""
    tot_p = sum((p for p, _ in scenarios), Fraction(0))
    assert tot_p == Fraction(1), "Probabilities must sum to 1"
    exact_cents = sum((p * v for p, v in scenarios), Fraction(0))

    # Half-up rounding: floor(x + 1/2)
    num = 2 * exact_cents.numerator + exact_cents.denominator
    den = 2 * exact_cents.denominator
    half_up = num // den

    # Python built-in round (half-to-even) for comparison
    round_even = round(float(exact_cents))
    return exact_cents, half_up, round_even


def main() -> None:
    # Two cases (SIMULATED):
    # Case A: Standard non-tie distribution (Bull: 25% @ $65.00, Base: 50% @ $50.00, Bear: 25% @ $35.00)
    # Target in cents: 25%*6500 + 50%*5000 + 25%*3500 = 1625 + 2500 + 875 = 5000 cents ($50.00)
    # Case B: Exact half-cent tie (Bull: 50% @ $50.03 [5003c], Bear: 50% @ $50.02 [5002c])
    # Expected value: 5002.5 cents -> half-up gives 5003 cents ($50.03), round-to-even gives 5002 cents ($50.02)
    case_a = [
        (Fraction(25, 100), 6500),
        (Fraction(50, 100), 5000),
        (Fraction(25, 100), 3500),
    ]

    case_b_tie = [
        (Fraction(1, 2), 5002),
        (Fraction(1, 2), 5003),
    ]

    print("SIMULATED Scenario-Weighted Price Target Computation (Integer Cents)")
    print("-" * 75)
    print("Case A: Standard Three-Scenario Model (Bull, Base, Bear)")
    for name, (p, val) in zip(["Bull", "Base", "Bear"], case_a, strict=True):
        print(f"  {name:<6} Scenario: Probability = {float(p):.2%}, Target = ${val / 100:.2f} ({val} cents)")
    exact_a, half_up_a, _even_a = compute_target_cents(case_a)
    print(f"  Exact Expected Value: {exact_a} cents (${float(exact_a) / 100:.4f})")
    print(f"  Half-Up Price Target: {half_up_a} cents (${half_up_a / 100:.2f})")
    print()

    print("Case B: Exact Half-Cent Tie (Illustrating Half-Up vs Python Round-to-Even)")
    for name, (p, val) in zip(["Scenario 1", "Scenario 2"], case_b_tie, strict=True):
        print(f"  {name:<12} Probability = {float(p):.2%}, Target = ${val / 100:.2f} ({val} cents)")
    exact_b, half_up_b, even_b = compute_target_cents(case_b_tie)
    print(f"  Exact Expected Value:       {exact_b} cents (${float(exact_b) / 100:.4f})")
    print(f"  Half-Up Rounded Target:     {half_up_b} cents (${half_up_b / 100:.2f}) [Correct convention]")
    print(f"  Round-to-Even Target:       {even_b} cents (${even_b / 100:.2f}) [Python round() flaw]")
    print("-" * 75)
    print("Rounding tie demonstrated: 5002.5 cents rounds half-up to 5003 cents.")


main()
