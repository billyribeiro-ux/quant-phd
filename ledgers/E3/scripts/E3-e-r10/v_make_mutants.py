"""Verifier r10: three NEW student-error mutants of the E3 reference, written as complete elicit.py modules.

Each mutant is reference.py with one change; the first docstring line names the student error. Each change is
asserted to apply exactly once, so no mutant is silently identical to the reference.
"""
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD10-E3-e")
REF = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"

def make(name, first_line, edits):
    src = REF
    for old, new in edits:
        assert src.count(old) == 1, (name, old[:60], src.count(old))
        src = src.replace(old, new)
    # the reference docstring is replaced by the mutant's own first line plus the reference text
    head, sep, rest = src.partition('"""')
    _, sep2, body = rest.partition('"""')
    src = f'"""{first_line}\n\n{rest.split(chr(34)*3, 1)[0]}"""{body}'
    (OUT / name).write_text(src, encoding="utf-8")
    print("wrote", name)

make(
    "r10f_01_standard_errors_from_observed_information_at_step_1e_minus_4.py",
    "Standard errors use the observed information by central differences of step 1e-4 instead of the step of the "
    "reference, which moves the lambda standard error by more than 10 percent on some participants.",
    [("    _, hess = _gradient_and_hessian(f, xi)\n",
      "    global _H\n    saved_h = _H\n    _H = 1e-4\n    _, hess = _gradient_and_hessian(f, xi)\n    _H = saved_h\n")],
)
make(
    "r10f_02_newton_stops_when_the_gradient_is_below_one_e_minus_four.py",
    "The Newton search stops once every partial derivative is below 1e-4, so the estimate is returned before it is a "
    "stationary point to the tolerance the page states.",
    [("        if max(abs(g) for g in grad) < 1e-7:\n", "        if max(abs(g) for g in grad) < 1e-4:\n")],
)
make(
    "r10f_03_mixed_sign_test_ignores_the_probability_of_each_prize.py",
    "The mixed-sign test ignores probabilities, so a lottery whose gain or loss has probability zero counts as mixed.",
    [
        ("    gains = any(x > 0 and p > 0 for x, p in zip(prizes, probs, strict=True))\n"
         "    losses = any(x < 0 and p > 0 for x, p in zip(prizes, probs, strict=True))\n",
         "    gains = any(x > 0 for x in prizes)\n    losses = any(x < 0 for x in prizes)\n"),
    ],
)
