"""Re-derives the numbers the suite's docstrings and the README quote for the fixed fixtures (round 14).

Run as: python -I fixture_numbers_r14.py <repo-root>. Uses the reference engine copied as elicit.py in a scratch dir.
"""

import json
import math
import os
import shutil
import sys
import tempfile

root = sys.argv[1]
work = tempfile.mkdtemp(prefix="e3d-r14-fix-")
for f in ("test_project.py", "instance.py"):
    shutil.copy(os.path.join(root, "course/modules/E/E3/grader", f), work)
shutil.copy(os.path.join(root, "course/modules/E/E3/grader/reference.py"), os.path.join(work, "elicit.py"))
sys.path.insert(0, work)
os.environ["QF_SEED"] = "0"
import elicit  # noqa: E402
import test_project as tp  # noqa: E402
from instance import make_instance  # noqa: E402

def show(name, fit):
    print(f"{name}: gamma {fit['gamma_hat']:.6f} lambda {fit['lambda_hat']:.6f} kappa {fit['kappa_hat']:.6f} "
          f"se_g {fit['se_gamma']:.5f} se_l {fit['se_lambda']:.4f} se_k {fit['se_kappa']:.4f} ll {fit['log_likelihood']:.4f}")

for seed in (30, 49, 108):
    inst = make_instance(seed)
    try:
        show(f"seed {seed} own", elicit.estimate(json.loads(str(inst["responses_json"]))))
    except Exception as err:  # noqa: BLE001
        print(f"seed {seed} own RAISED {type(err).__name__}")
inst49 = make_instance(49)
resp49 = json.loads(str(inst49["responses_json"]))
fit49 = elicit.estimate(resp49)
print("seed 49 score at 1e-5 and 1e-6:", tp._largest_score_component([tp.parse(r) for r in resp49], fit49["gamma_hat"], fit49["lambda_hat"], fit49["kappa_hat"], 1e-5), tp._largest_score_component([tp.parse(r) for r in resp49], fit49["gamma_hat"], fit49["lambda_hat"], fit49["kappa_hat"], 1e-6))
# Standard errors at steps 1e-5 and 1e-6 for seed 49 (the coordinate-change oracle of the suite)
th = [math.log(fit49["gamma_hat"] / (1 - fit49["gamma_hat"])), math.log(fit49["lambda_hat"]), math.log(fit49["kappa_hat"])]
parsed49 = [tp.parse(r) for r in resp49]
def observed_info(theta, h, parsed):
    """The suite's observed information, recomputed with the given participant (tp._observed_information uses seed 0)."""

    def at(*moves):
        y = list(theta)
        for idx, amount in moves:
            y[idx] += amount
        gamma = 1.0 / (1.0 + math.exp(-y[0]))
        return tp.oracle_loglik(parsed, gamma, math.exp(y[1]), math.exp(y[2]))

    f0 = at()
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4.0 * h * h)
            info[i][j] = info[j][i] = v
    return info


for h in (1e-5, 1e-6):
    info = observed_info(th, h, parsed49)
    print(f"seed 49 observed information diagonal at step {h}:", [info[i][i] for i in range(3)])
    cov = tp._invert3(info)
    g, l, k = fit49["gamma_hat"], fit49["lambda_hat"], fit49["kappa_hat"]
    if all(cov[i][i] > 0.0 for i in range(3)):
        print(f"seed 49 se at step {h}: gamma {g*(1-g)*math.sqrt(cov[0][0]):.5f} lambda {l*math.sqrt(cov[1][1]):.4f} kappa {k*math.sqrt(cov[2][2]):.4f}")
    else:
        print(f"seed 49 at step {h}: inverse information diagonal not positive:", [cov[i][i] for i in range(3)])
# Reverse summation order of the likelihood terms (the suite's docstring claim), at the same estimate
def ll_reverse(th, parsed):
    gamma = 1.0 / (1.0 + math.exp(-th[0])); lam = math.exp(th[1]); kappa = math.exp(th[2])
    total = 0.0
    for pa, qa, pb, qb, choice in reversed(parsed):
        z = kappa * (tp.oracle_prospect(pa, qa, gamma, lam) - tp.oracle_prospect(pb, qb, gamma, lam)) / 10_000.0
        total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
    return total
orig = tp.oracle_loglik
def fwd(parsed_, gamma, lam, kappa):
    return orig(parsed_, gamma, lam, kappa)
print("(reverse-order check is informational)", ll_reverse(th, parsed49) - fwd(parsed49, fit49["gamma_hat"], fit49["lambda_hat"], fit49["kappa_hat"]))
show("FIXED_26 (fixture)", elicit.estimate([{"pair_id": i, "choice": c, "prizes_a": pa, "probs_a": qa, "prizes_b": pb, "probs_b": qb} for i, c, pa, qa, pb, qb in tp.FIXED_26_ANSWERS]))
show("B-side 12 (fixture)", elicit.estimate([{"pair_id": i, "choice": tp.B_SIDE_CHOICES[i], "prizes_a": [tp.B_SIDE_SURE_A[i]], "probs_a": ["1"], "prizes_b": tp.B_SIDE_LOTTERIES[i][0], "probs_b": tp.B_SIDE_LOTTERIES[i][1]} for i in range(12)]))
allA = [{"pair_id": i, "choice": "A", "prizes_a": [tp.B_SIDE_SURE_A[i]], "probs_a": ["1"], "prizes_b": tp.B_SIDE_LOTTERIES[i][0], "probs_b": tp.B_SIDE_LOTTERIES[i][1]} for i in range(len(tp.B_SIDE_SURE_A))]
try:
    show("all-A (test_estimate_counts...)", elicit.estimate(allA))
except Exception as err:  # noqa: BLE001
    print("all-A RAISED", type(err).__name__, str(err)[:100])
shutil.rmtree(work, ignore_errors=True)
