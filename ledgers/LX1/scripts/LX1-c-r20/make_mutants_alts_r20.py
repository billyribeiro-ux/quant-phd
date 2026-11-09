"""LX1-c round 20: writes three NEW student-error mutants of the project labs (into ledgers/LX1/mutants/) and five
alternative correct implementations (into ledgers/LX1/scripts/LX1-c-r20/alts/). Each edit must match exactly once."""
import sys
from pathlib import Path

root = Path(sys.argv[1])
twins = root / "tests/labs/LX1"
muts = root / "ledgers/LX1/mutants"
alts = root / "ledgers/LX1/scripts/LX1-c-r20/alts"
alts.mkdir(parents=True, exist_ok=True)


def edit(src: Path, pairs, dest: Path, header: str = "") -> None:
    text = src.read_text(encoding="utf-8")
    for old, new in pairs:
        n = text.count(old)
        assert n == 1, f"{src.name}: pattern found {n} times: {old!r}"
        text = text.replace(old, new)
    dest.write_text(header + text, encoding="utf-8")
    print("wrote", dest.relative_to(root))


L1 = twins / "lab-LX1-project-1.py"
L2 = twins / "lab-LX1-project-2.py"
L3 = twins / "lab-LX1-project-3.py"
BURDEN = "    return 100 * (start_price / end_price - 1)"
edit(L1, [(BURDEN, "    return 100 * (1 - end_price / start_price)")], muts / "lx1c_r20n01_lab1_burden_base_is_end_value.py",
     "# Student error: the burden change is taken as a percent of the end real value, 100 * (1 - P_5 / P_0).\n")
edit(L2, [(BURDEN, "    return 100 * (start_price - end_price)")], muts / "lx1c_r20n02_lab2_burden_difference_of_prices.py",
     "# Student error: the burden change is the price-level difference in percent, 100 * (P_0 - P_5), with no division.\n")
edit(L3, [('WINDOW_THREE_FROM = "2025-10"', 'WINDOW_THREE_FROM = "2025-09"')],
     muts / "lx1c_r20n03_lab3_window_three_starts_2025_09.py",
     "# Student error: window three starts one month early, at 2025-09, so it holds 13 changes.\n")
edit(L3, [("if value == 0.0)", "if abs(value) < 1e-9)")],
     muts / "lx1c_r20n04_lab3_zero_test_with_tolerance.py",
     "# Student error: an 'exact' zero change is tested with a tolerance of 1e-9 instead of equality.\n")

# five alternative correct implementations (must reproduce the expected block exactly)
edit(L1, [("    return Fraction(nominal_cents) / price_level", "    return Fraction(nominal_cents) * (1 / price_level)"),
          (BURDEN, "    return 100 * (start_price / end_price) - 100")], alts / "alt1_lab1_reciprocal_and_rearranged.py")
edit(L2, [("    return ___", "    return Fraction(nominal_cents) * (1 / price_level)")] if False else
     [("        return ___" if False else "    return Fraction(nominal_cents) / price_level",
       "    return Fraction(nominal_cents) * (1 / price_level)"),
      (BURDEN, "    return 100 * start_price / end_price - 100")], alts / "alt2_lab2_reciprocal_and_rearranged.py")
edit(L3, [("math.log(float(rate / previous))", "math.log(float(rate) / float(previous))")],
     alts / "alt3_lab3_float_ratio_before_log.py")
edit(L3, [("item[0] >= WINDOW_TWO_FROM", "month_index(item[0]) >= month_index(WINDOW_TWO_FROM)")],
     alts / "alt4_lab3_window_two_by_month_index.py")
edit(L3, [("if value == 0.0)", "if not value)")], alts / "alt5_lab3_zero_by_truthiness.py")
