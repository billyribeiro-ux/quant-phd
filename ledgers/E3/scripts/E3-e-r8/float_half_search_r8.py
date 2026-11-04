"""Round-8: search for a CRRA gamma = 0 lottery where a float expected prize misrounds an exact half cent.

The page (project.html, Conventions "Whole cents") says that at gamma = 0 under the "crra" model the expected prize is
summed as an exact fraction before the single rounding, so that an exact half cent is recognised as a half. A student
who sums floats can therefore differ from the rule. This script finds such inputs, using the reference's own rounding
rule floor(y + 1/2) on the float sum, and compares with the exact Fraction sum rounded by floor(c + 1/2).

Run: .venv/bin/python -I ledgers/E3/scripts/E3-e-r8/float_half_search_r8.py
"""

import math
import random
from fractions import Fraction

random.seed(8)
DENOMS = [2, 3, 4, 5, 6, 8, 10, 12, 20, 40, 100]
found: list[tuple[list[int], list[str], float, Fraction]] = []
trials = 0
while len(found) < 6 and trials < 400_000:
    trials += 1
    k = random.choice([2, 3])
    d = random.choice(DENOMS)
    if d <= k:
        continue
    # probabilities: k positive fractions with denominator d summing to 1
    cuts = sorted(random.sample(range(1, d), k - 1))
    nums = [b - a for a, b in zip([0, *cuts], [*cuts, d], strict=True)]
    probs = [Fraction(n, d) for n in nums]
    prizes = [random.randint(-20000, 20000) for _ in range(k)]
    exact = sum((p * x for p, x in zip(probs, prizes, strict=True)), Fraction(0))
    flt = sum(float(p) * x for p, x in zip(probs, prizes, strict=True))
    exact_cents = math.floor(exact + Fraction(1, 2))
    float_cents = math.floor(flt + 0.5)
    if exact_cents != float_cents:
        found.append((prizes, [f"{p.numerator}/{p.denominator}" for p in probs], flt, exact))

print("trials", trials, "misrounding cases", len(found))
for prizes, probs, flt, exact in found:
    print("prizes", prizes, "probs", probs, "float_sum", repr(flt), "exact_sum", exact, "exact_cents",
          math.floor(exact + Fraction(1, 2)), "float_cents", math.floor(flt + 0.5))
