#!/usr/bin/env python3
"""Write ten student-error mutants k01-k10 of the M2 reference into ledgers/M2/mutants/.

Each mutant is reference.py with exactly one snippet replaced, and each replacement must match exactly once. The first
line of each docstring names the error, as tools/mutate_graders.py prints it.
"""

from __future__ import annotations

from pathlib import Path

REF = Path("/tmp/quant-b2/course/modules/M/M2/grader/reference.py")
OUT = Path("/tmp/quant-b2/ledgers/M2/mutants")

MUTANTS: list[tuple[str, str, str, str]] = [
    (
        "k01_unknown_scheme_raises_key_error_not_value_error",
        "fd_derivative raises KeyError, not ValueError, for a scheme outside forward and central.",
        "    raise ValueError(\"scheme must be 'forward' or 'central'\")",
        "    raise KeyError(scheme)",
    ),
    (
        "k02_bool_scheme_true_taken_as_forward",
        "fd_derivative takes the scheme True as forward, so a bool is accepted where the page names only the two strings.",
        '    if scheme == "forward":\n        return (f(x + step) - f(x)) / step',
        '    if scheme == "forward" or scheme is True:\n        return (f(x + step) - f(x)) / step',
    ),
    (
        "k03_bytes_scheme_decoded_then_accepted",
        "fd_derivative decodes a bytes scheme, so b'central' is accepted as the name central.",
        '    step = _positive_step(h)\n    if scheme == "forward":',
        '    step = _positive_step(h)\n    if isinstance(scheme, bytes):\n        scheme = scheme.decode()\n    if scheme == "forward":',
    ),
    (
        "k04_no_reflected_addition_on_dual_numbers",
        "The dual number has no reflected addition, so 2.0 + x raises TypeError instead of a derivative.",
        "    __radd__ = __add__\n",
        "",
    ),
    (
        "k05_negative_yield_price_truncated",
        "bond_price_cents truncates the unrounded price instead of rounding it when the yield is negative.",
        "    return round(price)",
        "    return round(price) if rate >= 0 else int(price)",
    ),
    (
        "k06_large_point_uses_a_difference_quotient",
        "ad_derivative switches to a central difference with step 1e-6 for |x| above 1e4, where the dual number is exact.",
        "    result = _lift(f(_Dual(float(x), 1.0)))",
        "    if abs(x) > 1e4:\n        s = 1e-6\n        return float((f(float(x) + s) - f(float(x) - s)) / (2 * s))\n"
        "    result = _lift(f(_Dual(float(x), 1.0)))",
    ),
    (
        "k07_central_scheme_skips_the_step_check",
        "fd_derivative skips the step check for the central scheme, so a zero step divides by zero.",
        '    step = _positive_step(h)\n    if scheme == "forward":',
        '    step = float(h) if scheme == "central" else _positive_step(h)\n    if scheme == "forward":',
    ),
    (
        "k08_yield_check_removed_from_the_cash_flows",
        "The yield check is removed, so a yield of -1 divides by zero and raises ZeroDivisionError, not ValueError.",
        "    rate = _yield_rate(instance)\n    face",
        '    rate = float(instance["yield_bps"]) / 10_000\n    face',
    ),
    (
        "k09_hessian_accepts_a_nan_step",
        "hessian_fd accepts a NaN step and returns a NaN matrix instead of raising ValueError.",
        "    step = _positive_step(h)\n    base = [float(v) for v in x]",
        "    step = float(h) if h != h else _positive_step(h)\n    base = [float(v) for v in x]",
    ),
    (
        "k10_hessian_refuses_steps_above_one_half",
        "hessian_fd refuses a step above one half, though the page accepts positive Hessian steps up to 1.",
        "    step = _positive_step(h)\n    base = [float(v) for v in x]",
        '    step = _positive_step(h)\n    if step > 0.5:\n        raise ValueError("the Hessian step is too large")\n'
        "    base = [float(v) for v in x]",
    ),
]


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    opening, _, after_open = source.partition('"""')
    module_doc, _, code = after_open.partition('"""')
    assert opening == "" and module_doc, "reference.py must open with a module docstring"
    doc_lines = module_doc.strip("\n").splitlines()
    for name, doc, old, new in MUTANTS:
        count = code.count(old)
        if count != 1:
            raise SystemExit(f"{name}: snippet matches {count} times, expected 1")
        new_doc = f'"""{doc}\n\nReference solution for the M2 project, with one student error.\n' + "\n".join(doc_lines[1:])
        text = new_doc + '\n"""' + code.replace(old, new)
        (OUT / f"{name}.py").write_text(text, encoding="utf-8")
        print(f"wrote {name}.py")


if __name__ == "__main__":
    main()
