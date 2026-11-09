"""Round-17 verifier: writes three new student-error lab mutants from the current twins.

Each mutant is a complete module. Its first docstring line names the error; the lab id line follows, as in the
other mutants, so harness_r17.py can identify the lab. Usage: python -I make_mutants_r17.py <checkout_root>.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
mdir = root / "ledgers/LX1/mutants"


def make(name: str, twin_name: str, error: str, old: str, new: str) -> None:
    twin = (root / "tests/labs/LX1" / twin_name).read_text(encoding="utf-8")
    assert twin.count(old) == 1, (name, twin.count(old))
    body = twin.replace(old, new, 1)
    assert body.startswith('"""LX1 project lab '), name
    text = f'"""Student error: {error}\n\n' + body[3:]
    (mdir / name).write_text(text, encoding="utf-8")
    print(name, len(text))


make(
    "r17n01_lab3_blank_gbp_cell_read_as_zero.py",
    "lab-LX1-project-3.py",
    "reads a blank GBP cell as a zero rate instead of raising ValueError, so a missing month is taken as a flat rate.",
    '            cell = row.get(column) or ""\n',
    '            cell = row.get(column) or "0"\n',
)
make(
    "r17n02_lab2_burden_end_price_is_period_four.py",
    "lab-LX1-project-2.py",
    "takes the burden change to period four, not period five, so the printed change is for the wrong period.",
    "    change = burden_change_percent(PATH[0], PATH[-1])\n",
    "    change = burden_change_percent(PATH[0], PATH[-2])\n",
)
make(
    "r17n03_lab3_mean_absolute_deviation_not_sd.py",
    "lab-LX1-project-3.py",
    "reports the mean absolute deviation of the changes from their mean as the dispersion, not the sample standard deviation.",
    "    sd = sample_sd_two_pass(values)\n",
    "    mu = math.fsum(values) / len(values)\n    sd = math.fsum(abs(v - mu) for v in values) / len(values)\n",
)
