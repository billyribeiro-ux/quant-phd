"""Lab AP2-L10-1: Linear Factor Models and Arbitrage Pricing Theory (APT).

Exact 4-asset, 2-factor economy in Fraction arithmetic without idiosyncratic noise (Assumption A8).
Demonstrates:
(1) Solving factor risk premia lambda_1, lambda_2 from two basis assets;
(2) Validating the exact linear pricing equation across remaining assets;
(3) Constructing a zero-cost, zero-factor-exposure portfolio and verifying that its payoff is zero.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # 4 assets, 2 systematic factors
    # Factor exposures B: [b_{i,1}, b_{i,2}]
    factor_loadings = [
        [Fraction(1, 1), Fraction(1, 2)],
        [Fraction(1, 2), Fraction(1, 1)],
        [Fraction(3, 2), Fraction(1, 4)],
        [Fraction(2, 1), Fraction(3, 4)],
    ]
    r_f = Fraction(2, 100)  # 2% riskless rate

    # True factor premia: lambda_1 = 5%, lambda_2 = 4%
    true_lambda_1 = Fraction(5, 100)
    true_lambda_2 = Fraction(4, 100)

    # Expected excess returns under exact factor pricing
    excess_returns = [factor_loadings[i][0] * true_lambda_1 + factor_loadings[i][1] * true_lambda_2 for i in range(4)]
    expected_returns = [r_f + excess_returns[i] for i in range(4)]

    print("--- 4-Asset, 2-Factor Economy (Exact Fraction) ---")
    for i in range(4):
        b1, b2 = factor_loadings[i][0], factor_loadings[i][1]
        print(f"Asset {i + 1}: b1={b1}, b2={b2}, E[r]={expected_returns[i]}, excess={excess_returns[i]}")

    # Step 1: Solve for factor premia from assets 1 and 2
    # [ b11  b12 ] [ l1 ] = [ y1 ]
    # [ b21  b22 ] [ l2 ]   [ y2 ]
    b11, b12 = factor_loadings[0][0], factor_loadings[0][1]
    b21, b22 = factor_loadings[1][0], factor_loadings[1][1]
    det = b11 * b22 - b12 * b21
    solved_l1 = (b22 * excess_returns[0] - b12 * excess_returns[1]) / det
    solved_l2 = (-b21 * excess_returns[0] + b11 * excess_returns[1]) / det

    print(f"\nSolved lambda_1: {solved_l1} (true: {true_lambda_1})")
    print(f"Solved lambda_2: {solved_l2} (true: {true_lambda_2})")
    print(f"Factor premia match exactly: {solved_l1 == true_lambda_1 and solved_l2 == true_lambda_2}")

    # Step 2: Test pricing on assets 3 and 4
    for i in (2, 3):
        pred_ex = factor_loadings[i][0] * solved_l1 + factor_loadings[i][1] * solved_l2
        print(f"Asset {i + 1}: pred excess={pred_ex}, actual={excess_returns[i]}, match={pred_ex == excess_returns[i]}")

    # Step 3: Construct an arbitrage portfolio with zero cost and zero factor exposure
    # Vector w = [7, -3, -5, 1] satisfies sum(w)=0, sum(w*b1)=0, sum(w*b2)=0
    w_arb = [Fraction(7, 1), Fraction(-3, 1), Fraction(-5, 1), Fraction(1, 1)]
    cost = sum(w_arb, Fraction(0, 1))
    exposure_1 = sum((w_arb[i] * factor_loadings[i][0] for i in range(4)), Fraction(0, 1))
    exposure_2 = sum((w_arb[i] * factor_loadings[i][1] for i in range(4)), Fraction(0, 1))
    payoff_excess = sum((w_arb[i] * excess_returns[i] for i in range(4)), Fraction(0, 1))

    print(f"\nArbitrage Portfolio weights: [{w_arb[0]}, {w_arb[1]}, {w_arb[2]}, {w_arb[3]}]")
    print(f"Initial cost:             {cost}")
    print(f"Factor 1 exposure:        {exposure_1}")
    print(f"Factor 2 exposure:        {exposure_2}")
    print(f"Total payoff:             {payoff_excess}")
    print(f"No-arbitrage condition holds: {cost == 0 and exposure_1 == 0 and exposure_2 == 0 and payoff_excess == 0}")


main()
