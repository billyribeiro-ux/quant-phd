"""Round 3, slice d: write the verifier's new student-error mutants from grader/reference.py by one change each.

Usage: python3 -I make_mutants_r3.py <checkout-root>. Each mutant gets a one-line docstring naming the student error.
"""

import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
ref = (root / "course/modules/M/M5/grader/reference.py").read_text(encoding="utf-8")
out_dir = root / "ledgers/M5/mutants"

MUTANTS = {
    "r3_01_operator_clamps_each_image_at_zero.py": (
        "Student-error mutant (M5 slice d round 3): bellman_operator clamps each image value at zero, as if utilities made "
        "every value nonnegative, so it departs from the definition for any input vector with a negative entry.",
        "    return _sweep(beta, alpha, points, _values(values, len(points)))",
        "    return [max(0.0, x) for x in _sweep(beta, alpha, points, _values(values, len(points)))]",
    ),
    "r3_02_continuation_uses_absolute_value.py": (
        "Student-error mutant (M5 slice d round 3): the continuation term is beta times the absolute value of V(k'), so a "
        "negative continuation value is read as positive.",
        "                best = max(best, math.sqrt(available - successor) + beta * continuation)",
        "                best = max(best, math.sqrt(available - successor) + beta * abs(continuation))",
    ),
    "r3_03_feasibility_tie_tolerance_of_1e-14.py": (
        "Student-error mutant (M5 slice d round 3): feasibility allows a successor up to 1e-14 above k**alpha, a "
        "float-rounding tolerance that the exact test k' <= k**alpha does not have.",
        "            if successor <= available:",
        "            if successor <= available + 1e-14:",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    # the first docstring line names the error; the reference docstring is replaced by the mutant's own
    first_doc_end = body.index('"""', 3) + 3
    body = f'"""{doc}"""\n\n' + body[first_doc_end:].lstrip("\n")
    (out_dir / name).write_text(body, encoding="utf-8")
    print("wrote", out_dir / name)
