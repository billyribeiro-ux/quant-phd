"""Round-10 numeric re-derivation for E3 slice e (run from the checkout root with .venv/bin/python -I).

Imports the reference engine (grader/reference.py, copied to a temp dir as elicit.py) and the grader's own test module
and instance generator, so every number is computed by the code the suite runs. Prints one labelled line per number.
"""

import json
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GRADER = ROOT / "course" / "modules" / "E" / "E3" / "grader"
TMP = Path(tempfile.mkdtemp(prefix="e3e_r10_"))
shutil.copy(GRADER / "reference.py", TMP / "elicit.py")
sys.path[:0] = [str(TMP), str(GRADER)]
os.environ.setdefault("QF_SEED", "0")

import elicit as ref  # noqa: E402
import test_project as tp  # noqa: E402
from instance import make_instance  # noqa: E402


def est_of(inst):
    return ref.estimate(json.loads(str(inst["responses_json"])))


# 1. Fixed participants used by the suite.
for seed in (30, 49):
    inst = make_instance(seed)
    e = est_of(inst)
    print(f"seed {seed}: gamma_hat={e['gamma_hat']:.6f} lambda_hat={e['lambda_hat']:.6f} kappa_hat={e['kappa_hat']:.6f} "
          f"se_gamma={e['se_gamma']:.5f} se_lambda={e['se_lambda']:.4f} se_kappa={e['se_kappa']:.4f}")

# 2. Standard-error oracle on seed 49 (test docstring numbers): oracle SE at steps 1e-5 and 1e-6, forward and reverse sum.
inst49 = make_instance(49)
resp49 = json.loads(str(inst49["responses_json"]))
e49 = est_of(inst49)
parsed_fwd = [tp.parse(r) for r in resp49]
parsed_rev = list(reversed(parsed_fwd))


def oracle_se(parsed, h):
    g, l, k = e49["gamma_hat"], e49["lambda_hat"], e49["kappa_hat"]
    theta = [math.log(g / (1 - g)), math.log(l), math.log(k)]
    cov = tp._invert3(tp._observed_information_for(parsed, theta, h) if hasattr(tp, "_observed_information_for")
                      else _obs(parsed, theta, h))
    return (g * (1 - g) * math.sqrt(cov[0][0]), l * math.sqrt(cov[1][1]), k * math.sqrt(cov[2][2]))


def _obs(parsed, theta, h):
    def at(*moves):
        y = list(theta)
        for idx, amount in moves:
            y[idx] += amount
        gm = 1.0 / (1.0 + math.exp(-y[0]))
        return tp.oracle_loglik(parsed, gm, math.exp(y[1]), math.exp(y[2]))

    f0 = at()
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2.0 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4.0 * h * h)
            info[i][j] = info[j][i] = v
    return info


for label, parsed in (("forward", parsed_fwd), ("reverse", parsed_rev)):
    for h in (1e-5, 1e-6):
        sg, sl, sk = oracle_se(parsed, h)
        print(f"seed 49 oracle SE {label} order step {h:g}: se_gamma={sg:.5f} se_lambda={sl:.2f} se_kappa={sk:.3f}")

# 3. The all-A fixture of test_estimate_counts_a_mixed_lottery_whether_or_not_it_was_chosen.
responses = [
    {"pair_id": i, "choice": "A", "prizes_a": [tp.B_SIDE_SURE_A[i]], "probs_a": ["1"],
     "prizes_b": tp.B_SIDE_LOTTERIES[i][0], "probs_b": tp.B_SIDE_LOTTERIES[i][1]}
    for i in range(len(tp.B_SIDE_SURE_A))
]
try:
    a = ref.estimate(responses)
    print("all-A fixture: " + " ".join(f"{k}={v:.6g}" for k, v in sorted(a.items())))
except Exception as exc:  # noqa: BLE001
    print("all-A fixture raised", type(exc).__name__, exc)
print("mixed-chosen fixture pairs:", len(tp.B_SIDE_SURE_A))
print("suite collected tests (module constants):", len([n for n in dir(tp) if n.startswith("test_")]))
shutil.rmtree(TMP, ignore_errors=True)
