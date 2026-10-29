"""Write the round-6 student-error mutants of the M2 project grader from the reference solution, one edit each."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
ref = (ROOT / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
out = ROOT / "ledgers/M2/mutants"

MUTANTS = {
    "r6_01_fd_step_silently_capped_at_one.py": (
        "fd_derivative silently caps a step above one at one, so a large positive step returns a quotient at step one.",
        "    step = _positive_step(h)\n    if scheme == \"forward\":",
        "    step = min(_positive_step(h), 1.0)\n    if scheme == \"forward\":",
    ),
    "r6_02_hessian_step_silently_capped_at_a_thousandth.py": (
        "hessian_fd silently caps the step at one thousandth, so a Hessian step of one returns entries at that step.",
        "    step = _positive_step(h)\n    base = [float(v) for v in x]",
        "    step = min(_positive_step(h), 1e-3)\n    base = [float(v) for v in x]",
    ),
    "r6_03_bond_price_discounts_one_year_short.py": (
        "bond_price_cents discounts the year-t cash flow by (1 + y) to the power t minus one, so the price is off by one year.",
        "    price = sum(cash * v**t for t, cash in flows)\n    return round(price)",
        "    price = sum(cash * v ** (t - 1) for t, cash in flows)\n    return round(price)",
    ),
    "r6_04_ad_constant_function_returns_its_value.py": (
        "ad_derivative returns the value of a constant result instead of its derivative, so a constant function returns its value.",
        "    result = _lift(f(_Dual(float(x), 1.0)))\n    return float(result.dot)",
        "    result = _lift(f(_Dual(float(x), 1.0)))\n    return float(result.value) if result.dot == 0.0 else float(result.dot)",
    ),
    "r6_05_hessian_mixed_entries_scaled_by_a_quarter.py": (
        "hessian_fd scales each mixed entry by one quarter, so each off-diagonal entry is a quarter of its value.",
        "            mixed = (\n                f(_moved(base, {i: step, j: step}))",
        "            mixed = 0.25 * (\n                f(_moved(base, {i: step, j: step}))",
    ),
}
for name, (doc, old, new) in MUTANTS.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    assert body.startswith('"""Reference solution'), name
    body = f'"""{doc}\n\n' + body[3:]
    (out / name).write_text(body, encoding="utf-8")
    print("wrote", name)
