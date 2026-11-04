"""Round-5 checks: reference price coefficients vs the suite's clearing oracle; Lab 2 values; stdlib-only imports.

Usage: python -I oracle_lab2_stdlib_check_r5.py <checkout-root>. Writes nothing; prints three sections.
"""

import ast
import glob
import importlib.util
import math
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
g = root / "course/modules/E/E4/grader"


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


ref = load(g / "reference.py", "ref")
tree = ast.parse((g / "test_project.py").read_text(encoding="utf-8"))
keep = [
    n
    for n in tree.body
    if (isinstance(n, ast.FunctionDef) and n.name in ("oracle_regressions", "oracle_price"))
    or (isinstance(n, ast.Assign) and any(getattr(t, "id", "") in ("A_CARA", "TAU_V", "TAU_E", "VAR_S") for t in n.targets))
]
ns: dict = {}
exec(compile(ast.fix_missing_locations(ast.Module(body=[ast.Import(names=[ast.alias("math")])] + keep, type_ignores=[])), "oracle", "exec"), ns)

print("== 1. reference price coefficients vs the suite's fixed-point clearing oracle")
worst = 0.0
for lam in [0.1, 0.3, 0.57, 0.9, 1.0]:
    for sd in [0.5, 0.7, 1.0]:
        bs, bu = ns["oracle_price"](lam, sd)
        rbs, rbu, _ = ref.price_coefficients(lam, sd)
        worst = max(worst, abs(bs - rbs), abs(bu - rbu))
print("max |oracle - reference| over 15 (lam, sd) pairs:", f"{worst:.3e}")

print("== 2. Lab 2 values at noise volume 0.70, cost 0.14")
print("gap at 0 =", f"{ref.gap_at_zero(0.70, 0.14):+.8f}", "| gap at 1 =", f"{ref.indifference_gap(1.0, 0.70, 0.14):+.8f}")
out = ref.solve_model(0.70, 0.14)
print("root =", f"{out['informed_fraction']:.10f}", "| informativeness =", f"{out['price_informativeness']:.10f}")

print("== 3. imports of reference.py and the five alternatives")
for f in sorted(glob.glob(str(root / "ledgers/E4/alternatives/*.py"))) + [str(g / "reference.py")]:
    t = ast.parse(Path(f).read_text(encoding="utf-8"))
    mods = set()
    for n in ast.walk(t):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        if isinstance(n, ast.ImportFrom) and n.module:
            mods.add(n.module.split(".")[0])
    print(Path(f).name, sorted(mods))
