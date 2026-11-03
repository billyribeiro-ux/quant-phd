"""Round-4 verifier mutants: the reference with one student error each (complete modules, one-line docstring first)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M2/mutants"

EDITS = {
    "r4_01_duration_divides_rounded_price.py": (
        "The duration ratio divides by the rounded integer price, not the unrounded price the contract names.",
        '        "duration_analytic": -first / price,',
        '        "duration_analytic": -first / round(price),',
    ),
    "r4_02_second_derivative_wrong_exponent.py": (
        "The second derivative uses discount exponent t + 1 instead of t + 2.",
        "    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)",
        "    second = sum(t * (t + 1) * cash * v ** (t + 1) for t, cash in flows)",
    ),
    "r4_03_step_check_accepts_nan.py": (
        "The step check tests for a value at or below zero, so NaN passes and returns a NaN estimate.",
        "    if not step > 0:",
        "    if step <= 0:",
    ),
}

for name, (doc, old, new) in EDITS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new, 1)
    lines = body.split("\n")
    # the reference opens with a multi-line docstring; the mutant opens with the one-line description instead
    end = body.index('"""', 3) + 3
    body = '"""' + doc + '"""' + body[end:]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
