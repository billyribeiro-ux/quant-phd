"""Witness that separates the rounding-once rule from rounding the probability first (mutant m36).

Capital 1 cent, base 1 cent, one bet: expected final wealth = 2p cents. For p = 1/4 - 1/10**7 the exact expectation is
0.49999998 cents, which half up gives 0 cents. Rounding p to six decimals first gives 0.25 and 0.5 cents, which gives 1.
Usage: python -I rounding_witness.py <dir containing martingale_checks.py> ; prints the engine's cents.
"""
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
import martingale_checks as sol  # noqa: E402

p = Fraction(1, 4) - Fraction(1, 10**7)
inst = {"horizon": 4, "win_probability": p, "stop_level": 1, "stop_cap": 1, "capital_cents": 1,
        "base_stake_cents": 1, "dyadic_level": 3, "barrier": 1}
out = sol.doubling_outcome(inst)
print("expected exact:", 2 * p, "float", float(2 * p))
print("expected_final_wealth_cents:", out["expected_final_wealth_cents"])
