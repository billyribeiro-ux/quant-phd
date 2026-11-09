"""Probe: CRRA certainty equivalent at an exact half cent with gamma = 1/2 (exact value 3.5 cents).

Wealth 1 cent, prizes 1 and 7 cents with probability 1/2 each. Final wealth 2 and 8: E sqrt = (sqrt 2 + sqrt 8)/2 = 3/sqrt 2,
its square is 4.5, so the certainty equivalent (a change from wealth) is exactly 3.5 cents. Run with -I after copying
reference.py to a scratch dir as elicit.py.
"""

import math
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
import elicit  # noqa: E402

half = Fraction(1, 2)
for name, mod in (("reference", elicit),):
    got = mod.certainty_equivalent_cents("crra", [1, 7], [half, half], {"gamma": 0.5}, 1)
    print(name, "crra gamma=0.5 wealth=1 prizes [1,7]:", got, "(exact value 3.5; page rule: exact half goes toward +infinity -> 4)")
expected = math.sqrt(0.5 * math.sqrt(2.0) + 0.5 * math.sqrt(8.0)) ** 2 - 1
print("float value of the change (unrounded):", repr(expected))
