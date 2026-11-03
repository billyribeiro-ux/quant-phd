"""Round-3 verifier (E3-d): the reference estimator on the twelve ANSWERS of Lab 3, against the printed digits of the
page (project.html lines 571-577), and the mixed-sign count (project.html line 383). Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B ledgers/E3/scripts/E3-d-r3/lab3_reference_r3.py
"""
import ast
import sys
from fractions import Fraction

sys.path.insert(0, "course/modules/E/E3/grader")
import reference as ref  # noqa: E402

tree = ast.parse(open("tests/labs/E3/lab-E3-project-3.py", encoding="utf-8").read())
answers = None
for node in tree.body:
    if isinstance(node, ast.AnnAssign) and getattr(node.target, "id", "") == "ANSWERS":
        answers = ast.literal_eval(node.value)
resp = [
    {"pair_id": a[0], "choice": a[1], "prizes_a": a[2], "probs_a": a[3], "prizes_b": a[4], "probs_b": a[5]}
    for a in answers
]
fit = ref.estimate(resp)
print({k: round(v, 6) for k, v in fit.items()})
checks = {
    "gamma_hat 0.6352": f"{fit['gamma_hat']:.4f}" == "0.6352",
    "lambda_hat 6.1503": f"{fit['lambda_hat']:.4f}" == "6.1503",
    "kappa_hat 2.0201": f"{fit['kappa_hat']:.4f}" == "2.0201",
    "se_gamma 0.32": f"{fit['se_gamma']:.2f}" == "0.32",
    "se_lambda 9.59": f"{fit['se_lambda']:.2f}" == "9.59",
    "se_kappa 1.86": f"{fit['se_kappa']:.2f}" == "1.86",
    "log_likelihood -7.1445": f"{fit['log_likelihood']:.4f}" == "-7.1445",
}
for name, ok in checks.items():
    print(name, ok)


def mixed(prizes, probs):
    probs = [Fraction(p) for p in probs]
    gain = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    loss = any(x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))
    return gain and loss


mixed_ids = [a[0] for a in answers if mixed(a[2], a[3]) or mixed(a[4], a[5])]
print("mixed-sign pairs:", len(mixed_ids), "| non-mixed pair_ids:", sorted(set(a[0] for a in answers) - set(mixed_ids)))
