"""Witness for the window-end grid intervals: a single root inside the first and last grid interval.
Usage: python -I witness_grid_ends_r7.py <checkout>"""
import importlib.util
import pathlib
import sys

root = pathlib.Path(sys.argv[1])


def load(path: pathlib.Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ref = load(root / "course/modules/CF/CF1/grader/reference.py", "ref")
m41 = load(root / "ledgers/CF1/mutants/m41_irr_grid_drops_last_interval.py", "m41")
m42 = load(root / "ledgers/CF1/mutants/m42_irr_grid_drops_first_interval.py", "m42")
cases = {
    "last interval, root x = 9990 (rate -0.9999 + 0.0001...)": [-9990.0, 1.0],
    "first interval, root x = 1.00005e-4 (rate about 9998.5)": [-1.00005e-4, 1.0],
    "middle, root x = 1 (rate 0)": [-1.0, 1.0],
}
for label, flows in cases.items():
    print(label, "flows", flows)
    print("  reference:", ref.irr_roots(flows))
    print("  m41 (last interval dropped):", m41.irr_roots(flows))
    print("  m42 (first interval dropped):", m42.irr_roots(flows))
