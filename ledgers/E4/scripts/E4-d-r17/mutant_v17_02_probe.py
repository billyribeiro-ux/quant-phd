"""Round 17: at the input where mutant_v17_02 reports its largest gap difference from the reference, compares the
mutant's reported gap with the suite's oracle gap at the mutant's own reported fraction (the test's own check, with
the page's 1e-14 precision for comparison). Usage: mutant_v17_02_probe.py <checkout>"""
import importlib.util as u
import sys
from pathlib import Path

root = sys.argv[1]
sys.path.insert(0, str(Path(root, "ledgers/E4/scripts/E4-d-r17")))
from suite_workspace_r17 import make_workspace  # noqa: E402

make_workspace(root, f"{root}/course/modules/E/E4/grader/reference.py")
import test_project as T  # noqa: E402


def load(path, name):
    spec = u.spec_from_file_location(name, path)
    mod = u.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = load(f"{root}/course/modules/E/E4/grader/reference.py", "ref")
M = load(f"{root}/ledgers/E4/mutants/mutant_v17_02_price_slope_drops_uninformed_term.py", "mut")
sd, c = 0.6697478991596639, 0.12436974789915967
for name, mod in (("reference", R), ("mutant_v17_02", M)):
    out = mod.solve_model(sd, c)
    lam, gap = out["informed_fraction"], out["indifference_gap"]
    og = T.oracle_gap(lam, sd, c)
    print(f"{name}: lambda {lam!r} reported gap {gap!r} oracle gap at that lambda {og!r} |diff| {abs(gap - og)!r}")
