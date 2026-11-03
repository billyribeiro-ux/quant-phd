"""Write the round-3 student-error mutants: each is the reference with exactly one edited line."""

import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
ref = (ROOT / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M2/mutants"

edits = {
    "r3_01_dprice_dy_is_a_central_difference_of_the_price.py": (
        "dprice_dy is a numerical central difference of the unrounded price at step 1e-5, not the stated formula.",
        '        "dprice_dy": first,\n',
        '        "dprice_dy": (_price(instance, rate + 1e-5) - _price(instance, rate - 1e-5)) / 2e-5,\n',
    ),
    "r3_02_convexity_divides_by_the_rounded_price.py": (
        "convexity_analytic divides the second derivative by the rounded integer price, not the unrounded price.",
        '        "convexity_analytic": second / price,\n',
        '        "convexity_analytic": second / round(price),\n',
    ),
    "r3_03_coupon_truncated_to_whole_cents.py": (
        "the coupon is truncated to whole cents before discounting, so fractional-cent coupons are lost.",
        "    coupon = face * instance[\"coupon_bps\"] / 10_000\n",
        "    coupon = float(int(face * instance[\"coupon_bps\"] / 10_000))\n",
    ),
    "r3_04_hessian_diagonal_divided_by_h_not_h_squared.py": (
        "each Hessian diagonal entry is a second difference divided by h, not by h squared.",
        "        hessian[i][i] = (up - 2 * f0 + down) / (step * step)\n",
        "        hessian[i][i] = (up - 2 * f0 + down) / step\n",
    ),
}
helper = (
    "\n\ndef _price(instance: dict[str, Any], rate: float) -> float:\n"
    "    flows, _ = _cash_flows(instance)\n"
    "    v = 1 / (1 + rate)\n"
    "    return sum(cash * v**t for t, cash in flows)\n"
)
for name, (doc, old, new) in edits.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    if "_price(" in new:
        body = body.replace("\n\ndef _yield_rate", helper + "\n\ndef _yield_rate", 1)
    first_line, rest = body.split("\n", 1)
    body = f'"""{doc}"""\n' + rest.split('"""', 2)[2].lstrip("\n") if False else body
    # replace the module docstring with the mutant description on its first line
    end = body.index('"""', 3) + 3
    module_doc = f'"""{doc}\n\nThe reference with this single edit.\n"""'
    body = module_doc + body[end:]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
