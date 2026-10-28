"""Write three round-8 student-error mutants (m45-m47) from the reference. Usage: python -I make_mutants_r8.py <checkout>"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
DOC_45 = '"""Payback uses a strict test, so a cumulative flow of exactly zero does not count as recovered, against the page rule zero or more."""\n'
DOC_46 = '"""The IRR bisection stops when the bracket is within 1e-6 of x relative, so a root is not refined to the 1e-7 rate tolerance."""\n'
DOC_47 = '"""The Fisher function accepts an inflation of -100 percent instead of raising ValueError, because the inflation check is missing."""\n'


def body(text: str) -> str:
    # drop the reference's module docstring (the first triple-quoted block) and keep the rest of the module
    head, _, rest = text.partition('"""')
    _, _, rest = rest.partition('"""')
    return rest
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text()
out = root / "ledgers/CF1/mutants"


def sub(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, (old[:70], text.count(old))
    return text.replace(old, new)


# m45: payback treats exactly zero cumulative flow as not yet recovered (strict inequality, against "zero or more").
m45 = sub(ref, "        if cumulative + discounted[t] >= 0.0:\n", "        if cumulative + discounted[t] > 0.0:\n")
m45 = DOC_45 + body(m45)
(out / "m45_payback_strict_recovery_test.py").write_text(m45)

# m46: the IRR root bisection stops at a 1e-6 relative bracket in x, so roots are far from the 1e-7 rate tolerance.
m46 = sub(ref, "                if hi - lo <= 1e-15 * hi:\n", "                if hi - lo <= 1e-6 * hi:\n")
m46 = DOC_46 + body(m46)
(out / "m46_irr_bisection_stops_at_1e6.py").write_text(m46)

# m47: the Fisher form skips the validation of inflation, so an inflation of -100 percent is accepted.
m47 = sub(ref, "    _check_rate(real)\n    _check_rate(inflation)\n    return (1.0 + real)", "    _check_rate(real)\n    return (1.0 + real)")
m47 = DOC_47 + body(m47)
(out / "m47_fisher_inflation_unchecked.py").write_text(m47)
print("wrote m45-m47")
