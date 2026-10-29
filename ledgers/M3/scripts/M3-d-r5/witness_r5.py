"""Witness check: the reference and the two surviving mutants on the boundary inputs named in the rows."""
import importlib.util
from pathlib import Path

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

ref = load(Path("course/modules/M/M3/grader/reference.py"), "ref")
m_strict = load(Path("ledgers/M3/mutants/r3d_m01_is_psd_strict_at_minus_tol.py"), "m1")
m_scaled = load(Path("ledgers/M3/mutants/r5d_m01_is_psd_tolerance_scaled_by_diagonal.py"), "m2")
cases = [
    ("diag(-0.5,1,1), tol=0.5 (eigenvalue exactly -tol)", [[-0.5, 0, 0], [0, 1, 0], [0, 0, 1]], 0.5),
    ("diag(-1e-10,1,1), default tol (exactly -tol)", [[-1e-10, 0, 0], [0, 1, 0], [0, 0, 1]], 1e-10),
    ("diag(100,-5e-9), default tol", [[100.0, 0], [0, -5e-9]], 1e-10),
]
for label, a, tol in cases:
    print(label, "| reference:", ref.is_psd(a, tol=tol), "| strict mutant:", m_strict.is_psd(a, tol=tol), "| scaled mutant:", m_scaled.is_psd(a, tol=tol))
