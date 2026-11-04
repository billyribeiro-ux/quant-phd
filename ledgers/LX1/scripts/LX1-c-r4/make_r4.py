"""Writes round-4 student-error mutants (from the project twins) under ledgers/LX1/mutants/."""
import pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE4-LX1-c")
TW = ROOT / "tests/labs/LX1"
OUT = ROOT / "ledgers/LX1/mutants"
SPEC = [
    ("lab-LX1-project-2.py", "lx1c_r4n01_lab2_burden_as_share_of_end_price.py",
     "return 100 * (start_price / end_price - 1)", "return 100 * (1 - end_price / start_price)"),
    ("lab-LX1-project-2.py", "lx1c_r4n02_lab2_nominal_debt_typed_in_dollars.py",
     "NOMINAL_DEBT_CENTS = 4_000_000", "NOMINAL_DEBT_CENTS = 40_000"),
    ("lab-LX1-project-2.py", "lx1c_r4n03_lab2_burden_rounded_to_whole_percent.py",
     "print(f\"  change: {fixed_two(round_half_up(change * 100))}\")", "print(f\"  change: {fixed_two(round_half_up(change) * 100)}\")"),
    ("lab-LX1-project-3.py", "lx1c_r4n04_lab3_window_one_drops_first_change.py",
     "window_one = changes\n", "window_one = changes[1:]\n"),
    ("lab-LX1-project-3.py", "lx1c_r4n05_lab3_sd_reported_per_year.py",
     "{show(100 * sd, 2)}\")\n    print(f\"  largest", "{show(100 * sd * 12 ** 0.5, 2)}\")\n    print(f\"  largest"),
    ("lab-LX1-project-3.py", "lx1c_r4n06_lab3_window_two_from_1999_12.py",
     'WINDOW_TWO_FROM = "2000-01"', 'WINDOW_TWO_FROM = "1999-12"'),
]
for twin, name, old, new in SPEC:
    src = (TW / twin).read_text(encoding="utf-8")
    assert src.count(old) == 1, (name, src.count(old))
    (OUT / name).write_text(src.replace(old, new), encoding="utf-8")
    print("wrote", name)
