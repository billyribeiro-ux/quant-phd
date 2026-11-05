"""Write four new student-error mutants of the M2 reference into ledgers/M2/mutants/ (each differs from reference.py by one edit)."""
from pathlib import Path

root = Path("/Users/billyribeiro/.fanout/wt/verifyD11-M2-e")
ref = (root / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
HEAD = '"""Reference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.'
assert ref.count(HEAD) == 1
edits = {
    "w11e_01_forward_quotient_uses_floor_division.py": (
        "Student error: the forward quotient uses floor division, so the derivative is truncated to a whole number.",
        "        return (f(x + step) - f(x)) / step\n",
        "        return (f(x + step) - f(x)) // step\n",
    ),
    "w11e_02_step_read_with_int_refuses_fractional_steps.py": (
        "Student error: the step is read with int(), so every step below 1 is treated as zero and refused.",
        "    step = float(h)\n",
        "    step = float(int(h))\n",
    ),
    "w11e_03_duration_divides_by_the_price_in_dollars.py": (
        "Student error: the duration divides the cents derivative by the price converted to dollars.",
        '        "duration_analytic": -first / price,\n',
        '        "duration_analytic": -first / (price / 100),\n',
    ),
    "w11e_04_yield_check_compares_basis_points_with_minus_one.py": (
        "Student error: the yield check compares basis points with -1, so any yield below -0.01 percent is refused.",
        "    if yield_bps <= -10_000:\n",
        "    if yield_bps <= -1:\n",
    ),
}
out = root / "ledgers/M2/mutants"
for name, (first_line, old, new) in edits.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new).replace(HEAD, '"""' + first_line + "\n\nReference solution with one student edit.", 1)
    assert body != ref
    (out / name).write_text(body, encoding="utf-8")
    print("wrote", name)
