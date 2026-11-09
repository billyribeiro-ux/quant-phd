"""Round 1 (LX1-c): runs the four scenarios of tests/test_lx1_project_lab3.py against each embedded survivor of the
lab 3 mutant set, with the twin path swapped to the mutant (test module imported unchanged). Prints, per survivor, which
scenarios raise AssertionError (killed by that scenario) or pass (not killed by it). Usage: python -I survivor_tests_r1.py <repo_root>"""
import importlib.util
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "tools"))
spec = importlib.util.spec_from_file_location("lx1_t3", root / "tests" / "test_lx1_project_lab3.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
survivors = ["r17n01_lab3_blank_gbp_cell_read_as_zero.py", "lx1c_r18n02_lab3_difference_of_printed_sds.py",
             "lx1c_r18n03_lab3_zero_change_tested_after_rounding_to_four_places.py",
             "lx1c_r18n04_lab3_window_two_centred_on_window_one_mean.py",
             "lx1c_r18n05_lab3_blank_cell_carried_forward_as_flat_rate.py",
             "lx1c_r20n04_lab3_zero_test_with_tolerance.py", "lx1c_r23n02_lab3_population_sd_denominator_n.py"]
header, rows = mod.snapshot()
for name in survivors:
    twin = root / "ledgers" / "LX1" / "mutants" / name
    results = {}
    mod.run_twin_on.__defaults__ = (twin,)
    mod.TWIN = twin
    for label, value in (("blank", ""), ("non-decimal", "n/a")):
        with tempfile.TemporaryDirectory() as d:
            try:
                mod.test_a_blank_or_non_decimal_gbp_cell_raises_value_error(Path(d), value)
                results[f"blank/{label}"] = "pass"
            except AssertionError:
                results[f"blank/{label}"] = "KILLED"
    with tempfile.TemporaryDirectory() as d:
        try:
            mod.test_a_month_that_does_not_follow_the_previous_one_raises_value_error(Path(d))
            results["gap"] = "pass"
        except AssertionError:
            results["gap"] = "KILLED"
    print(name, results)
