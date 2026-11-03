"""Round-4 verifier (E3-d): writes four new student-error mutants of the E3 reference into ledgers/E3/mutants/.

Each mutant is the reference solution with exactly one change; every anchor must occur exactly once (asserted).
The first docstring line of each mutant describes the student error (tools/mutate_graders.py prints it).
Run from the checkout: .venv/bin/python ledgers/E3/scripts/E3-d-r4/make_d4_mutants_r4.py <checkout-root>
"""
import ast
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SRC = (ROOT / "course/modules/E/E3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E3/mutants"

MUTANTS = {
    "e3d4_01_reported_log_likelihood_is_negated.py": (
        "The reported log_likelihood is the negative of the likelihood at the estimate, a sign slip in the return.",
        [('"log_likelihood": _objective(xi, parsed),', '"log_likelihood": -_objective(xi, parsed),')],
    ),
    "e3d4_02_probabilities_rounded_to_denominator_1000.py": (
        "Each probability is rounded to the nearest fraction with denominator at most 1000 before the exact sum check, "
        "so a sum that is off by 1e-13 is accepted.",
        [("probs.append(Fraction(p))", "probs.append(Fraction(p).limit_denominator(1000))")],
    ),
    "e3d4_03_crra_wealth_check_uses_absolute_value.py": (
        "The CRRA wealth check compares the absolute value of wealth plus prize with zero, so a negative final wealth "
        "passes the check and is sent to the power function.",
        [("if any(wealth_cents + x <= 0 for x in prizes):", "if any(abs(wealth_cents + x) <= 0 for x in prizes):")],
    ),
    "e3d4_04_log_kappa_clamped_at_zero_in_objective.py": (
        "The search clamps log kappa at zero inside the objective, so a choice precision below 1 is fitted as if it were "
        "1 and the estimate is not the maximum.",
        [("return _logit_sum(parsed, gamma, math.exp(a), math.exp(b))",
          "return _logit_sum(parsed, gamma, math.exp(a), math.exp(max(b, 0.0)))")],
    ),
}

tree = ast.parse(SRC)
doc = tree.body[0]
assert isinstance(doc, ast.Expr) and isinstance(doc.value, ast.Constant)
lines = SRC.splitlines(keepends=True)
body_start = doc.end_lineno  # 1-based line of the docstring's last line
rest = "".join(lines[body_start:])

for name, (description, edits) in MUTANTS.items():
    text = rest
    for old, new in edits:
        count = text.count(old)
        assert count >= 1, (name, old)
        assert count == len(text.split(old)) - 1
        text = text.replace(old, new)
    header = (
        f'"""{description}\n\n'
        "Round-4 verifier (E3-d) mutant: the reference solution with the single change above. Standard library only.\n"
        '"""\n'
    )
    (OUT / name).write_text(header + text, encoding="utf-8")
    print("wrote", name, "| changed occurrences:", [t[0] and text.count(t[1]) for t in edits])
