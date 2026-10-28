"""Writes the three round-4 student-error mutants (m17-m19) from grader/reference.py. Usage: python3 -I mk_r4_mutants.py <checkout>"""
import pathlib
import sys

ck = pathlib.Path(sys.argv[1])
src = (ck / "course/modules/M/M2/grader/reference.py").read_text(encoding="utf-8")
out = ck / "ledgers/M2/mutants"


def make(name: str, doc: str, old: str, new: str) -> None:
    assert src.count(old) == 1, (name, src.count(old))
    text = src.replace(old, new, 1)
    a = text.index('"""')
    b = text.index('"""', a + 3) + 3
    (out / name).write_text(f'"""{doc}"""' + text[b:], encoding="utf-8")


make("m17_fd_refuses_steps_above_ten.py",
     "_positive_step refuses any step above ten, so fd_derivative raises ValueError for a large positive step.",
     '    if not step > 0:\n        raise ValueError("the step h must be above zero")',
     '    if not step > 0 or step > 10:\n        raise ValueError("the step h must be above zero")')
make("m18_hessian_refuses_step_of_one_or_more.py",
     "hessian_fd treats a step of one or more as invalid and raises ValueError, though the page says positive steps are accepted.",
     "    step = _positive_step(h)\n    base = [float(v) for v in x]",
     '    step = _positive_step(h)\n    if step >= 1:\n        raise ValueError("the Hessian step must be below one")\n    base = [float(v) for v in x]')
make("m19_yield_refused_at_minus_half.py",
     "_yield_rate refuses any yield at or below -0.5, so bond_price_cents raises for a negative yield the page accepts.",
     "    if yield_bps <= -10_000:",
     "    if yield_bps <= -5_000:")
