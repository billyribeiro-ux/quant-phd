"""Round-4: re-derive the rank-target numbers quoted in project.html and the grader docstrings."""

import math
from fractions import Fraction

# project.html Conventions: q = 0.1, n = 20, epsilon 0.05
exact_gap = Fraction(0.1) * 20 - Fraction(0.05) * 20
print("exact q n - eps n (q=0.1,n=20,eps=0.05) =", float(exact_gap), "> 1:", exact_gap > 1, "ceil:", math.ceil(exact_gap))
print("float version: ", 0.1 * 20 - 0.05 * 20, "ceil:", math.ceil(0.1 * 20 - 0.05 * 20))
# test witness q = 0.2500004, n = 20, eps = 0.05
qn = Fraction(0.2500004) * 20
slack = Fraction(0.05) * 20
print("q n =", float(qn), " eps n =", float(slack), " exact target:", math.ceil(qn - slack))
print("q rounded to 6 places target:", math.ceil(Fraction(round(0.2500004, 6)) * 20 - slack))
print("answer 4 at-or-below count 4 >= qn - slack =", float(qn - slack), ":", 4 >= qn - slack, "; 5 satisfies:", 5 >= qn - slack)
# Lab 3 median target (lab output checked by run_labs)
n = 11
print("Lab 3 median target:", max(1, math.ceil(Fraction(1, 2) * n - Fraction("0.1") * n)), "gap", float(Fraction(1, 2) * n - Fraction("0.1") * n))
# Lab 1 bound
print("Lab 1 bound 4n:", 4 * 12)
# Exemplar B: Welford identity check on a random stream with exact arithmetic
import random
rng = random.Random(3)
xs = [Fraction(rng.randint(-50, 50), 7) for _ in range(9)]
mean = Fraction(0); S = Fraction(0)
for k, x in enumerate(xs, start=1):
    d = x - mean
    mean_new = mean + d / k
    S = S + d * (x - mean_new)
    mean = mean_new
    assert mean == sum(xs[:k]) / k
    assert S == sum((y - sum(xs[:k]) / k) ** 2 for y in xs[:k])
print("Welford update identity (mean and S) holds exactly on 9 random rationals: True")
