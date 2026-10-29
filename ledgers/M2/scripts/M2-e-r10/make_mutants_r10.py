"""Round-10 verifier-authored student-error mutants of the M2 reference (ledgers/M2/mutants/r10_*.py)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M2/grader/reference.py").read_text()
OUT = ROOT / "ledgers/M2/mutants"
HEAD = '"""Reference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.'

MUTANTS = {
    "r10_01_moved_point_aliases_the_base_list.py": (
        "    point = list(base)\n",
        "    point = base\n",
        "_moved returns the base list itself rather than a copy, so each moved point shifts the base for the next call.",
    ),
    "r10_02_hessian_mixed_entry_divided_by_h_not_h_squared.py": (
        "            hessian[i][j] = mixed / (4 * step * step)\n",
        "            hessian[i][j] = mixed / (4 * step)\n",
        "hessian_fd divides the mixed entries by 4h rather than 4h^2, a dimension error that scales them by 1/h.",
    ),
    "r10_03_dual_reflected_subtraction_negates_value_only.py": (
        "        return _Dual(o.value - self.value, o.dot - self.dot)\n",
        "        return _Dual(o.value - self.value, self.dot - o.dot)\n",
        "The reflected subtraction c - x on a dual number gives the right value but negates the derivative the wrong way.",
    ),
    "r10_04_ad_returns_value_not_derivative_for_products.py": (
        "        return _Dual(self.value * o.value, self.value * o.dot + self.dot * o.value)\n",
        "        return _Dual(self.value * o.value, self.value * o.dot)\n",
        "The dual product keeps only the a * db term and drops the da * b term of the product rule.",
    ),
}

for name, (old, new, desc) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    first, rest = body.split("\n", 1)
    assert first.startswith(HEAD), name
    (OUT / name).write_text('"""' + desc + "\n" + rest)
    print("wrote", name)
