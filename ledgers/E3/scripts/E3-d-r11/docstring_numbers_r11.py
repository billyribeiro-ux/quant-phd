"""Round-11: re-derive the numbers quoted in test_project.py docstrings with the reference engine.
(a) seed 49: se_lambda and se_gamma at steps 1e-5 and 1e-6, forward and reverse summation order (test_standard_errors_match...);
(b) the all-A degenerate set (test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen): kappa_hat and standard errors."""
import json
import math
import sys
from pathlib import Path

work = Path(sys.argv[1])
sys.path.insert(0, str(work))
import elicit  # noqa: E402
import test_project as tp  # noqa: E402
from instance import make_instance  # noqa: E402

inst = make_instance(49)
resp = json.loads(str(inst["responses_json"]))
parsed = [tp.parse(r) for r in resp]
est = elicit.estimate(resp)
g, l, k = est["gamma_hat"], est["lambda_hat"], est["kappa_hat"]
theta = [math.log(g / (1 - g)), math.log(l), math.log(k)]


def se_at(parsed_list, h, ll=None):
    """Observed information at theta on the given participant's parsed responses (the test helper uses seed 0 only)."""
    ll = ll or (lambda pl, gg, ll_, kk: tp.oracle_loglik(pl, gg, ll_, kk))

    def at(*moves):
        y = list(theta)
        for idx, amount in moves:
            y[idx] += amount
        gam = 1.0 / (1.0 + math.exp(-y[0]))
        return ll(parsed_list, gam, math.exp(y[1]), math.exp(y[2]))

    f0 = at()
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            info[i][j] = info[j][i] = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4.0 * h * h)
    cov = tp._invert3(info)
    return g * (1 - g) * math.sqrt(cov[0][0]), l * math.sqrt(cov[1][1]), k * math.sqrt(cov[2][2])


for h in (1e-5, 1e-6):
    sg, sl, sk = se_at(parsed, h)
    print(f"seed49 step {h:g}: se_gamma={sg:.5f} se_lambda={sl:.6f} se_kappa={sk:.4f}")
rev = list(reversed(parsed))
# reverse summation order: the oracle sums the terms in reverse order
orig_ll = tp.oracle_loglik


def reversed_ll(pl, gg, ll_, kk):
    total = 0.0
    for pa, qa, pb, qb, choice in reversed(pl):
        z = kk * (tp.oracle_prospect(pa, qa, gg, ll_) - tp.oracle_prospect(pb, qb, gg, ll_)) / 10_000.0
        total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return total


for h in (1e-5, 1e-6):
    fwd = se_at(parsed, h)
    rv = se_at(parsed, h, ll=reversed_ll)
    print(f"seed49 reverse order step {h:g}: se_lambda {rv[1]:.3f} ({100*(rv[1]/fwd[1]-1):+.2f}%) se_gamma {rv[0]:.5f} ({100*(rv[0]/fwd[0]-1):+.2f}%)")

# (b) all-A degenerate set, as in test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen
responses = [
    {"pair_id": i, "choice": "A", "prizes_a": [tp.B_SIDE_SURE_A[i]], "probs_a": ["1"],
     "prizes_b": tp.B_SIDE_LOTTERIES[i][0], "probs_b": tp.B_SIDE_LOTTERIES[i][1]}
    for i in range(len(tp.B_SIDE_SURE_A))
]
e2 = elicit.estimate(responses)
print("all-A:", {x: round(v, 4) for x, v in e2.items()})
