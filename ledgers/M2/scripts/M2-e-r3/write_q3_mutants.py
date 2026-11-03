"""Writes four round-3 student-error mutants of grader/reference.py into ledgers/M2/mutants/ (verifier-authored)."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
out = root / "ledgers/M2/mutants"

edits = {
    "q3_01_forward_quotient_divides_by_rounded_step_gap.py": (
        "_positive_step accepts a positive step, but the forward quotient divides by the gap (x + h) - x as floating point "
        "computes it, not by h.",
        '        return (f(x + step) - f(x)) / step\n',
        '        gap = (x + step) - x\n        return (f(x + step) - f(x)) / gap\n',
    ),
    "q3_02_duration_divides_by_the_rounded_price.py": (
        "sensitivities divides dprice_dy by the price rounded to whole cents, not by the unrounded price, in duration_analytic.",
        '        "duration_analytic": -first / price,\n',
        '        "duration_analytic": -first / round(price),\n',
    ),
    "q3_03_second_derivative_uses_t_times_t_minus_one.py": (
        "sensitivities uses t(t-1) rather than t(t+1) as the coefficient of the second derivative of each discount factor.",
        '    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)\n',
        '    second = sum(t * (t - 1) * cash * v ** (t + 2) for t, cash in flows)\n',
    ),
    "q3_04_number_times_dual_drops_the_derivative.py": (
        "_Dual multiplication from the left by a plain number keeps the value but drops the derivative of the dual number.",
        '    __rmul__ = __mul__\n',
        '    def __rmul__(self, other: Any) -> _Dual:\n'
        '        o = _lift(other)\n'
        '        return _Dual(o.value * self.value, o.dot * self.value)\n',
    ),
}

for name, (first_line, old, new) in edits.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    # The module docstring's first line is replaced by a description of the error, as the mutant contract requires.
    head, rest = body.split('"""', 2)[1], body.split('"""', 2)[2]
    body = '"""' + first_line + "\n" + head.split("\n", 1)[1] + '"""' + rest
    (out / name).write_text(body, encoding="utf-8")
    print("wrote", name)
