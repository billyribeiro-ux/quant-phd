"""c148 'not a general property': three priors {0.2, 0.3, 0.9}, u(W) = -1/W, W1 = 110000, WL = 95000.

Run: python -I ledgers/E3/scripts/E3-g-r3/c148_counterexample.py
"""
from fractions import Fraction as F

W1, WL = F(110000), F(95000)


def g(p: F) -> F:
    return p / W1 + (1 - p) / WL


priors = [F(2, 10), F(3, 10), F(9, 10)]
inv = [g(p) for p in priors]
tau = F(1, 2)
ce_alpha = 1 / (tau * max(inv) + (1 - tau) * min(inv))
avg = sum(priors) / len(priors)
ce_avg = 1 / g(avg)
print("alpha-MEU tau=1/2 CE =", float(ce_alpha), " EU CE at average prior", float(avg), "=", float(ce_avg))
print("differ:", ce_alpha != ce_avg)
