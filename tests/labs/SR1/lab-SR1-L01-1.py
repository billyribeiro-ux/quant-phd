"""Lab SR1-L01-1: Diamond-Dybvig Liquidity Insurance and First-Best Contract.

Verifies the first-best risk pooling allocation against autarky using exact Fraction
arithmetic. Demonstrates that demand deposits provide optimal liquidity insurance
by transferring consumption from late patient consumers to early impatient consumers.
"""

from fractions import Fraction


def main() -> None:
    # Model parameters
    lambda_early = Fraction(1, 2)  # Probability of impatient type
    one_minus_lambda = Fraction(1, 2)  # Probability of patient type
    r_mature = Fraction(4, 1)  # Long-term asset payoff at t=2
    l_salvage = Fraction(1, 2)  # Illiquid salvage return at t=1

    # First-best social planner problem under CRRA utility u(c) = 1 - 1/c (gamma = 2):
    # u'(c) = c^(-2). Optimality condition: u'(c1*) = r_mature * u'(c2*)
    # c1^(-2) = 4 * c2^(-2) ==> c2* = 2 * c1*
    # Resource constraint: lambda * c1* + (1 - lambda) * c2* / r_mature = 1
    # (1/2) * c1* + (1/2) * (2 * c1*) / 4 = 1 ==> (3/4) * c1* = 1 ==> c1* = 4/3
    c1_star = Fraction(4, 3)
    c2_star = Fraction(8, 3)

    # Expected utility calculation: u(c) = 1 - 1/c
    def utility(c: Fraction) -> Fraction:
        return Fraction(1, 1) - Fraction(1, 1) / c

    eu_first_best = lambda_early * utility(c1_star) + one_minus_lambda * utility(c2_star)

    # Autarky benchmark: isolated agent chooses liquid storage alpha in [0, 1]
    # c1(alpha) = alpha + (1 - alpha) * l_salvage = (1 + alpha) / 2
    # c2(alpha) = alpha + (1 - alpha) * r_mature = 4 - 3 * alpha
    # For alpha = 1 (full liquid storage): c1 = 1, c2 = 1
    eu_autarky_liquid = lambda_early * utility(Fraction(1, 1)) + one_minus_lambda * utility(Fraction(1, 1))
    # For alpha = 0 (full illiquid investment): c1 = 1/2, c2 = 4
    eu_autarky_illiquid = lambda_early * utility(l_salvage) + one_minus_lambda * utility(r_mature)

    # Bank demand deposit implementation
    liquid_buffer = lambda_early * c1_star
    long_asset = Fraction(1, 1) - liquid_buffer
    c2_bank = (long_asset * r_mature) / one_minus_lambda

    print(f"First-Best Early Consumption c1*: {c1_star} ({float(c1_star):.4f})")
    print(f"First-Best Late Consumption c2*: {c2_star} ({float(c2_star):.4f})")
    print(f"Bank Liquid Storage Buffer: {liquid_buffer} ({float(liquid_buffer):.4f})")
    print(f"Bank Illiquid Long Investment: {long_asset} ({float(long_asset):.4f})")
    print(f"Delivered Date 2 Payoff per Patient Depositor: {c2_bank} ({float(c2_bank):.4f})")
    print(f"Expected Utility (First-Best Contract): {eu_first_best} ({float(eu_first_best):.6f})")
    print(f"Expected Utility (Autarky 100% Liquid): {eu_autarky_liquid} ({float(eu_autarky_liquid):.6f})")
    print(f"Expected Utility (Autarky 100% Illiquid): {eu_autarky_illiquid} ({float(eu_autarky_illiquid):.6f})")


main()
