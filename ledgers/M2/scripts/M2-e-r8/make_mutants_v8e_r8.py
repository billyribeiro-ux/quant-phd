"""Write the verifier's round-8 student-error mutants: the reference with one line changed each."""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
ref = (ROOT / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
out = ROOT / "ledgers/M2/mutants"
specs = [
    ("v8e_01_yield_at_minus_one_passes_the_check.py",
     "Yield check uses < instead of <=, so a yield of exactly -1 is not refused and divides by zero.",
     '    if yield_bps <= -10_000:\n        raise ValueError("the yield must be above -1 (-10000 basis points)")',
     '    if yield_bps < -10_000:\n        raise ValueError("the yield must be above -1 (-10000 basis points)")'),
    ("v8e_02_price_nudged_up_before_rounding.py",
     "bond_price_cents adds 1e-9 cents before rounding, so an exact half cent goes up instead of to the even cent.",
     "    return round(price)\n",
     "    return round(price + 1e-9)\n"),
    ("v8e_03_duration_divides_by_the_rounded_price.py",
     "duration_analytic divides by the rounded integer price rather than the unrounded price.",
     '        "duration_analytic": -first / price,',
     '        "duration_analytic": -first / round(price),'),
    ("v8e_04_second_derivative_uses_t_times_t_minus_one.py",
     "d2price_dy2 weights each term by t(t-1) instead of t(t+1), the typo of a sign in the index.",
     "    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)",
     "    second = sum(t * (t - 1) * cash * v ** (t + 2) for t, cash in flows)"),
]
for name, doc, old, new in specs:
    assert ref.count(old) == 1, (name, ref.count(old))
    text = ref.replace(old, new, 1)
    # one-line description as the module docstring, then the reference body
    body = text.split('"""', 2)[2]
    text = f'"""{doc}\n\nReference solution with one line changed (verifier round 8, slice e).\n"""' + body
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
