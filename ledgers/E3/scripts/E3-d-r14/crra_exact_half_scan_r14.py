"""Scan CRRA gamma = 1/2 instances whose exact certainty equivalent is a half cent, and compare the reference's rounding.

Finals F1 = 2 s^2 and F2 = 8 s^2 (probability 1/2 each) give E sqrt F = 3 s / sqrt 2, its square 9 s^2 / 2 (exact),
so CE = 9 s^2 / 2 - W is a half-integer whenever s is odd and W is an integer. Half up gives (9 s^2 + 1) / 2 - W.
Run with -I; argv[1] is a scratch dir holding the engine as elicit.py.
"""

import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
import elicit  # noqa: E402

half = Fraction(1, 2)
checked = mismatches = 0
examples = []
for s in range(1, 60, 2):
    for wealth in range(1, 60):
        f1, f2 = 2 * s * s, 8 * s * s
        exact = Fraction(9 * s * s, 2) - wealth
        assert exact.denominator == 2
        got = elicit.certainty_equivalent_cents("crra", [f1 - wealth, f2 - wealth], [half, half], {"gamma": 0.5}, wealth)
        want = int(exact + half)  # floor(x + 1/2), the page's rule for an exact half
        checked += 1
        if got != want:
            mismatches += 1
            if len(examples) < 5:
                examples.append((s, wealth, str(exact), got, want))
print("checked", checked, "mismatches", mismatches, "examples (s, wealth, exact, got, want):", examples)
