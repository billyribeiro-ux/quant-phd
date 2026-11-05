# Writes the three round-9 student-error mutants (complete elicit.py modules) from the reference, one change each.
from pathlib import Path

REF = Path("course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = Path("ledgers/E3/mutants")


def mutate(name: str, description: str, old: str, new: str) -> None:
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new, 1)
    doc_end = body.index('"""', body.index('"""') + 3) + 3
    text = f'"""{description}"""' + body[doc_end:]
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)


mutate(
    "r9_01_lambda_frozen_at_its_grid_value",
    "estimate never moves lambda from the starting grid value: the Newton step leaves the lambda coordinate at zero.",
    "                step = _solve(lower, grad)\n",
    "                step = _solve(lower, grad)\n                step[1] = 0.0\n",
)
mutate(
    "r9_02_lambda_climbs_downhill",
    "the maximiser takes its lambda gradient with the wrong sign, so lambda descends the likelihood.",
    "        grad, hess = _gradient_and_hessian(f, xi)\n        if max(abs(g) for g in grad) < 1e-7:\n",
    "        grad, hess = _gradient_and_hessian(f, xi)\n        grad[1] = -grad[1]\n        if max(abs(g) for g in grad) < 1e-7:\n",
)
mutate(
    "r9_03_lambda_reported_as_its_log",
    "estimate reports the log of lambda, not lambda, as lambda_hat.",
    '        "lambda_hat": lam,\n',
    '        "lambda_hat": a,\n',
)
mutate(
    "r9_04_convergence_test_ignores_lambda",
    "the maximiser stops once the gamma and kappa gradients are below 1e-7, so lambda may stop short of its maximum.",
    "        if max(abs(g) for g in grad) < 1e-7:\n            return xi\n",
    "        if max(abs(grad[0]), abs(grad[2])) < 1e-7:\n            return xi\n",
)
