"""Round-7 alternative correct implementations (must MATCH the expected block of their lab)."""
import pathlib
ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE7-LX1-c")
G = ROOT / "ledgers/LX1/scripts/LX1-c-r7/gen"
def alt(name, src, edits):
    for old, new in edits:
        assert src.count(old) == 1, (name, old)
        src = src.replace(old, new)
    (G / name).write_text(src, encoding="utf-8")
    print("wrote", name)
L1 = (ROOT / "tests/labs/LX1/lab-LX1-project-1.py").read_text(encoding="utf-8")
L2 = (ROOT / "tests/labs/LX1/lab-LX1-project-2.py").read_text(encoding="utf-8")
L3 = (ROOT / "tests/labs/LX1/lab-LX1-project-3.py").read_text(encoding="utf-8")
alt("alt7_lab1_float_real_value.py", L1, [
    ("    return Fraction(nominal_cents) / price_level", "    return Fraction(float(nominal_cents) / float(price_level))"),
])
alt("alt7_lab2_burden_as_difference_over_end.py", L2, [
    ("    return 100 * (start_price / end_price - 1)", "    return 100 * (start_price - end_price) / end_price"),
])
alt("alt7_lab3_slice_windows_and_statistics_variance.py", L3, [
    ("    window_two = [item for item in changes if item[0] >= WINDOW_TWO_FROM]", "    window_two = changes[-321:]"),
    ("    window_three = [item for item in changes if item[0] >= WINDOW_THREE_FROM]", "    window_three = changes[-12:]"),
    ("    return math.sqrt(math.fsum((value - mean) ** 2 for value in values) / (n - 1))", "    return math.sqrt(statistics.variance(values))"),
])
