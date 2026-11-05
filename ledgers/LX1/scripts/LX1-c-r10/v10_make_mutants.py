"""Round-10 verifier: writes four new student-error mutants of the project labs (complete modules, one error each)
from the twins under tests/labs/LX1/. Each replacement must match exactly once or the script exits non-zero.
Argument 1 is the checkout root."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
TWIN = root / "tests/labs/LX1"
OUT = root / "ledgers/LX1/mutants"

SPECS = [
    ("lx1c_r10n01_lab3_gbp_read_as_pounds_per_dollar.py",
     "lab-LX1-project-3.py",
     "Student reads the GBP column as pounds per dollar and inverts every rate before taking logs. "
     "LX1 project lab 3 (rung 3 check).",
     [("rows.append((month, Fraction(Decimal(cell))))", "rows.append((month, 1 / Fraction(Decimal(cell))))")]),
    ("lx1c_r10n02_lab2_real_debt_floored_to_whole_cent.py",
     "lab-LX1-project-2.py",
     "Student's real debt is the nominal debt divided by the price level with floor division, which truncates "
     "the cent. LX1 project lab 2 (rung 2 completion).",
     [("    return Fraction(nominal_cents) / price_level", "    return Fraction(nominal_cents) // price_level")]),
    ("lx1c_r10n03_lab1_burden_without_minus_one.py",
     "lab-LX1-project-1.py",
     "Student's burden change is 100 times the price-level ratio without subtracting one, so it reports the "
     "level of the burden rather than its change. LX1 project lab 1 (rung 1 worked example).",
     [("    return 100 * (start_price / end_price - 1)", "    return 100 * (start_price / end_price)")]),
    ("lx1c_r10n04_lab1_two_decimals_without_zero_padding.py",
     "lab-LX1-project-1.py",
     "Student's money formatter drops the zero padding of the cents, so 100000.00 prints as 100000.0. "
     "LX1 project lab 1 (rung 1 worked example).",
     [('    return f"{sign}{whole}.{part:02d}"', '    return f"{sign}{whole}.{part}"')]),
]

for name, twin, doc, reps in SPECS:
    text = (TWIN / twin).read_text(encoding="utf-8")
    lines = text.split("\n")
    # The twin's first line is its docstring opener; replace the whole module docstring with a one-line error note.
    end = text.index('"""', text.index('"""') + 3) + 3
    body = text[end:]
    for old, new in reps:
        count = body.count(old)
        if count != 1:
            sys.exit(f"{name}: replacement target found {count} times: {old!r}")
        body = body.replace(old, new)
    out = f'"""{doc}"""' + body
    (OUT / name).write_text(out, encoding="utf-8")
    print("wrote", name)
