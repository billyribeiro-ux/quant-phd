"""Writes this round's student-error mutants of the three project lab twins (each a complete module; each mutation asserted to apply once)."""
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
twins = root / "tests/labs/LX1"
out = root / "ledgers/LX1/mutants"
specs = [
    ("lab-LX1-project-3.py", "r12n01_lab3_window_three_strict_inequality.py",
     "project lab 3. Student's window-three filter uses a strict inequality, so the first change of 2025-10 is dropped (11 changes, not 12).",
     'window_three = [item for item in changes if item[0] >= WINDOW_THREE_FROM]',
     'window_three = [item for item in changes if item[0] > WINDOW_THREE_FROM]'),
    ("lab-LX1-project-3.py", "r12n02_lab3_largest_change_printed_as_magnitude.py",
     "project lab 3. Student prints the largest monthly change as its magnitude, dropping the sign of the largest change.",
     'print(f"  largest monthly log change by size, percent, with its sign: {show(100 * biggest, 2)} ({biggest_month})")',
     'print(f"  largest monthly log change by size, percent, with its sign: {show(100 * abs(biggest), 2)} ({biggest_month})")'),
    ("lab-LX1-project-3.py", "r12n03_lab3_zero_test_with_tolerance_1e4.py",
     "project lab 3. Student counts a change as zero when its absolute value is below 1e-4 (0.01 percent), not when it is exactly zero.",
     'zeros = sum(1 for value in values if value == 0.0)',
     'zeros = sum(1 for value in values if abs(value) < 1e-4)'),
    ("lab-LX1-project-2.py", "r12n04_lab2_price_level_scaled_by_100.py",
     "project lab 2 (rung 2). Student divides the nominal debt by the price level in percent, so every real value is 1/100 of the answer.",
     "    return Fraction(nominal_cents) / price_level\n",
     "    return Fraction(nominal_cents) / (price_level * 100)\n"),
    ("lab-LX1-project-1.py", "r12n05_lab1_part_c_rising_minus_falling.py",
     "project lab 1 (rung 1). Student subtracts the falling path from the rising path in Part C, so the sign of the difference is reversed.",
     '    print(f"  difference: {fixed_two(round_half_up(falling_end - rising_end))}")',
     '    print(f"  difference: {fixed_two(round_half_up(rising_end - falling_end))}")'),
]
for src, name, doc, old, new in specs:
    text = (twins / src).read_text(encoding="utf-8")
    assert text.count(old) == 1, (name, text.count(old))
    text = text.replace(old, new, 1)
    # the docstring's first line names the error; the first line of the file is the docstring opener
    first, rest = text.split("\n", 1)
    if first.startswith('"""'):
        text = '"""' + doc + "\n" + first[3:] + "\n" + rest
    else:
        text = '"""' + doc + '\n"""\n' + text
    (out / name).write_text(text, encoding="utf-8")
    print("wrote", name)
