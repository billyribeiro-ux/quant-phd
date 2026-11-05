"""Write five new student-error mutants of the M2 reference into ledgers/M2/mutants (round 10, slice e).

Each mutant is a complete solution module. Its module docstring's first line names the student error.
"""
import pathlib
import sys

ref = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])


def patch(text: str, old: str, new: str, header: str) -> str:
    assert text.count(old) == 1, ("not unique", old[:70])
    text = text.replace(old, new)
    # replace the module docstring's first line with the student-error description
    first, rest = text.split('"""', 2)[0:2], text.split('"""', 2)
    body = rest[2]
    doc = rest[1]
    doc_lines = doc.split("\n")
    doc_lines[0] = header
    return rest[0] + '"""' + "\n".join(doc_lines) + '"""' + body


mutants = {
    "w10e_01_bond_price_discounts_each_cash_flow_one_year_short.py": (
        "    price = sum(cash * v**t for t, cash in flows)\n    return round(price)",
        "    price = sum(cash * v ** (t - 1) for t, cash in flows)\n    return round(price)",
        "Student error: the price discounts each year's cash flow one period short, by (1 + y)**(t - 1).",
    ),
    "w10e_02_scheme_name_accepted_in_any_case.py": (
        '    if scheme == "forward":\n        return (f(x + step) - f(x)) / step\n    if scheme == "central":\n        return (f(x + step) - f(x - step)) / (2 * step)',
        '    name = scheme.lower() if isinstance(scheme, str) else scheme\n    if name == "forward":\n        return (f(x + step) - f(x)) / step\n    if name == "central":\n        return (f(x + step) - f(x - step)) / (2 * step)',
        "Student error: the scheme name is compared case-insensitively, so Central and Forward are accepted.",
    ),
    "w10e_03_central_quotient_forgets_the_factor_two.py": (
        "        return (f(x + step) - f(x - step)) / (2 * step)",
        "        return (f(x + step) - f(x - step)) / step",
        "Student error: the central quotient divides the symmetric difference by h, not 2h, so it is twice the derivative.",
    ),
    "w10e_04_duration_uses_the_rounded_price.py": (
        '        "duration_analytic": -first / price,',
        '        "duration_analytic": -first / round(price),',
        "Student error: the duration -P'/P divides by the price rounded to whole cents instead of the unrounded price.",
    ),
    "w10e_05_hessian_mixed_entry_divided_by_h_squared.py": (
        "            hessian[i][j] = mixed / (4 * step * step)",
        "            hessian[i][j] = mixed / (step * step)",
        "Student error: the mixed Hessian entry divides by h squared instead of 4h squared, so it is four times too large.",
    ),
}

for name, (old, new, header) in mutants.items():
    text = patch(ref, old, new, header)
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", out / name)
