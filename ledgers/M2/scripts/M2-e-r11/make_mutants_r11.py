"""Round-11 verifier-authored student-error mutants of the M2 reference (ledgers/M2/mutants/r11_*.py)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M2/grader/reference.py").read_text()
OUT = ROOT / "ledgers/M2/mutants"
HEAD = '"""Reference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.'

MUTANTS = {
    "r11_01_central_quotient_missing_factor_two.py": (
        '        return (f(x + step) - f(x - step)) / (2 * step)\n',
        '        return (f(x + step) - f(x - step)) / step\n',
        "fd_derivative's central quotient divides by h rather than 2h, so every central estimate is doubled.",
    ),
    "r11_02_bond_price_truncates_instead_of_rounding.py": (
        '    return round(price)\n',
        '    return int(price)\n',
        "bond_price_cents truncates the unrounded price toward zero instead of rounding half to even.",
    ),
    "r11_03_duration_uses_rounded_price.py": (
        '        "duration_analytic": -first / price,\n',
        '        "duration_analytic": -first / round(price),\n',
        "sensitivities divides by the rounded integer price when it forms the duration, mixing the two prices.",
    ),
    "r11_04_hessian_mixed_cross_term_sign_slip.py": (
        "{i: step, j: -step}))\n                - f(_moved(base, {i: -step, j: step}))",
        "{i: step, j: -step}))\n                + f(_moved(base, {i: -step, j: step}))",
        "hessian_fd adds rather than subtracts the (i-, j+) evaluation of the mixed difference, a sign slip.",
    ),
}

for name, (old, new, desc) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    first, rest = body.split("\n", 1)
    assert first.startswith(HEAD), name
    (OUT / name).write_text('"""' + desc + "\n" + rest)
    print("wrote", name)
