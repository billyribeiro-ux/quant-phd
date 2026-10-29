"""Write round-8 student-error mutants of the M2 reference into ledgers/M2/mutants/ (verifier-authored)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M2/grader/reference.py").read_text()
OUT = ROOT / "ledgers/M2/mutants"
HEAD = '"""Reference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.'

MUTANTS = {
    "r8_01_yield_divided_by_one_thousand.py": (
        "    return float(yield_bps) / 10_000\n",
        "    return float(yield_bps) / 1_000\n",
        "_yield_rate converts basis points to a decimal by dividing by 1000 instead of 10000, so every yield is ten times too large.",
    ),
    "r8_02_hessian_diagonal_drops_factor_two.py": (
        "        hessian[i][i] = (up - 2 * f0 + down) / (step * step)\n",
        "        hessian[i][i] = (up - f0 + down) / (step * step)\n",
        "hessian_fd forms the diagonal second difference as f(x+h) - f(x) + f(x-h), without the term -2 f(x).",
    ),
    "r8_03_price_returned_as_rounded_float.py": (
        "    return round(price)\n",
        "    return round(price, 2)\n",
        "bond_price_cents rounds the price to two decimal places and returns a float, so it is not an integer number of cents.",
    ),
    "r8_04_cash_flows_stop_one_year_early.py": (
        "    flows = [(t, coupon + (face if t == years else 0.0)) for t in range(1, years + 1)]\n",
        "    flows = [(t, coupon + (face if t == years else 0.0)) for t in range(1, years)]\n",
        "_cash_flows leaves out the final year, so the bond has one payment fewer than its maturity.",
    ),
    "r8_05_reflected_subtraction_sign_error.py": (
        "        return _Dual(o.value - self.value, o.dot - self.dot)\n",
        "        return _Dual(o.value - self.value, o.dot + self.dot)\n",
        "_Dual.__rsub__ keeps the sign of the derivative of the subtracted dual number, so the derivative of 1 - x is 1 instead of -1.",
    ),
}

for name, (old, new, desc) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    first, rest = body.split("\n", 1)
    assert first.startswith(HEAD), name
    (OUT / name).write_text('"""' + desc + "\n" + rest)
    print("wrote", name)
