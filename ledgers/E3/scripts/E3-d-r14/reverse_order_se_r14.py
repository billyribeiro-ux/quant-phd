"""Checks the suite docstring claim (test_project.py, test_standard_errors_match...): summing the likelihood terms in
reverse order moves se_lambda of seed 49 to 136.78 at step 1e-5 and to 98.09 at step 1e-6. Run with -I."""

import math
import os
import shutil
import sys
import tempfile

root = sys.argv[1]
work = tempfile.mkdtemp(prefix="e3d-r14-rev-")
for f in ("test_project.py", "instance.py"):
    shutil.copy(os.path.join(root, "course/modules/E/E3/grader", f), work)
shutil.copy(os.path.join(root, "course/modules/E/E3/grader/reference.py"), os.path.join(work, "elicit.py"))
sys.path.insert(0, work)
os.environ["QF_SEED"] = "0"
import elicit  # noqa: E402
import test_project as tp  # noqa: E402
from instance import make_instance  # noqa: E402

inst = make_instance(49)
resp = __import__("json").loads(str(inst["responses_json"]))
parsed = [tp.parse(r) for r in resp]
fit = elicit.estimate(resp)
g, l, k = fit["gamma_hat"], fit["lambda_hat"], fit["kappa_hat"]


def make_ll(order):
    def ll(gamma, lam, kappa):
        total = 0.0
        for pa, qa, pb, qb, choice in order:
            z = kappa * (tp.oracle_prospect(pa, qa, gamma, lam) - tp.oracle_prospect(pb, qb, gamma, lam)) / 10_000.0
            total += -math.log1p(math.exp(-z)) if choice == "A" else -math.log1p(math.exp(z))
        return total
    return ll


def se_lambda(ll, h):
    th = [math.log(g / (1 - g)), math.log(l), math.log(k)]

    def at(*moves):
        y = list(th)
        for i, d in moves:
            y[i] += d
        return ll(1.0 / (1.0 + math.exp(-y[0])), math.exp(y[1]), math.exp(y[2]))

    f0 = at()
    info = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        info[i][i] = -(at((i, h)) - 2 * f0 + at((i, -h))) / (h * h)
        for j in range(i + 1, 3):
            v = -(at((i, h), (j, h)) - at((i, h), (j, -h)) - at((i, -h), (j, h)) + at((i, -h), (j, -h))) / (4 * h * h)
            info[i][j] = info[j][i] = v
    cov = tp._invert3(info)
    return l * math.sqrt(cov[1][1]) if cov[1][1] > 0 else float("nan")


fwd = make_ll(parsed)
rev = make_ll(list(reversed(parsed)))
for h in (1e-5, 1e-6):
    a, b = se_lambda(fwd, h), se_lambda(rev, h)
    print(f"step {h}: forward se_lambda {a:.4f}, reverse se_lambda {b:.4f}, change {100 * (b - a) / a:+.2f}%")
shutil.rmtree(work, ignore_errors=True)
