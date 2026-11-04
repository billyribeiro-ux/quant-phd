"""Round-7 checks: (1) the all-A degenerate set behind the new grader test docstring (test_project.py, the
test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen docstring); (2) the L04 Example 2.5 integrated values
and the mean-preserving-spread construction; (3) the new grader fixtures' mixed-sign facts.
Run: python -I degenerate_and_example_r7.py <checkout> <scratch dir containing test_project.py, instance.py, elicit.py>
"""
import math
import sys
from fractions import Fraction
from pathlib import Path

checkout, scratch = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(scratch))
import elicit as sol  # noqa: E402  (the reference engine copied as elicit.py)
import test_project as t  # noqa: E402

responses = [
    {"pair_id": k, "choice": "A", "prizes_a": [t.B_SIDE_SURE_A[k]], "probs_a": ["1"],
     "prizes_b": t.B_SIDE_LOTTERIES[k][0], "probs_b": t.B_SIDE_LOTTERIES[k][1]}
    for k in range(len(t.B_SIDE_SURE_A))
]
fit = sol.estimate(responses)
print("all-A set: kappa_hat=%.1f se_gamma=%.1f se_lambda=%.1f se_kappa=%.1f" % (
    fit["kappa_hat"], fit["se_gamma"], fit["se_lambda"], fit["se_kappa"]))
print("all-A set: standard errors above 1e5 for every parameter:", all(fit[k] > 1e5 for k in ("se_gamma", "se_lambda", "se_kappa")))
print("B-side fixture lotteries all mixed:", all(t.mixed([int(x) for x in p], [Fraction(q) for q in pq]) for p, pq in t.B_SIDE_LOTTERIES))

# L04 Example 2.5: X = {2000: 1/2, 4000: 1/2}, Y = {1000: 1/4, 3000: 1/2, 5000: 1/4}; I(t) = sum p (t - x)^+ (Lemma 1.2)
X = {2000: Fraction(1, 2), 4000: Fraction(1, 2)}
Y = {1000: Fraction(1, 4), 3000: Fraction(1, 2), 5000: Fraction(1, 4)}


def integrated(dist, s):
    return sum(p * max(s - x, 0) for x, p in dist.items())


S = [1000, 2000, 3000, 4000, 5000]
print("L04 Ex2.5 I_X:", [str(integrated(X, s)) for s in S])
print("L04 Ex2.5 I_Y:", [str(integrated(Y, s)) for s in S])
print("L04 Ex2.5 means:", sum(x * p for x, p in X.items()), sum(x * p for x, p in Y.items()))
# mean-preserving spread: each X atom split into a below and an above atom with equal halves and the same average
split = {1000: Fraction(1, 4), 3000: Fraction(1, 4) + Fraction(1, 4), 5000: Fraction(1, 4)}
print("L04 Ex2.5 spread check (2000->1000,3000; 4000->3000,5000) equals Y:", split == Y)
print("L04 Ex2.5 I_Y and I_X: X dominates Y in the second order:", all(integrated(X, s) <= integrated(Y, s) for s in S))
