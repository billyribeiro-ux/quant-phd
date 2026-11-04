"""Round-6 slice e: writes four new student-error mutants and two new correct alternative engines.

Each is the reference module with exactly the listed textual replacements; every replacement must match once.
"""
import pathlib, re, sys

ROOT = pathlib.Path(sys.argv[1])
REF = (ROOT / "course/modules/M/M2/grader/reference.py").read_text()
HEAD = '"""Reference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.'
assert REF.count(HEAD) == 1


def build(first_line: str, repl: list[tuple[str, str, int]]) -> str:
    text = REF.replace(HEAD, '"""' + first_line + '\n\nReference solution for the M2 project: sensitivity_engine.py, the sensitivity engine.', 1)
    for old, new, count in repl:
        n = text.count(old)
        assert n == count, (old, n, count)
        text = text.replace(old, new)
    return text


MUTANTS = {
    "v6e_01_duration_is_macaulay_not_modified": (
        "duration_analytic is the Macaulay duration -P'(y)(1 + y)/P(y) in years, not the modified duration -P'(y)/P(y).",
        [('"duration_analytic": -first / price,', '"duration_analytic": -first * (1 + rate) / price,', 1)],
    ),
    "v6e_02_central_quotient_uses_one_sided_numerator": (
        "fd_derivative central scheme uses the one-sided numerator (f(x+h) - f(x)) / (2h), which is of order h, not h squared.",
        [("return (f(x + step) - f(x - step)) / (2 * step)", "return (f(x + step) - f(x)) / (2 * step)", 1)],
    ),
    "v6e_03_sensitivities_drop_the_face_repayment": (
        "sensitivities removes the face repayment from the final cash flow before differentiating, so dprice_dy is the derivative of a coupon-only price.",
        [
            (
                "    flows, rate = _cash_flows(instance)\n    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    first",
                "    flows, rate = _cash_flows(instance)\n"
                "    flows = [(t, cash - (float(instance['face_cents']) if t == int(instance['maturity_years']) else 0.0)) for t, cash in flows]\n"
                "    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    first",
                1,
            )
        ],
    ),
    "v6e_04_forward_estimate_is_the_midpoint_quotient": (
        "fd_derivative forward scheme returns the midpoint quotient (f(x + h/2) - f(x - h/2)) / h, not the forward quotient.",
        [
            (
                "return (f(x + step) - f(x)) / step",
                "return (f(x + step / 2) - f(x - step / 2)) / step",
                1,
            )
        ],
    ),
}

for name, (first, repl) in MUTANTS.items():
    (ROOT / "ledgers/M2/mutants" / (name + ".py")).write_text(build(first, repl))
    print("wrote mutant", name)

# Correct alternative A: discounting by exp and log1p, sums by math.fsum, price rounded from a float.
alt_a = REF
alt_a = alt_a.replace("from collections.abc import Callable\nfrom typing import Any\n",
                      "import math\nfrom collections.abc import Callable\nfrom typing import Any\n", 1)
for old, new, count in [
    ("    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    return round(price)",
     "    lg = math.log1p(rate)\n    price = math.fsum(cash * math.exp(-t * lg) for t, cash in flows)\n    return round(price)", 1),
    ("    v = 1 / (1 + rate)\n    price = sum(cash * v**t for t, cash in flows)\n    first = -sum(t * cash * v ** (t + 1) for t, cash in flows)\n    second = sum(t * (t + 1) * cash * v ** (t + 2) for t, cash in flows)",
     "    lg = math.log1p(rate)\n    price = math.fsum(cash * math.exp(-t * lg) for t, cash in flows)\n    first = -math.fsum(t * cash * math.exp(-(t + 1) * lg) for t, cash in flows)\n    second = math.fsum(t * (t + 1) * cash * math.exp(-(t + 2) * lg) for t, cash in flows)", 1),
]:
    assert alt_a.count(old) == count, old[:60]
    alt_a = alt_a.replace(old, new)
(ROOT / ledger if False else ROOT / "ledgers/M2/scripts/M2-e-r6/alts_r6/alt_r6_a_exp_log_discounting_fsum.py").write_text(alt_a)

# Correct alternative B: central estimate by the five-point stencil (order h to the fourth), forward unchanged.
old_c = '        return (f(x + step) - f(x - step)) / (2 * step)'
assert REF.count(old_c) == 1
alt_b = REF.replace(old_c, '        return (-f(x + 2 * step) + 8 * f(x + step) - 8 * f(x - step) + f(x - 2 * step)) / (12 * step)', 1)
(ROOT / "ledgers/M2/scripts/M2-e-r6/alts_r6/alt_r6_b_five_point_central.py").write_text(alt_b)
print("wrote alternatives")
