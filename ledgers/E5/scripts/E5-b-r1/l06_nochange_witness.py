"""Witness for the L06 lab check no_change_only_at_natural_rate (tests/labs/E5/lab-E5-L06-1.py line 208).

The lab prints `no_change == zero_gap`, a count equality. The hypothesis on the page states a per-period
implication: inflation is unchanged in a period only when that period's gap is zero. This script feeds the
same count logic a path in which the per-period implication fails in both periods; the count check still prints True.
"""
from fractions import Fraction as F

pairs = [(F(0), True), (F(1, 100), False)]  # (gap, inflation changed?) per period
zero_gap = sum(1 for g, _ in pairs if g == 0)
no_change = sum(1 for _, changed in pairs if not changed)
print("count_check", no_change == zero_gap)
per_period = all((not changed) == (g == 0) for g, changed in pairs)
print("per_period_implication", per_period)
