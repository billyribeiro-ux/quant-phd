"""Lab AP2-L09-1: The Intertemporal CAPM (ICAPM) and state-variable hedging premia.

Finite-state economy in exact Fraction arithmetic.
Two factors: market factor m and state-variable hedging factor h (with Cov(m, h) = 0).
Demonstrates that each asset's CAPM alpha equals its intertemporal hedging premium:
alpha_i^CAPM = beta_{i,h} * lambda_h.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # Factor risk premia
    lambda_m = Fraction(6, 100)  # 6% market risk premium
    lambda_h = Fraction(3, 100)  # 3% state-variable hedging premium
    r_f = Fraction(2, 100)  # 2% riskless rate

    # Three assets with different factor exposures (betas)
    # Asset 1: low market beta, positive hedging beta (hedges adverse shifts)
    # Asset 2: market-matching beta, zero hedging beta
    # Asset 3: high market beta, negative hedging beta
    betas_m = [Fraction(7, 10), Fraction(1, 1), Fraction(13, 10)]
    betas_h = [Fraction(5, 10), Fraction(0, 1), Fraction(-4, 10)]

    # Expected excess returns under the 2-factor ICAPM pricing equation:
    # E[r_i] - r_f = beta_{i,m} * lambda_m + beta_{i,h} * lambda_h
    excess_returns = [betas_m[i] * lambda_m + betas_h[i] * lambda_h for i in range(3)]
    expected_returns = [r_f + excess_returns[i] for i in range(3)]

    # CAPM single-factor benchmark:
    # Market excess return is lambda_m
    # CAPM predicted excess return = beta_{i,m} * lambda_m
    capm_excess = [betas_m[i] * lambda_m for i in range(3)]

    # CAPM pricing error (alpha)
    capm_alphas = [excess_returns[i] - capm_excess[i] for i in range(3)]

    # Theoretical hedging premia
    hedging_premia = [betas_h[i] * lambda_h for i in range(3)]

    print("--- ICAPM Two-Factor Economy (Exact Fraction) ---")
    print(f"Riskless rate r_f:           {r_f}")
    print(f"Market risk premium lambda_m:{lambda_m}")
    print(f"Hedging premium lambda_h:    {lambda_h}")

    for i in range(3):
        print(f"\nAsset {i + 1}:")
        print(f"  beta_m: {betas_m[i]}, beta_h: {betas_h[i]}")
        print(f"  Total expected return:      {expected_returns[i]}")
        print(f"  Total excess return:        {excess_returns[i]}")
        print(f"  CAPM predicted excess:      {capm_excess[i]}")
        print(f"  CAPM alpha:                 {capm_alphas[i]}")
        print(f"  Hedging premium (beta_h*lh):{hedging_premia[i]}")
        print(f"  Alpha equals hedging premium: {capm_alphas[i] == hedging_premia[i]}")

    all_match = all(capm_alphas[i] == hedging_premia[i] for i in range(3))
    print(f"\nExact identity holds for all assets: {all_match}")


main()
