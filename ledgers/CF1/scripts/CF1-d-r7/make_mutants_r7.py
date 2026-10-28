"""Write round-7 student-error mutants (m41-m44) from the reference engine. Usage: python -I make_mutants_r7.py <checkout>"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
ref = (root / "course/modules/CF/CF1/grader/reference.py").read_text()
out = root / "ledgers/CF1/mutants"
specs = {
    "m41_irr_grid_drops_last_interval.py": (
        "The IRR grid scan skips the last pair of neighbouring samples, the interval next to the window end x = 10000, "
        "so a sign change there is not reported.",
        "for k1, k2 in itertools.pairwise(nonzero):",
        "for k1, k2 in itertools.pairwise(nonzero[:-1]):",
    ),
    "m42_irr_grid_drops_first_interval.py": (
        "The IRR grid scan skips the first pair of neighbouring samples, the interval next to the window start "
        "x = 0.0001, so a sign change there is not reported.",
        "for k1, k2 in itertools.pairwise(nonzero):",
        "for k1, k2 in itertools.pairwise(nonzero[1:]):",
    ),
    "m43_fisher_divides_instead_of_multiplying.py": (
        "The student reads the Fisher identity as a division: nominal = (1 + real) / (1 + inflation) - 1.",
        "return (1.0 + real) * (1.0 + inflation) - 1.0",
        "return (1.0 + real) / (1.0 + inflation) - 1.0",
    ),
    "m44_npv_discounts_from_period_one.py": (
        "NPV indexes the flows from one, so the outlay at period 0 is discounted by one period.",
        "return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows))",
        "return sum(cf / (1.0 + rate) ** t for t, cf in enumerate(flows, start=1))",
    ),
}
start = ref.index('"""')
end = ref.index('"""', start + 3) + 3
for name, (doc, old, new) in specs.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    text = ref[:start] + '"""' + doc + '"""' + ref[end:]
    text = text.replace(old, new)
    (out / name).write_text(text)
    print("wrote", name)
