"""Write round-7 student-error mutants of the M2 reference into ledgers/M2/mutants/ (verifier-authored)."""
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M2/grader/reference.py").read_text()
OUT = ROOT / "ledgers/M2/mutants"
HEAD = '"""Reference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.'

MUTANTS = {
    "r7_01_no_reflected_multiplication_on_dual_numbers.py": (
        "    __rmul__ = __mul__\n",
        "",
        "ad_derivative fails on 2.0 * x because the dual number has no reflected multiplication, so a number on the left raises TypeError.",
    ),
    "r7_02_second_sensitivity_factor_t_minus_one.py": (
        "second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)",
        "second = sum(t * (t - 1) * cash * v ** (t + 2) for t, cash in flows)",
        "d2price_dy2 uses the factor t(t-1) instead of t(t+1), an off-by-one in the second derivative of the discount factor.",
    ),
    "r7_03_first_sensitivity_drops_the_time_factor.py": (
        "first = -sum(t * cash * v ** (t + 1) for t, cash in flows)",
        "first = -sum(cash * v ** (t + 1) for t, cash in flows)",
        "dprice_dy omits the factor t from the chain rule on the discount exponent, so it is the derivative of the wrong sum.",
    ),
    "r7_04_hessian_mixed_entry_sign_error.py": (
        "                + f(_moved(base, {i: -step, j: -step}))",
        "                - f(_moved(base, {i: -step, j: -step}))",
        "hessian_fd gives the (-h,-h) corner of the mixed difference the wrong sign, so each off-diagonal entry is biased.",
    ),
    "r7_05_face_value_added_every_year.py": (
        "flows = [(t, coupon + (face if t == years else 0.0)) for t in range(1, years + 1)]",
        "flows = [(t, coupon + face) for t in range(1, years + 1)]",
        "bond cash flows add the face value to every year's coupon instead of only the final year, which overprices the bond.",
    ),
}

for name, (old, new, desc) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new)
    first, rest = body.split("\n", 1)
    assert first.startswith(HEAD), name
    (OUT / name).write_text('"""' + desc + "\n" + rest)
    print("wrote", name)
