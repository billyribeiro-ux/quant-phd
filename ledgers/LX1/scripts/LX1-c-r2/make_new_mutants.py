"""LX1-c round 2: write the four new student-error mutants as complete lab modules under ledgers/LX1/mutants/.

Each file is the current twin with one student error applied; the docstring's first line describes the error.
Run from the repo root.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TW2 = (ROOT / "tests/labs/LX1/lab-LX1-project-2.py").read_text(encoding="utf-8")
TW3 = (ROOT / "tests/labs/LX1/lab-LX1-project-3.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/LX1/mutants"


def swap(src: str, old: str, new: str) -> str:
    assert src.count(old) == 1, old
    return src.replace(old, new)


def write(name: str, src: str, description: str) -> None:
    assert src.startswith('"""')
    body = f'"""{description} ' + src[3:]
    (OUT / name).write_text(body, encoding="utf-8")


write("lx1c_r2n01_real_value_truncated.py",
      swap(TW2, "cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))",
           "cents = int(real_debt_cents(NOMINAL_DEBT_CENTS, price))"),
      "Student truncates the real value to whole cents with int() instead of rounding half up.")
write("lx1c_r2n02_lagged_price_level.py",
      swap(TW2, "cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, price))",
           "cents = round_half_up(real_debt_cents(NOMINAL_DEBT_CENTS, PATH[max(t - 1, 0)]))"),
      "Student divides by the previous period's price level, a lagged price in every real value.")
write("lx1c_r2n03_window_three_drops_last_change.py",
      swap(TW3, "window_three = [item for item in changes if item[0] >= WINDOW_THREE_FROM]",
           'window_three = [item for item in changes if WINDOW_THREE_FROM <= item[0] < "2026-09"]'),
      "Student stops the current window one month early, dropping the last change 2026-09.")
write("lx1c_r2n04_log_change_sign_flipped.py",
      swap(TW3, "math.log(float(rate / previous))", "math.log(float(previous / rate))"),
      "Student takes the log change as ln(S_(m-1) / S_m), a sign error in every monthly change.")
print("written")
