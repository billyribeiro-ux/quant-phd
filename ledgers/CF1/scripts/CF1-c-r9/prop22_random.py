"""Random check of Proposition 2.2 (L05): for conventional flows and r >= 0 where both paybacks exist, tau_D >= tau_S."""

import random
from fractions import Fraction as F

rng = random.Random(9)
checked = 0
violations = 0
for _ in range(20000):
    n_years = rng.randint(1, 7)
    rate = F(rng.randint(0, 40), 100)
    flows = [-rng.randint(1, 1000)] + [rng.randint(0, 800) for _ in range(n_years)]
    v = 1 / (1 + rate)
    cum = 0
    disc = 0
    tau_s = None
    tau_d = None
    for t, c in enumerate(flows):
        cum += c
        disc += c * v**t
        if t >= 1 and tau_s is None and cum >= 0:
            tau_s = t
        if t >= 1 and tau_d is None and disc >= 0:
            tau_d = t
    if tau_s is not None and tau_d is not None:
        checked += 1
        if tau_d < tau_s:
            violations += 1
print("prop2.2 random checks with both paybacks:", checked, "violations:", violations)
