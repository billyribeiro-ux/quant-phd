"""Write round-9 student-error mutants of the M2 reference into ledgers/M2/mutants/ (verifier-authored)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M2/grader/reference.py").read_text()
OUT = ROOT / "ledgers/M2/mutants"
HEAD = '"""Reference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.'

MUTANTS = {
    "r9_01_central_quotient_missing_factor_two.py": (
        "        return (f(x + step) - f(x - step)) / (2 * step)\n",
        "        return (f(x + step) - f(x - step)) / step\n",
        "fd_derivative central scheme divides by h rather than 2h, so the central estimate is twice the derivative.",
    ),
    "r9_02_zero_step_accepted.py": (
        "    if not step > 0:\n",
        "    if step < 0:\n",
        "_positive_step accepts a step of exactly zero, so a zero step reaches the division instead of raising ValueError.",
    ),
    "r9_03_duration_sign_dropped.py": (
        '        "duration_analytic": -first / price,\n',
        '        "duration_analytic": first / price,\n',
        "sensitivities reports duration as first / price, dropping the minus sign, so the duration is negative.",
    ),
}

for name, (old, new, desc) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    first, rest = body.split("\n", 1)
    assert first.startswith(HEAD), name
    (OUT / name).write_text('"""' + desc + "\n" + rest)
    print("wrote", name)
